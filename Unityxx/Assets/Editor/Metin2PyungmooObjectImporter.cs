using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;

public static class Metin2PyungmooObjectImporter
{
    private const string ScenePath = "Assets/Scenes/Pyungmoo.unity";
    private const string GeneratedRootName = "Objects";
    private const string GeneratedReportPath = "Assets/Metin2Generated/Pyungmoo/PyungmooObjectImportReport.txt";

    // Metin2 map object coordinates are in world units.
    // X/Y use 200 world units per 4 Unity meters -> 0.02 m/unit.
    // Z uses the same height convention as the current terrain importer.
    private const float ObjectXYScale = 0.02f;
    private const float ObjectZScale = 0.005f;
    private const bool AddMeshColliders = true;

    [MenuItem("Metin2/Pyungmoo/Import Map Objects")]
    public static void ImportMapObjects()
    {
        try
        {
            Scene scene = OpenPyungmooScene();
            GameObject mapRoot = GameObject.Find("Pyungmoo");
            if (mapRoot == null)
                throw new InvalidOperationException("Pyungmoo GameObject'i bulunamadı.");

            Transform oldRoot = mapRoot.transform.Find(GeneratedRootName);
            if (oldRoot != null)
                UnityEngine.Object.DestroyImmediate(oldRoot.gameObject);

            Transform objectRoot = new GameObject(GeneratedRootName).transform;
            objectRoot.SetParent(mapRoot.transform, false);

            string repoRoot = GetRepoRoot();
            string mapRootPath = Path.Combine(
                repoRoot, "Metin2Client", "OutdoorC1", "metin2_map_c1");

            string propertyRoot = Path.Combine(
                repoRoot, "Metin2Client", "Property", "property");

            if (!Directory.Exists(mapRootPath))
                throw new DirectoryNotFoundException("C1 map klasörü bulunamadı:\n" + mapRootPath);

            if (!Directory.Exists(propertyRoot))
                throw new DirectoryNotFoundException("Property klasörü bulunamadı:\n" + propertyRoot);

            Dictionary<uint, PropertyEntry> propertyById = LoadProperties(propertyRoot);
            Dictionary<string, GameObject> modelByName = BuildModelIndex();

            var report = new StringBuilder();
            report.AppendLine("Pyungmoo Object Import Report");
            report.AppendLine(DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"));
            report.AppendLine();

            int chunkCount = 0;
            int objectCount = 0;
            int modelLoaded = 0;
            int missingProperty = 0;
            int missingModel = 0;
            int colliderCount = 0;

            var missingPropertyIds = new Dictionary<uint, int>();
            var missingModelNames = new Dictionary<string, int>(StringComparer.OrdinalIgnoreCase);

            foreach (string chunkDir in DiscoverChunkDirectories(mapRootPath))
            {
                string areaFile = Path.Combine(chunkDir, "areadata.txt");
                if (!File.Exists(areaFile))
                    continue;

                string chunkName = Path.GetFileName(chunkDir);
                Transform chunkRoot = new GameObject("Objects_" + chunkName).transform;
                chunkRoot.SetParent(objectRoot, false);

                List<AreaObject> objects = ParseAreaData(areaFile);
                chunkCount++;

                foreach (AreaObject areaObject in objects)
                {
                    objectCount++;

                    if (!propertyById.TryGetValue(areaObject.PropertyId, out PropertyEntry property))
                    {
                        missingProperty++;
                        Increment(missingPropertyIds, areaObject.PropertyId);
                        continue;
                    }

                    if (string.IsNullOrWhiteSpace(property.ModelKey))
                    {
                        missingModel++;
                        Increment(missingModelNames, $"<empty> property {property.PropertyName}");
                        continue;
                    }

                    if (!modelByName.TryGetValue(NormalizeKey(property.ModelKey), out GameObject model))
                    {
                        missingModel++;
                        Increment(missingModelNames, property.ModelKey);
                        continue;
                    }

                    GameObject instance = PrefabUtility.InstantiatePrefab(model) as GameObject;
                    if (instance == null)
                    {
                        missingModel++;
                        Increment(missingModelNames, property.ModelKey);
                        continue;
                    }

                    instance.name =
                        $"OBJ_{areaObject.ObjectIndex:000}_{Sanitize(property.PropertyName)}";

                    instance.transform.SetParent(chunkRoot, false);
                    instance.transform.position = ConvertPosition(areaObject);
                    instance.transform.rotation = ConvertRotation(areaObject.Rotation);
                    instance.isStatic = true;

                    if (AddMeshColliders)
                        colliderCount += AddColliders(instance);

                    modelLoaded++;
                }
            }

            report.AppendLine($"Chunk sayısı: {chunkCount}");
            report.AppendLine($"AreaData object sayısı: {objectCount}");
            report.AppendLine($"Yerleştirilen model: {modelLoaded}");
            report.AppendLine($"Eksik Property: {missingProperty}");
            report.AppendLine($"Eksik FBX/model: {missingModel}");
            report.AppendLine($"Eklenen MeshCollider: {colliderCount}");
            report.AppendLine();

            if (missingPropertyIds.Count > 0)
            {
                report.AppendLine("Eksik Property ID'leri:");
                foreach (var item in missingPropertyIds.OrderByDescending(x => x.Value))
                    report.AppendLine($"  {item.Key} x{item.Value}");
                report.AppendLine();
            }

            if (missingModelNames.Count > 0)
            {
                report.AppendLine("Bulunamayan model adları:");
                foreach (var item in missingModelNames.OrderByDescending(x => x.Value))
                    report.AppendLine($"  {item.Key} x{item.Value}");
            }

            WriteReport(report.ToString());

            EditorSceneManager.MarkSceneDirty(scene);
            EditorSceneManager.SaveScene(scene, ScenePath);
            AssetDatabase.SaveAssets();
            AssetDatabase.Refresh();

            Selection.activeGameObject = objectRoot.gameObject;

            EditorUtility.DisplayDialog(
                "Pyungmoo objeleri hazır",
                $"Chunk: {chunkCount}\n" +
                $"AreaData objesi: {objectCount}\n" +
                $"Yerleştirilen: {modelLoaded}\n" +
                $"Eksik Property: {missingProperty}\n" +
                $"Eksik model: {missingModel}\n\n" +
                $"Detay raporu:\n{GeneratedReportPath}",
                "Tamam");
        }
        catch (Exception ex)
        {
            Debug.LogException(ex);
            EditorUtility.DisplayDialog("Pyungmoo object import hatası", ex.Message, "Tamam");
        }
    }

    private static Scene OpenPyungmooScene()
    {
        if (!File.Exists(Path.Combine(Application.dataPath, "Scenes", "Pyungmoo.unity")))
            throw new FileNotFoundException("Pyungmoo sahnesi bulunamadı.", ScenePath);

        Scene scene = SceneManager.GetActiveScene();
        if (!string.Equals(scene.path, ScenePath, StringComparison.OrdinalIgnoreCase))
            scene = EditorSceneManager.OpenScene(ScenePath, OpenSceneMode.Single);

        return scene;
    }

    private static string GetRepoRoot()
    {
        string projectRoot = Directory.GetParent(Application.dataPath).FullName;
        return Directory.GetParent(projectRoot).FullName;
    }

    private static IEnumerable<string> DiscoverChunkDirectories(string mapRoot)
    {
        Regex regex = new Regex(@"^\d{6}$", RegexOptions.CultureInvariant);

        return Directory.GetDirectories(mapRoot)
            .Where(d => regex.IsMatch(Path.GetFileName(d)))
            .OrderBy(d => Path.GetFileName(d), StringComparer.Ordinal);
    }

    private static Dictionary<uint, PropertyEntry> LoadProperties(string root)
    {
        var result = new Dictionary<uint, PropertyEntry>();
        string[] files = Directory.GetFiles(root, "*.*", SearchOption.AllDirectories)
            .Where(f =>
            {
                string ext = Path.GetExtension(f);
                return ext.Equals(".pr", StringComparison.OrdinalIgnoreCase) ||
                       ext.Equals(".prb", StringComparison.OrdinalIgnoreCase) ||
                       ext.Equals(".prd", StringComparison.OrdinalIgnoreCase) ||
                       ext.Equals(".prt", StringComparison.OrdinalIgnoreCase) ||
                       ext.Equals(".pte", StringComparison.OrdinalIgnoreCase) ||
                       ext.Equals(".pre", StringComparison.OrdinalIgnoreCase) ||
                       ext.Equals(".pra", StringComparison.OrdinalIgnoreCase);
            })
            .ToArray();

        foreach (string file in files)
        {
            try
            {
                string text = File.ReadAllText(file);

                Match idMatch = Regex.Match(
                    text,
                    @"(?m)^\s*YPRT\s*\r?\n\s*(\d+)\s*$",
                    RegexOptions.CultureInvariant);

                if (!idMatch.Success)
                    continue;

                if (!uint.TryParse(idMatch.Groups[1].Value, NumberStyles.None,
                        CultureInfo.InvariantCulture, out uint id))
                    continue;

                Match nameMatch = Regex.Match(
                    text,
                    @"(?mi)^\s*propertyname\s+""([^""]+)""");

                string propertyName = nameMatch.Success
                    ? nameMatch.Groups[1].Value
                    : Path.GetFileNameWithoutExtension(file);

                Match modelMatch = Regex.Match(
                    text,
                    @"(?mi)^\s*(?:buildingfile|dungeonblockfile|treefile|effectfile)\s+""([^""]+\.(?:gr2|spt|mse))""");

                string modelKey = null;
                if (modelMatch.Success)
                    modelKey = Path.GetFileNameWithoutExtension(
                        modelMatch.Groups[1].Value.Replace('\\', '/'));

                var entry = new PropertyEntry
                {
                    Id = id,
                    PropertyName = propertyName,
                    ModelKey = modelKey,
                    SourcePath = file
                };

                // Prefer a property that explicitly resolves to the shared
                // zone/b/obj or zone/c/building model, rather than a ghost/variant.
                if (!result.TryGetValue(id, out PropertyEntry existing) ||
                    ScoreProperty(entry) > ScoreProperty(existing))
                {
                    result[id] = entry;
                }
            }
            catch (Exception ex)
            {
                Debug.LogWarning($"Property okunamadı: {file}\n{ex.Message}");
            }
        }

        Debug.Log($"Pyungmoo Property index: {result.Count} ID (pr/prb/prd/prt/pte/pre/pra)");
        return result;
    }

    private static int ScoreProperty(PropertyEntry entry)
    {
        string path = entry.SourcePath.Replace('\\', '/').ToLowerInvariant();
        int score = 0;

        if (path.Contains("/property/c/"))
            score += 100;
        else if (path.Contains("/property/b/"))
            score += 90;

        if (path.EndsWith(".prb"))
            score += 20;
        else if (path.EndsWith(".prd"))
            score += 15;
        else if (path.EndsWith(".prt"))
            score += 10;

        if (path.Contains("/ghost/"))
            score -= 50;

        if (!string.IsNullOrEmpty(entry.ModelKey))
            score += 10;

        return score;
    }

    private static Dictionary<string, GameObject> BuildModelIndex()
    {
        var result = new Dictionary<string, GameObject>(StringComparer.OrdinalIgnoreCase);

        string[] guids = AssetDatabase.FindAssets("t:Model");

        foreach (string guid in guids)
        {
            string path = AssetDatabase.GUIDToAssetPath(guid);

            // FBX/Model ana assetini kullan.
            GameObject model = AssetDatabase.LoadAssetAtPath<GameObject>(path);
            if (model == null)
                continue;

            string key = NormalizeKey(Path.GetFileNameWithoutExtension(path));
            if (!result.ContainsKey(key))
                result[key] = model;

            // Existing converter workflows sometimes append "out".
            if (!key.EndsWith("out", StringComparison.OrdinalIgnoreCase))
            {
                string outKey = NormalizeKey(key + "out");
                if (!result.ContainsKey(outKey))
                    result[outKey] = model;
            }
        }

        Debug.Log($"Unity model index: {result.Count} isim");
        return result;
    }

    private static string NormalizeKey(string value)
    {
        if (string.IsNullOrWhiteSpace(value))
            return string.Empty;

        return value.Trim()
            .Replace('\\', '/')
            .Split('/')
            .Last()
            .ToLowerInvariant();
    }

    private static List<AreaObject> ParseAreaData(string file)
    {
        var result = new List<AreaObject>();
        string[] lines = File.ReadAllLines(file);

        for (int i = 0; i < lines.Length; i++)
        {
            string trimmed = lines[i].Trim();

            if (!trimmed.StartsWith("Start Object", StringComparison.OrdinalIgnoreCase))
                continue;

            int objectIndex = result.Count;
            Match objectMatch = Regex.Match(trimmed, @"Start Object(\d+)",
                RegexOptions.IgnoreCase | RegexOptions.CultureInvariant);
            if (objectMatch.Success)
                int.TryParse(objectMatch.Groups[1].Value, out objectIndex);

            List<string> data = new List<string>();

            for (i = i + 1; i < lines.Length; i++)
            {
                string t = lines[i].Trim();

                if (t.StartsWith("End Object", StringComparison.OrdinalIgnoreCase))
                    break;

                if (!string.IsNullOrEmpty(t))
                    data.Add(t);
            }

            if (data.Count < 4)
                continue;

            if (!TryParseVector3(data[0], out Vector3 position))
                continue;

            if (!uint.TryParse(data[1], NumberStyles.Integer,
                    CultureInfo.InvariantCulture, out uint propertyId))
            {
                continue;
            }

            if (!TryParseVector3(data[2].Replace('#', ' '), out Vector3 rotation))
                rotation = Vector3.zero;

            float heightOffset = 0.0f;
            float.TryParse(
                data[3],
                NumberStyles.Float,
                CultureInfo.InvariantCulture,
                out heightOffset);

            result.Add(new AreaObject
            {
                ObjectIndex = objectIndex,
                PropertyId = propertyId,
                Position = position,
                Rotation = rotation,
                HeightOffset = heightOffset
            });
        }

        return result;
    }

    private static bool TryParseVector3(string value, out Vector3 result)
    {
        string[] parts = value.Split(
            new[] { ' ', '\t', '#' },
            StringSplitOptions.RemoveEmptyEntries);

        if (parts.Length < 3)
        {
            result = Vector3.zero;
            return false;
        }

        if (!float.TryParse(parts[0], NumberStyles.Float, CultureInfo.InvariantCulture, out float x))
        {
            result = Vector3.zero;
            return false;
        }

        if (!float.TryParse(parts[1], NumberStyles.Float, CultureInfo.InvariantCulture, out float y))
        {
            result = Vector3.zero;
            return false;
        }

        if (!float.TryParse(parts[2], NumberStyles.Float, CultureInfo.InvariantCulture, out float z))
        {
            result = Vector3.zero;
            return false;
        }

        result = new Vector3(x, y, z);
        return true;
    }

    private static Vector3 ConvertPosition(AreaObject areaObject)
    {
        return new Vector3(
            areaObject.Position.x * ObjectXYScale,
            areaObject.Position.z * ObjectZScale +
                areaObject.HeightOffset * ObjectZScale,
            -areaObject.Position.y * ObjectXYScale);
    }

    private static Quaternion ConvertRotation(Vector3 sourceRotation)
    {
        // Source map uses Z-up; Unity uses Y-up.
        // This basis change preserves full yaw/pitch/roll instead of handling
        // only the common third-angle rotation.
        Quaternion sourceToUnity = Quaternion.Euler(-90.0f, 0.0f, 0.0f);
        Quaternion sourceRotationQuaternion =
            Quaternion.Euler(sourceRotation.x, sourceRotation.y, sourceRotation.z);

        return sourceToUnity *
               sourceRotationQuaternion *
               Quaternion.Inverse(sourceToUnity);
    }

    private static int AddColliders(GameObject root)
    {
        int added = 0;

        MeshFilter[] filters = root.GetComponentsInChildren<MeshFilter>(true);

        foreach (MeshFilter filter in filters)
        {
            if (filter.sharedMesh == null)
                continue;

            if (filter.GetComponent<MeshCollider>() != null)
                continue;

            MeshCollider collider = filter.gameObject.AddComponent<MeshCollider>();
            collider.sharedMesh = filter.sharedMesh;
            collider.convex = false;
            added++;
        }

        return added;
    }

    private static void WriteReport(string text)
    {
        string absolute = Path.Combine(
            Directory.GetParent(Application.dataPath).FullName,
            GeneratedReportPath.Substring("Assets/".Length)
                .Replace('/', Path.DirectorySeparatorChar));

        string dir = Path.GetDirectoryName(absolute);
        if (!string.IsNullOrEmpty(dir))
            Directory.CreateDirectory(dir);

        File.WriteAllText(absolute, text, Encoding.UTF8);
        AssetDatabase.ImportAsset(GeneratedReportPath, ImportAssetOptions.ForceUpdate);
    }

    private static void Increment<TKey>(Dictionary<TKey, int> dictionary, TKey key)
    {
        dictionary.TryGetValue(key, out int count);
        dictionary[key] = count + 1;
    }

    private static string Sanitize(string value)
    {
        foreach (char c in Path.GetInvalidFileNameChars())
            value = value.Replace(c, '_');

        return value.Replace(' ', '_');
    }

    private sealed class PropertyEntry
    {
        public uint Id;
        public string PropertyName;
        public string ModelKey;
        public string SourcePath;
    }

    private sealed class AreaObject
    {
        public int ObjectIndex;
        public uint PropertyId;
        public Vector3 Position;
        public Vector3 Rotation;
        public float HeightOffset;
    }
}
