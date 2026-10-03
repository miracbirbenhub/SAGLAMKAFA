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
    private const int TerrainSamples = 129; // 128 cells + 1 seam vertex; final 2 source samples are padding.
    private const int CellsPerChunk = 256;

    // Metin2 MapSetting commonly uses CellScale=200 and HeightScale=0.5.
    // We treat Metin2 positions as centimeters: 200 -> 2 meters/cell and 0.5 -> 0.005 meters/raw height unit.
    private const float CellScaleMeters = 2.0f;
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
            var chunks = DiscoverChunks(sourceRoot);

            if (chunks.Count == 0)
                throw new InvalidOperationException("metin2_map_c1 içinde 000000 gibi terrain chunk klasörleri bulunamadı.");

            PrepareGeneratedFolders();
            AssetDatabase.Refresh();

            var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            var mapRoot = new GameObject("Pyungmoo");
            var terrainRoot = new GameObject("Terrain");
            terrainRoot.transform.SetParent(mapRoot.transform, false);

            var chunkBounds = new Bounds();
            bool hasBounds = false;

            foreach (var chunk in chunks)
            {
                var go = BuildChunk(sourceRoot, chunk, terrainRoot.transform);

                var renderer = go.GetComponent<MeshRenderer>();
                if (renderer != null)
                {
                    var b = renderer.bounds;
                    if (!hasBounds)
                    {
                        chunkBounds = b;
                        hasBounds = true;
                    }
                    else
                    {
                        chunkBounds.Encapsulate(b);
                    }
                }
            }

            CreateLighting(mapRoot.transform);
            CreateTemporaryPlayer(mapRoot.transform, chunkBounds);

            EditorSceneManager.SaveScene(scene, ScenePath);
            EditorBuildSettings.scenes = AddSceneToBuildSettings(ScenePath);

            Selection.activeGameObject = mapRoot;
            SceneView.lastActiveSceneView?.FrameSelected();

            AssetDatabase.SaveAssets();
            AssetDatabase.Refresh();

            EditorUtility.DisplayDialog(
                "Pyungmoo hazır",
                $"Pyungmoo terrain oluşturuldu. Chunk: {chunks.Count}\n" +
                $"Harita boyutu yaklaşık: {GetMapWidth(chunks):0} m × {GetMapDepth(chunks):0} m\n\n" +
                "Assets/Scenes/Pyungmoo.unity açıldı. Play ile geçici karakterle gezebilirsin.",
                "Tamam");
        }
        catch (Exception ex)
        {
            Debug.LogException(ex);
            EditorUtility.DisplayDialog("Pyungmoo import hatası", ex.Message, "Tamam");
        }
    }

    [MenuItem("Metin2/Pyungmoo/Open Source Folder")]
    public static void OpenSourceFolder()
    {
        string path = FindSourceRoot();
        EditorUtility.RevealInFinder(path);
    }

    private static string FindSourceRoot()
    {
        string projectRoot = Directory.GetParent(Application.dataPath).FullName;
        string repoRoot = Directory.GetParent(projectRoot).FullName;
        string source = Path.Combine(repoRoot, "Metin2Client", "OutdoorC1", "metin2_map_c1");

        if (!Directory.Exists(source))
            throw new DirectoryNotFoundException(
                "Pyungmoo kaynak klasörü bulunamadı. Beklenen yol:\n" + source);

        return source;
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

            int x = int.Parse(m.Groups[1].Value);
            int y = int.Parse(m.Groups[2].Value);

            string height = Path.Combine(dir, "height.raw");
            string minimap = Path.Combine(dir, "minimap.dds");

            if (!File.Exists(height))
                continue;

            result.Add(new ChunkInfo
            {
                Name = name,
                X = x,
                Y = y,
                Directory = dir,
                HeightPath = height,
                MinimapPath = File.Exists(minimap) ? minimap : null
            });
        }

        return result.OrderBy(c => c.X).ThenBy(c => c.Y).ToList();
    }

    private static GameObject BuildChunk(string sourceRoot, ChunkInfo chunk, Transform parent)
    {
        byte[] heightBytes = File.ReadAllBytes(chunk.HeightPath);
        int expected = HeightSamples * HeightSamples * 2;

        if (heightBytes.Length != expected)
            throw new InvalidDataException(
                $"{chunk.Name}/height.raw boyutu {heightBytes.Length} bayt; beklenen {expected}.");

        var vertices = new Vector3[TerrainSamples * TerrainSamples];
        var uvs = new Vector2[vertices.Length];

        for (int z = 0; z < TerrainSamples; z++)
        {
            for (int x = 0; x < TerrainSamples; x++)
            {
                int srcIndex = (z * HeightSamples + x) * 2;
                ushort rawHeight = (ushort)(heightBytes[srcIndex] | (heightBytes[srcIndex + 1] << 8));
                float y = rawHeight * HeightScaleMetersPerRawUnit;

                int i = z * TerrainSamples + x;
                vertices[i] = new Vector3(
                    x * HeightSampleSpacingMeters,
                    y,
                    z * HeightSampleSpacingMeters);

                float u = x / (float)(TerrainSamples - 1);
                float v = z / (float)(TerrainSamples - 1);
                uvs[i] = new Vector2(u, 1.0f - v);
            }
        }

        int quadCount = TerrainSamples - 1;
        int[] triangles = new int[quadCount * quadCount * 6];
        int ti = 0;

        for (int z = 0; z < quadCount; z++)
        {
            for (int x = 0; x < quadCount; x++)
            {
                int a = z * TerrainSamples + x;
                int b = a + 1;
                int c = a + TerrainSamples;
                int d = c + 1;

                triangles[ti++] = a;
                triangles[ti++] = c;
                triangles[ti++] = b;

                triangles[ti++] = b;
                triangles[ti++] = c;
                triangles[ti++] = d;
            }
        }

        string meshPath = $"{GeneratedRoot}/Meshes/Pyungmoo_{chunk.Name}.asset";
        string materialPath = $"{GeneratedRoot}/Materials/Pyungmoo_{chunk.Name}.mat";

        DeleteAssetIfExists(meshPath);
        DeleteAssetIfExists(materialPath);

        var mesh = new Mesh
        {
            name = $"Pyungmoo_{chunk.Name}",
            vertices = vertices,
            triangles = triangles,
            uv = uvs
        };
        mesh.RecalculateNormals();
        mesh.RecalculateBounds();
        mesh.UploadMeshData(false);

        AssetDatabase.CreateAsset(mesh, meshPath);

        var material = new Material(FindGroundShader())
        {
            name = $"Pyungmoo_{chunk.Name}"
        };
        material.SetFloat("_Smoothness", 0.0f);

        if (!string.IsNullOrEmpty(chunk.MinimapPath))
        {
            string destination = $"{GeneratedRoot}/Minimap/{chunk.Name}.dds";
            string absoluteDestination = Path.GetFullPath(Path.Combine(
                Directory.GetParent(Application.dataPath).FullName,
                destination.Substring("Assets/".Length)));

            Directory.CreateDirectory(Path.GetDirectoryName(absoluteDestination));

            if (File.Exists(absoluteDestination))
                File.Delete(absoluteDestination);

            File.Copy(chunk.MinimapPath, absoluteDestination);
            AssetDatabase.ImportAsset(destination, ImportAssetOptions.ForceUpdate);

            var texture = AssetDatabase.LoadAssetAtPath<Texture2D>(destination);
            if (texture != null)
            {
                texture.wrapMode = TextureWrapMode.Clamp;
                texture.filterMode = FilterMode.Bilinear;
                material.mainTexture = texture;
                material.SetTexture("_BaseMap", texture);
            }
        }

        AssetDatabase.CreateAsset(material, materialPath);

        var go = new GameObject($"Chunk_{chunk.Name}");
        go.transform.SetParent(parent, false);
        go.transform.localPosition = new Vector3(
            chunk.X * CellsPerChunk * CellScaleMeters,
            0.0f,
            chunk.Y * CellsPerChunk * CellScaleMeters);

        go.isStatic = true;

        var renderer = go.AddComponent<MeshRenderer>();
        renderer.sharedMaterial = material;

        var filter = go.AddComponent<MeshFilter>();
        filter.sharedMesh = mesh;

        var collider = go.AddComponent<MeshCollider>();
        collider.sharedMesh = mesh;
        collider.convex = false;

        return go;
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
        player.transform.position = new Vector3(center.x, bounds.max.y + 5.0f, center.z);

        var primitiveCollider = player.GetComponent<CapsuleCollider>();
        if (primitiveCollider != null)
            UnityEngine.Object.DestroyImmediate(primitiveCollider);

        var controller = player.AddComponent<CharacterController>();
        controller.height = 2.0f;
        controller.radius = 0.45f;
        controller.center = new Vector3(0.0f, 1.0f, 0.0f);
        controller.slopeLimit = 48.0f;
        controller.stepOffset = 0.35f;

        var bodyRenderer = player.GetComponent<MeshRenderer>();
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

        Camera.main?.gameObject.SetActive(false);
    }

    private static EditorBuildSettingsScene[] AddSceneToBuildSettings(string scenePath)
    {
        var scenes = EditorBuildSettings.scenes.ToList();
        scenes.RemoveAll(s => s.path.Equals(scenePath, StringComparison.OrdinalIgnoreCase));
        scenes.Insert(0, new EditorBuildSettingsScene(scenePath, true));
        return scenes.ToArray();
    }

    private static float GetMapWidth(List<ChunkInfo> chunks)
    {
        return (chunks.Max(c => c.X) + 1) * CellsPerChunk * CellScaleMeters;
    }

    private static float GetMapDepth(List<ChunkInfo> chunks)
    {
        return (chunks.Max(c => c.Y) + 1) * CellsPerChunk * CellScaleMeters;
    }

    private static void PrepareGeneratedFolders()
    {
        string projectRoot = Directory.GetParent(Application.dataPath).FullName;

        foreach (string relative in new[]
                 {
                     "Assets/Metin2Generated/Pyungmoo/Meshes",
                     "Assets/Metin2Generated/Pyungmoo/Materials",
                     "Assets/Metin2Generated/Pyungmoo/Minimap"
                 })
        {
            Directory.CreateDirectory(Path.Combine(projectRoot, relative));
        }
    }

    private static void DeleteAssetIfExists(string assetPath)
    {
        if (AssetDatabase.LoadAssetAtPath<UnityEngine.Object>(assetPath) != null)
            AssetDatabase.DeleteAsset(assetPath);
    }

    private sealed class ChunkInfo
    {
        public string Name;
        public int X;
        public int Y;
        public string Directory;
        public string HeightPath;
        public string MinimapPath;
    }
}
