using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;

public static class Metin2PyungmooImporter
{
    private const int HeightSamples = 131;
    private const int TerrainVertices = 257;
    private const int TerrainCells = 256;
    private const int TileRawSize = 258;

    // One Metin2 terrain chunk is 256 x 256 half-cells.
    // tile.raw uses 100 world units (= 1 meter) per half-cell.
    // height.raw stores 131 samples spanning the 128 terrain cells,
    // so we interpolate them across the 256 one-meter mesh intervals.
    private const float CellScaleMeters = 1.0f;
    private const float HeightScaleMetersPerRawUnit = 0.005f;
    private const float HeightSampleSpacingMeters = CellScaleMeters * 2.0f;

    private const string GeneratedRoot = "Assets/Metin2Generated/Pyungmoo";
    private const string ScenePath = "Assets/Scenes/Pyungmoo.unity";

    [MenuItem("Metin2/Pyungmoo/Import Pyungmoo")]
    public static void ImportPyungmoo()
    {
        try
        {
            string sourceRoot = FindSourceRoot();
            string textureSetPath = FindTextureSet(sourceRoot);
            var textureSet = ParseTextureSet(textureSetPath);
            var chunks = DiscoverChunks(sourceRoot);

            if (chunks.Count == 0)
                throw new InvalidOperationException("metin2_map_c1 içinde terrain chunk klasörleri bulunamadı.");

            PrepareGeneratedRoot();
            AssetDatabase.Refresh();

            var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            var mapRoot = new GameObject("Pyungmoo");
            var terrainRoot = new GameObject("Terrain");
            terrainRoot.transform.SetParent(mapRoot.transform, false);

            var allMaterials = BuildTextureMaterials(sourceRoot, textureSet);

            Bounds mapBounds = default;
            bool hasBounds = false;

            foreach (var chunk in chunks)
            {
                var go = BuildChunk(chunk, terrainRoot.transform, allMaterials);

                MeshRenderer renderer = go.GetComponent<MeshRenderer>();
                if (renderer != null)
                {
                    if (!hasBounds)
                    {
                        mapBounds = renderer.bounds;
                        hasBounds = true;
                    }
                    else
                    {
                        mapBounds.Encapsulate(renderer.bounds);
                    }
                }
            }

            CreateLighting(mapRoot.transform);
            CreateTemporaryPlayer(mapRoot.transform, mapBounds);

            EditorSceneManager.SaveScene(scene, ScenePath);
            AddSceneToBuildSettings(ScenePath);

            AssetDatabase.SaveAssets();
            AssetDatabase.Refresh();

            Selection.activeGameObject = mapRoot;
            SceneView.lastActiveSceneView?.FrameSelected();

            EditorUtility.DisplayDialog(
                "Pyungmoo hazır",
                $"Gerçek terrain + tile.raw texture dağılımı oluşturuldu.\n" +
                $"Chunk: {chunks.Count}\n" +
                $"TextureSet: metin2_c1.txt\n\n" +
                "Assets/Scenes/Pyungmoo.unity açıldı. Play ile gezebilirsin.",
                "Tamam");
        }
        catch (Exception ex)
        {
            Debug.LogException(ex);
            EditorUtility.DisplayDialog("Pyungmoo import hatası", ex.Message, "Tamam");
        }
    }

    private static string FindSourceRoot()
    {
        string projectRoot = Directory.GetParent(Application.dataPath).FullName;
        string repoRoot = Directory.GetParent(projectRoot).FullName;

        string source = Path.Combine(repoRoot, "Metin2Client", "OutdoorC1", "metin2_map_c1");
        if (!Directory.Exists(source))
        {
            throw new DirectoryNotFoundException(
                "Pyungmoo kaynak klasörü bulunamadı. Beklenen yol:\n" + source);
        }

        return source;
    }

    private static string FindTextureSet(string sourceRoot)
    {
        string projectRoot = Directory.GetParent(Application.dataPath).FullName;
        string repoRoot = Directory.GetParent(projectRoot).FullName;
        string path = Path.Combine(repoRoot, "Metin2Client", "textureset", "textureset", "metin2_c1.txt");

        if (!File.Exists(path))
            throw new FileNotFoundException("metin2_c1.txt bulunamadı.", path);

        return path;
    }

    private static List<ChunkInfo> DiscoverChunks(string root)
    {
        var regex = new Regex(@"^(\d{3})(\d{3})$");
        var result = new List<ChunkInfo>();

        foreach (string dir in Directory.GetDirectories(root))
        {
            string name = Path.GetFileName(dir);
            Match m = regex.Match(name);
            if (!m.Success)
                continue;

            string height = Path.Combine(dir, "height.raw");
            string tile = Path.Combine(dir, "tile.raw");

            if (!File.Exists(height) || !File.Exists(tile))
                continue;

            if (new FileInfo(height).Length != HeightSamples * HeightSamples * 2)
                throw new InvalidDataException($"{name}/height.raw boyutu beklenen 34322 bayt değil.");

            if (new FileInfo(tile).Length != TileRawSize * TileRawSize)
                throw new InvalidDataException($"{name}/tile.raw boyutu beklenen 66564 bayt değil.");

            result.Add(new ChunkInfo
            {
                Name = name,
                X = int.Parse(m.Groups[1].Value),
                Y = int.Parse(m.Groups[2].Value),
                Directory = dir,
                HeightPath = height,
                TilePath = tile
            });
        }

        return result.OrderBy(c => c.X).ThenBy(c => c.Y).ToList();
    }

    private static Dictionary<int, TextureEntry> ParseTextureSet(string path)
    {
        string[] lines = File.ReadAllLines(path);
        var result = new Dictionary<int, TextureEntry>();

        int currentId = -1;
        string currentPath = null;
        float uScale = 1f;
        float vScale = 1f;
        int numericValuesRead = 0;

        foreach (string rawLine in lines)
        {
            string line = rawLine.Trim();

            Match startMatch = Regex.Match(line, @"^Start Texture(\d+)$");
            if (startMatch.Success)
            {
                currentId = int.Parse(startMatch.Groups[1].Value);
                currentPath = null;
                uScale = 1f;
                vScale = 1f;
                numericValuesRead = 0;
                continue;
            }

            if (currentId < 0)
                continue;

            if (line.StartsWith("\"") && line.EndsWith("\""))
            {
                currentPath = line.Substring(1, line.Length - 2);
                continue;
            }

            if (line.StartsWith("End Texture", StringComparison.OrdinalIgnoreCase))
            {
                if (!string.IsNullOrEmpty(currentPath))
                {
                    result[currentId] = new TextureEntry
                    {
                        Id = currentId,
                        SourcePath = currentPath,
                        UScale = uScale,
                        VScale = vScale
                    };
                }

                currentId = -1;
                currentPath = null;
                numericValuesRead = 0;
                continue;
            }

            string[] parts = line.Split(new[] { ' ', '\t' }, StringSplitOptions.RemoveEmptyEntries);
            if (parts.Length == 1 &&
                float.TryParse(
                    parts[0],
                    System.Globalization.NumberStyles.Float,
                    System.Globalization.CultureInfo.InvariantCulture,
                    out float numeric))
            {
                // TextureSet format:
                // line 1: texture path
                // line 2: U scale
                // line 3: V scale
                // line 4+: additional flags/settings
                if (numericValuesRead == 0)
                    uScale = numeric;
                else if (numericValuesRead == 1)
                    vScale = numeric;

                numericValuesRead++;
            }
        }

        if (result.Count == 0)
            throw new InvalidDataException("metin2_c1.txt içinden TextureSet okunamadı.");

        Debug.Log($"Pyungmoo TextureSet: {result.Count} texture okundu.");
        return result;
    }

    private static Dictionary<int, Material> BuildTextureMaterials(
        string sourceRoot,
        Dictionary<int, TextureEntry> textureSet)
    {
        string assetsRoot = Application.dataPath;
        string projectRoot = Directory.GetParent(assetsRoot).FullName;
        string repoRoot = Directory.GetParent(projectRoot).FullName;

        string textureOutput = Path.Combine(
            assetsRoot, "Metin2Generated", "Pyungmoo", "Textures");
        string materialOutput = "Assets/Metin2Generated/Pyungmoo/Materials";

        Directory.CreateDirectory(textureOutput);
        Directory.CreateDirectory(Path.Combine(assetsRoot, "Metin2Generated", "Pyungmoo", "Meshes"));
        Directory.CreateDirectory(Path.Combine(assetsRoot, "Metin2Generated", "Pyungmoo", "Materials"));

        var materials = new Dictionary<int, Material>();

        foreach (var pair in textureSet.OrderBy(p => p.Key))
        {
            TextureEntry entry = pair.Value;
            string sourceFile = ResolveTerrainTexture(repoRoot, entry.SourcePath);

            if (string.IsNullOrEmpty(sourceFile) || !File.Exists(sourceFile))
            {
                Debug.LogWarning($"Pyungmoo TextureSet {entry.Id}: kaynak DDS bulunamadı: {entry.SourcePath}");
                continue;
            }

            string safeName = $"Tex_{entry.Id:00}_{Sanitize(Path.GetFileNameWithoutExtension(sourceFile))}";
            string destinationAsset = $"Assets/Metin2Generated/Pyungmoo/Textures/{safeName}.dds";
            string destinationAbsolute = Path.Combine(
                assetsRoot,
                destinationAsset.Substring("Assets/".Length).TrimStart('/').Replace('/', Path.DirectorySeparatorChar));

            // Metin2'nin eski DDS dosyaları 256x256 DXT1 olsa da yalnızca 5-6 mip
            // içeriyor. Unity 6 tam mip zinciri beklediği için dosyayı tek mip olarak
            // normalize ediyoruz; Unity eksik mipleri kendi oluşturabilir.
            byte[] sourceBytes = File.ReadAllBytes(sourceFile);
            byte[] unityDds = NormalizeDdsForUnity(sourceBytes);
            File.WriteAllBytes(destinationAbsolute, unityDds);

            AssetDatabase.ImportAsset(destinationAsset, ImportAssetOptions.ForceUpdate);

            Texture2D texture = AssetDatabase.LoadAssetAtPath<Texture2D>(destinationAsset);
            if (texture == null)
            {
                Debug.LogWarning($"DDS Unity'ye import edilemedi: {destinationAsset}");
                continue;
            }

            var material = new Material(FindGroundShader())
            {
                name = $"Pyungmoo_Tex_{entry.Id:00}"
            };

            material.mainTexture = texture;
            material.SetTexture("_BaseMap", texture);
            material.mainTextureScale = new Vector2(entry.UScale, entry.VScale);
            material.SetFloat("_Smoothness", 0.0f);

            string materialPath = $"{materialOutput}/Pyungmoo_Tex_{entry.Id:00}.mat";
            DeleteAssetIfExists(materialPath);
            AssetDatabase.CreateAsset(material, materialPath);

            materials[entry.Id] = material;
        }

        if (materials.Count == 0)
            throw new InvalidOperationException("Pyungmoo TextureSet'teki DDS'lerin hiçbiri import edilemedi.");

        return materials;
    }

    private static byte[] NormalizeDdsForUnity(byte[] source)
    {
        if (source == null || source.Length < 128)
            throw new InvalidDataException("DDS dosyası 128 bayttan küçük.");

        if (source[0] != (byte)'D' ||
            source[1] != (byte)'D' ||
            source[2] != (byte)'S' ||
            source[3] != (byte)' ')
        {
            throw new InvalidDataException("Geçersiz DDS magic.");
        }

        uint headerSize = ReadUInt32(source, 4);
        if (headerSize != 124)
            throw new InvalidDataException($"Beklenmeyen DDS header boyutu: {headerSize}");

        int height = (int)ReadUInt32(source, 12);
        int width = (int)ReadUInt32(source, 16);
        string fourCC = new string(new[]
        {
            (char)source[84], (char)source[85], (char)source[86], (char)source[87]
        });

        if (width <= 0 || height <= 0)
            throw new InvalidDataException($"Geçersiz DDS boyutu: {width}x{height}");

        // Şu anki Metin2 terrain seti DXT1. Diğer DDS türlerini yanlışlıkla
        // dönüştürmemek için yalnızca DXT1'i normalize ediyoruz.
        if (!string.Equals(fourCC, "DXT1", StringComparison.Ordinal))
            return source;

        int blockWidth = Mathf.Max(1, (width + 3) / 4);
        int blockHeight = Mathf.Max(1, (height + 3) / 4);
        int topMipSize = blockWidth * blockHeight * 8;
        int payloadStart = 128;

        if (source.Length < payloadStart + topMipSize)
            throw new InvalidDataException(
                $"DDS DXT1 payload eksik. Beklenen en az {payloadStart + topMipSize} bayt, mevcut {source.Length}.");

        byte[] result = new byte[payloadStart + topMipSize];
        Buffer.BlockCopy(source, 0, result, 0, payloadStart);
        Buffer.BlockCopy(source, payloadStart, result, payloadStart, topMipSize);

        // dwFlags: DDSD_MIPMAPCOUNT bitini kaldır.
        uint flags = ReadUInt32(result, 8);
        flags &= ~0x00020000u;
        WriteUInt32(result, 8, flags);

        // dwMipMapCount = 1.
        WriteUInt32(result, 28, 1u);

        // dwCaps: DDSCAPS_TEXTURE kalsın; COMPLEX/MIPMAP kalksın.
        uint caps = ReadUInt32(result, 108);
        caps &= ~(0x00000008u | 0x00400000u);
        caps |= 0x00001000u;
        WriteUInt32(result, 108, caps);

        return result;
    }

    private static uint ReadUInt32(byte[] bytes, int offset)
    {
        return (uint)(
            bytes[offset] |
            (bytes[offset + 1] << 8) |
            (bytes[offset + 2] << 16) |
            (bytes[offset + 3] << 24));
    }

    private static void WriteUInt32(byte[] bytes, int offset, uint value)
    {
        bytes[offset] = (byte)(value & 0xFF);
        bytes[offset + 1] = (byte)((value >> 8) & 0xFF);
        bytes[offset + 2] = (byte)((value >> 16) & 0xFF);
        bytes[offset + 3] = (byte)((value >> 24) & 0xFF);
    }

    private static string ResolveTerrainTexture(string repoRoot, string sourcePath)
    {
        string normalized = sourcePath.Replace('\\', '/');
        int marker = normalized.IndexOf("terrainmaps/", StringComparison.OrdinalIgnoreCase);
        if (marker < 0)
            return null;

        string relative = normalized.Substring(marker + "terrainmaps/".Length);
        string exactB = Path.Combine(repoRoot, "Metin2Client", "Terrain", "ymir work", "terrainmaps", "b",
            relative.Substring(relative.IndexOf('/') + 1).Replace('/', Path.DirectorySeparatorChar));

        // metin2_c1.txt references terrainmaps/b/...; use that first.
        if (File.Exists(exactB))
            return exactB;

        // Fallback to terrainmaps/c/... for C empire assets.
        string exactC = Path.Combine(repoRoot, "Metin2Client", "Terrain", "ymir work", "terrainmaps", "c",
            relative.Substring(relative.IndexOf('/') + 1).Replace('/', Path.DirectorySeparatorChar));

        return File.Exists(exactC) ? exactC : null;
    }

    private static GameObject BuildChunk(
        ChunkInfo chunk,
        Transform parent,
        Dictionary<int, Material> materials)
    {
        byte[] heightBytes = File.ReadAllBytes(chunk.HeightPath);
        byte[] tileBytes = File.ReadAllBytes(chunk.TilePath);

        var vertices = new Vector3[TerrainVertices * TerrainVertices];
        var uvs = new Vector2[vertices.Length];

        for (int z = 0; z < TerrainVertices; z++)
        {
            for (int x = 0; x < TerrainVertices; x++)
            {
                float sourceX = x * 0.5f;
                float sourceZ = z * 0.5f;

                int x0 = Mathf.Clamp(Mathf.FloorToInt(sourceX), 0, HeightSamples - 2);
                int z0 = Mathf.Clamp(Mathf.FloorToInt(sourceZ), 0, HeightSamples - 2);
                int x1 = x0 + 1;
                int z1 = z0 + 1;

                float fx = sourceX - x0;
                float fz = sourceZ - z0;

                float h00 = ReadHeight(heightBytes, x0, z0);
                float h10 = ReadHeight(heightBytes, x1, z0);
                float h01 = ReadHeight(heightBytes, x0, z1);
                float h11 = ReadHeight(heightBytes, x1, z1);

                float h0 = Mathf.Lerp(h00, h10, fx);
                float h1 = Mathf.Lerp(h01, h11, fx);
                float height = Mathf.Lerp(h0, h1, fz);

                int i = z * TerrainVertices + x;
                vertices[i] = new Vector3(
                    x * CellScaleMeters,
                    height,
                    z * CellScaleMeters);

                uvs[i] = new Vector2(
                    x / (float)TerrainCells,
                    z / (float)TerrainCells);
            }
        }

        var textureIds = materials.Keys.OrderBy(id => id).ToList();
        var submeshTriangles = new Dictionary<int, List<int>>();
        foreach (int id in textureIds)
            submeshTriangles[id] = new List<int>(4096);

        int fallbackId = textureIds.Contains(8) ? 8 : textureIds[0];

        for (int z = 0; z < TerrainCells; z++)
        {
            for (int x = 0; x < TerrainCells; x++)
            {
                // tile.raw is 258 x 258. The playable 256 x 256 region is the inner area.
                int tileId = tileBytes[(z + 1) * TileRawSize + (x + 1)];
                if (!submeshTriangles.ContainsKey(tileId))
                    tileId = fallbackId;

                List<int> triangles = submeshTriangles[tileId];

                int a = z * TerrainVertices + x;
                int b = a + 1;
                int c = a + TerrainVertices;
                int d = c + 1;

                triangles.Add(a);
                triangles.Add(c);
                triangles.Add(b);

                triangles.Add(b);
                triangles.Add(c);
                triangles.Add(d);
            }
        }

        string meshPath = $"{GeneratedRoot}/Meshes/Pyungmoo_{chunk.Name}.asset";
        DeleteAssetIfExists(meshPath);

        var mesh = new Mesh
        {
            name = $"Pyungmoo_{chunk.Name}"
        };

        mesh.indexFormat = UnityEngine.Rendering.IndexFormat.UInt32;
        mesh.vertices = vertices;
        mesh.uv = uvs;
        mesh.subMeshCount = textureIds.Count;

        for (int i = 0; i < textureIds.Count; i++)
            mesh.SetTriangles(submeshTriangles[textureIds[i]], i, false);

        mesh.RecalculateNormals();
        mesh.RecalculateBounds();
        mesh.UploadMeshData(false);

        AssetDatabase.CreateAsset(mesh, meshPath);

        var go = new GameObject($"Chunk_{chunk.Name}");
        go.transform.SetParent(parent, false);
        go.transform.localPosition = new Vector3(
            chunk.X * TerrainCells * CellScaleMeters,
            0.0f,
            chunk.Y * TerrainCells * CellScaleMeters);
        go.isStatic = true;

        var filter = go.AddComponent<MeshFilter>();
        filter.sharedMesh = mesh;

        var renderer = go.AddComponent<MeshRenderer>();
        renderer.sharedMaterials = textureIds.Select(id => materials[id]).ToArray();

        var collider = go.AddComponent<MeshCollider>();
        collider.sharedMesh = mesh;
        collider.convex = false;

        return go;
    }

    private static float ReadHeight(byte[] bytes, int x, int z)
    {
        int index = (z * HeightSamples + x) * 2;
        ushort raw = (ushort)(bytes[index] | (bytes[index + 1] << 8));
        return raw * HeightScaleMetersPerRawUnit;
    }

    private static Shader FindGroundShader()
    {
        Shader shader = Shader.Find("Universal Render Pipeline/Lit");
        if (shader != null)
            return shader;

        shader = Shader.Find("Standard");
        if (shader != null)
            return shader;

        throw new InvalidOperationException("Uygun Unity zemin shader'ı bulunamadı.");
    }

    private static void CreateLighting(Transform parent)
    {
        var sun = new GameObject("Sun");
        sun.transform.SetParent(parent, false);
        sun.transform.rotation = Quaternion.Euler(50.0f, -35.0f, 0.0f);

        var light = sun.AddComponent<Light>();
        light.type = LightType.Directional;
        light.intensity = 1.15f;
        light.shadows = LightShadows.Soft;

        RenderSettings.ambientMode = UnityEngine.Rendering.AmbientMode.Trilight;
        RenderSettings.ambientIntensity = 1.0f;
    }

    private static void CreateTemporaryPlayer(Transform parent, Bounds bounds)
    {
        var player = GameObject.CreatePrimitive(PrimitiveType.Capsule);
        player.name = "TemporaryPlayer";
        player.transform.SetParent(parent, false);

        Vector3 center = bounds.center;
        player.transform.position = new Vector3(center.x, bounds.max.y + 8.0f, center.z);

        CapsuleCollider primitiveCollider = player.GetComponent<CapsuleCollider>();
        if (primitiveCollider != null)
            UnityEngine.Object.DestroyImmediate(primitiveCollider);

        var controller = player.AddComponent<CharacterController>();
        controller.height = 2.0f;
        controller.radius = 0.45f;
        controller.center = new Vector3(0.0f, 1.0f, 0.0f);
        controller.slopeLimit = 48.0f;
        controller.stepOffset = 0.35f;

        Renderer bodyRenderer = player.GetComponent<Renderer>();
        if (bodyRenderer != null)
        {
            var playerMaterial = new Material(FindGroundShader());
            playerMaterial.color = new Color(0.2f, 0.55f, 1.0f);
            bodyRenderer.sharedMaterial = playerMaterial;
        }

        var movement = player.AddComponent<TemporaryPlayerController>();

        var cameraObject = new GameObject("PlayerCamera");
        cameraObject.transform.SetParent(player.transform, false);
        cameraObject.transform.localPosition = new Vector3(0.0f, 3.0f, -7.0f);
        cameraObject.transform.localRotation = Quaternion.Euler(16.0f, 0.0f, 0.0f);

        var camera = cameraObject.AddComponent<Camera>();
        camera.fieldOfView = 60.0f;
        camera.nearClipPlane = 0.05f;
        camera.farClipPlane = 5000.0f;
        cameraObject.AddComponent<AudioListener>();

        movement.CameraTransform = cameraObject.transform;
        movement.Camera = camera;
    }

    private static void PrepareGeneratedRoot()
    {
        if (AssetDatabase.IsValidFolder(GeneratedRoot))
            AssetDatabase.DeleteAsset(GeneratedRoot);

        string assetsRoot = Application.dataPath;
        Directory.CreateDirectory(Path.Combine(assetsRoot, "Metin2Generated", "Pyungmoo", "Meshes"));
        Directory.CreateDirectory(Path.Combine(assetsRoot, "Metin2Generated", "Pyungmoo", "Materials"));
        Directory.CreateDirectory(Path.Combine(assetsRoot, "Metin2Generated", "Pyungmoo", "Textures"));
    }

    private static void DeleteAssetIfExists(string assetPath)
    {
        if (AssetDatabase.LoadAssetAtPath<UnityEngine.Object>(assetPath) != null)
            AssetDatabase.DeleteAsset(assetPath);
    }

    private static void AddSceneToBuildSettings(string scenePath)
    {
        var scenes = EditorBuildSettings.scenes.ToList();
        scenes.RemoveAll(s => s.path.Equals(scenePath, StringComparison.OrdinalIgnoreCase));
        scenes.Insert(0, new EditorBuildSettingsScene(scenePath, true));
        EditorBuildSettings.scenes = scenes.ToArray();
    }

    private static string Sanitize(string name)
    {
        foreach (char c in Path.GetInvalidFileNameChars())
            name = name.Replace(c, '_');
        return name.Replace(' ', '_');
    }

    private sealed class ChunkInfo
    {
        public string Name;
        public int X;
        public int Y;
        public string Directory;
        public string HeightPath;
        public string TilePath;
    }

    private sealed class TextureEntry
    {
        public int Id;
        public string SourcePath;
        public float UScale;
        public float VScale;
    }
}
