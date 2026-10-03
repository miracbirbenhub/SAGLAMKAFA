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

public static class Metin2PyungmooDirectBuildingImporter
{
    private const string ScenePath = "Assets/Scenes/Pyungmoo.unity";
    private const string BuildingFolder = "Assets/Metin2Imported/Building";
    private const string RootName = "DirectBuildingObjects";
    private const string ReportPath =
        "Assets/Metin2Generated/Pyungmoo/PyungmooDirectBuildingReport.txt";

    // Same coordinate convention already used by the terrain/object importer.
    private const float CoordinateScale = 0.02f;

    [MenuItem("Metin2/Pyungmoo/LEGACY - Import Existing Building FBX Direct")]
    public static void ImportExistingBuildingFbxDirect()
    {
        try
        {
            Scene scene = OpenScene();

            GameObject mapRoot = GameObject.Find("Pyungmoo");
            if (mapRoot == null)
                throw new InvalidOperationException(
                    "Pyungmoo GameObject'i bulunamadı.");

            Transform oldRoot = mapRoot.transform.Find(RootName);
            if (oldRoot != null)
                UnityEngine.Object.DestroyImmediate(oldRoot.gameObject);

            Transform root = new GameObject(RootName).transform;
            root.SetParent(mapRoot.transform, false);

            string repoRoot = GetRepoRoot();

            string mapRootPath = FindDirectoryOrThrow(
                repoRoot,
                Path.Combine("Metin2Client", "OutdoorC1", "metin2_map_c1"),
                Path.Combine("OutdoorC1", "metin2_map_c1"));

            string propertyRoot = FindDirectoryOrThrow(
                repoRoot,
                Path.Combine("Metin2Client", "Property", "property"),
                Path.Combine("Metin2Client", "Property"),
                Path.Combine("Property", "property"),
                Path.Combine("Property"));

            var propertyRoots = new List<string> { propertyRoot };

            string season3PropertyRoot = Path.Combine(
                repoRoot,
                "Metin2Client",
                "season3_eu",
                "property");

            if (Directory.Exists(season3PropertyRoot))
                propertyRoots.Add(season3PropertyRoot);

            List<string> areaFiles = DiscoverAreaFiles(mapRootPath);
            if (areaFiles.Count == 0)
                throw new InvalidOperationException(
                    "C1 içinde areadata.txt bulunamadı.");

            List<AreaObject> allObjects = new List<AreaObject>();
            foreach (string areaFile in areaFiles)
                allObjects.AddRange(ParseAreaData(areaFile));

            Dictionary<string, GameObject> models =
                BuildExistingBuildingModelIndex();

            if (models.Count == 0)
                throw new InvalidOperationException(
                    "Assets/Metin2Imported/Building altında Unity'nin yükleyebildiği FBX bulunamadı.");

            Dictionary<uint, BuildingProperty> buildingProperties =
                LoadBuildingPropertyIndex(propertyRoots, models);

            int placed = 0;
            int matchedProperty = 0;
            int missingProperty = 0;
            int missingModel = 0;
            int previewPlaced = 0;

            var missingIds = new Dictionary<uint, int>();
            var missingModelNames =
                new Dictionary<string, int>(StringComparer.OrdinalIgnoreCase);

            // The current C1 AreaData in this repository does not reference most
            // of the C1 Building Property IDs. Do not invent map coordinates for
            // those objects. Instead, create a visible library preview so the
            // imported FBX assets can be verified directly inside the scene.

            string currentChunk = null;
            Transform currentChunkRoot = null;
            int chunkCount = 0;

            foreach (string areaFile in areaFiles)
            {
                string chunkName =
                    Path.GetFileName(Path.GetDirectoryName(areaFile));

                if (!string.Equals(
                        currentChunk,
                        chunkName,
                        StringComparison.OrdinalIgnoreCase))
                {
                    currentChunk = chunkName;
                    currentChunkRoot =
                        new GameObject("Buildings_" + chunkName).transform;
                    currentChunkRoot.SetParent(root, false);
                    chunkCount++;
                }

                foreach (AreaObject obj in ParseAreaData(areaFile))
                {
                    if (!buildingProperties.TryGetValue(
                            obj.PropertyId,
                            out BuildingProperty property))
                    {
                        missingProperty++;
                        Increment(missingIds, obj.PropertyId);
                        continue;
                    }

                    matchedProperty++;

                    if (!TryFindModel(
                            models,
                            property.ModelKey,
                            out GameObject model))
                    {
                        missingModel++;
                        Increment(
                            missingModelNames,
                            property.SourceModelName);
                        continue;
                    }

                    GameObject instance =
                        PrefabUtility.InstantiatePrefab(model) as GameObject;

                    if (instance == null)
                    {
                        missingModel++;
                        Increment(
                            missingModelNames,
                            property.SourceModelName);
                        continue;
                    }

                    instance.name =
                        $"BUILD_{obj.ObjectIndex:000}_{Sanitize(property.PropertyName)}";

                    instance.transform.SetParent(
                        currentChunkRoot,
                        false);

                    instance.transform.position =
                        new Vector3(
                            obj.Position.x * CoordinateScale,
                            obj.Position.z * CoordinateScale,
                            -obj.Position.y * CoordinateScale);

                    instance.transform.rotation =
                        ConvertRotation(obj.Rotation);

                    instance.isStatic = true;
                    AddMeshColliders(instance);

                    placed++;
                }
            }

            if (matchedProperty < 3 && models.Count > 0)
            {
                previewPlaced = CreateBuildingLibraryPreview(
                    mapRoot,
                    models,
                    placed);
            }

            var report = new StringBuilder();
            report.AppendLine("Pyungmoo Direct Building Import Report");
            report.AppendLine(
                DateTime.Now.ToString(
                    "yyyy-MM-dd HH:mm:ss",
                    CultureInfo.InvariantCulture));
            report.AppendLine();
            report.AppendLine($"Map root: {mapRootPath}");
            report.AppendLine($"AreaData files: {areaFiles.Count}");
            report.AppendLine($"Chunks: {chunkCount}");
            report.AppendLine($"AreaData objects: {allObjects.Count}");
            report.AppendLine(
                $"Unique AreaData Property IDs: {allObjects.Select(o => o.PropertyId).Distinct().Count()}");
            report.AppendLine(
                $"Building Property IDs indexed: {buildingProperties.Count}");
            report.AppendLine($"Property -> Building matches: {matchedProperty}");
            report.AppendLine($"Placed Building FBX: {placed}");
            report.AppendLine($"Building library preview FBX: {previewPlaced}");
            report.AppendLine($"Missing Property ID: {missingProperty}");
            report.AppendLine($"Missing existing Building FBX: {missingModel}");
            report.AppendLine($"Existing Building FBX indexed: {models.Count}");
            report.AppendLine();
            report.AppendLine(
                "Noesis: kullanılmadı.");
            report.AppendLine(
                "Kaynak model klasörü: Assets/Metin2Imported/Building");
            report.AppendLine(
                "Koordinat: x*0.02, y=z*0.02, z=-sourceY*0.02");

            if (missingIds.Count > 0)
            {
                report.AppendLine();
                report.AppendLine("Eksik Property ID'leri:");
                foreach (var item in missingIds.OrderByDescending(x => x.Value))
                    report.AppendLine($"  {item.Key} x{item.Value}");
            }

            if (missingModelNames.Count > 0)
            {
                report.AppendLine();
                report.AppendLine("Mevcut klasörde bulunamayan model adları:");
                foreach (var item in missingModelNames.OrderByDescending(x => x.Value))
                    report.AppendLine($"  {item.Key} x{item.Value}");
            }

            string absoluteReport =
                Path.Combine(
                    Application.dataPath,
                    "Metin2Generated",
                    "Pyungmoo",
                    "PyungmooDirectBuildingReport.txt");

            Directory.CreateDirectory(Path.GetDirectoryName(absoluteReport));
            File.WriteAllText(
                absoluteReport,
                report.ToString(),
                new UTF8Encoding(false));

            EditorSceneManager.MarkSceneDirty(scene);
            EditorSceneManager.SaveScene(scene, ScenePath);

            AssetDatabase.SaveAssets();
            AssetDatabase.Refresh();

            Selection.activeGameObject = root.gameObject;

            EditorUtility.DisplayDialog(
                "Direct Building Import tamamlandı",
                $"AreaData: {allObjects.Count}\n" +
                $"Building Property records with existing FBX: {buildingProperties.Count}\n" +
                $"AreaData -> Building eşleşmesi: {matchedProperty}\n" +
                $"Haritaya yerleştirilen gerçek Building instance: {placed}\n" +
                "Not: Bu sayaç 47 FBX'in hepsini yerleştirmez; sadece AreaData'da gerçekten referanslanan modelleri yerleştirir.\n" +
                $"Preview olarak yerleştirilen FBX: {previewPlaced}\n" +
                $"Eksik Property: {missingProperty}\n" +
                $"Eksik Building FBX: {missingModel}\n\n" +
                "Noesis kullanılmadı.\n" +
                $"Rapor: {ReportPath}",
                "Tamam");
        }
        catch (Exception ex)
        {
            UnityEngine.Debug.LogException(ex);
            EditorUtility.ClearProgressBar();

            EditorUtility.DisplayDialog(
                "Direct Building Import hatası",
                ex.Message,
                "Tamam");
        }
    }

    private static int CreateBuildingLibraryPreview(
        GameObject mapRoot,
        Dictionary<string, GameObject> models,
        int alreadyPlaced)
    {
        const string previewRootName = "BuildingLibraryPreview";
        Transform old = mapRoot.transform.Find(previewRootName);
        if (old != null)
            UnityEngine.Object.DestroyImmediate(old.gameObject);

        Transform root = new GameObject(previewRootName).transform;
        root.SetParent(mapRoot.transform, false);

        Bounds bounds = new Bounds(Vector3.zero, new Vector3(200f, 20f, 200f));
        bool haveBounds = false;

        foreach (Renderer renderer in
                 mapRoot.GetComponentsInChildren<Renderer>(true))
        {
            if (renderer == null ||
                renderer.transform.IsChildOf(root))
                continue;

            if (!haveBounds)
            {
                bounds = renderer.bounds;
                haveBounds = true;
            }
            else
            {
                bounds.Encapsulate(renderer.bounds);
            }
        }

        Vector3 center = haveBounds ? bounds.center : Vector3.zero;
        float topY = haveBounds ? bounds.max.y : 0f;

        // Keep the preview close to the map center but leave a visible gap
        // between large buildings. This is explicitly a visual asset check,
        // not a replacement for AreaData coordinates.
        const int columns = 7;
        const float spacing = 45f;
        int index = 0;

        foreach (GameObject model in
                 models.Values.Distinct())
        {
            if (model == null)
                continue;

            GameObject instance =
                PrefabUtility.InstantiatePrefab(model) as GameObject;

            if (instance == null)
                continue;

            int row = index / columns;
            int column = index % columns;

            instance.name =
                $"PREVIEW_{index:000}_{Sanitize(model.name)}";

            instance.transform.SetParent(root, false);
            instance.transform.position =
                new Vector3(
                    center.x + (column - (columns - 1) * 0.5f) * spacing,
                    topY + 2f,
                    center.z + row * spacing);
            instance.transform.rotation = Quaternion.identity;
            instance.isStatic = true;

            index++;
        }

        UnityEngine.Debug.Log(
            $"Building library preview: {index} FBX placed under {previewRootName}. " +
            $"Actual AreaData placements: {alreadyPlaced}");

        return index;
    }

    private static Dictionary<uint, BuildingProperty>
        LoadBuildingPropertyIndex(
            IEnumerable<string> propertyRoots,
            Dictionary<string, GameObject> models)
    {
        var result = new Dictionary<uint, BuildingProperty>();

        string[] allowedExtensions =
        {
            ".pr", ".prb", ".prt", ".ptr",
            ".prd", ".pte", ".pre", ".pra"
        };

        int candidates = 0;
        int accepted = 0;

        foreach (string root in propertyRoots.Where(Directory.Exists))
        {
            foreach (string file in Directory.EnumerateFiles(
                         root,
                         "*.*",
                         SearchOption.AllDirectories))
            {
                if (!allowedExtensions.Contains(
                        Path.GetExtension(file),
                        StringComparer.OrdinalIgnoreCase))
                    continue;

                string text;
                try
                {
                    text = File.ReadAllText(file);
                }
                catch
                {
                    continue;
                }

                Match idMatch = Regex.Match(
                    text,
                    @"^\s*YPRT\s*\r?\n\s*(\d+)\s*$",
                    RegexOptions.Multiline |
                    RegexOptions.CultureInvariant);

                if (!idMatch.Success ||
                    !ulong.TryParse(
                        idMatch.Groups[1].Value,
                        NumberStyles.None,
                        CultureInfo.InvariantCulture,
                        out ulong rawId))
                    continue;

                uint id = unchecked((uint)rawId);

                Match sourceMatch = Regex.Match(
                    text,
                    @"^\s*(?:buildingfile|dungenblockfile|dungeonblockfile)\s+""([^""]+)""",
                    RegexOptions.Multiline |
                    RegexOptions.IgnoreCase |
                    RegexOptions.CultureInvariant);

                if (!sourceMatch.Success)
                    continue;

                string sourcePath = sourceMatch.Groups[1].Value;
                string sourceName =
                    Path.GetFileNameWithoutExtension(sourcePath);

                if (string.IsNullOrWhiteSpace(sourceName))
                    continue;

                string modelKey =
                    FindModelKey(models, sourceName);

                if (string.IsNullOrEmpty(modelKey))
                    continue;

                candidates++;

                Match propertyNameMatch = Regex.Match(
                    text,
                    @"^\s*propertyname\s+""([^""]+)""",
                    RegexOptions.Multiline |
                    RegexOptions.IgnoreCase |
                    RegexOptions.CultureInvariant);

                Match typeMatch = Regex.Match(
                    text,
                    @"^\s*propertytype\s+""([^""]+)""",
                    RegexOptions.Multiline |
                    RegexOptions.IgnoreCase |
                    RegexOptions.CultureInvariant);

                var candidate = new BuildingProperty
                {
                    Id = id,
                    PropertyName =
                        propertyNameMatch.Success
                            ? propertyNameMatch.Groups[1].Value
                            : Path.GetFileNameWithoutExtension(file),
                    PropertyType =
                        typeMatch.Success
                            ? typeMatch.Groups[1].Value
                            : string.Empty,
                    SourcePath = sourcePath,
                    SourceModelName = sourceName,
                    ModelKey = modelKey,
                    PropertyFile = file
                };

                if (!result.TryGetValue(id, out BuildingProperty old) ||
                    BuildingPropertyScore(candidate) >
                    BuildingPropertyScore(old))
                {
                    result[id] = candidate;
                    accepted++;
                }
            }
        }

        UnityEngine.Debug.Log(
            $"Direct building property index: {result.Count} IDs, " +
            $"candidates with existing FBX={candidates}, replacements={accepted}");

        return result;
    }

    private static int BuildingPropertyScore(BuildingProperty p)
    {
        int score = 0;
        string source = (p.SourcePath ?? string.Empty)
            .Replace('\\', '/')
            .ToLowerInvariant();

        if (source.Contains("/zone/c/building/"))
            score += 100;
        if (source.Contains("/building/"))
            score += 50;
        if (string.Equals(
                p.PropertyType,
                "Building",
                StringComparison.OrdinalIgnoreCase))
            score += 20;

        string model = NormalizeModelKey(p.SourceModelName);
        if (model.StartsWith("c1-", StringComparison.OrdinalIgnoreCase) ||
            model.StartsWith("c1_", StringComparison.OrdinalIgnoreCase))
            score += 20;

        return score;
    }

    private static Dictionary<string, GameObject>
        BuildExistingBuildingModelIndex()
    {
        var result =
            new Dictionary<string, GameObject>(
                StringComparer.OrdinalIgnoreCase);

        AssetDatabase.Refresh(ImportAssetOptions.ForceUpdate);

        // Search the active Unity project's Assets folder directly.
        // This does not depend on where the Git repository itself is located.
        string assetsRoot = Application.dataPath;

        string[] absoluteFolders =
        {
            Path.Combine(assetsRoot, "Metin2Imported", "Building"),
            Path.Combine(assetsRoot, "Metin2Imported", "Buildings")
        };

        int physicalFbxCount = 0;

        foreach (string absoluteFolder in absoluteFolders)
        {
            if (!Directory.Exists(absoluteFolder))
                continue;

            string[] files = Directory.GetFiles(
                absoluteFolder,
                "*.fbx",
                SearchOption.AllDirectories);

            physicalFbxCount += files.Length;

            foreach (string file in files)
            {
                string relativeToAssets =
                    Path.GetRelativePath(
                        assetsRoot,
                        file)
                    .Replace('\\', '/');

                string assetPath =
                    "Assets/" + relativeToAssets;

                TryAddFbxAsset(result, assetPath);
            }
        }

        // Also ask Unity which Model assets exist in the intended folders.
        foreach (string folder in new[]
                 {
                     "Assets/Metin2Imported/Building",
                     "Assets/Metin2Imported/Buildings"
                 })
        {
            string[] guids;
            try
            {
                guids = AssetDatabase.FindAssets(
                    "t:Model",
                    new[] { folder });
            }
            catch
            {
                guids = Array.Empty<string>();
            }

            foreach (string guid in guids)
            {
                string assetPath =
                    AssetDatabase.GUIDToAssetPath(guid);

                if (assetPath.EndsWith(
                        ".fbx",
                        StringComparison.OrdinalIgnoreCase))
                {
                    TryAddFbxAsset(result, assetPath);
                }
            }
        }

        UnityEngine.Debug.Log(
            $"Direct Building FBX discovery: " +
            $"physicalFBX={physicalFbxCount}, " +
            $"usableAliases={result.Count}, " +
            $"Assets={assetsRoot}");

        return result;
    }

    private static void TryAddFbxAsset(
        Dictionary<string, GameObject> result,
        string assetPath)
    {
        if (string.IsNullOrWhiteSpace(assetPath) ||
            !assetPath.EndsWith(
                ".fbx",
                StringComparison.OrdinalIgnoreCase))
            return;

        GameObject prefab = null;

        try
        {
            AssetDatabase.ImportAsset(
                assetPath,
                ImportAssetOptions.ForceSynchronousImport |
                ImportAssetOptions.ForceUpdate);

            prefab =
                AssetDatabase.LoadAssetAtPath<GameObject>(
                    assetPath);

            if (prefab == null)
            {
                prefab =
                    AssetDatabase.LoadAllAssetsAtPath(assetPath)
                        .OfType<GameObject>()
                        .FirstOrDefault();
            }
        }
        catch (Exception ex)
        {
            UnityEngine.Debug.LogWarning(
                $"FBX import/load hatası: {assetPath}\n{ex.Message}");
            return;
        }

        if (prefab == null)
        {
            UnityEngine.Debug.LogWarning(
                $"FBX dosyası mevcut fakat Unity GameObject çıkaramadı: {assetPath}");
            return;
        }

        string fileName =
            Path.GetFileNameWithoutExtension(assetPath);

        AddModelAlias(
            result,
            fileName,
            prefab,
            fileName.IndexOf(
                "_lod_",
                StringComparison.OrdinalIgnoreCase) >= 0);

        AddModelAlias(
            result,
            NormalizeModelKey(fileName),
            prefab,
            fileName.IndexOf(
                "_lod_",
                StringComparison.OrdinalIgnoreCase) >= 0);
    }
    private static void AddModelAlias(
        Dictionary<string, GameObject> result,
        string key,
        GameObject prefab,
        bool isLod)
    {
        if (string.IsNullOrWhiteSpace(key) || prefab == null)
            return;

        if (!result.ContainsKey(key))
        {
            result.Add(key, prefab);
            return;
        }

        // Keep the non-LOD model when both a normal and an LOD FBX exist.
        if (!isLod)
            result[key] = prefab;
    }

    private static string FindModelKey(
        Dictionary<string, GameObject> models,
        string sourceName)
    {
        string normalized = NormalizeModelKey(sourceName);

        if (models.ContainsKey(normalized))
            return normalized;

        if (models.ContainsKey(sourceName))
            return sourceName;

        // The ready library contains c1-* FBX files while some client
        // Property records can point to the equivalent b1-* asset.
        string empireAlias = ConvertEmpirePrefix(normalized, 'c');
        if (models.ContainsKey(empireAlias))
            return empireAlias;

        // Also allow a/a1 -> c1 and b/b1 -> c1 equivalence.
        foreach (char prefix in new[] { 'a', 'b' })
        {
            string alias = ConvertEmpirePrefix(normalized, prefix);
            if (models.ContainsKey(alias))
                return alias;
        }

        return null;
    }

    private static bool TryFindModel(
        Dictionary<string, GameObject> models,
        string key,
        out GameObject model)
    {
        if (models.TryGetValue(key, out model))
            return true;

        string normalized = NormalizeModelKey(key);
        if (models.TryGetValue(normalized, out model))
            return true;

        model = null;
        return false;
    }

    private static string NormalizeModelKey(string name)
    {
        if (string.IsNullOrWhiteSpace(name))
            return string.Empty;

        string value = name.Trim();

        value = Regex.Replace(
            value,
            @"_lod_\d+out$",
            string.Empty,
            RegexOptions.IgnoreCase |
            RegexOptions.CultureInvariant);

        value = Regex.Replace(
            value,
            @"_lod_\d+$",
            string.Empty,
            RegexOptions.IgnoreCase |
            RegexOptions.CultureInvariant);

        value = Regex.Replace(
            value,
            @"out$",
            string.Empty,
            RegexOptions.IgnoreCase |
            RegexOptions.CultureInvariant);

        return value.ToLowerInvariant();
    }

    private static string ConvertEmpirePrefix(
        string normalized,
        char targetPrefix)
    {
        if (string.IsNullOrWhiteSpace(normalized))
            return normalized;

        if (normalized.Length >= 3 &&
            (normalized[0] == 'a' ||
             normalized[0] == 'b' ||
             normalized[0] == 'c') &&
            normalized[1] == '1' &&
            (normalized[2] == '-' || normalized[2] == '_'))
        {
            return targetPrefix + normalized.Substring(1);
        }

        return normalized;
    }

    private static List<string> DiscoverAreaFiles(string mapRoot)
    {
        return Directory.EnumerateFiles(
                mapRoot,
                "areadata.txt",
                SearchOption.AllDirectories)
            .Where(
                p =>
                Regex.IsMatch(
                    Path.GetFileName(
                        Path.GetDirectoryName(p)) ?? string.Empty,
                    @"^\d{6}$"))
            .OrderBy(
                p => Path.GetFileName(
                    Path.GetDirectoryName(p)),
                StringComparer.Ordinal)
            .ToList();
    }

    private static List<AreaObject> ParseAreaData(string file)
    {
        var result = new List<AreaObject>();
        string[] lines = File.ReadAllLines(file);

        for (int i = 0; i < lines.Length; i++)
        {
            string trimmed = lines[i].Trim();

            if (!trimmed.StartsWith(
                    "Start Object",
                    StringComparison.OrdinalIgnoreCase))
                continue;

            Match objectMatch = Regex.Match(
                trimmed,
                @"Start Object(\d+)",
                RegexOptions.IgnoreCase |
                RegexOptions.CultureInvariant);

            int objectIndex = result.Count;

            if (objectMatch.Success)
            {
                int.TryParse(
                    objectMatch.Groups[1].Value,
                    NumberStyles.Integer,
                    CultureInfo.InvariantCulture,
                    out objectIndex);
            }

            var data = new List<string>();

            for (int j = i + 1; j < lines.Length; j++)
            {
                string line = lines[j].Trim();

                if (line.StartsWith(
                        "End Object",
                        StringComparison.OrdinalIgnoreCase))
                {
                    i = j;
                    break;
                }

                if (!string.IsNullOrWhiteSpace(line))
                    data.Add(line);
            }

            if (data.Count < 2)
                continue;

            if (!TryParseVector3(data[0], out Vector3 position))
                continue;

            if (!uint.TryParse(
                    data[1],
                    NumberStyles.Integer,
                    CultureInfo.InvariantCulture,
                    out uint propertyId))
                continue;

            Vector3 rotation = Vector3.zero;
            if (data.Count >= 3)
                TryParseVector3(data[2].Replace('#', ' '), out rotation);

            float heightOffset = 0.0f;
            if (data.Count >= 4)
            {
                float.TryParse(
                    data[3],
                    NumberStyles.Float,
                    CultureInfo.InvariantCulture,
                    out heightOffset);
            }

            result.Add(
                new AreaObject
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

    private static bool TryParseVector3(
        string value,
        out Vector3 result)
    {
        string[] parts = value.Split(
            new[] { ' ', '\t', '#' },
            StringSplitOptions.RemoveEmptyEntries);

        if (parts.Length < 3)
        {
            result = Vector3.zero;
            return false;
        }

        if (!float.TryParse(
                parts[0],
                NumberStyles.Float,
                CultureInfo.InvariantCulture,
                out float x) ||
            !float.TryParse(
                parts[1],
                NumberStyles.Float,
                CultureInfo.InvariantCulture,
                out float y) ||
            !float.TryParse(
                parts[2],
                NumberStyles.Float,
                CultureInfo.InvariantCulture,
                out float z))
        {
            result = Vector3.zero;
            return false;
        }

        result = new Vector3(x, y, z);
        return true;
    }

    private static Quaternion ConvertRotation(Vector3 rotation)
    {
        return Quaternion.Euler(
            rotation.x,
            rotation.y,
            rotation.z);
    }

    private static void AddMeshColliders(GameObject root)
    {
        MeshFilter[] filters =
            root.GetComponentsInChildren<MeshFilter>(true);

        foreach (MeshFilter filter in filters)
        {
            if (filter.sharedMesh == null)
                continue;

            if (filter.GetComponent<MeshCollider>() != null)
                continue;

            var collider = filter.gameObject.AddComponent<MeshCollider>();
            collider.sharedMesh = filter.sharedMesh;
            collider.convex = false;
        }
    }

    private static Scene OpenScene()
    {
        SceneAsset asset =
            AssetDatabase.LoadAssetAtPath<SceneAsset>(ScenePath);

        if (asset == null)
            throw new FileNotFoundException(
                "Pyungmoo scene bulunamadı.",
                ScenePath);

        Scene scene = SceneManager.GetActiveScene();

        if (!string.Equals(
                scene.path,
                ScenePath,
                StringComparison.OrdinalIgnoreCase))
        {
            scene = EditorSceneManager.OpenScene(
                ScenePath,
                OpenSceneMode.Single);
        }

        return scene;
    }

    private static string GetRepoRoot()
    {
        string projectRoot =
            Directory.GetParent(Application.dataPath).FullName;

        return Directory.GetParent(projectRoot).FullName;
    }

    private static string FindDirectoryOrThrow(
        string repoRoot,
        params string[] candidates)
    {
        foreach (string relative in candidates)
        {
            string full = Path.Combine(repoRoot, relative);
            if (Directory.Exists(full))
                return full;
        }

        throw new DirectoryNotFoundException(
            "Gerekli klasör bulunamadı:\n" +
            string.Join("\n", candidates));
    }

    private static void Increment<TKey>(
        Dictionary<TKey, int> dictionary,
        TKey key)
    {
        if (dictionary.TryGetValue(key, out int count))
            dictionary[key] = count + 1;
        else
            dictionary[key] = 1;
    }

    private static string Sanitize(string name)
    {
        if (string.IsNullOrWhiteSpace(name))
            return "Unknown";

        foreach (char c in Path.GetInvalidFileNameChars())
            name = name.Replace(c, '_');

        return name.Replace(' ', '_');
    }

    private sealed class AreaObject
    {
        public int ObjectIndex;
        public uint PropertyId;
        public Vector3 Position;
        public Vector3 Rotation;
        public float HeightOffset;
    }

    private sealed class BuildingProperty
    {
        public uint Id;
        public string PropertyName;
        public string PropertyType;
        public string SourcePath;
        public string SourceModelName;
        public string ModelKey;
        public string PropertyFile;
    }
}
