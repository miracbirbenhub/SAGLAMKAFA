using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using UnityEditor;
using UnityEditor.Build.Reporting;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;

public static class Metin2PyungmooFinalImporter
{
    private const string ScenePath = "Assets/Scenes/Pyungmoo.unity";
    private const string BuildingFolder = "Assets/Metin2Imported/Building";
    private const string NpcFolder = "Assets/Metin2Imported/NPC";
    private const string BuildingRootName = "FINAL_Buildings";
    private const string NpcRootName = "FINAL_NPCs";
    private const string BuildingLibraryRootName = "Metin2BuildingAssetLibrary";
    private const string NpcLibraryRootName = "Metin2NpcAssetLibrary";
    private const string ReportPath = "Assets/Metin2Generated/Pyungmoo/PyungmooFinalImportReport.txt";

    private const float AreaCoordinateScale = 0.02f;
    private const float NpcCoordinateScale = 2.0f;
    private const float RayStartHeight = 5000.0f;
    private const float GroundOffset = 0.05f;

    private static readonly string[] PropertyExtensions =
    {
        ".pr", ".prb", ".prt", ".ptr", ".prd", ".pte", ".pre", ".pra"
    };

    private static readonly NpcPlacement[] NpcPlacements =
    {
        new(20340, "Bedensel Savaş Öğretmeni", "jinno_patrol_spear", 444, 623, 7),
        new(20341, "Zihinsel Savaş Öğretmeni", "jinno_patrol_spear", 444, 627, 7),
        new(20342, "Yakın Dövüş Öğretmeni", "jinno_patrol_spear", 444, 631, 7),
        new(20343, "Uzak Dövüş Öğretmeni", "jinno_patrol_spear", 444, 635, 7),
        new(20344, "Büyülü Silah Öğretmeni", "jinno_patrol_spear", 443, 644, 7),
        new(20345, "Kara Büyü Öğretmeni", "jinno_patrol_spear", 443, 648, 7),
        new(20346, "İyileştirme Öğretmeni", "jinno_patrol_spear", 443, 652, 7),
        new(20347, "Ejderha Gücü Öğretmeni", "jinno_patrol_spear", 443, 656, 7),

        new(9001, "Silahçı", "arms", 430, 607, 8),
        new(9002, "Zırhçı", "defence", 403, 586, 1),
        new(9003, "Bakkal", "goods", 383, 693, 5),
        new(9005, "Depocu", "hotel_grandfa", 315, 560, 3),
        new(9006, "Yaşlı Kadın", "hotel_grandma", 417, 671, 6),
        new(20016, "Demirci", "blacksmith", 393, 692, 5),

        new(20008, "Octavio", "mr_restaurant", 340, 747, 7),
        new(20023, "Soon", "bookworm", 454, 530, 0),
        new(20002, "Aranyo", "auntie", 343, 560, 0),
        new(20003, "Ah-Yu", "baby_and_mom", 378, 577, 0),
        new(20005, "Yonah", "ceramist", 292, 718, 0),
        new(20006, "Mirine", "girl_lost_elder_brother", 336, 770, 0),
        new(20011, "Uriel", "plant_researcher", 425, 716, 0),
        new(20018, "Baek-Go", "doctor", 465, 612, 0),
        new(20041, "Sarhoş", "beggar", 323, 617, 0),

        new(20355, "Köy Meydanı Gardiyanı", "guard_leader", 286, 639, 0),
        new(20354, "Şehir Gardiyanı", "guard_leader", 468, 714, 0),
        new(20084, "Biyolog Chaegirab", "chagirap", 285, 285, 0),
        new(20086, "Handu-Up", "handaup", 447, 928, 0),
        new(20087, "Wonda-Rim", "wondaim", 456, 936, 0),

        new(20358, "İsimsiz Çiçekler", "nnflower", 771, 78, 0),
        new(20357, "Weol Anıtı", "moonstone", 114, 960, 0),
        new(20349, "Seyis", "jinno_patrol_spear", 396, 735, 2)
    };

    [MenuItem("Metin2/Pyungmoo/FINAL - ALL Buildings + ALL NPCs + VERIFY")]
    public static void ImportFinal()
    {
        string report = string.Empty;
        try
        {
            report = RunPipeline();
            EditorUtility.DisplayDialog(
                "Pyungmoo FINAL doğrulama BAŞARILI",
                report,
                "Tamam");
        }
        catch (Exception ex)
        {
            Debug.LogException(ex);
            report = "FINAL IMPORT FAILED\n\n" + ex;
            WriteReport(report);
            EditorUtility.DisplayDialog(
                "Pyungmoo FINAL import HATASI",
                ex.Message + "\n\nRapor:\n" + ReportPath,
                "Tamam");
        }
    }

    public static string RunPipeline()
    {
        Scene scene = OpenScene();
        GameObject mapRoot = GameObject.Find("Pyungmoo");
        if (mapRoot == null)
            throw new InvalidOperationException("Pyungmoo GameObject'i bulunamadı.");

        ValidateBuildSettings();

        string repoRoot = GetRepoRoot();
        string mapSource = FindDirectoryOrThrow(
            repoRoot,
            Path.Combine("Metin2Client", "OutdoorC1", "metin2_map_c1"),
            Path.Combine("OutdoorC1", "metin2_map_c1"));

        string propertyRoot = FindDirectoryOrThrow(
            repoRoot,
            Path.Combine("Metin2Client", "Property", "property"),
            Path.Combine("Metin2Client", "Property"),
            Path.Combine("Property", "property"),
            Path.Combine("Property"));

        List<string> areaFiles = DiscoverAreaFiles(mapSource);
        if (areaFiles.Count != 20)
            throw new InvalidOperationException(
                "Pyungmoo C1 beklenen 20 AreaData chunk'ına sahip değil. Bulunan: " + areaFiles.Count);

        List<BuildingModel> buildingModels = DiscoverModels(BuildingFolder);
        List<BuildingModel> npcModels = DiscoverModels(NpcFolder);

        int buildingInvalid = buildingModels.Count(x => !string.IsNullOrEmpty(x.ValidationError));
        int npcInvalid = npcModels.Count(x => !string.IsNullOrEmpty(x.ValidationError));

        if (buildingModels.Count == 0)
            throw new InvalidOperationException("Building FBX bulunamadı: " + BuildingFolder);
        if (npcModels.Count == 0)
            throw new InvalidOperationException("NPC FBX bulunamadı: " + NpcFolder);

        Dictionary<string, BuildingModel> buildingCanonical =
            buildingModels
                .Where(x => !x.IsLod && x.Prefab != null && string.IsNullOrEmpty(x.ValidationError))
                .GroupBy(x => x.CanonicalKey, StringComparer.OrdinalIgnoreCase)
                .ToDictionary(
                    g => g.Key,
                    g => g.First(),
                    StringComparer.OrdinalIgnoreCase);

        Dictionary<string, BuildingModel> npcIndex =
            npcModels
                .Where(x => x.Prefab != null && string.IsNullOrEmpty(x.ValidationError))
                .GroupBy(x => x.CanonicalKey, StringComparer.OrdinalIgnoreCase)
                .ToDictionary(
                    g => g.Key,
                    g => g.First(),
                    StringComparer.OrdinalIgnoreCase);

        if (buildingInvalid > 0)
            throw new InvalidOperationException(
                "Building FBX preflight hatası: " + buildingInvalid + " asset kullanılamıyor.");
        if (npcInvalid > 0)
            throw new InvalidOperationException(
                "NPC FBX preflight hatası: " + npcInvalid + " asset kullanılamıyor.");

        if (buildingModels.Count != 47)
            throw new InvalidOperationException(
                "Pyungmoo Building klasöründe beklenen 47 FBX yerine " +
                buildingModels.Count + " FBX bulundu.");
        if (npcModels.Count != 22)
            throw new InvalidOperationException(
                "Pyungmoo NPC klasöründe beklenen 22 FBX yerine " +
                npcModels.Count + " FBX bulundu.");

        List<AreaObject> areaObjects = areaFiles
            .SelectMany(ParseAreaData)
            .ToList();

        if (areaObjects.Count != 1748)
            throw new InvalidOperationException(
                "Pyungmoo AreaData beklenen 1748 nesne yerine " +
                areaObjects.Count + " nesne içeriyor.");

        var propertyRoots = new List<string> { propertyRoot };

        string zonePropertyRoot =
            Path.Combine(repoRoot, "Metin2Client", "Zone");
        if (Directory.Exists(zonePropertyRoot))
            propertyRoots.Add(zonePropertyRoot);

        string season3PropertyRoot =
            Path.Combine(repoRoot, "Metin2Client", "season3_eu", "property");
        if (Directory.Exists(season3PropertyRoot))
            propertyRoots.Add(season3PropertyRoot);

        Dictionary<uint, BuildingProperty> buildingProperties =
            LoadBuildingProperties(propertyRoots, repoRoot, buildingCanonical);

        if (buildingProperties.Count == 0)
            throw new InvalidOperationException(
                "C1 Building Property kayıtları bulunamadı.");

        var buildingRefs = new List<ResolvedBuilding>();
        var unresolvedBuildingIds = new Dictionary<uint, int>();

        foreach (AreaObject obj in areaObjects)
        {
            if (!buildingProperties.TryGetValue(obj.PropertyId, out BuildingProperty property))
                continue;

            if (!buildingCanonical.TryGetValue(
                    NormalizeModelKey(property.SourceModelName),
                    out BuildingModel model))
            {
                AddCount(unresolvedBuildingIds, obj.PropertyId);
                continue;
            }

            buildingRefs.Add(new ResolvedBuilding(obj, property, model));
        }

        if (unresolvedBuildingIds.Count > 0)
        {
            string ids = string.Join(
                ", ",
                unresolvedBuildingIds.Keys
                    .Take(30)
                    .Select(x => x.ToString(CultureInfo.InvariantCulture)));

            throw new InvalidOperationException(
                "Building Property kayıtları bulundu fakat ilgili FBX çözülemedi. " +
                "Property ID'leri: " + ids);
        }

        if (buildingRefs.Count == 0)
        {
            string ids = string.Join(
                ", ",
                areaObjects.Select(x => x.PropertyId).Distinct().Take(30));

            throw new InvalidOperationException(
                "C1 AreaData ile hiçbir Building Property eşleşmedi. " +
                "CRC çözümlemesi bu veri kümesini eşleştiremedi.\nÖrnek AreaData ID'leri: " + ids);
        }

        var missingNpcModels = NpcPlacements
            .Select(x => x.ModelKey)
            .Distinct(StringComparer.OrdinalIgnoreCase)
            .Where(x => !npcIndex.ContainsKey(NormalizeModelKey(x)))
            .ToList();

        if (missingNpcModels.Count > 0)
            throw new InvalidOperationException(
                "Eksik NPC modelleri: " + string.Join(", ", missingNpcModels));

        Bounds mapBounds = CalculateMapBounds(mapRoot);

        DeleteOldRoots(mapRoot);

        Transform buildingRoot = CreateRoot(mapRoot, BuildingRootName);
        Transform npcRoot = CreateRoot(mapRoot, NpcRootName);

        int buildingPlaced = 0;
        var buildingErrors = new List<string>();

        foreach (ResolvedBuilding resolved in buildingRefs)
        {
            GameObject instance =
                PrefabUtility.InstantiatePrefab(resolved.Model.Prefab) as GameObject;

            if (instance == null)
            {
                buildingErrors.Add(
                    "Building instantiate başarısız: " + resolved.Model.Path);
                continue;
            }

            instance.name =
                "BUILD_" +
                resolved.AreaObject.ObjectIndex.ToString("0000", CultureInfo.InvariantCulture) +
                "_" +
                Sanitize(resolved.Property.PropertyName);

            instance.transform.SetParent(buildingRoot, false);
            instance.transform.position = new Vector3(
                resolved.AreaObject.Position.x * AreaCoordinateScale,
                (resolved.AreaObject.Position.z +
                    resolved.AreaObject.HeightOffset) * AreaCoordinateScale,
                -resolved.AreaObject.Position.y * AreaCoordinateScale);
            instance.transform.rotation =
                ConvertRotation(resolved.AreaObject.Rotation);
            instance.isStatic = true;

            AddMeshColliders(instance);
            buildingPlaced++;
        }

        if (buildingErrors.Count > 0)
            throw new InvalidOperationException(
                "Building instance hataları:\n" + string.Join("\n", buildingErrors.Take(20)));

        int npcPlaced = 0;
        var groundMisses = new List<string>();

        foreach (NpcPlacement placement in NpcPlacements)
        {
            BuildingModel model = npcIndex[NormalizeModelKey(placement.ModelKey)];
            Vector3 xz = new Vector3(
                placement.MapX * NpcCoordinateScale,
                0.0f,
                placement.MapY * NpcCoordinateScale);

            if (!TryProjectToTerrain(xz, out float groundY))
            {
                groundMisses.Add(
                    placement.Vnum.ToString(CultureInfo.InvariantCulture) +
                    " " +
                    placement.DisplayName);
                continue;
            }

            GameObject instance =
                PrefabUtility.InstantiatePrefab(model.Prefab) as GameObject;

            if (instance == null)
                throw new InvalidOperationException(
                    "NPC instantiate başarısız: " + model.Path);

            instance.name =
                "NPC_" +
                placement.Vnum.ToString(CultureInfo.InvariantCulture) +
                "_" +
                Sanitize(placement.DisplayName);

            instance.transform.SetParent(npcRoot, false);
            instance.transform.position =
                new Vector3(xz.x, groundY + GroundOffset, xz.z);
            instance.transform.rotation =
                Quaternion.Euler(0.0f, placement.Direction * 45.0f, 0.0f);

            Metin2NpcIdentity identity =
                instance.GetComponent<Metin2NpcIdentity>();

            if (identity == null)
                identity = instance.AddComponent<Metin2NpcIdentity>();

            identity.Initialize(
                placement.Vnum,
                placement.DisplayName,
                new Vector2Int(placement.MapX, placement.MapY));

            npcPlaced++;
        }

        if (groundMisses.Count > 0)
            throw new InvalidOperationException(
                "NPC terrain raycast başarısız. Konumlar:\n" +
                string.Join("\n", groundMisses));

        Transform buildingLibrary =
            CreateInactiveAssetLibrary(
                mapRoot,
                BuildingLibraryRootName,
                buildingModels,
                mapBounds);

        Transform npcLibrary =
            CreateInactiveAssetLibrary(
                mapRoot,
                NpcLibraryRootName,
                npcModels,
                mapBounds);

        string validation = ValidateFinalScene(
            mapRoot,
            buildingRoot,
            npcRoot,
            buildingLibrary,
            npcLibrary,
            buildingModels.Count,
            npcModels.Count,
            buildingPlaced,
            npcPlaced);

        if (!validation.StartsWith("PASS", StringComparison.Ordinal))
            throw new InvalidOperationException(validation);

        EditorSceneManager.MarkSceneDirty(scene);
        if (!EditorSceneManager.SaveScene(scene, ScenePath))
            throw new InvalidOperationException("Pyungmoo sahnesi kaydedilemedi.");

        AssetDatabase.SaveAssets();
        AssetDatabase.Refresh();

        // Persisted-state verification: reload the serialized scene and verify
        // the same prefab links, instance counts, inactive asset libraries,
        // renderer/mesh/material state and the absence of legacy/placeholder roots.
        scene = EditorSceneManager.OpenScene(
            ScenePath,
            OpenSceneMode.Single);

        mapRoot = GameObject.Find("Pyungmoo");
        if (mapRoot == null)
            throw new InvalidOperationException(
                "Save/reload sonrası Pyungmoo root bulunamadı.");

        Transform persistedBuildingRoot =
            mapRoot.transform.Find(BuildingRootName);
        Transform persistedNpcRoot =
            mapRoot.transform.Find(NpcRootName);
        Transform persistedBuildingLibrary =
            mapRoot.transform.Find(BuildingLibraryRootName);
        Transform persistedNpcLibrary =
            mapRoot.transform.Find(NpcLibraryRootName);

        string persistedValidation = ValidateFinalScene(
            mapRoot,
            persistedBuildingRoot,
            persistedNpcRoot,
            persistedBuildingLibrary,
            persistedNpcLibrary,
            buildingModels.Count,
            npcModels.Count,
            buildingPlaced,
            npcPlaced);

        if (!persistedValidation.StartsWith(
                "PASS",
                StringComparison.Ordinal))
        {
            throw new InvalidOperationException(
                "Kaydetme + yeniden açma doğrulaması başarısız:\n" +
                persistedValidation);
        }

        BuildValidationResult standaloneValidation =
            RunStandaloneWindowsBuildValidation();

        if (!standaloneValidation.Passed)
        {
            throw new InvalidOperationException(
                "StandaloneWindows64 build doğrulaması başarısız:\n" +
                standaloneValidation.Message);
        }

        StringBuilder report = new StringBuilder();
        report.AppendLine("PYUNGMOO FINAL IMPORT / VERIFY");
        report.AppendLine(DateTime.Now.ToString(
            "yyyy-MM-dd HH:mm:ss",
            CultureInfo.InvariantCulture));
        report.AppendLine();
        report.AppendLine("STATUS: PASS");
        report.AppendLine();
        report.AppendLine("SOURCE");
        report.AppendLine("  AreaData files: " + areaFiles.Count);
        report.AppendLine("  AreaData objects: " + areaObjects.Count);
        report.AppendLine("  Unique AreaData IDs: " +
            areaObjects.Select(x => x.PropertyId).Distinct().Count());
        report.AppendLine("  Pyungmoo Build Settings: enabled");
        report.AppendLine("  Building Property records indexed: " +
            buildingProperties.Count);
        report.AppendLine("  AreaData -> Building references: " +
            buildingRefs.Count);
        report.AppendLine();
        report.AppendLine("BUILDINGS");
        report.AppendLine("  Building FBX files: " + buildingModels.Count);
        report.AppendLine("  Non-LOD canonical building models: " +
            buildingCanonical.Count);
        report.AppendLine("  Map building instances: " + buildingPlaced);
        report.AppendLine("  Inactive build-inclusion library instances: " +
            buildingLibrary.childCount);
        report.AppendLine("  Unresolved building IDs during index: " +
            unresolvedBuildingIds.Count);
        report.AppendLine();
        report.AppendLine("NPC");
        report.AppendLine("  NPC FBX files: " + npcModels.Count);
        report.AppendLine("  NPC placement records: " + NpcPlacements.Length);
        report.AppendLine("  Map NPC instances: " + npcPlaced);
        report.AppendLine("  Inactive build-inclusion library instances: " +
            npcLibrary.childCount);
        report.AppendLine("  Placeholders: 0");
        report.AppendLine();
        report.AppendLine("VALIDATION");
        report.AppendLine("  Pre-save: " + validation.Replace("\n", "\n  "));
        report.AppendLine("  Post-save/reload: " + persistedValidation.Replace("\n", "\n  "));
        report.AppendLine();
        report.AppendLine("STANDALONE BUILD");
        report.AppendLine("  " + standaloneValidation.Message.Replace("\n", "\n  "));
        report.AppendLine();
        report.AppendLine(
            "All 47 Building FBX assets and all 22 NPC FBX assets are serialized into the Pyungmoo scene.");
        report.AppendLine(
            "LOD Building FBXs are included in an inactive library so they are in the build without duplicating gameplay geometry.");
        report.AppendLine(
            "Actual map Building instances use non-LOD FBX assets resolved from AreaData/Property data.");

        report.AppendLine();
        report.AppendLine("NOTE");
        report.AppendLine(
            "Remaining AreaData IDs that are not classified as Building are other map resources and are not silently converted into buildings.");

        WriteReport(report.ToString());
        Selection.activeGameObject = buildingRoot.gameObject;

        return
            "AreaData: " + areaObjects.Count + "\n" +
            "Building FBX: " + buildingModels.Count + "\n" +
            "Map Building instance: " + buildingPlaced + "\n" +
            "NPC FBX: " + npcModels.Count + "\n" +
            "Map NPC instance: " + npcPlaced + "\n" +
            "Placeholder: 0\n\n" +
            "PASS - save/reload verify OK - report: " + ReportPath;
    }

    private static void ValidateBuildSettings()
    {
        EditorBuildSettingsScene[] scenes =
            EditorBuildSettings.scenes ?? Array.Empty<EditorBuildSettingsScene>();

        string expectedGuid =
            AssetDatabase.AssetPathToGUID(ScenePath);

        EditorBuildSettingsScene pyungmoo = scenes.FirstOrDefault(
            x => string.Equals(
                x.path,
                ScenePath,
                StringComparison.OrdinalIgnoreCase));

        if (pyungmoo == null)
            throw new InvalidOperationException(
                "Pyungmoo.unity Build Settings listesinde yok.");

        if (!pyungmoo.enabled)
            throw new InvalidOperationException(
                "Pyungmoo.unity Build Settings içinde devre dışı.");

        if (!string.IsNullOrEmpty(expectedGuid) &&
            !string.IsNullOrEmpty(pyungmoo.guid) &&
            !string.Equals(
                expectedGuid,
                pyungmoo.guid,
                StringComparison.OrdinalIgnoreCase))
        {
            throw new InvalidOperationException(
                "Pyungmoo Build Settings GUID uyuşmazlığı.");
        }
    }

    private sealed class BuildValidationResult
    {
        public readonly bool Passed;
        public readonly string Message;

        public BuildValidationResult(bool passed, string message)
        {
            Passed = passed;
            Message = message;
        }
    }

    private static BuildValidationResult RunStandaloneWindowsBuildValidation()
    {
        string tempRoot = Path.Combine(
            Path.GetTempPath(),
            "SAGLAMKAFA_Pyungmoo_BuildValidation");

        try
        {
            if (Directory.Exists(tempRoot))
                Directory.Delete(tempRoot, true);

            Directory.CreateDirectory(tempRoot);

            string buildPath = Path.Combine(
                tempRoot,
                "PyungmooValidation.exe");

            BuildReport report = BuildPipeline.BuildPlayer(
                new BuildPlayerOptions
                {
                    scenes = new[] { ScenePath },
                    locationPathName = buildPath,
                    target = BuildTarget.StandaloneWindows64,
                    options = BuildOptions.StrictMode
                });

            bool passed =
                report.summary.result == BuildResult.Succeeded &&
                report.summary.totalErrors == 0;

            StringBuilder message = new StringBuilder();

            message.Append(
                passed ? "PASS" : "FAIL");

            message.Append(
                " - result=" +
                report.summary.result +
                ", errors=" +
                report.summary.totalErrors +
                ", warnings=" +
                report.summary.totalWarnings);

            if (!passed)
            {
                foreach (BuildStep step in report.steps)
                {
                    if (step.messages == null)
                        continue;

                    foreach (BuildStepMessage buildMessage in step.messages)
                    {
                        if (buildMessage.type == LogType.Error ||
                            buildMessage.type == LogType.Exception)
                        {
                            message.AppendLine();
                            message.Append(
                                "BUILD ERROR: " +
                                buildMessage.content);
                        }
                    }
                }
            }

            return new BuildValidationResult(
                passed,
                message.ToString());
        }
        catch (Exception ex)
        {
            return new BuildValidationResult(
                false,
                "FAIL - BuildPipeline exception: " + ex);
        }
        finally
        {
            try
            {
                if (Directory.Exists(tempRoot))
                    Directory.Delete(tempRoot, true);
            }
            catch (Exception cleanupEx)
            {
                Debug.LogWarning(
                    "Pyungmoo temporary build cleanup failed: " +
                    cleanupEx.Message);
            }
        }
    }

    private static Scene OpenScene()
    {
        Scene scene = SceneManager.GetActiveScene();
        if (!string.Equals(scene.path, ScenePath, StringComparison.OrdinalIgnoreCase))
            scene = EditorSceneManager.OpenScene(ScenePath, OpenSceneMode.Single);

        return scene;
    }

    private static List<BuildingModel> DiscoverModels(string folder)
    {
        string absoluteFolder =
            Path.Combine(
                Directory.GetParent(Application.dataPath).FullName,
                folder.Substring("Assets/".Length)
                    .Replace('/', Path.DirectorySeparatorChar));

        if (!Directory.Exists(absoluteFolder))
            return new List<BuildingModel>();

        List<BuildingModel> result = new List<BuildingModel>();

        foreach (string file in Directory.GetFiles(
                     absoluteFolder,
                     "*.fbx",
                     SearchOption.AllDirectories)
                 .OrderBy(x => x, StringComparer.OrdinalIgnoreCase))
        {
            string relative =
                Path.GetRelativePath(
                    Directory.GetParent(Application.dataPath).FullName,
                    file)
                .Replace('\\', '/');

            string assetPath = relative.StartsWith("Assets/", StringComparison.OrdinalIgnoreCase)
                ? relative
                : "Assets/" + relative;

            GameObject prefab = null;
            string error = string.Empty;

            try
            {
                AssetDatabase.ImportAsset(
                    assetPath,
                    ImportAssetOptions.ForceSynchronousImport |
                    ImportAssetOptions.ForceUpdate);

                prefab =
                    AssetDatabase.LoadAssetAtPath<GameObject>(assetPath);

                if (prefab == null)
                {
                    prefab =
                        AssetDatabase.LoadAllAssetsAtPath(assetPath)
                            .OfType<GameObject>()
                            .FirstOrDefault();
                }

                error = ValidatePrefab(prefab, assetPath);
            }
            catch (Exception ex)
            {
                error = ex.Message;
            }

            string name = Path.GetFileNameWithoutExtension(file);
            result.Add(new BuildingModel
            {
                Path = assetPath,
                Prefab = prefab,
                CanonicalKey = NormalizeModelKey(name),
                IsLod = name.IndexOf("_lod_", StringComparison.OrdinalIgnoreCase) >= 0,
                ValidationError = error
            });
        }

        return result;
    }

    private static string ValidatePrefab(GameObject prefab, string assetPath)
    {
        if (prefab == null)
            return "Unity GameObject olarak yüklenemedi.";

        Renderer[] renderers =
            prefab.GetComponentsInChildren<Renderer>(true);

        if (renderers.Length == 0)
            return "Renderer yok.";

        foreach (Renderer renderer in renderers)
        {
            if (renderer.sharedMaterials == null ||
                renderer.sharedMaterials.Length == 0)
                return "Renderer material slotu yok: " + renderer.name;

            if (renderer.sharedMaterials.Any(x => x == null))
                return "Null material bulundu: " + renderer.name;

            if (renderer.sharedMaterials.Any(
                    x => x != null && x.shader == null))
                return "Shader eksik: " + renderer.name;

            if (renderer.bounds.size.sqrMagnitude <= 0.000001f)
                return "Renderer bounds boş: " + renderer.name;
        }

        foreach (MeshFilter filter in
                 prefab.GetComponentsInChildren<MeshFilter>(true))
        {
            if (filter.sharedMesh == null)
                return "MeshFilter sharedMesh null: " + filter.name;
        }

        foreach (SkinnedMeshRenderer skinned in
                 prefab.GetComponentsInChildren<SkinnedMeshRenderer>(true))
        {
            if (skinned.sharedMesh == null)
                return "SkinnedMeshRenderer sharedMesh null: " + skinned.name;
        }

        return string.Empty;
    }

    private static Dictionary<uint, BuildingProperty> LoadBuildingProperties(
        IEnumerable<string> propertyRoots,
        string repoRoot,
        Dictionary<string, BuildingModel> buildingCanonical)
    {
        var result = new Dictionary<uint, BuildingProperty>();
        var scores = new Dictionary<uint, int>();
        var ambiguous = new HashSet<uint>();

        foreach (string root in propertyRoots.Where(Directory.Exists))
        foreach (string file in Directory.EnumerateFiles(
                     root,
                     "*.*",
                     SearchOption.AllDirectories)
                 .Where(x =>
                     PropertyExtensions.Contains(
                         Path.GetExtension(x),
                         StringComparer.OrdinalIgnoreCase)))
        {
            string text;
            try
            {
                text = File.ReadAllText(file);
            }
            catch
            {
                continue;
            }

            Match sourceMatch = Regex.Match(
                text,
                @"(?im)^\s*buildingfile\s+""([^""]+)""");

            if (!sourceMatch.Success)
                continue;

            string sourcePath = sourceMatch.Groups[1].Value;
            string sourceName =
                Path.GetFileNameWithoutExtension(sourcePath);

            string normalized = NormalizeModelKey(sourceName);

            string canonicalModelKey = ResolveC1CanonicalKey(normalized);

            if (string.IsNullOrEmpty(canonicalModelKey))
                continue;

            Match idMatch = Regex.Match(
                text,
                @"(?im)^\s*YPRT\s*\r?\n\s*(\d+)\s*$");

            if (!idMatch.Success ||
                !uint.TryParse(
                    idMatch.Groups[1].Value,
                    NumberStyles.None,
                    CultureInfo.InvariantCulture,
                    out uint propertyId))
                continue;

            Match nameMatch = Regex.Match(
                text,
                @"(?im)^\s*propertyname\s+""([^""]+)""");

            BuildingProperty property = new BuildingProperty
            {
                Id = propertyId,
                PropertyName = nameMatch.Success
                    ? nameMatch.Groups[1].Value
                    : Path.GetFileNameWithoutExtension(file),
                SourcePath = sourcePath,
                SourceModelName = sourceName,
                SourcePropertyFile = file
            };

            RegisterId(result, scores, ambiguous, propertyId, property, 1000);

            string propertyFileName =
                Path.GetFileName(file);
            string propertyFileStem =
                Path.GetFileNameWithoutExtension(file);

            RegisterStringAlias(
                result, scores, ambiguous,
                propertyFileName, property, 260);

            RegisterStringAlias(
                result, scores, ambiguous,
                propertyFileStem, property, 250);

            RegisterStringAlias(
                result, scores, ambiguous,
                sourceName, property, 350);

            RegisterStringAlias(
                result, scores, ambiguous,
                Path.GetFileName(sourcePath), property, 360);

            RegisterStringAlias(
                result, scores, ambiguous,
                sourcePath, property, 300);

            string normalizedSourcePath =
                sourcePath.Replace('\\', '/');

            RegisterStringAlias(
                result, scores, ambiguous,
                normalizedSourcePath, property, 310);

            RegisterStringAlias(
                result, scores, ambiguous,
                normalizedSourcePath.ToUpperInvariant(), property, 320);

            RegisterStringAlias(
                result, scores, ambiguous,
                "./" + normalizedSourcePath.ToUpperInvariant(), property, 325);

            RegisterStringAlias(
                result, scores, ambiguous,
                "./" + normalizedSourcePath.Replace('/', '\\').ToUpperInvariant(), property, 325);

            RegisterStringAlias(
                result, scores, ambiguous,
                Path.GetFileName(sourcePath).ToUpperInvariant(), property, 365);

            RegisterStringAlias(
                result, scores, ambiguous,
                Path.GetFileNameWithoutExtension(sourcePath).ToUpperInvariant(), property, 355);

            try
            {
                uint propertyFileCrc = ComputeCrc32File(file);
                RegisterId(
                    result, scores, ambiguous,
                    propertyFileCrc, property, 850);
            }
            catch
            {
            }

            string sourceFile =
                FindSourceFile(repoRoot, sourcePath, ResolveC1CanonicalKey(normalized));

            if (!string.IsNullOrEmpty(sourceFile) &&
                File.Exists(sourceFile))
            {
                try
                {
                    uint fileCrc = ComputeCrc32File(sourceFile);
                    RegisterId(
                        result, scores, ambiguous,
                        fileCrc, property, 900);
                }
                catch
                {
                }
            }
        }

        foreach (uint id in ambiguous)
            result.Remove(id);

        return result;
    }

    private static void RegisterStringAlias(
        Dictionary<uint, BuildingProperty> result,
        Dictionary<uint, int> scores,
        HashSet<uint> ambiguous,
        string text,
        BuildingProperty property,
        int score)
    {
        if (string.IsNullOrWhiteSpace(text))
            return;

        RegisterId(
            result,
            scores,
            ambiguous,
            ComputeCrc32String(text),
            property,
            score);
    }

    private static void RegisterId(
        Dictionary<uint, BuildingProperty> result,
        Dictionary<uint, int> scores,
        HashSet<uint> ambiguous,
        uint id,
        BuildingProperty property,
        int score)
    {
        if (ambiguous.Contains(id))
            return;

        if (!result.TryGetValue(id, out BuildingProperty old))
        {
            result.Add(id, property);
            scores[id] = score;
            return;
        }

        if (string.Equals(
                NormalizeModelKey(old.SourceModelName),
                NormalizeModelKey(property.SourceModelName),
                StringComparison.OrdinalIgnoreCase))
        {
            if (score > scores[id])
            {
                result[id] = property;
                scores[id] = score;
            }
            return;
        }

        if (score > scores[id])
        {
            result[id] = property;
            scores[id] = score;
            return;
        }

        if (score == scores[id])
        {
            result.Remove(id);
            scores.Remove(id);
            ambiguous.Add(id);
        }
    }

    private static string FindSourceFile(string repoRoot, string sourcePath, string canonicalModelKey)
    {
        string fileName = Path.GetFileName(sourcePath);
        if (string.IsNullOrWhiteSpace(fileName))
            return null;

        string normalized = sourcePath.Replace('\\', '/');
        int marker = normalized.IndexOf(
            "ymir work/",
            StringComparison.OrdinalIgnoreCase);

        if (marker >= 0)
        {
            string suffix =
                normalized.Substring(marker + "ymir work/".Length)
                    .Replace('/', Path.DirectorySeparatorChar);

            string[] roots =
            {
                Path.Combine(repoRoot, "Metin2Client", "Zone", "ymir work"),
                Path.Combine(repoRoot, "Metin2Client"),
                Path.Combine(repoRoot, "Zone", "ymir work"),
                repoRoot
            };

            foreach (string root in roots)
            {
                string candidate = Path.Combine(root, suffix);
                if (File.Exists(candidate))
                    return candidate;
            }
        }

        string directCandidate =
            Path.Combine(repoRoot, "Metin2Client", "Zone", "ymir work", "zone", "c", "building", fileName);

        if (File.Exists(directCandidate))
            return directCandidate;

        if (!string.IsNullOrWhiteSpace(canonicalModelKey))
        {
            string canonicalFileName = canonicalModelKey + Path.GetExtension(fileName);
            string canonicalCandidate =
                Path.Combine(repoRoot, "Metin2Client", "Zone", "ymir work", "zone", "c", "building", canonicalFileName);

            if (File.Exists(canonicalCandidate))
                return canonicalCandidate;
        }

        string searchRoot =
            Path.Combine(repoRoot, "Metin2Client", "Zone");

        if (Directory.Exists(searchRoot))
        {
            try
            {
                string found =
                    Directory.EnumerateFiles(
                            searchRoot,
                            fileName,
                            SearchOption.AllDirectories)
                        .FirstOrDefault();
                if (!string.IsNullOrEmpty(found))
                    return found;
            }
            catch
            {
            }
        }

        return null;
    }

    private static string ResolveC1CanonicalKey(string normalized)
    {
        if (string.IsNullOrWhiteSpace(normalized))
            return string.Empty;

        normalized = NormalizeModelKey(normalized);

        if (normalized.StartsWith("c1-", StringComparison.OrdinalIgnoreCase) ||
            normalized.StartsWith("c1_", StringComparison.OrdinalIgnoreCase))
            return normalized;

        foreach (char prefix in new[] { 'a', 'b' })
        {
            if (normalized.StartsWith(prefix + "1-", StringComparison.OrdinalIgnoreCase) ||
                normalized.StartsWith(prefix + "1_", StringComparison.OrdinalIgnoreCase))
                return "c" + normalized.Substring(1);
        }

        return string.Empty;
    }

    private static uint ComputeCrc32File(string path)
    {
        using FileStream stream = File.OpenRead(path);
        uint crc = 0xFFFFFFFFu;
        byte[] buffer = new byte[1024 * 64];
        int read;

        while ((read = stream.Read(buffer, 0, buffer.Length)) > 0)
        {
            for (int i = 0; i < read; i++)
            {
                crc ^= buffer[i];
                for (int bit = 0; bit < 8; bit++)
                    crc = (crc & 1u) != 0
                        ? (crc >> 1) ^ 0xEDB88320u
                        : crc >> 1;
            }
        }

        return ~crc;
    }

    private static uint ComputeCrc32String(string value)
    {
        return ComputeCrc32Bytes(Encoding.UTF8.GetBytes(value));
    }

    private static uint ComputeCrc32Bytes(byte[] data)
    {
        uint crc = 0xFFFFFFFFu;

        foreach (byte value in data)
        {
            crc ^= value;
            for (int bit = 0; bit < 8; bit++)
                crc = (crc & 1u) != 0
                    ? (crc >> 1) ^ 0xEDB88320u
                    : crc >> 1;
        }

        return ~crc;
    }

    private static Transform CreateInactiveAssetLibrary(
        GameObject mapRoot,
        string rootName,
        List<BuildingModel> models,
        Bounds mapBounds)
    {
        Transform existing = mapRoot.transform.Find(rootName);
        if (existing != null)
            UnityEngine.Object.DestroyImmediate(existing.gameObject);

        GameObject root = new GameObject(rootName);
        root.transform.SetParent(mapRoot.transform, false);
        root.SetActive(false);

        const int columns = 8;
        const float spacing = 25.0f;

        for (int i = 0; i < models.Count; i++)
        {
            BuildingModel model = models[i];
            if (model.Prefab == null)
                throw new InvalidOperationException(
                    "Library için prefab yok: " + model.Path);

            GameObject instance =
                PrefabUtility.InstantiatePrefab(model.Prefab) as GameObject;

            if (instance == null)
                throw new InvalidOperationException(
                    "Library instantiate başarısız: " + model.Path);

            instance.name =
                "ASSET_" +
                i.ToString("000", CultureInfo.InvariantCulture) +
                "_" +
                Path.GetFileNameWithoutExtension(model.Path);

            instance.transform.SetParent(root.transform, false);

            int row = i / columns;
            int col = i % columns;

            instance.transform.localPosition =
                new Vector3(col * spacing, 0.0f, row * spacing);

            instance.transform.localRotation = Quaternion.identity;
            instance.isStatic = true;
        }

        return root.transform;
    }

    private static string ValidateFinalScene(
        GameObject mapRoot,
        Transform buildingRoot,
        Transform npcRoot,
        Transform buildingLibrary,
        Transform npcLibrary,
        int buildingAssetCount,
        int npcAssetCount,
        int buildingPlaced,
        int npcPlaced)
    {
        var errors = new List<string>();

        if (mapRoot == null)
            errors.Add("Pyungmoo root null.");

        if (buildingRoot == null)
            errors.Add("FINAL_Buildings root missing.");

        if (npcRoot == null)
            errors.Add("FINAL_NPCs root missing.");

        if (buildingLibrary == null || buildingLibrary.childCount != buildingAssetCount)
            errors.Add(
                "Building library count mismatch: " +
                (buildingLibrary == null ? 0 : buildingLibrary.childCount) +
                "/" + buildingAssetCount);

        if (npcLibrary == null || npcLibrary.childCount != npcAssetCount)
            errors.Add(
                "NPC library count mismatch: " +
                (npcLibrary == null ? 0 : npcLibrary.childCount) +
                "/" + npcAssetCount);

        if (buildingAssetCount != 47)
            errors.Add("Expected 47 Building FBX assets, got " + buildingAssetCount);

        if (npcAssetCount != 22)
            errors.Add("Expected 22 NPC FBX assets, got " + npcAssetCount);

        if (npcPlaced <= 0)
            errors.Add("No NPC instances were placed.");

        if (npcPlaced != NpcPlacements.Length)
            errors.Add(
                "NPC placement count mismatch: " +
                npcPlaced + "/" + NpcPlacements.Length);

        if (buildingPlaced <= 0)
            errors.Add("No Building instances were placed from AreaData.");

        if (buildingRoot != null)
        {
            if (buildingRoot.childCount != buildingPlaced)
                errors.Add(
                    "Building scene instance count mismatch: " +
                    buildingRoot.childCount + "/" + buildingPlaced);

            foreach (Transform child in buildingRoot)
            {
                ValidateSceneInstance(
                    child.gameObject,
                    BuildingFolder,
                    errors);

                if (child.name.IndexOf(
                        "PLACEHOLDER",
                        StringComparison.OrdinalIgnoreCase) >= 0)
                    errors.Add("Building placeholder remains: " + child.name);
            }
        }

        if (npcRoot != null)
        {
            if (npcRoot.childCount != npcPlaced)
                errors.Add(
                    "NPC scene instance count mismatch: " +
                    npcRoot.childCount + "/" + npcPlaced);

            foreach (Transform child in npcRoot)
            {
                ValidateSceneInstance(
                    child.gameObject,
                    NpcFolder,
                    errors);

                if (child.name.IndexOf(
                        "PLACEHOLDER",
                        StringComparison.OrdinalIgnoreCase) >= 0)
                    errors.Add("NPC placeholder remains: " + child.name);

                if (child.GetComponent<Metin2NpcIdentity>() == null)
                    errors.Add("NPC identity component missing: " + child.name);
            }
        }

        ValidateLibrary(buildingLibrary, BuildingFolder, buildingAssetCount, errors);
        ValidateLibrary(npcLibrary, NpcFolder, npcAssetCount, errors);

        string[] legacyRootNames =
        {
            "DirectBuildingObjects",
            "Metin2Buildings",
            "BuildingFBXPreview",
            "BuildingLibraryPreview",
            "NPCs"
        };

        foreach (string name in legacyRootNames)
        {
            if (mapRoot != null && mapRoot.transform.Find(name) != null)
                errors.Add("Legacy root still exists: " + name);
        }

        if (errors.Count == 0)
            return "PASS\nNo missing FBX, no missing mesh/material, no placeholders, no legacy roots, no scene count mismatches.";

        return "FAIL\n" + string.Join("\n", errors);
    }

    private static void ValidateLibrary(
        Transform library,
        string expectedFolder,
        int expectedCount,
        List<string> errors)
    {
        if (library == null)
            return;

        if (library.gameObject.activeSelf)
            errors.Add("Asset library must remain inactive: " + library.name);

        var paths = new HashSet<string>(StringComparer.OrdinalIgnoreCase);

        foreach (Transform child in library)
        {
            ValidateSceneInstance(child.gameObject, expectedFolder, errors);

            GameObject source =
                PrefabUtility.GetCorrespondingObjectFromSource(
                    child.gameObject) as GameObject;

            if (source == null)
            {
                errors.Add(
                    "Library child has no prefab source: " +
                    child.name);
                continue;
            }

            string path = AssetDatabase.GetAssetPath(source);
            if (string.IsNullOrEmpty(path) ||
                !path.StartsWith(
                    expectedFolder + "/",
                    StringComparison.OrdinalIgnoreCase))
            {
                errors.Add(
                    "Library child points outside expected folder: " +
                    child.name);
            }

            if (!paths.Add(path))
                errors.Add("Duplicate library asset reference: " + path);
        }

        if (library.childCount != expectedCount)
            errors.Add(
                "Library child count mismatch: " +
                library.childCount + "/" + expectedCount);
    }

    private static void ValidateSceneInstance(
        GameObject instance,
        string expectedFolder,
        List<string> errors)
    {
        if (instance == null)
        {
            errors.Add("Null scene instance.");
            return;
        }

        Vector3 p = instance.transform.position;
        if (float.IsNaN(p.x) || float.IsNaN(p.y) || float.IsNaN(p.z) ||
            float.IsInfinity(p.x) || float.IsInfinity(p.y) || float.IsInfinity(p.z))
        {
            errors.Add("Invalid transform position: " + instance.name);
        }

        GameObject source =
            PrefabUtility.GetCorrespondingObjectFromSource(instance)
            as GameObject;

        if (source == null)
        {
            errors.Add("Scene instance has no FBX prefab source: " + instance.name);
        }
        else
        {
            string sourcePath = AssetDatabase.GetAssetPath(source);
            if (string.IsNullOrEmpty(sourcePath) ||
                !sourcePath.StartsWith(
                    expectedFolder + "/",
                    StringComparison.OrdinalIgnoreCase))
            {
                errors.Add(
                    "Wrong model source for " +
                    instance.name +
                    ": " +
                    sourcePath);
            }
        }

        Renderer[] renderers =
            instance.GetComponentsInChildren<Renderer>(true);

        if (renderers.Length == 0)
        {
            errors.Add("No Renderer: " + instance.name);
            return;
        }

        foreach (Renderer renderer in renderers)
        {
            if (renderer.sharedMaterials == null ||
                renderer.sharedMaterials.Length == 0)
            {
                errors.Add(
                    "Renderer has no materials: " +
                    instance.name +
                    "/" +
                    renderer.name);
            }
            else if (renderer.sharedMaterials.Any(x => x == null))
            {
                errors.Add(
                    "Renderer contains null material: " +
                    instance.name +
                    "/" +
                    renderer.name);
            }
            else if (renderer.sharedMaterials.Any(x => x.shader == null))
            {
                errors.Add(
                    "Renderer contains material with missing shader: " +
                    instance.name +
                    "/" +
                    renderer.name);
            }

            if (renderer.bounds.size.sqrMagnitude <= 0.000001f)
                errors.Add(
                    "Renderer bounds empty: " +
                    instance.name +
                    "/" +
                    renderer.name);
        }

        foreach (MeshFilter filter in
                 instance.GetComponentsInChildren<MeshFilter>(true))
        {
            if (filter.sharedMesh == null)
                errors.Add(
                    "MeshFilter sharedMesh null: " +
                    instance.name +
                    "/" +
                    filter.name);
        }

        foreach (SkinnedMeshRenderer skinned in
                 instance.GetComponentsInChildren<SkinnedMeshRenderer>(true))
        {
            if (skinned.sharedMesh == null)
                errors.Add(
                    "SkinnedMeshRenderer sharedMesh null: " +
                    instance.name +
                    "/" +
                    skinned.name);
        }
    }

    private static Bounds CalculateMapBounds(GameObject mapRoot)
    {
        bool hasBounds = false;
        Bounds bounds = default;

        foreach (Renderer renderer in
                 mapRoot.GetComponentsInChildren<Renderer>(true))
        {
            if (renderer == null)
                continue;

            if (!hasBounds)
            {
                bounds = renderer.bounds;
                hasBounds = true;
            }
            else
            {
                bounds.Encapsulate(renderer.bounds);
            }
        }

        return hasBounds
            ? bounds
            : new Bounds(Vector3.zero, new Vector3(2048, 100, 2560));
    }

    private static void AddMeshColliders(GameObject root)
    {
        foreach (MeshFilter filter in
                 root.GetComponentsInChildren<MeshFilter>(true))
        {
            if (filter.sharedMesh == null)
                continue;

            if (filter.GetComponent<MeshCollider>() != null)
                continue;

            MeshCollider collider =
                filter.gameObject.AddComponent<MeshCollider>();
            collider.sharedMesh = filter.sharedMesh;
        }
    }

    private static bool TryProjectToTerrain(
        Vector3 xz,
        out float groundY)
    {
        Ray ray = new Ray(
            new Vector3(xz.x, RayStartHeight, xz.z),
            Vector3.down);

        if (Physics.Raycast(
                ray,
                out RaycastHit hit,
                RayStartHeight + 100.0f,
                ~0,
                QueryTriggerInteraction.Ignore))
        {
            groundY = hit.point.y;
            return true;
        }

        groundY = 0.0f;
        return false;
    }

    private static bool TryParseUInt32Token(string token, out uint value)
    {
        if (uint.TryParse(
                token,
                NumberStyles.None,
                CultureInfo.InvariantCulture,
                out value))
            return true;

        if (long.TryParse(
                token,
                NumberStyles.Integer,
                CultureInfo.InvariantCulture,
                out long signed))
        {
            value = unchecked((uint)signed);
            return true;
        }

        value = 0u;
        return false;
    }

    private static Vector3 ParseVector3(string line)
    {
        string[] parts =
            line.Split(
                new[] { ' ', '\t' },
                StringSplitOptions.RemoveEmptyEntries);

        if (parts.Length < 3)
            throw new InvalidDataException(
                "Vector3 satırı bozuk: " + line);

        return new Vector3(
            float.Parse(parts[0], CultureInfo.InvariantCulture),
            float.Parse(parts[1], CultureInfo.InvariantCulture),
            float.Parse(parts[2], CultureInfo.InvariantCulture));
    }

    private static List<AreaObject> ParseAreaData(string file)
    {
        string[] lines = File.ReadAllLines(file);
        var result = new List<AreaObject>();

        for (int i = 0; i < lines.Length; i++)
        {
            string trimmed = lines[i].Trim();

            if (!trimmed.StartsWith(
                    "Start Object",
                    StringComparison.OrdinalIgnoreCase))
                continue;

            Match objectMatch =
                Regex.Match(
                    trimmed,
                    @"Start Object(\d+)",
                    RegexOptions.IgnoreCase |
                    RegexOptions.CultureInvariant);

            int objectIndex = result.Count;

            if (objectMatch.Success)
            {
                objectIndex = int.Parse(
                    objectMatch.Groups[1].Value,
                    CultureInfo.InvariantCulture);
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

            if (data.Count < 4)
                throw new InvalidDataException(
                    file +
                    " Object" +
                    objectIndex +
                    " eksik kayıt.");

            Vector3 position = ParseVector3(data[0]);

            uint propertyId;
            if (!TryParseUInt32Token(data[1], out propertyId))
                throw new InvalidDataException(
                    file + " Object" + objectIndex +
                    " Property/CRC32 değeri bozuk: " + data[1]);

            string rotationLine = data[2];
            string[] rotationParts = rotationLine.Split(
                new[] { '#' },
                StringSplitOptions.RemoveEmptyEntries);

            Vector3 rotation = Vector3.zero;

            if (rotationParts.Length == 1)
            {
                rotation.z =
                    float.Parse(
                        rotationParts[0],
                        CultureInfo.InvariantCulture);
            }
            else if (rotationParts.Length >= 3)
            {
                rotation.x =
                    float.Parse(
                        rotationParts[0],
                        CultureInfo.InvariantCulture);
                rotation.y =
                    float.Parse(
                        rotationParts[1],
                        CultureInfo.InvariantCulture);
                rotation.z =
                    float.Parse(
                        rotationParts[2],
                        CultureInfo.InvariantCulture);
            }

            float heightOffset =
                float.Parse(
                    data[3],
                    CultureInfo.InvariantCulture);

            result.Add(new AreaObject
            {
                ObjectIndex = objectIndex,
                Position = position,
                PropertyId = propertyId,
                Rotation = rotation,
                HeightOffset = heightOffset
            });
        }

        return result;
    }

    private static List<string> DiscoverAreaFiles(string root)
    {
        return Directory.EnumerateFiles(
                root,
                "areadata.txt",
                SearchOption.AllDirectories)
            .Where(x =>
                Regex.IsMatch(
                    Path.GetFileName(
                        Path.GetDirectoryName(x) ?? string.Empty),
                    @"^\d{6}$"))
            .OrderBy(
                x => Path.GetFileName(
                    Path.GetDirectoryName(x) ?? string.Empty),
                StringComparer.Ordinal)
            .ToList();
    }

    private static Transform CreateRoot(GameObject mapRoot, string name)
    {
        Transform old = mapRoot.transform.Find(name);
        if (old != null)
            UnityEngine.Object.DestroyImmediate(old.gameObject);

        GameObject go = new GameObject(name);
        go.transform.SetParent(mapRoot.transform, false);
        return go.transform;
    }

    private static void DeleteOldRoots(GameObject mapRoot)
    {
        string[] names =
        {
            "DirectBuildingObjects",
            "Metin2Buildings",
            "BuildingFBXPreview",
            "BuildingLibraryPreview",
            "BuildingAssetLibrary",
            "NPCs",
            BuildingRootName,
            NpcRootName,
            BuildingLibraryRootName,
            NpcLibraryRootName
        };

        foreach (string name in names)
        {
            Transform child = mapRoot.transform.Find(name);
            if (child != null)
                UnityEngine.Object.DestroyImmediate(child.gameObject);
        }
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

    private static void WriteReport(string text)
    {
        string absolute =
            Path.Combine(Application.dataPath, ReportPath.Substring("Assets/".Length));

        string directory = Path.GetDirectoryName(absolute);
        if (!string.IsNullOrEmpty(directory))
            Directory.CreateDirectory(directory);

        File.WriteAllText(
            absolute,
            text,
            new UTF8Encoding(false));
    }

    private static void AddCount(
        Dictionary<uint, int> dict,
        uint id)
    {
        dict.TryGetValue(id, out int current);
        dict[id] = current + 1;
    }

    private static string NormalizeModelKey(string name)
    {
        if (string.IsNullOrWhiteSpace(name))
            return string.Empty;

        string value = name.Trim().ToLowerInvariant();

        value = Regex.Replace(
            value,
            @"_lod_\d+out$",
            string.Empty);

        value = Regex.Replace(
            value,
            @"_lod_\d+$",
            string.Empty);

        value = Regex.Replace(
            value,
            @"out$",
            string.Empty);

        return value;
    }

    private static Quaternion ConvertRotation(Vector3 source)
    {
        Quaternion sourceRotation =
            Quaternion.Euler(
                source.x,
                source.y,
                source.z);

        Quaternion basis =
            Quaternion.Euler(-90.0f, 0.0f, 0.0f);

        return basis *
               sourceRotation *
               Quaternion.Inverse(basis);
    }

    private static string Sanitize(string name)
    {
        foreach (char c in Path.GetInvalidFileNameChars())
            name = name.Replace(c, '_');

        return name.Replace(' ', '_');
    }

    private sealed class BuildingModel
    {
        public string Path;
        public GameObject Prefab;
        public string CanonicalKey;
        public bool IsLod;
        public string ValidationError;
    }

    private sealed class BuildingProperty
    {
        public uint Id;
        public string PropertyName;
        public string SourcePath;
        public string SourceModelName;
        public string SourcePropertyFile;
    }

    private sealed class ResolvedBuilding
    {
        public AreaObject AreaObject;
        public BuildingProperty Property;
        public BuildingModel Model;

        public ResolvedBuilding(
            AreaObject areaObject,
            BuildingProperty property,
            BuildingModel model)
        {
            AreaObject = areaObject;
            Property = property;
            Model = model;
        }
    }

    private struct AreaObject
    {
        public int ObjectIndex;
        public Vector3 Position;
        public uint PropertyId;
        public Vector3 Rotation;
        public float HeightOffset;
    }

    private sealed class NpcPlacement
    {
        public readonly int Vnum;
        public readonly string DisplayName;
        public readonly string ModelKey;
        public readonly int MapX;
        public readonly int MapY;
        public readonly int Direction;

        public NpcPlacement(
            int vnum,
            string displayName,
            string modelKey,
            int mapX,
            int mapY,
            int direction)
        {
            Vnum = vnum;
            DisplayName = displayName;
            ModelKey = modelKey;
            MapX = mapX;
            MapY = mapY;
            Direction = direction;
        }
    }
}
