using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using UnityEditor;
using UnityEditor.Build.Reporting;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;

public static class Metin2PyungmooIntegrationValidator
{
    private const string ScenePath = "Assets/Scenes/Pyungmoo.unity";
    private const string RootName = "Pyungmoo";
    private const string BuildingFolder = "Assets/Metin2Imported/Building";
    private const string NpcFolder = "Assets/Metin2Imported/NPC";
    private const string BuildingGalleryName = "BuildingFBXPreview";
    private const string BuildingRootName = "DirectBuildingObjects";
    private const string NpcRootName = "NPCs";
    private const string ReportPath =
        "Assets/Metin2Generated/Pyungmoo/PyungmooCompleteValidation.txt";

    [MenuItem("Metin2/Pyungmoo/Validate Complete Integration")]
    public static void ValidateFromMenu()
    {
        ValidationResult result = ValidateCurrentScene();

        WriteReport(result);

        EditorUtility.DisplayDialog(
            result.Passed ? "Pyungmoo VALIDATION PASS" : "Pyungmoo VALIDATION FAILED",
            result.ToDisplayText(),
            "Tamam");
    }

    public static ValidationResult ValidateCurrentScene()
    {
        var result = new ValidationResult();

        try
        {
            Scene scene = SceneManager.GetActiveScene();

            if (!string.Equals(
                    scene.path,
                    ScenePath,
                    StringComparison.OrdinalIgnoreCase))
            {
                result.Fail($"Aktif sahne Pyungmoo değil: {scene.path}");
                scene = EditorSceneManager.OpenScene(
                    ScenePath,
                    OpenSceneMode.Single);
            }

            result.Check(
                File.Exists(Path.Combine(
                    Directory.GetParent(Application.dataPath).FullName,
                    ScenePath.Replace('/', Path.DirectorySeparatorChar))),
                "Pyungmoo.unity dosyası mevcut.");

            GameObject mapRoot = GameObject.Find(RootName);
            if (mapRoot == null)
            {
                result.Fail("Pyungmoo kök GameObject'i bulunamadı.");
                return result;
            }

            ValidateBuildSettings(result);
            ValidateC1BuildingSourceCoverage(result);
            ValidateBuildingAssetsAndGallery(result, mapRoot.transform);
            ValidateDirectBuildingInstances(result, mapRoot.transform);
            ValidateDirectBuildingReport(result);
            ValidateNpcAssetsAndScene(result, mapRoot.transform);
            ValidateMapObjects(result, mapRoot.transform);

            AssetDatabase.SaveAssets();
            AssetDatabase.Refresh();

            result.Check(
                !EditorSceneManager.IsSceneDirty(scene),
                "Pyungmoo sahnesi kaydedilmiş.");
        }
        catch (Exception ex)
        {
            result.Fail("Validator exception: " + ex);
        }

        return result;
    }

    public static ValidationResult ValidateAndBuildPlayer()
    {
        ValidationResult result = ValidateCurrentScene();

        if (!result.Passed)
            return result;

        try
        {
            string tempRoot = Path.Combine(
                Path.GetTempPath(),
                "SAGLAMKAFA_PyungmooValidation");

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

            result.Check(
                report.summary.result == BuildResult.Succeeded &&
                report.summary.totalErrors == 0,
                $"StandaloneWindows64 build sonucu: {report.summary.result}, errors={report.summary.totalErrors}");

            if (report.summary.result != BuildResult.Succeeded ||
                report.summary.totalErrors != 0)
            {
                foreach (BuildStep step in report.steps)
                {
                    if (step.messages == null)
                        continue;

                    foreach (BuildStepMessage message in step.messages)
                    {
                        if (message.type == LogType.Error ||
                            message.type == LogType.Exception)
                        {
                            result.Fail(
                                $"Build error: {message.content}");
                        }
                    }
                }
            }

            try
            {
                if (Directory.Exists(tempRoot))
                    Directory.Delete(tempRoot, true);
            }
            catch
            {
                // Validation result is independent of temp cleanup.
            }
        }
        catch (Exception ex)
        {
            result.Fail(
                "Unity player build validation exception: " + ex.Message);
        }

        return result;
    }

    private static void ValidateBuildSettings(ValidationResult result)
    {
        bool enabled = EditorBuildSettings.scenes.Any(
            s => s.enabled &&
                 string.Equals(
                     s.path,
                     ScenePath,
                     StringComparison.OrdinalIgnoreCase));

        result.Check(
            enabled,
            "Pyungmoo build settings içinde aktif.");
    }

    private static void ValidateC1BuildingSourceCoverage(
        ValidationResult result)
    {
        string projectRoot =
            Directory.GetParent(Application.dataPath).FullName;

        string repoRoot =
            Directory.GetParent(projectRoot).FullName;

        string propertyRoot = Path.Combine(
            repoRoot,
            "Metin2Client",
            "Property",
            "property",
            "c");

        string buildingSourceRoot = Path.Combine(
            repoRoot,
            "Metin2Client",
            "Zone",
            "ymir work",
            "zone",
            "c",
            "building");

        if (!Directory.Exists(propertyRoot))
        {
            result.Fail(
                "C1 Building Property klasörü bulunamadı: " +
                propertyRoot);
            return;
        }

        if (!Directory.Exists(buildingSourceRoot))
        {
            result.Fail(
                "C1 Building GR2 klasörü bulunamadı: " +
                buildingSourceRoot);
            return;
        }

        string[] propertyFiles =
            Directory.GetFiles(
                    propertyRoot,
                    "*.prb",
                    SearchOption.AllDirectories)
                .OrderBy(p => p, StringComparer.OrdinalIgnoreCase)
                .ToArray();

        var modelNames =
            new HashSet<string>(
                StringComparer.OrdinalIgnoreCase);

        var missingGr2 =
            new HashSet<string>(
                StringComparer.OrdinalIgnoreCase);

        foreach (string propertyFile in propertyFiles)
        {
            string text;

            try
            {
                text = File.ReadAllText(propertyFile);
            }
            catch
            {
                continue;
            }

            Match sourceMatch = Regex.Match(
                text,
                @"^\s*(?:buildingfile|dungenblockfile|dungeonblockfile)\s+""([^""]+)""",
                RegexOptions.Multiline |
                RegexOptions.IgnoreCase |
                RegexOptions.CultureInvariant);

            if (!sourceMatch.Success)
                continue;

            string sourcePath = sourceMatch.Groups[1].Value
                .Replace('\\', '/');

            if (!sourcePath.Contains(
                    "/zone/c/building/",
                    StringComparison.OrdinalIgnoreCase))
                continue;

            string modelName =
                Path.GetFileNameWithoutExtension(sourcePath);

            if (string.IsNullOrWhiteSpace(modelName))
                continue;

            modelNames.Add(
                NormalizeBuildingName(modelName));

            string gr2Path = Path.Combine(
                buildingSourceRoot,
                Path.GetFileName(sourcePath));

            if (!File.Exists(gr2Path))
                missingGr2.Add(
                    Path.GetFileName(sourcePath));
        }

        result.AddMetric(
            "C1 Building Property source models",
            modelNames.Count);

        result.AddMetric(
            "C1 Building source GR2 missing",
            missingGr2.Count);

        result.Check(
            modelNames.Count == 36,
            $"C1 Property'deki benzersiz Building model sayısı beklenen 36 ({modelNames.Count}).");

        result.Check(
            missingGr2.Count == 0,
            "C1 Property tarafından referanslanan Building GR2'lerin tamamı mevcut.");

        string absoluteFolder = Path.Combine(
            Application.dataPath,
            "Metin2Imported",
            "Building");

        string[] fbxFiles = Directory.Exists(absoluteFolder)
            ? Directory.GetFiles(
                absoluteFolder,
                "*.*",
                SearchOption.AllDirectories)
                .Where(p =>
                    p.EndsWith(
                        ".fbx",
                        StringComparison.OrdinalIgnoreCase))
                .ToArray()
            : Array.Empty<string>();

        var normalizedFbx =
            new HashSet<string>(
                fbxFiles.Select(
                    p => NormalizeBuildingName(
                        Path.GetFileNameWithoutExtension(p))),
                StringComparer.OrdinalIgnoreCase);

        foreach (string modelName in modelNames)
        {
            result.Check(
                normalizedFbx.Contains(modelName),
                $"C1 Building Property -> FBX: {modelName}");
        }
    }

    private static string NormalizeBuildingName(string name)
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
            @"out$",
            string.Empty,
            RegexOptions.IgnoreCase |
            RegexOptions.CultureInvariant);

        return value.ToLowerInvariant();
    }

    private static void ValidateBuildingAssetsAndGallery(
        ValidationResult result,
        Transform mapRoot)
    {
        string absoluteFolder = Path.Combine(
            Application.dataPath,
            "Metin2Imported",
            "Building");

        string[] physicalFbx = Directory.Exists(absoluteFolder)
            ? Directory.GetFiles(
                absoluteFolder,
                "*.*",
                SearchOption.AllDirectories)
                .Where(p =>
                    p.EndsWith(
                        ".fbx",
                        StringComparison.OrdinalIgnoreCase))
                .OrderBy(p => p, StringComparer.OrdinalIgnoreCase)
                .ToArray()
            : Array.Empty<string>();

        result.AddMetric("Building FBX fiziksel", physicalFbx.Length);

        Transform gallery = mapRoot.Find(BuildingGalleryName);
        if (gallery == null)
        {
            result.Fail(
                $"Pyungmoo/{BuildingGalleryName} bulunamadı.");
            return;
        }

        var referenced = new Dictionary<string, int>(
            StringComparer.OrdinalIgnoreCase);

        int rendererless = 0;

        foreach (Transform child in gallery)
        {
            Renderer[] renderers =
                child.GetComponentsInChildren<Renderer>(true);

            if (renderers.Length == 0)
                rendererless++;

            GameObject source =
                PrefabUtility.GetCorrespondingObjectFromSource(
                    child.gameObject);

            if (source == null)
                continue;

            string sourcePath = AssetDatabase.GetAssetPath(source);
            if (string.IsNullOrWhiteSpace(sourcePath) ||
                !sourcePath.EndsWith(
                    ".fbx",
                    StringComparison.OrdinalIgnoreCase))
                continue;

            referenced.TryGetValue(sourcePath, out int count);
            referenced[sourcePath] = count + 1;
        }

        result.AddMetric(
            "Building gallery instance",
            referenced.Values.Sum());

        result.AddMetric(
            "Building gallery rendererless",
            rendererless);

        result.Check(
            physicalFbx.Length == 47,
            $"Building FBX envanteri tam 47 adet ({physicalFbx.Length}).");

        result.Check(
            physicalFbx.Length == referenced.Count,
            $"Her Building FBX galeriye en az bir kez referanslanmış ({referenced.Count}/{physicalFbx.Length}).");

        foreach (string absolutePath in physicalFbx)
        {
            string assetPath = ToAssetPath(absolutePath);
            referenced.TryGetValue(assetPath, out int count);

            result.Check(
                count == 1,
                $"Building FBX tam bir kez sahnede: {assetPath} (count={count})");
        }

        result.Check(
            rendererless == 0,
            "Building gallery içindeki bütün instance'larda Renderer var.");
    }

    private static void ValidateDirectBuildingInstances(
        ValidationResult result,
        Transform mapRoot)
    {
        Transform root = mapRoot.Find(BuildingRootName);

        if (root == null)
        {
            result.Fail(
                $"Pyungmoo/{BuildingRootName} bulunamadı; AreaData building instance katmanı oluşturulmamış.");
            return;
        }

        int instances = 0;
        int invalid = 0;

        foreach (Transform chunk in root)
        {
            foreach (Transform child in chunk)
            {
                GameObject source =
                    PrefabUtility.GetCorrespondingObjectFromSource(
                        child.gameObject);

                if (source == null)
                    continue;

                string sourcePath = AssetDatabase.GetAssetPath(source);
                if (!sourcePath.EndsWith(
                        ".fbx",
                        StringComparison.OrdinalIgnoreCase))
                    continue;

                instances++;

                if (child.GetComponentsInChildren<Renderer>(true).Length == 0)
                    invalid++;
            }
        }

        result.AddMetric(
            "Direct AreaData building instance",
            instances);

        result.AddMetric(
            "Direct building invalid",
            invalid);

        result.Check(
            instances > 0,
            "AreaData'dan en az bir gerçek Building FBX instance oluşturulmuş.");

        result.Check(
            invalid == 0,
            "Gerçek Building instance'ların tamamında Renderer var.");
    }

    private static void ValidateDirectBuildingReport(
        ValidationResult result)
    {
        string reportPath = Path.Combine(
            Application.dataPath,
            "Metin2Generated",
            "Pyungmoo",
            "PyungmooDirectBuildingReport.txt");

        if (!File.Exists(reportPath))
        {
            result.Fail(
                "Direct Building importer raporu bulunamadı: " +
                reportPath);
            return;
        }

        string report = File.ReadAllText(reportPath);

        int matches = ParseReportInt(
            report,
            "AreaData -> Building eşleşmesi:");

        int placed = ParseReportInt(
            report,
            "Haritaya yerleştirilen gerçek Building instance:");

        int missingModel = ParseReportInt(
            report,
            "Eksik Building FBX:");

        result.AddMetric(
            "Direct report building matches",
            matches);

        result.AddMetric(
            "Direct report placed buildings",
            placed);

        result.AddMetric(
            "Direct report missing Building FBX",
            missingModel);

        result.Check(
            matches == placed,
            $"Direct importer eşleşme ve placement sayısı aynı ({matches}/{placed}).");

        result.Check(
            missingModel == 0,
            "Eşleşmiş hiçbir AreaData Building referansında FBX eksik değil.");
    }

    private static int ParseReportInt(
        string report,
        string label)
    {
        Match match = Regex.Match(
            report ?? string.Empty,
            "^\\s*" +
            Regex.Escape(label) +
            "\\s*(?:=|:)?" +
            "\\s*(\\d+)",
            RegexOptions.Multiline |
            RegexOptions.CultureInvariant);

        return match.Success
            ? int.Parse(
                match.Groups[1].Value,
                System.Globalization.CultureInfo.InvariantCulture)
            : -1;
    }

    private static void ValidateNpcAssetsAndScene(
        ValidationResult result,
        Transform mapRoot)
    {
        string absoluteFolder = Path.Combine(
            Application.dataPath,
            "Metin2Imported",
            "NPC");

        string[] physicalFbx = Directory.Exists(absoluteFolder)
            ? Directory.GetFiles(
                absoluteFolder,
                "*.*",
                SearchOption.AllDirectories)
                .Where(p =>
                    p.EndsWith(
                        ".fbx",
                        StringComparison.OrdinalIgnoreCase))
                .OrderBy(p => p, StringComparer.OrdinalIgnoreCase)
                .ToArray()
            : Array.Empty<string>();

        result.AddMetric("NPC FBX fiziksel", physicalFbx.Length);

        Transform root = mapRoot.Find(NpcRootName);
        if (root == null)
        {
            result.Fail($"Pyungmoo/{NpcRootName} bulunamadı.");
            return;
        }

        int identityCount = 0;
        int placeholderCount = 0;
        int rendererless = 0;

        var usedModels = new Dictionary<string, int>(
            StringComparer.OrdinalIgnoreCase);
        var vnums = new Dictionary<int, int>();

        foreach (Metin2NpcIdentity identity in
                 root.GetComponentsInChildren<Metin2NpcIdentity>(true))
        {
            if (identity.transform.parent != root)
                continue;

            identityCount++;

            if (identity.gameObject.name.StartsWith(
                    "NPC_PLACEHOLDER_",
                    StringComparison.OrdinalIgnoreCase))
            {
                placeholderCount++;
            }

            if (identity.gameObject.GetComponentsInChildren<Renderer>(true).Length == 0)
            {
                rendererless++;
            }

            vnums.TryGetValue(identity.Vnum, out int count);
            vnums[identity.Vnum] = count + 1;

            GameObject source =
                PrefabUtility.GetCorrespondingObjectFromSource(
                    identity.gameObject);

            if (source == null)
                continue;

            string sourcePath = AssetDatabase.GetAssetPath(source);
            if (!sourcePath.EndsWith(
                    ".fbx",
                    StringComparison.OrdinalIgnoreCase))
                continue;

            usedModels.TryGetValue(sourcePath, out int used);
            usedModels[sourcePath] = used + 1;
        }

        result.AddMetric("NPC scene identity", identityCount);
        result.AddMetric("NPC placeholder", placeholderCount);
        result.AddMetric("NPC rendererless", rendererless);
        result.AddMetric("NPC unique VNUM", vnums.Count);

        result.Check(
            physicalFbx.Length == 22,
            $"NPC FBX envanteri tam 22 adet ({physicalFbx.Length}).");

        result.Check(
            identityCount == 31,
            $"C1 NPC placement katmanı beklenen 31 kayıt içeriyor ({identityCount}).");

        result.Check(
            placeholderCount == 0,
            "NPC placeholder kullanılmıyor.");

        result.Check(
            rendererless == 0,
            "Bütün NPC instance'larında Renderer mevcut.");

        result.Check(
            physicalFbx.Length == usedModels.Count,
            $"Her NPC FBX en az bir gerçek NPC tarafından kullanılıyor ({usedModels.Count}/{physicalFbx.Length}).");

        foreach (string absolutePath in physicalFbx)
        {
            string assetPath = ToAssetPath(absolutePath);
            usedModels.TryGetValue(assetPath, out int count);

            result.Check(
                count > 0,
                $"NPC FBX sahnede kullanılıyor: {assetPath}");
        }
    }

    private static void ValidateMapObjects(
        ValidationResult result,
        Transform mapRoot)
    {
        Transform root = mapRoot.Find("MapObjects");

        if (root == null)
        {
            result.Fail("Pyungmoo/MapObjects bulunamadı.");
            return;
        }

        int objectCount = root.GetComponentsInChildren<Transform>(true).Length - 1;
        int chunkCount = root
            .Cast<Transform>()
            .Count();

        result.AddMetric(
            "MapObjects descendants",
            Math.Max(0, objectCount));

        result.AddMetric(
            "MapObjects chunks",
            chunkCount);

        result.Check(
            chunkCount > 0,
            "MapObjects chunk root'ları mevcut.");
    }

    private static string ToAssetPath(string absolutePath)
    {
        string assetsRoot = Application.dataPath
            .Replace('\', '/')
            .TrimEnd('/');

        string normalized = absolutePath
            .Replace('\', '/');

        if (normalized.StartsWith(
                assetsRoot + "/",
                StringComparison.OrdinalIgnoreCase))
        {
            return "Assets/" +
                   normalized.Substring(
                       assetsRoot.Length + 1);
        }

        return normalized;
    }

    public static void WriteReport(ValidationResult result)
    {
        string absoluteReport = Path.Combine(
            Application.dataPath,
            ReportPath.Substring("Assets/".Length)
                .Replace('/', Path.DirectorySeparatorChar));

        Directory.CreateDirectory(
            Path.GetDirectoryName(absoluteReport));

        File.WriteAllText(
            absoluteReport,
            result.ToReportText(),
            new UTF8Encoding(false));

        AssetDatabase.Refresh();
    }

    public sealed class ValidationResult
    {
        private readonly List<string> checks = new List<string>();
        private readonly List<string> failures = new List<string>();
        private readonly List<string> metrics = new List<string>();

        public bool Passed => failures.Count == 0;

        internal void Check(bool condition, string message)
        {
            checks.Add((condition ? "PASS: " : "FAIL: ") + message);

            if (!condition)
                failures.Add(message);
        }

        internal void Fail(string message)
        {
            checks.Add("FAIL: " + message);
            failures.Add(message);
        }

        internal void AddMetric(string name, int value)
        {
            metrics.Add($"{name}: {value}");
        }

        public string ToDisplayText()
        {
            var sb = new StringBuilder();

            sb.AppendLine(Passed
                ? "Bütün entegrasyon kontrolleri geçti."
                : "En az bir entegrasyon kontrolü başarısız.");

            sb.AppendLine();

            if (metrics.Count > 0)
            {
                sb.AppendLine("Ölçümler:");
                foreach (string metric in metrics)
                    sb.AppendLine("  " + metric);

                sb.AppendLine();
            }

            if (failures.Count > 0)
            {
                sb.AppendLine("Hatalar:");
                foreach (string failure in failures)
                    sb.AppendLine("  " + failure);
            }

            return sb.ToString();
        }

        public string ToReportText()
        {
            var sb = new StringBuilder();

            sb.AppendLine("Pyungmoo Complete Integration Validation");
            sb.AppendLine(DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"));
            sb.AppendLine();
            sb.AppendLine("RESULT: " + (Passed ? "PASS" : "FAIL"));
            sb.AppendLine();

            sb.AppendLine("METRICS");
            foreach (string metric in metrics)
                sb.AppendLine(metric);

            sb.AppendLine();
            sb.AppendLine("CHECKS");
            foreach (string check in checks)
                sb.AppendLine(check);

            return sb.ToString();
        }
    }
}
