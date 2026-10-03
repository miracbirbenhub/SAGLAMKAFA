using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using Process = System.Diagnostics.Process;
using ProcessStartInfo = System.Diagnostics.ProcessStartInfo;

using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;

public static class Metin2PyungmooObjectImporter
{
    private const string ScenePath = "Assets/Scenes/Pyungmoo.unity";
    private const string ObjectRootName = "MapObjects";
    private const string AutoModelFolder = "Assets/Metin2Generated/Pyungmoo/AutoModels";
    private const string ReportPath = "Assets/Metin2Generated/Pyungmoo/PyungmooObjectImportReport.txt";

    // AreaData coordinates are in 100-unit map cells.
    // The map terrain uses CellScale=200, so one AreaData unit is 0.02 Unity metres.
    // Source Y axis is inverted relative to Unity Z.
    private const float CoordinateScale = 0.02f;

    private const int NoesisTimeoutMs = 120000;

    [MenuItem("Metin2/Pyungmoo/Import Map Objects")]
    public static void ImportMapObjects()
    {
        try
        {
            Scene scene = OpenPyungmooScene();

            GameObject mapRoot = GameObject.Find("Pyungmoo");
            if (mapRoot == null)
                throw new InvalidOperationException("Pyungmoo GameObject'i bulunamadı.");

            DeleteExistingObjectRoot(mapRoot);

            Transform objectRoot = new GameObject(ObjectRootName).transform;
            objectRoot.SetParent(mapRoot.transform, false);

            string repoRoot = GetRepoRoot();

            string mapRootPath = FindDirectoryOrThrow(
                repoRoot,
                Path.Combine("Metin2Client", "OutdoorC1", "metin2_map_c1"),
                Path.Combine("OutdoorC1", "metin2_map_c1"));

            List<string> areaFiles = DiscoverAreaFiles(mapRootPath);
            if (areaFiles.Count == 0)
                throw new InvalidOperationException(
                    "Pyungmoo C1 içinde areadata.txt bulunamadı:\n" + mapRootPath);

            string propertyRoot = FindDirectoryOrThrow(
                repoRoot,
                Path.Combine("Metin2Client", "Property", "property"),
                Path.Combine("Metin2Client", "Property"),
                Path.Combine("Property", "property"),
                Path.Combine("Property"));

            var propertyRoots = new List<string>
            {
                propertyRoot
            };

            string season3PropertyRoot = Path.Combine(
                repoRoot,
                "Metin2Client",
                "season3_eu",
                "property");

            if (Directory.Exists(season3PropertyRoot))
                propertyRoots.Add(season3PropertyRoot);

            Dictionary<uint, PropertyEntry> properties =
                LoadProperties(propertyRoots);

            var allObjects = new List<AreaObject>();

            foreach (string areaFile in areaFiles)
                allObjects.AddRange(ParseAreaData(areaFile));

            int propertyMatches = allObjects.Count(
                o => properties.ContainsKey(o.PropertyId));

            int uniquePropertyMatches = allObjects
                .Where(o => properties.ContainsKey(o.PropertyId))
                .Select(o => o.PropertyId)
                .Distinct()
                .Count();

            UnityEngine.Debug.Log(
                $"Pyungmoo preflight: AreaData={allObjects.Count}, " +
                $"Property matches={propertyMatches}, " +
                $"unique Property matches={uniquePropertyMatches}, " +
                $"Property index={properties.Count}");

            // Resolve each Property's source by its full "ymir work/..." path,
            // not merely by basename. The client can contain the same filename
            // in multiple zones/maps.
            Dictionary<string, string> sourceByRelativePath =
                BuildSourceFileIndex(repoRoot);

            string noesisPath = FindNoesis(repoRoot);

            ConversionStats conversion = new ConversionStats();

            if (!string.IsNullOrEmpty(noesisPath))
            {
                List<PropertyEntry> neededProperties = allObjects
                    .Where(o => properties.ContainsKey(o.PropertyId))
                    .Select(o => properties[o.PropertyId])
                    .Where(IsGeometryProperty)
                    .GroupBy(p => NormalizePropertySourcePath(p.SourcePath),
                        StringComparer.OrdinalIgnoreCase)
                    .Select(g => g.First())
                    .ToList();

                conversion = AutoConvertMissingModels(
                    noesisPath,
                    neededProperties,
                    sourceByRelativePath);
            }
            else
            {
                UnityEngine.Debug.LogWarning(
                    "Noesis.exe bulunamadı; eksik modeller dönüştürülmeyecek.");
            }

            AssetDatabase.Refresh();

            Dictionary<string, GameObject> modelIndex = BuildModelIndex();

            int chunkCount = 0;
            int placed = 0;
            int missingProperty = 0;
            int missingModel = 0;
            int unsupportedProperty = 0;

            var missingPropertyIds = new Dictionary<uint, int>();
            var missingModels = new Dictionary<string, int>(
                StringComparer.OrdinalIgnoreCase);

            string currentChunk = null;
            Transform currentChunkRoot = null;

            foreach (string areaFile in areaFiles)
            {
                string chunkName = Path.GetFileName(
                    Path.GetDirectoryName(areaFile));

                if (!string.Equals(
                        currentChunk,
                        chunkName,
                        StringComparison.OrdinalIgnoreCase))
                {
                    currentChunk = chunkName;

                    currentChunkRoot = new GameObject(
                        "Objects_" + chunkName).transform;

                    currentChunkRoot.SetParent(
                        objectRoot,
                        false);

                    chunkCount++;
                }

                foreach (AreaObject obj in ParseAreaData(areaFile))
                {
                    if (!properties.TryGetValue(
                            obj.PropertyId,
                            out PropertyEntry property))
                    {
                        missingProperty++;
                        Increment(
                            missingPropertyIds,
                            obj.PropertyId);
                        continue;
                    }

                    if (!IsGeometryProperty(property))
                    {
                        unsupportedProperty++;
                        continue;
                    }

                    string modelName =
                        Path.GetFileNameWithoutExtension(
                            property.SourcePath);

                    if (!TryFindModel(
                            modelIndex,
                            modelName,
                            out GameObject model))
                    {
                        missingModel++;
                        Increment(
                            missingModels,
                            modelName);
                        continue;
                    }

                    GameObject instance =
                        PrefabUtility.InstantiatePrefab(model)
                        as GameObject;

                    if (instance == null)
                    {
                        missingModel++;
                        Increment(
                            missingModels,
                            modelName);
                        continue;
                    }

                    instance.name =
                        $"OBJ_{obj.ObjectIndex:000}_{Sanitize(property.PropertyName)}";

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

            var report = new StringBuilder();

            report.AppendLine("Pyungmoo Object Import Report");
            report.AppendLine(
                DateTime.Now.ToString(
                    "yyyy-MM-dd HH:mm:ss",
                    CultureInfo.InvariantCulture));
            report.AppendLine();
            report.AppendLine($"Map root: {mapRootPath}");
            report.AppendLine($"AreaData files: {areaFiles.Count}");
            report.AppendLine($"Chunk: {chunkCount}");
            report.AppendLine($"AreaData objesi: {allObjects.Count}");
            report.AppendLine(
                $"Property eşleşmesi: {propertyMatches}");
            report.AppendLine(
                $"Unique Property eşleşmesi: {uniquePropertyMatches}");
            report.AppendLine(
                $"Yerleştirilen: {placed}");
            report.AppendLine(
                $"Eksik Property: {missingProperty}");
            report.AppendLine(
                $"Eksik model/FBX: {missingModel}");
            report.AppendLine(
                $"Desteklenmeyen Property türü: {unsupportedProperty}");
            report.AppendLine(
                $"Yeni FBX: {conversion.Converted}");
            report.AppendLine(
                $"Mevcut model: {conversion.AlreadyExisting}");
            report.AppendLine(
                $"Kaynak bulunamadı: {conversion.MissingSource}");
            report.AppendLine(
                $"Noesis hatası: {conversion.Failed}");

            if (conversion.FailureDetails.Count > 0)
            {
                report.AppendLine();
                report.AppendLine("Noesis hata detayları:");

                foreach (string detail in conversion.FailureDetails)
                {
                    report.AppendLine(detail);
                    report.AppendLine();
                }
            }

            report.AppendLine();
            report.AppendLine(
                $"Noesis: {(string.IsNullOrEmpty(noesisPath) ? "bulunamadı" : noesisPath)}");
            report.AppendLine(
                "Noesis dönüşümü: -rotate 90 0 0");
            report.AppendLine(
                "Koordinat ölçeği: 50 Metin2 unit = 1 Unity metre (0.02 m/unit)");
            report.AppendLine();

            if (missingModels.Count > 0)
            {
                report.AppendLine(
                    "Bulunamayan Unity model adları:");

                foreach (var item in missingModels
                             .OrderByDescending(x => x.Value))
                {
                    report.AppendLine(
                        $"  {item.Key} x{item.Value}");
                }

                report.AppendLine();
            }

            if (missingPropertyIds.Count > 0)
            {
                report.AppendLine(
                    "Bulunamayan Property ID'leri:");

                foreach (var item in missingPropertyIds
                             .OrderByDescending(x => x.Value))
                {
                    report.AppendLine(
                        $"  {item.Key} x{item.Value}");
                }
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
                $"AreaData: {allObjects.Count}\n" +
                $"Property eşleşmesi: {propertyMatches}\n" +
                $"Yerleştirilen: {placed}\n" +
                $"Eksik Property: {missingProperty}\n" +
                $"Eksik model: {missingModel}\n" +
                $"Yeni FBX: {conversion.Converted}\n" +
                $"Noesis hata: {conversion.Failed}\n\n" +
                $"Rapor:\n{ReportPath}",
                "Tamam");
        }
        catch (Exception ex)
        {
            UnityEngine.Debug.LogException(ex);

            EditorUtility.DisplayDialog(
                "Pyungmoo object import hatası",
                ex.Message,
                "Tamam");
        }
    }


    [MenuItem("Metin2/Pyungmoo/Import Existing Buildings Only")]
    public static void ImportExistingBuildingsOnly()
    {
        try
        {
            Scene scene = OpenPyungmooScene();

            GameObject mapRoot = GameObject.Find("Pyungmoo");
            if (mapRoot == null)
                throw new InvalidOperationException("Pyungmoo GameObject'i bulunamadı.");

            const string buildingsRootName = "Metin2Buildings";
            Transform oldRoot = mapRoot.transform.Find(buildingsRootName);
            if (oldRoot != null)
                UnityEngine.Object.DestroyImmediate(oldRoot.gameObject);

            Transform buildingsRoot =
                new GameObject(buildingsRootName).transform;
            buildingsRoot.SetParent(mapRoot.transform, false);

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

            Dictionary<uint, PropertyEntry> properties =
                LoadProperties(propertyRoots);

            List<string> areaFiles = DiscoverAreaFiles(mapRootPath);

            const string buildingFolder =
                "Assets/Metin2Imported/Building";

            Dictionary<string, GameObject> buildingModels =
                BuildBuildingModelIndex(buildingFolder);

            UnityEngine.Debug.Log(
                $"Pyungmoo existing Building model index: {buildingModels.Count} alias");

            // A single YPRT/CRC can appear in multiple Property files.
            // Prefer the candidate whose source basename actually exists
            // in our prepared Building FBX library. This prevents a generic
            // object such as general_obj_* from winning over a C1 building.
            PreferPropertiesForExistingBuildings(
                properties,
                propertyRoots,
                buildingModels);

            int buildingProperties = 0;
            int placed = 0;
            int missingProperty = 0;
            int missingModel = 0;

            var missingModels =
                new Dictionary<string, int>(
                    StringComparer.OrdinalIgnoreCase);

            foreach (string areaFile in areaFiles)
            {
                string chunkName = Path.GetFileName(
                    Path.GetDirectoryName(areaFile));

                Transform chunkRoot =
                    new GameObject("Buildings_" + chunkName).transform;

                chunkRoot.SetParent(buildingsRoot, false);

                foreach (AreaObject obj in ParseAreaData(areaFile))
                {
                    if (!properties.TryGetValue(
                            obj.PropertyId,
                            out PropertyEntry property))
                    {
                        missingProperty++;
                        continue;
                    }

                    if (!IsBuildingProperty(property))
                        continue;

                    buildingProperties++;

                    string modelName =
                        Path.GetFileNameWithoutExtension(
                            property.SourcePath);

                    if (!TryFindBuildingModel(
                            buildingModels,
                            modelName,
                            out GameObject model))
                    {
                        missingModel++;
                        Increment(missingModels, modelName);
                        continue;
                    }

                    GameObject instance =
                        PrefabUtility.InstantiatePrefab(model)
                        as GameObject;

                    if (instance == null)
                    {
                        missingModel++;
                        Increment(missingModels, modelName);
                        continue;
                    }

                    instance.name =
                        $"BUILD_{obj.ObjectIndex:000}_{Sanitize(property.PropertyName)}";

                    instance.transform.SetParent(
                        chunkRoot,
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

            var report = new StringBuilder();
            report.AppendLine("Pyungmoo Existing Building Import Report");
            report.AppendLine(
                DateTime.Now.ToString(
                    "yyyy-MM-dd HH:mm:ss",
                    CultureInfo.InvariantCulture));
            report.AppendLine();
            report.AppendLine($"AreaData files: {areaFiles.Count}");
            report.AppendLine($"Building Property: {buildingProperties}");
            report.AppendLine($"Yerleştirilen mevcut Building FBX: {placed}");
            report.AppendLine($"Eksik Property: {missingProperty}");
            report.AppendLine($"Eksik Building FBX: {missingModel}");
            report.AppendLine();
            report.AppendLine(
                "Kaynak klasör: Assets/Metin2Imported/Building");
            report.AppendLine(
                "Koordinat ölçeği: 0.02 Unity m / AreaData unit");
            report.AppendLine(
                "Bu importer Noesis ile yeni model üretmez.");

            if (missingModels.Count > 0)
            {
                report.AppendLine();
                report.AppendLine("Bulunamayan Building model adları:");

                foreach (var item in missingModels
                             .OrderByDescending(x => x.Value))
                {
                    report.AppendLine(
                        $"  {item.Key} x{item.Value}");
                }
            }

            File.WriteAllText(
                Path.Combine(
                    Application.dataPath,
                    "Metin2Generated",
                    "Pyungmoo",
                    "PyungmooBuildingImportReport.txt"),
                report.ToString());

            EditorSceneManager.MarkSceneDirty(scene);
            EditorSceneManager.SaveScene(scene, ScenePath);

            AssetDatabase.SaveAssets();
            AssetDatabase.Refresh();

            Selection.activeGameObject =
                buildingsRoot.gameObject;

            EditorUtility.DisplayDialog(
                "Building yerleşimi tamamlandı",
                $"Building Property: {buildingProperties}\n" +
                $"Yerleştirilen mevcut FBX: {placed}\n" +
                $"Eksik Building FBX: {missingModel}\n\n" +
                "Sadece Assets/Metin2Imported/Building kullanıldı.\n" +
                "Yeni Noesis dönüşümü yapılmadı.\n\n" +
                "Rapor:\nAssets/Metin2Generated/Pyungmoo/PyungmooBuildingImportReport.txt",
                "Tamam");
        }
        catch (Exception ex)
        {
            UnityEngine.Debug.LogException(ex);
            EditorUtility.DisplayDialog(
                "Building import hatası",
                ex.Message,
                "Tamam");
        }
    }

    [MenuItem("Metin2/Pyungmoo/Rebuild Buildings From AreaData")]
    public static void RebuildBuildingsFromAreaData()
    {
        try
        {
            Scene scene = OpenPyungmooScene();

            GameObject mapRoot = GameObject.Find("Pyungmoo");
            if (mapRoot == null)
                throw new InvalidOperationException("Pyungmoo GameObject'i bulunamadı.");

            const string buildingsRootName = "Metin2Buildings";

            Transform oldRoot =
                mapRoot.transform.Find(buildingsRootName);

            if (oldRoot != null)
                UnityEngine.Object.DestroyImmediate(
                    oldRoot.gameObject);

            Transform buildingsRoot =
                new GameObject(buildingsRootName).transform;

            buildingsRoot.SetParent(
                mapRoot.transform,
                false);

            string repoRoot = GetRepoRoot();

            string mapRootPath = FindDirectoryOrThrow(
                repoRoot,
                Path.Combine(
                    "Metin2Client",
                    "OutdoorC1",
                    "metin2_map_c1"),
                Path.Combine(
                    "OutdoorC1",
                    "metin2_map_c1"));

            string propertyRoot = FindDirectoryOrThrow(
                repoRoot,
                Path.Combine(
                    "Metin2Client",
                    "Property",
                    "property"),
                Path.Combine(
                    "Metin2Client",
                    "Property"),
                Path.Combine(
                    "Property",
                    "property"),
                Path.Combine(
                    "Property"));

            var propertyRoots =
                new List<string>
                {
                    propertyRoot
                };

            string season3PropertyRoot =
                Path.Combine(
                    repoRoot,
                    "Metin2Client",
                    "season3_eu",
                    "property");

            if (Directory.Exists(
                    season3PropertyRoot))
            {
                propertyRoots.Add(
                    season3PropertyRoot);
            }

            Dictionary<uint, PropertyEntry> properties =
                LoadProperties(propertyRoots);

            List<string> areaFiles =
                DiscoverAreaFiles(mapRootPath);

            const string buildingFolder =
                "Assets/Metin2Imported/Building";

            Dictionary<string, GameObject> buildingModels =
                BuildBuildingModelIndex(
                    buildingFolder);

            PreferPropertiesForExistingBuildings(
                properties,
                propertyRoots,
                buildingModels);

            int buildingObjects = 0;
            int matchedReadyModels = 0;
            int placed = 0;
            int missingProperty = 0;
            int missingReadyModel = 0;

            var missingModels =
                new Dictionary<string, int>(
                    StringComparer.OrdinalIgnoreCase);

            foreach (string areaFile in areaFiles)
            {
                string chunkName =
                    Path.GetFileName(
                        Path.GetDirectoryName(areaFile));

                Transform chunkRoot =
                    new GameObject(
                        "Buildings_" + chunkName).transform;

                chunkRoot.SetParent(
                    buildingsRoot,
                    false);

                foreach (AreaObject obj in
                         ParseAreaData(areaFile))
                {
                    if (!properties.TryGetValue(
                            obj.PropertyId,
                            out PropertyEntry property))
                    {
                        missingProperty++;
                        continue;
                    }

                    if (!IsBuildingProperty(
                            property))
                    {
                        continue;
                    }

                    buildingObjects++;

                    string modelName =
                        Path.GetFileNameWithoutExtension(
                            NormalizePropertySourcePath(
                                property.SourcePath));

                    if (string.IsNullOrWhiteSpace(
                            modelName))
                    {
                        modelName =
                            property.PropertyName;
                    }

                    if (!TryFindBuildingModel(
                            buildingModels,
                            modelName,
                            out GameObject model))
                    {
                        missingReadyModel++;

                        Increment(
                            missingModels,
                            modelName);

                        continue;
                    }

                    matchedReadyModels++;

                    GameObject instance =
                        PrefabUtility.InstantiatePrefab(
                            model) as GameObject;

                    if (instance == null)
                    {
                        missingReadyModel++;

                        Increment(
                            missingModels,
                            modelName);

                        continue;
                    }

                    instance.name =
                        $"BUILD_{obj.ObjectIndex:000}_{Sanitize(property.PropertyName)}";

                    instance.transform.SetParent(
                        chunkRoot,
                        false);

                    instance.transform.position =
                        new Vector3(
                            obj.Position.x * CoordinateScale,
                            obj.Position.z * CoordinateScale,
                            -obj.Position.y * CoordinateScale);

                    instance.transform.rotation =
                        ConvertRotation(obj.Rotation);

                    instance.isStatic = true;

                    AddMeshColliders(
                        instance);

                    placed++;
                }
            }

            var report =
                new StringBuilder();

            report.AppendLine(
                "Pyungmoo Prepared Building Placement Report");

            report.AppendLine(
                DateTime.Now.ToString(
                    "yyyy-MM-dd HH:mm:ss",
                    CultureInfo.InvariantCulture));

            report.AppendLine();

            report.AppendLine(
                $"AreaData files: {areaFiles.Count}");

            report.AppendLine(
                $"Building object instances: {buildingObjects}");

            report.AppendLine(
                $"Hazır FBX ile eşleşen instance: {matchedReadyModels}");

            report.AppendLine(
                $"Yerleştirilen: {placed}");

            report.AppendLine(
                $"Eksik Property: {missingProperty}");

            report.AppendLine(
                $"Hazır FBX bulunamayan: {missingReadyModel}");

            report.AppendLine();

            report.AppendLine(
                "Kaynak: Assets/Metin2Imported/Building");

            report.AppendLine(
                "Noesis kullanılmadı.");

            report.AppendLine(
                "Yeni FBX üretilmedi.");

            report.AppendLine(
                "Koordinat ölçeği: 0.02 Unity m / AreaData unit");

            if (missingModels.Count > 0)
            {
                report.AppendLine();

                report.AppendLine(
                    "Hazır klasörde bulunamayan kaynak modeller:");

                foreach (var item in
                         missingModels.OrderByDescending(
                             x => x.Value))
                {
                    report.AppendLine(
                        $"  {item.Key} x{item.Value}");
                }
            }

            string reportAbsolute =
                Path.Combine(
                    Application.dataPath,
                    "Metin2Generated",
                    "Pyungmoo",
                    "PyungmooBuildingRebuildReport.txt");

            string reportDirectory =
                Path.GetDirectoryName(
                    reportAbsolute);

            if (!string.IsNullOrEmpty(
                    reportDirectory))
            {
                Directory.CreateDirectory(
                    reportDirectory);
            }

            File.WriteAllText(
                reportAbsolute,
                report.ToString(),
                new UTF8Encoding(false));

            EditorSceneManager.MarkSceneDirty(
                scene);

            EditorSceneManager.SaveScene(
                scene,
                ScenePath);

            AssetDatabase.SaveAssets();
            AssetDatabase.Refresh();

            Selection.activeGameObject =
                buildingsRoot.gameObject;

            EditorUtility.DisplayDialog(
                "Pyungmoo hazır binalar yerleştirildi",
                $"Building instances: {buildingObjects}\n" +
                $"Hazır FBX eşleşmesi: {matchedReadyModels}\n" +
                $"Yerleştirilen: {placed}\n" +
                $"Eksik hazır FBX: {missingReadyModel}\n\n" +
                "Noesis çalıştırılmadı.\n" +
                "Sadece Assets/Metin2Imported/Building kullanıldı.",
                "Tamam");
        }
        catch (Exception ex)
        {
            UnityEngine.Debug.LogException(ex);
            EditorUtility.ClearProgressBar();

            EditorUtility.DisplayDialog(
                "Pyungmoo Building placement hatası",
                ex.Message,
                "Tamam");
        }
    }

    private static bool IsBuildingProperty(PropertyEntry property)
    {
        if (property == null ||
            string.IsNullOrWhiteSpace(property.SourcePath))
            return false;

        if (string.Equals(
                property.PropertyType,
                "Building",
                StringComparison.OrdinalIgnoreCase))
            return true;

        string source =
            property.SourcePath
                .Replace('\\', '/')
                .ToLowerInvariant();

        return source.Contains("/building/") ||
               source.StartsWith("building/") ||
               source.Contains("\\building\\");
    }

    private static void PreferPropertiesForExistingBuildings(
        Dictionary<uint, PropertyEntry> properties,
        IEnumerable<string> propertyRoots,
        Dictionary<string, GameObject> buildingModels)
    {
        if (properties == null ||
            propertyRoots == null ||
            buildingModels == null ||
            buildingModels.Count == 0)
            return;

        var preferredNames =
            new HashSet<string>(
                buildingModels.Keys
                    .Select(NormalizeBuildingModelName)
                    .Where(n => !string.IsNullOrWhiteSpace(n)),
                StringComparer.OrdinalIgnoreCase);

        string[] allowedExtensions =
        {
            ".pr",
            ".prb",
            ".prt",
            ".ptr",
            ".prd",
            ".pte",
            ".pre",
            ".pra"
        };

        int overrides = 0;

        foreach (string root in propertyRoots.Where(Directory.Exists))
        {
            foreach (string file in Directory.EnumerateFiles(
                         root,
                         "*.*",
                         SearchOption.AllDirectories)
                     .Where(f =>
                         allowedExtensions.Contains(
                             Path.GetExtension(f),
                             StringComparer.OrdinalIgnoreCase)))
            {
                try
                {
                    string text = File.ReadAllText(file);

                    Match idMatch =
                        Regex.Match(
                            text,
                            @"(?m)^\\s*YPRT\\s*\\r?\\n\\s*(\\d+)\\s*$",
                            RegexOptions.CultureInvariant);

                    if (!idMatch.Success ||
                        !ulong.TryParse(
                            idMatch.Groups[1].Value,
                            NumberStyles.None,
                            CultureInfo.InvariantCulture,
                            out ulong rawId))
                    {
                        continue;
                    }

                    uint id = unchecked((uint)rawId);

                    Match sourceMatch =
                        Regex.Match(
                            text,
                            @"(?mi)^\\s*(?:buildingfile|dungenblockfile|dungeonblockfile|treefile|effectfile|ambiencefile)\\s+""([^""]+)""");

                    if (!sourceMatch.Success)
                        continue;

                    string sourcePath =
                        sourceMatch.Groups[1].Value;

                    string sourceName =
                        Path.GetFileNameWithoutExtension(
                            sourcePath);

                    string normalized =
                        NormalizeBuildingModelName(sourceName);

                    if (string.IsNullOrWhiteSpace(normalized) ||
                        !preferredNames.Contains(normalized))
                        continue;

                    Match propertyNameMatch =
                        Regex.Match(
                            text,
                            @"(?mi)^\\s*propertyname\\s+""([^""]+)""");

                    Match typeMatch =
                        Regex.Match(
                            text,
                            @"(?mi)^\\s*propertytype\\s+""([^""]+)""");

                    var candidate =
                        new PropertyEntry
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
                            SourcePropertyFile = file
                        };

                    if (!properties.TryGetValue(
                            id,
                            out PropertyEntry existing) ||
                        !string.Equals(
                            NormalizeBuildingModelName(
                                Path.GetFileNameWithoutExtension(
                                    existing.SourcePath ?? string.Empty)),
                            normalized,
                            StringComparison.OrdinalIgnoreCase))
                    {
                        properties[id] = candidate;
                        overrides++;
                    }
                }
                catch
                {
                }
            }
        }

        UnityEngine.Debug.Log(
            $"Existing Building Property overrides: {overrides}");
    }

    private static Dictionary<string, GameObject>
        BuildBuildingModelIndex(string folder)
    {
        var result =
            new Dictionary<string, GameObject>(
                StringComparer.OrdinalIgnoreCase);

        string projectRoot =
            Directory.GetParent(Application.dataPath).FullName;

        string absoluteFolder =
            Path.Combine(
                projectRoot,
                folder.Substring("Assets/".Length)
                    .Replace(
                        '/',
                        Path.DirectorySeparatorChar));

        if (!Directory.Exists(absoluteFolder))
        {
            UnityEngine.Debug.LogWarning(
                $"Building FBX klasörü bulunamadı: {absoluteFolder}");
            return result;
        }

        string[] files =
            Directory.GetFiles(
                absoluteFolder,
                "*.fbx",
                SearchOption.AllDirectories);

        UnityEngine.Debug.Log(
            $"Building FBX dosyaları bulundu: {files.Length} -> {absoluteFolder}");

        foreach (string file in files.OrderBy(
                     p => p,
                     StringComparer.OrdinalIgnoreCase))
        {
            string assetPath =
                "Assets/" +
                Path.GetRelativePath(
                    Path.Combine(
                        projectRoot,
                        "Assets"),
                    file)
                .Replace('\\', '/');

            GameObject prefab = null;

            try
            {
                AssetDatabase.ImportAsset(
                    assetPath,
                    ImportAssetOptions.ForceSynchronousImport);

                prefab =
                    AssetDatabase.LoadAssetAtPath<GameObject>(
                        assetPath);

                if (prefab == null)
                {
                    prefab =
                        AssetDatabase.LoadAllAssetsAtPath(
                                assetPath)
                            .OfType<GameObject>()
                            .FirstOrDefault();
                }
            }
            catch (Exception ex)
            {
                UnityEngine.Debug.LogWarning(
                    $"Building asset import/load hatası: {assetPath}\n{ex.Message}");
            }

            if (prefab == null)
            {
                UnityEngine.Debug.LogWarning(
                    $"Building FBX GameObject olarak yüklenemedi: {assetPath}");
                continue;
            }

            string name =
                Path.GetFileNameWithoutExtension(file);

            AddBuildingModelAlias(
                result,
                name,
                prefab);

            string normalized =
                NormalizeBuildingModelName(name);

            if (!string.IsNullOrEmpty(normalized))
                AddBuildingModelAlias(
                    result,
                    normalized,
                    prefab);
        }

        UnityEngine.Debug.Log(
            $"Existing Building FBX index: {result.Count} alias");

        return result;
    }

    private static void AddBuildingModelAlias(
        Dictionary<string, GameObject> result,
        string name,
        GameObject prefab)
    {
        if (string.IsNullOrWhiteSpace(name) ||
            prefab == null)
            return;

        if (!result.ContainsKey(name))
            result.Add(name, prefab);
    }

    private static string NormalizeBuildingModelName(
        string name)
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

        return value;
    }

    private static bool TryFindBuildingModel(
        Dictionary<string, GameObject> modelIndex,
        string modelName,
        out GameObject model)
    {
        if (modelIndex.TryGetValue(
                modelName,
                out model))
        {
            return true;
        }

        string normalized =
            NormalizeBuildingModelName(modelName);

        if (!string.IsNullOrEmpty(normalized) &&
            modelIndex.TryGetValue(
                normalized,
                out model))
        {
            return true;
        }

        string[] candidates =
        {
            modelName + "out",
            modelName + "_lod_01out",
            normalized + "out",
            normalized + "_lod_01out"
        };

        foreach (string candidate in candidates.Distinct(
                     StringComparer.OrdinalIgnoreCase))
        {
            if (modelIndex.TryGetValue(
                    candidate,
                    out model))
            {
                return true;
            }
        }

        model = null;
        return false;
    }

    private static Scene OpenPyungmooScene()
    {
        SceneAsset sceneAsset =
            AssetDatabase.LoadAssetAtPath<SceneAsset>(ScenePath);

        if (sceneAsset == null)
            throw new FileNotFoundException(
                "Pyungmoo sahnesi Unity AssetDatabase içinde bulunamadı.",
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
            string full = Path.Combine(
                repoRoot,
                relative);

            if (Directory.Exists(full))
                return full;
        }

        string parent =
            Directory.GetParent(repoRoot)?.FullName;

        if (!string.IsNullOrEmpty(parent))
        {
            foreach (string relative in candidates)
            {
                string leaf =
                    Path.GetFileName(
                        relative.TrimEnd(
                            Path.DirectorySeparatorChar,
                            Path.AltDirectorySeparatorChar));

                try
                {
                    string found =
                        Directory.EnumerateDirectories(
                                parent,
                                leaf,
                                SearchOption.AllDirectories)
                            .FirstOrDefault();

                    if (!string.IsNullOrEmpty(found))
                        return found;
                }
                catch
                {
                }
            }
        }

        throw new DirectoryNotFoundException(
            "Gerekli klasör bulunamadı:\n" +
            string.Join("\n", candidates));
    }

    private static List<string> DiscoverAreaFiles(
        string mapRoot)
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

    private static Dictionary<uint, PropertyEntry>
        LoadProperties(IEnumerable<string> propertyRoots)
    {
        var result =
            new Dictionary<uint, PropertyEntry>();

        string[] allowedExtensions =
        {
            ".pr",
            ".prb",
            ".prt",
            ".ptr",
            ".prd",
            ".pte",
            ".pre",
            ".pra"
        };

        IEnumerable<string> files =
            propertyRoots
                .Where(Directory.Exists)
                .SelectMany(
                    root =>
                        Directory.EnumerateFiles(
                            root,
                            "*.*",
                            SearchOption.AllDirectories))
                .Where(
                    f =>
                    allowedExtensions.Contains(
                        Path.GetExtension(f),
                        StringComparer.OrdinalIgnoreCase));

        foreach (string file in files)
        {
            try
            {
                string text = File.ReadAllText(file);

                Match idMatch =
                    Regex.Match(
                        text,
                        @"(?m)^\s*YPRT\s*\r?\n\s*(\d+)\s*$",
                        RegexOptions.CultureInvariant);

                if (!idMatch.Success)
                    continue;

                if (!ulong.TryParse(
                        idMatch.Groups[1].Value,
                        NumberStyles.None,
                        CultureInfo.InvariantCulture,
                        out ulong rawId))
                {
                    continue;
                }

                // AreaData stores the object CRC as a 32-bit value.
                // Some older .prt files in this client contain the same
                // numeric CRC written above the uint range; normalize those
                // values to their low 32 bits.
                uint id = unchecked((uint)rawId);

                Match propertyNameMatch =
                    Regex.Match(
                        text,
                        @"(?mi)^\s*propertyname\s+""([^""]+)""");

                string propertyName =
                    propertyNameMatch.Success
                        ? propertyNameMatch.Groups[1].Value
                        : Path.GetFileNameWithoutExtension(file);

                Match typeMatch =
                    Regex.Match(
                        text,
                        @"(?mi)^\s*propertytype\s+""([^""]+)""");

                string propertyType =
                    typeMatch.Success
                        ? typeMatch.Groups[1].Value
                        : string.Empty;

                Match sourceMatch =
                    Regex.Match(
                        text,
                        @"(?mi)^\s*(?:buildingfile|dungenblockfile|dungeonblockfile|treefile|effectfile|ambiencefile)\s+""([^""]+)""");

                string sourcePath =
                    sourceMatch.Success
                        ? sourceMatch.Groups[1].Value
                        : null;

                var entry =
                    new PropertyEntry
                    {
                        Id = id,
                        PropertyName = propertyName,
                        PropertyType = propertyType,
                        SourcePath = sourcePath,
                        SourcePropertyFile = file
                    };

                if (!result.TryGetValue(
                        id,
                        out PropertyEntry existing) ||
                    PropertyScore(entry) >
                    PropertyScore(existing))
                {
                    result[id] = entry;
                }
            }
            catch (Exception ex)
            {
                UnityEngine.Debug.LogWarning(
                    $"Property okunamadı: {file}\n{ex.Message}");
            }
        }

        UnityEngine.Debug.Log(
            $"Pyungmoo Property index: {result.Count} ID " +
            $"({propertyRoots.Count()} kök)");

        return result;
    }

    private static int PropertyScore(
        PropertyEntry entry)
    {
        int score = 0;

        string path =
            entry.SourcePropertyFile
                .Replace('\\', '/')
                .ToLowerInvariant();

        if (!string.IsNullOrEmpty(entry.SourcePath))
            score += 100;

        if (path.Contains("/property/c/"))
            score += 30;

        if (path.Contains("/property/b/"))
            score += 20;

        if (string.Equals(
                entry.PropertyType,
                "Building",
                StringComparison.OrdinalIgnoreCase))
        {
            score += 10;
        }

        if (string.Equals(
                entry.PropertyType,
                "Tree",
                StringComparison.OrdinalIgnoreCase))
        {
            score += 5;
        }

        return score;
    }

    private static Dictionary<string, string>
        BuildSourceFileIndex(string repoRoot)
    {
        var result =
            new Dictionary<string, string>(
                StringComparer.OrdinalIgnoreCase);

        string clientRoot = Path.Combine(
            repoRoot,
            "Metin2Client");

        if (!Directory.Exists(clientRoot))
            clientRoot = repoRoot;

        foreach (string pattern in new[] { "*.gr2", "*.spt" })
        {
            foreach (string file in Directory.EnumerateFiles(
                         clientRoot,
                         pattern,
                         SearchOption.AllDirectories))
            {
                string relative =
                    Path.GetRelativePath(
                        clientRoot,
                        file)
                    .Replace('\\', '/');

                string normalized =
                    NormalizePropertySourcePath(
                        relative);

                if (!string.IsNullOrEmpty(normalized) &&
                    !result.ContainsKey(normalized))
                {
                    result.Add(normalized, file);
                }
            }
        }

        UnityEngine.Debug.Log(
            $"Metin2 exact source index: {result.Count} dosya");

        return result;
    }

    private static string NormalizePropertySourcePath(
        string sourcePath)
    {
        if (string.IsNullOrWhiteSpace(sourcePath))
            return string.Empty;

        string s =
            sourcePath.Trim()
                .Replace('\\', '/');

        int marker =
            s.IndexOf(
                "ymir work/",
                StringComparison.OrdinalIgnoreCase);

        if (marker >= 0)
        {
            s = s.Substring(
                marker + "ymir work/".Length);
        }
        else
        {
            s = s.TrimStart('/');
        }

        return s.ToLowerInvariant();
    }

    private static string ResolvePropertySource(
        string propertySourcePath,
        Dictionary<string, string> sourceIndex)
    {
        string key =
            NormalizePropertySourcePath(
                propertySourcePath);

        if (sourceIndex.TryGetValue(
                key,
                out string exact))
        {
            return exact;
        }

        // Fallback: some unpack layouts omit "ymir work" from the
        // relative path. Try suffix matching only after exact lookup.
        foreach (KeyValuePair<string, string> pair in sourceIndex)
        {
            if (pair.Key.EndsWith(
                    key,
                    StringComparison.OrdinalIgnoreCase))
            {
                return pair.Value;
            }
        }

        return null;
    }

    private static bool IsGeometryProperty(
        PropertyEntry property)
    {
        if (property == null ||
            string.IsNullOrWhiteSpace(property.SourcePath))
        {
            return false;
        }

        string source =
            property.SourcePath.ToLowerInvariant();

        return source.EndsWith(".gr2") ||
               source.EndsWith(".spt");
    }

    private static ConversionStats
        AutoConvertMissingModels(
            string noesisPath,
            List<PropertyEntry> neededProperties,
            Dictionary<string, string> sourceByRelativePath)
    {
        string projectRoot =
            Directory.GetParent(Application.dataPath).FullName;

        string repoRoot =
            Directory.GetParent(projectRoot).FullName;

        string outputRoot =
            Path.Combine(
                projectRoot,
                AutoModelFolder
                    .Substring("Assets/".Length)
                    .Replace(
                        '/',
                        Path.DirectorySeparatorChar));

        Directory.CreateDirectory(outputRoot);

        HashSet<string> existingModels =
            AssetDatabase.FindAssets("t:Model")
                .Select(AssetDatabase.GUIDToAssetPath)
                .Select(Path.GetFileNameWithoutExtension)
                .Where(n => !string.IsNullOrWhiteSpace(n))
                .ToHashSet(
                    StringComparer.OrdinalIgnoreCase);

        var stats = new ConversionStats();

        foreach (PropertyEntry property in neededProperties)
        {
            if (string.IsNullOrWhiteSpace(property.SourcePath))
            {
                stats.MissingSource++;
                continue;
            }

            string sourceFile =
                ResolvePropertySource(
                    property.SourcePath,
                    sourceByRelativePath);

            if (string.IsNullOrEmpty(sourceFile))
            {
                stats.MissingSource++;
                UnityEngine.Debug.LogWarning(
                    $"Property source bulunamadı: {property.PropertyName} -> {property.SourcePath}");
                continue;
            }

            string modelName =
                Path.GetFileNameWithoutExtension(
                    sourceFile);

            string dedicatedSptConverter =
                Path.GetExtension(sourceFile)
                    .Equals(".spt", StringComparison.OrdinalIgnoreCase)
                    ? FindSptFbxConverter(repoRoot)
                    : null;

            if (existingModels.Contains(modelName) ||
                existingModels.Contains(modelName + "out"))
            {
                stats.AlreadyExisting++;
                continue;
            }

            string outputFbx =
                Path.Combine(
                    outputRoot,
                    modelName + ".fbx");

            if (File.Exists(outputFbx))
            {
                stats.Converted++;
                continue;
            }

            try
            {
                // Older Noesis builds can be unreliable when input/output
                // paths contain non-ASCII characters. Stage the conversion
                // through an ASCII-only temporary directory.
                string tempRoot =
                    Path.Combine(
                        Path.GetTempPath(),
                        "SAGLAMKAFA_Noesis");

                string safeModelName =
                    Regex.Replace(
                        modelName ?? "model",
                        @"[^A-Za-z0-9._-]",
                        "_");

                string workFolder =
                    Path.Combine(
                        tempRoot,
                        safeModelName + "_" +
                        Guid.NewGuid().ToString("N"));

                Directory.CreateDirectory(workFolder);

                string stagedInput =
                    Path.Combine(
                        workFolder,
                        Path.GetFileName(sourceFile));

                string stagedOutput =
                    Path.Combine(
                        workFolder,
                        safeModelName + ".fbx");

                File.Copy(
                    sourceFile,
                    stagedInput,
                    true);

                if (!string.IsNullOrEmpty(dedicatedSptConverter))
                {
                    string dedicatedOutput =
                        Path.Combine(
                            workFolder,
                            Path.GetFileNameWithoutExtension(
                                stagedInput) + ".fbx");

                    string dedicatedStdout;
                    string dedicatedStderr;
                    int dedicatedExitCode;

                    if (TryRunSptFbxConverter(
                            dedicatedSptConverter,
                            stagedInput,
                            dedicatedOutput,
                            out dedicatedStdout,
                            out dedicatedStderr,
                            out dedicatedExitCode))
                    {
                        File.Copy(
                            dedicatedOutput,
                            outputFbx,
                            true);

                        stats.Converted++;

                        try
                        {
                            if (Directory.Exists(workFolder))
                                Directory.Delete(workFolder, true);
                        }
                        catch
                        {
                        }

                        EditorUtility.DisplayProgressBar(
                            "Pyungmoo modelleri",
                            modelName,
                            stats.Converted /
                            (float)Math.Max(
                                1,
                                neededProperties.Count));

                        continue;
                    }

                    UnityEngine.Debug.LogWarning(
                        $"Özel SPT converter başarısız, Noesis fallback kullanılacak: {modelName}\n" +
                        $"Converter={dedicatedSptConverter}\n" +
                        $"ExitCode={dedicatedExitCode}\n" +
                        $"STDOUT:\n{dedicatedStdout}\n" +
                        $"STDERR:\n{dedicatedStderr}");
                }

                string[] optionSets =
                {
                    "-fbxnewexport -fbxmeshmerge -rotate 90 0 0",
                    "-fbxnewexport -fbxmeshmerge -rotate 90 0 0 -notex",
                    "-fbxmeshmerge -rotate 90 0 0 -notex"
                };

                bool success = false;
                int exitCode = -1;
                string stdout = string.Empty;
                string stderr = string.Empty;

                foreach (string options in optionSets)
                {
                    if (File.Exists(stagedOutput))
                        File.Delete(stagedOutput);

                    string arguments =
                        $"?cmode \"{stagedInput}\" \"{stagedOutput}\" {options}";

                    UnityEngine.Debug.Log(
                        $"Noesis GR2/SPT -> FBX: {modelName}\n" +
                        $"Source: {sourceFile}\n" +
                        $"Staged: {stagedInput}\n" +
                        $"Args: {arguments}");

                    using (Process process = new Process())
                    {
                        process.StartInfo =
                            new ProcessStartInfo
                            {
                                FileName = noesisPath,
                                Arguments = arguments,
                                WorkingDirectory =
                                    Path.GetDirectoryName(noesisPath),
                                UseShellExecute = false,
                                CreateNoWindow = true,
                                RedirectStandardOutput = true,
                                RedirectStandardError = true
                            };

                        process.Start();

                        if (!process.WaitForExit(NoesisTimeoutMs))
                        {
                            try { process.Kill(); }
                            catch { }

                            exitCode = -1;
                            stderr = "Noesis timeout.";
                            continue;
                        }

                        exitCode = process.ExitCode;
                        stdout = process.StandardOutput.ReadToEnd();
                        stderr = process.StandardError.ReadToEnd();

                        if (exitCode == 0 &&
                            File.Exists(stagedOutput) &&
                            new FileInfo(stagedOutput).Length > 0)
                        {
                            success = true;
                            break;
                        }

                        UnityEngine.Debug.LogWarning(
                            $"Noesis denemesi başarısız: {modelName}\n" +
                            $"Options={options}\n" +
                            $"ExitCode={exitCode}\n" +
                            $"STDOUT:\n{stdout}\n" +
                            $"STDERR:\n{stderr}");
                    }
                }

                if (!success)
                {
                    stats.Failed++;

                    string detail =
                        $"FAILED: {modelName}\n" +
                        $"Source={sourceFile}\n" +
                        $"ExitCode={exitCode}\n" +
                        $"STDOUT:\n{stdout}\n" +
                        $"STDERR:\n{stderr}";

                    stats.FailureDetails.Add(detail);
                    UnityEngine.Debug.LogWarning(detail);

                    try
                    {
                        if (Directory.Exists(workFolder))
                            Directory.Delete(workFolder, true);
                    }
                    catch
                    {
                    }

                    continue;
                }

                File.Copy(
                    stagedOutput,
                    outputFbx,
                    true);

                try
                {
                    if (Directory.Exists(workFolder))
                        Directory.Delete(workFolder, true);
                }
                catch
                {
                }

                stats.Converted++;

                EditorUtility.DisplayProgressBar(
                    "Pyungmoo modelleri",
                    modelName,
                    stats.Converted /
                    (float)Math.Max(
                        1,
                        neededProperties.Count));
            }
            catch (Exception ex)
            {
                stats.Failed++;

                string detail =
                    $"EXCEPTION: {modelName}\n" +
                    $"Source={sourceFile}\n" +
                    ex;

                stats.FailureDetails.Add(detail);

                UnityEngine.Debug.LogWarning(detail);
            }
        }

        EditorUtility.ClearProgressBar();

        UnityEngine.Debug.Log(
            $"Pyungmoo model conversion: " +
            $"new={stats.Converted}, " +
            $"existing={stats.AlreadyExisting}, " +
            $"missingSource={stats.MissingSource}, " +
            $"failed={stats.Failed}");

        return stats;
    }

    private static Dictionary<string, GameObject>
        BuildModelIndex()
    {
        var result =
            new Dictionary<string, GameObject>(
                StringComparer.OrdinalIgnoreCase);

        foreach (string guid in
                 AssetDatabase.FindAssets("t:Model"))
        {
            string path =
                AssetDatabase.GUIDToAssetPath(guid);

            GameObject model =
                AssetDatabase.LoadAssetAtPath<GameObject>(
                    path);

            if (model == null)
                continue;

            string name =
                Path.GetFileNameWithoutExtension(path);

            if (string.IsNullOrWhiteSpace(name))
                continue;

            if (!result.ContainsKey(name))
                result.Add(name, model);
        }

        UnityEngine.Debug.Log(
            $"Unity model index: {result.Count} model");

        return result;
    }

    private static bool TryFindModel(
        Dictionary<string, GameObject> modelIndex,
        string modelName,
        out GameObject model)
    {
        if (modelIndex.TryGetValue(
                modelName,
                out model))
        {
            return true;
        }

        if (modelIndex.TryGetValue(
                modelName + "out",
                out model))
        {
            return true;
        }

        model = null;
        return false;
    }

    private static List<AreaObject>
        ParseAreaData(string file)
    {
        var result =
            new List<AreaObject>();

        string[] lines =
            File.ReadAllLines(file);

        for (int i = 0;
             i < lines.Length;
             i++)
        {
            string trimmed =
                lines[i].Trim();

            if (!trimmed.StartsWith(
                    "Start Object",
                    StringComparison.OrdinalIgnoreCase))
            {
                continue;
            }

            Match objectMatch =
                Regex.Match(
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

            var data =
                new List<string>();

            for (int j = i + 1;
                 j < lines.Length;
                 j++)
            {
                string line =
                    lines[j].Trim();

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

            if (data.Count < 4)
                continue;

            if (!TryParseVector3(
                    data[0],
                    out Vector3 position))
            {
                continue;
            }

            if (!uint.TryParse(
                    data[1],
                    NumberStyles.Integer,
                    CultureInfo.InvariantCulture,
                    out uint propertyId))
            {
                continue;
            }

            Vector3 rotation =
                Vector3.zero;

            TryParseVector3(
                data[2].Replace('#', ' '),
                out rotation);

            float heightOffset = 0.0f;

            float.TryParse(
                data[3],
                NumberStyles.Float,
                CultureInfo.InvariantCulture,
                out heightOffset);

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
        string[] parts =
            value.Split(
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
                out float x))
        {
            result = Vector3.zero;
            return false;
        }

        if (!float.TryParse(
                parts[1],
                NumberStyles.Float,
                CultureInfo.InvariantCulture,
                out float y))
        {
            result = Vector3.zero;
            return false;
        }

        if (!float.TryParse(
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

    private static string FindSptFbxConverter(
        string repoRoot)
    {
        string userProfile =
            Environment.GetFolderPath(
                Environment.SpecialFolder.UserProfile);

        string oneDrive =
            Environment.GetEnvironmentVariable(
                "OneDrive");

        var candidates =
            new List<string>
            {
                Path.Combine(repoRoot, "Spt2Fbx.exe"),
                Path.Combine(repoRoot, "SPT-to-FBX-Converter", "Spt2Fbx.exe"),
                Path.Combine(repoRoot, "SPT-to-FBX-Converter", "Spt-to-FBX.exe"),
                Path.Combine(repoRoot, "shared_3d_exporting", "Spt2Fbx.exe"),
                Path.Combine(
                    Directory.GetParent(repoRoot).FullName,
                    "Spt2Fbx.exe"),
                Path.Combine(
                    Directory.GetParent(repoRoot).FullName,
                    "SPT-to-FBX-Converter",
                    "Spt2Fbx.exe"),
                Path.Combine(userProfile, "Desktop", "Spt2Fbx.exe"),
                Path.Combine(userProfile, "Downloads", "Spt2Fbx.exe")
            };

        if (!string.IsNullOrEmpty(oneDrive))
        {
            candidates.Add(
                Path.Combine(
                    oneDrive,
                    "Desktop",
                    "Spt2Fbx.exe"));

            candidates.Add(
                Path.Combine(
                    oneDrive,
                    "Desktop",
                    "SPT-to-FBX-Converter",
                    "Spt2Fbx.exe"));
        }

        return candidates
            .Where(File.Exists)
            .Distinct(StringComparer.OrdinalIgnoreCase)
            .FirstOrDefault();
    }

    private static bool TryRunSptFbxConverter(
        string converterPath,
        string inputSpt,
        string outputFbx,
        out string stdout,
        out string stderr,
        out int exitCode)
    {
        stdout = string.Empty;
        stderr = string.Empty;
        exitCode = -1;

        string arguments =
            $"\"{inputSpt}\"";

        try
        {
            using (Process process = new Process())
            {
                process.StartInfo =
                    new ProcessStartInfo
                    {
                        FileName = converterPath,
                        Arguments = arguments,
                        WorkingDirectory =
                            Path.GetDirectoryName(converterPath),
                        UseShellExecute = false,
                        CreateNoWindow = true,
                        RedirectStandardOutput = true,
                        RedirectStandardError = true
                    };

                process.Start();

                if (!process.WaitForExit(NoesisTimeoutMs))
                {
                    try { process.Kill(); }
                    catch { }

                    stderr = "SPT converter timeout.";
                    return false;
                }

                exitCode = process.ExitCode;
                stdout = process.StandardOutput.ReadToEnd();
                stderr = process.StandardError.ReadToEnd();

                return exitCode == 0 &&
                       File.Exists(outputFbx) &&
                       new FileInfo(outputFbx).Length > 0;
            }
        }
        catch (Exception ex)
        {
            stderr = ex.ToString();
            return false;
        }
    }

    private static Quaternion ConvertRotation(
        Vector3 sourceRotation)
    {
        // The AreaData rotation is expressed in the source
        // coordinate basis. Preserve all three angles while
        // changing the up-axis to Unity.
        Quaternion basis =
            Quaternion.Euler(-90.0f, 0.0f, 0.0f);

        Quaternion source =
            Quaternion.Euler(
                sourceRotation.x,
                sourceRotation.y,
                sourceRotation.z);

        return basis *
               source *
               Quaternion.Inverse(basis);
    }

    private static void AddMeshColliders(
        GameObject root)
    {
        foreach (MeshFilter filter in
                 root.GetComponentsInChildren<MeshFilter>(
                     true))
        {
            if (filter.sharedMesh == null)
                continue;

            if (filter.GetComponent<MeshCollider>() != null)
                continue;

            MeshCollider collider =
                filter.gameObject.AddComponent<MeshCollider>();

            collider.sharedMesh =
                filter.sharedMesh;

            collider.convex = false;
        }
    }

    private static string FindNoesis(
        string repoRoot)
    {
        string userProfile =
            Environment.GetFolderPath(
                Environment.SpecialFolder.UserProfile);

        string oneDrive =
            Environment.GetEnvironmentVariable(
                "OneDrive");

        var candidates =
            new List<string>
            {
                Path.Combine(
                    repoRoot,
                    "shared_3d_exporting",
                    "noesis",
                    "noesis",
                    "Noesis.exe"),

                Path.Combine(
                    Directory.GetParent(repoRoot).FullName,
                    "shared_3d_exporting",
                    "noesis",
                    "noesis",
                    "Noesis.exe"),

                Path.Combine(
                    userProfile,
                    "shared_3d_exporting",
                    "noesis",
                    "noesis",
                    "Noesis.exe")
            };

        if (!string.IsNullOrEmpty(oneDrive))
        {
            candidates.Add(
                Path.Combine(
                    oneDrive,
                    "Desktop",
                    "shared_3d_exporting",
                    "noesis",
                    "noesis",
                    "Noesis.exe"));

            candidates.Add(
                Path.Combine(
                    oneDrive,
                    "Masaüstü",
                    "shared_3d_exporting",
                    "noesis",
                    "noesis",
                    "Noesis.exe"));
        }

        foreach (string candidate in candidates)
        {
            if (File.Exists(candidate))
                return candidate;
        }

        string parent =
            Directory.GetParent(repoRoot)?.FullName;

        if (!string.IsNullOrEmpty(parent))
        {
            try
            {
                return Directory.EnumerateFiles(
                        parent,
                        "Noesis.exe",
                        SearchOption.AllDirectories)
                    .FirstOrDefault();
            }
            catch
            {
            }
        }

        return null;
    }

    private static void DeleteExistingObjectRoot(
        GameObject mapRoot)
    {
        Transform old =
            mapRoot.transform.Find(
                ObjectRootName);

        if (old != null)
            UnityEngine.Object.DestroyImmediate(
                old.gameObject);
    }

    private static void WriteReport(
        string text)
    {
        string projectRoot =
            Directory.GetParent(Application.dataPath).FullName;

        string absolute =
            Path.Combine(
                projectRoot,
                ReportPath
                    .Substring("Assets/".Length)
                    .Replace(
                        '/',
                        Path.DirectorySeparatorChar));

        string dir =
            Path.GetDirectoryName(absolute);

        if (!string.IsNullOrEmpty(dir))
            Directory.CreateDirectory(dir);

        File.WriteAllText(
            absolute,
            text,
            new UTF8Encoding(false));

        AssetDatabase.ImportAsset(
            ReportPath,
            ImportAssetOptions.ForceUpdate);
    }

    private static void Increment<TKey>(
        Dictionary<TKey, int> dictionary,
        TKey key)
    {
        if (dictionary.TryGetValue(
                key,
                out int count))
        {
            dictionary[key] = count + 1;
        }
        else
        {
            dictionary[key] = 1;
        }
    }

    private static string Sanitize(
        string value)
    {
        if (string.IsNullOrWhiteSpace(value))
            return "Object";

        foreach (char c in
                 Path.GetInvalidFileNameChars())
        {
            value = value.Replace(
                c,
                '_');
        }

        return value.Replace(
            ' ',
            '_');
    }

    private sealed class AreaObject
    {
        public int ObjectIndex;
        public uint PropertyId;
        public Vector3 Position;
        public Vector3 Rotation;
        public float HeightOffset;
    }

    private sealed class PropertyEntry
    {
        public uint Id;
        public string PropertyName;
        public string PropertyType;
        public string SourcePath;
        public string SourcePropertyFile;
    }

    private sealed class ConversionStats
    {
        public int Converted;
        public int AlreadyExisting;
        public int MissingSource;
        public int Failed;
        public readonly List<string> FailureDetails =
            new List<string>();
    }
}
