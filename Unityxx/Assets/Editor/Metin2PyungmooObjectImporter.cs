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

    // Metin2 map/object coordinates: 100 world units = 1 Unity meter.
    // The source Y axis points opposite to Unity's Z axis.
    private const float CoordinateScale = 0.01f;
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
                    "C1 map içinde areadata.txt bulunamadı:\n" + mapRootPath);

            // IMPORTANT:
            // The CRC written in AreaData is the CRC32 ObjectID of the actual
            // source object file. Do not depend on a matching .prb/.prt filename.
            string zoneRoot = FindDirectoryOrThrow(
                repoRoot,
                Path.Combine("Metin2Client", "Zone"),
                Path.Combine("Zone"));

            Dictionary<uint, SourceObject> sourceByCrc = BuildSourceObjectIndex(zoneRoot, repoRoot);

            UnityEngine.Debug.Log(
                $"Pyungmoo source object index: {sourceByCrc.Count} CRC");

            List<AreaObject> allObjects = new List<AreaObject>();
            foreach (string areaFile in areaFiles)
                allObjects.AddRange(ParseAreaData(areaFile));

            int directCrcMatches = allObjects.Count(o => sourceByCrc.ContainsKey(o.PropertyId));
            int uniqueDirectCrcMatches = allObjects
                .Where(o => sourceByCrc.ContainsKey(o.PropertyId))
                .Select(o => o.PropertyId)
                .Distinct()
                .Count();

            UnityEngine.Debug.Log(
                $"Pyungmoo CRC preflight: objects={allObjects.Count}, " +
                $"directSourceMatches={directCrcMatches}, " +
                $"uniqueMatches={uniqueDirectCrcMatches}");

            string noesisPath = FindNoesis(repoRoot);

            int autoConverted = 0;
            int existingModels = 0;
            int missingSource = 0;
            int conversionFailed = 0;

            if (!string.IsNullOrEmpty(noesisPath))
            {
                HashSet<string> neededNames = allObjects
                    .Where(o => sourceByCrc.ContainsKey(o.PropertyId))
                    .Select(o => sourceByCrc[o.PropertyId])
                    .Where(s => IsConvertible3DSource(s))
                    .Select(s => Path.GetFileNameWithoutExtension(s.Path))
                    .ToHashSet(StringComparer.OrdinalIgnoreCase);

                ConversionStats conversion = AutoConvertMissingGr2(
                    noesisPath,
                    neededNames,
                    sourceByCrc.Values,
                    repoRoot);

                autoConverted = conversion.Converted;
                existingModels = conversion.AlreadyExisting;
                missingSource = conversion.MissingSource;
                conversionFailed = conversion.Failed;
            }
            else
            {
                UnityEngine.Debug.LogWarning(
                    "Noesis.exe bulunamadı. Var olan FBX modelleri kullanılacak; " +
                    "eksik GR2'ler otomatik dönüştürülmeyecek.");
            }

            AssetDatabase.Refresh();

            Dictionary<string, GameObject> modelIndex = BuildModelIndex();

            int placed = 0;
            int noSourceMatch = 0;
            int noUnityModel = 0;
            int unsupportedSource = 0;
            int colliderCount = 0;

            var missingCrcs = new Dictionary<uint, int>();
            var missingModelNames = new Dictionary<string, int>(StringComparer.OrdinalIgnoreCase);
            var placedSources = new Dictionary<string, int>(StringComparer.OrdinalIgnoreCase);

            Transform currentChunkRoot = null;
            string currentChunkName = null;
            int chunkCount = 0;

            foreach (string areaFile in areaFiles)
            {
                string chunkName = Path.GetFileName(Path.GetDirectoryName(areaFile));
                if (!string.Equals(currentChunkName, chunkName, StringComparison.OrdinalIgnoreCase))
                {
                    currentChunkName = chunkName;
                    currentChunkRoot = new GameObject("Objects_" + chunkName).transform;
                    currentChunkRoot.SetParent(objectRoot, false);
                    chunkCount++;
                }

                foreach (AreaObject areaObject in ParseAreaData(areaFile))
                {
                    if (!sourceByCrc.TryGetValue(areaObject.PropertyId, out SourceObject source))
                    {
                        noSourceMatch++;
                        Increment(missingCrcs, areaObject.PropertyId);
                        continue;
                    }

                    if (!IsConvertible3DSource(source))
                    {
                        unsupportedSource++;
                        continue;
                    }

                    string modelName = Path.GetFileNameWithoutExtension(source.Path);

                    if (!TryFindModel(modelIndex, modelName, out GameObject model))
                    {
                        noUnityModel++;
                        Increment(missingModelNames, modelName);
                        continue;
                    }

                    GameObject instance = PrefabUtility.InstantiatePrefab(model) as GameObject;
                    if (instance == null)
                    {
                        noUnityModel++;
                        Increment(missingModelNames, modelName);
                        continue;
                    }

                    instance.name =
                        $"OBJ_{areaObject.ObjectIndex:000}_{Sanitize(modelName)}";

                    instance.transform.SetParent(currentChunkRoot, false);
                    instance.transform.position = ConvertPosition(areaObject.Position);

                    // AreaData rotations are XYZ in source coordinates.
                    // For the common C1 objects, the third value is the yaw.
                    instance.transform.rotation = ConvertRotation(areaObject.Rotation);

                    instance.isStatic = true;

                    if (AddMeshColliders(instance))
                        colliderCount++;

                    placed++;
                    Increment(placedSources, modelName);
                }
            }

            StringBuilder report = new StringBuilder();
            report.AppendLine("Pyungmoo Object Import Report");
            report.AppendLine(DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"));
            report.AppendLine();
            report.AppendLine($"Map root: {mapRootPath}");
            report.AppendLine($"AreaData files: {areaFiles.Count}");
            report.AppendLine($"Chunk sayısı: {chunkCount}");
            report.AppendLine($"AreaData objesi: {allObjects.Count}");
            report.AppendLine($"Direct CRC -> source eşleşmesi: {directCrcMatches}");
            report.AppendLine($"Direct CRC unique eşleşmesi: {uniqueDirectCrcMatches}");
            report.AppendLine($"Yerleştirilen: {placed}");
            report.AppendLine($"Eksik source CRC: {noSourceMatch}");
            report.AppendLine($"Unity model eksik: {noUnityModel}");
            report.AppendLine($"Desteklenmeyen source türü: {unsupportedSource}");
            report.AppendLine($"Yeni FBX: {autoConverted}");
            report.AppendLine($"Zaten mevcut model: {existingModels}");
            report.AppendLine($"Kaynak bulunamadı: {missingSource}");
            report.AppendLine($"Noesis dönüşüm hatası: {conversionFailed}");
            report.AppendLine($"Eklenen MeshCollider: {colliderCount}");
            report.AppendLine($"Noesis: {(string.IsNullOrEmpty(noesisPath) ? "bulunamadı" : noesisPath)}");
            report.AppendLine();
            report.AppendLine("Noesis parametresi: -rotate 90 0 0");
            report.AppendLine("CRC yöntemi: source object dosyasının byte içeriklerinden CRC32.");
            report.AppendLine();

            if (placedSources.Count > 0)
            {
                report.AppendLine("Yerleştirilen model adları:");
                foreach (var item in placedSources.OrderByDescending(x => x.Value))
                    report.AppendLine($"  {item.Key} x{item.Value}");
                report.AppendLine();
            }

            if (missingModelNames.Count > 0)
            {
                report.AppendLine("Unity'de bulunamayan model adları:");
                foreach (var item in missingModelNames.OrderByDescending(x => x.Value))
                    report.AppendLine($"  {item.Key} x{item.Value}");
                report.AppendLine();
            }

            if (missingCrcs.Count > 0)
            {
                report.AppendLine("Kaynak dosyada bulunamayan CRC'ler:");
                foreach (var item in missingCrcs.OrderByDescending(x => x.Value))
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
                $"AreaData objesi: {allObjects.Count}\n" +
                $"CRC -> source: {directCrcMatches}\n" +
                $"Yerleştirilen: {placed}\n" +
                $"Eksik source: {noSourceMatch}\n" +
                $"Eksik Unity model: {noUnityModel}\n" +
                $"Yeni FBX: {autoConverted}\n" +
                $"Noesis hata: {conversionFailed}\n\n" +
                $"Detay raporu:\n{ReportPath}",
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

    private static Scene OpenPyungmooScene()
    {
        // Unity tarafında proje içindeki Assets yolunu doğrudan kullan.
        // Fiziksel dosya yolu üretmek yerine AssetDatabase kontrolü yapıyoruz;
        // böylece repo/project klasör derinliği değişse bile sahne bulunur.
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
        string projectRoot = Directory.GetParent(Application.dataPath).FullName;
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

        string parent = Directory.GetParent(repoRoot)?.FullName;
        if (!string.IsNullOrEmpty(parent))
        {
            foreach (string relative in candidates)
            {
                string leaf = Path.GetFileName(
                    relative.TrimEnd(
                        Path.DirectorySeparatorChar,
                        Path.AltDirectorySeparatorChar));

                try
                {
                    string found = Directory
                        .EnumerateDirectories(
                            parent,
                            leaf,
                            SearchOption.AllDirectories)
                        .FirstOrDefault();

                    if (!string.IsNullOrEmpty(found))
                        return found;
                }
                catch
                {
                    // Explicit candidates were already tested.
                }
            }
        }

        throw new DirectoryNotFoundException(
            "Klasör bulunamadı: " +
            string.Join(" | ", candidates));
    }

    private static List<string> DiscoverAreaFiles(string mapRoot)
    {
        return Directory
            .EnumerateFiles(
                mapRoot,
                "areadata.txt",
                SearchOption.AllDirectories)
            .Where(IsSixDigitChunkParent)
            .OrderBy(
                p => Path.GetFileName(Path.GetDirectoryName(p)),
                StringComparer.Ordinal)
            .ToList();
    }

    private static bool IsSixDigitChunkParent(string areaFile)
    {
        string name = Path.GetFileName(Path.GetDirectoryName(areaFile));
        return Regex.IsMatch(name ?? string.Empty, @"^\d{6}$");
    }

    private static Dictionary<uint, SourceObject> BuildSourceObjectIndex(
        string zoneRoot,
        string repoRoot)
    {
        var result = new Dictionary<uint, SourceObject>();

        foreach (string file in EnumerateObjectSourceFiles(zoneRoot, repoRoot))
        {
            string ext = Path.GetExtension(file);

            // Only formats that can represent a map object or tree model are
            // indexed here. Effects/ambience are not forced into FBX.
            if (!ext.Equals(".gr2", StringComparison.OrdinalIgnoreCase) &&
                !ext.Equals(".spt", StringComparison.OrdinalIgnoreCase))
                continue;

            try
            {
                uint crc = ComputeCrc32(file);

                if (!result.ContainsKey(crc))
                {
                    result.Add(
                        crc,
                        new SourceObject
                        {
                            Crc = crc,
                            Path = file
                        });
                }
            }
            catch (Exception ex)
            {
                UnityEngine.Debug.LogWarning(
                    $"CRC okunamadı: {file}\n{ex.Message}");
            }
        }

        return result;
    }

    private static IEnumerable<string> EnumerateObjectSourceFiles(
        string zoneRoot,
        string repoRoot)
    {
        var seen = new HashSet<string>(StringComparer.OrdinalIgnoreCase);

        foreach (string pattern in new[] { "*.gr2", "*.spt" })
        {
            foreach (string file in Directory.EnumerateFiles(
                zoneRoot,
                pattern,
                SearchOption.AllDirectories))
            {
                if (seen.Add(Path.GetFullPath(file)))
                    yield return file;
            }
        }

        // Fallback for unusual unpack layouts.
        foreach (string pattern in new[] { "*.gr2", "*.spt" })
        {
            foreach (string file in Directory.EnumerateFiles(
                repoRoot,
                pattern,
                SearchOption.AllDirectories))
            {
                string normalized = file.Replace('\\', '/');

                if (normalized.IndexOf(
                        "/Unityxx/",
                        StringComparison.OrdinalIgnoreCase) >= 0)
                    continue;

                if (seen.Add(Path.GetFullPath(file)))
                    yield return file;
            }
        }
    }

    private static ConversionStats AutoConvertMissingGr2(
        string noesisPath,
        HashSet<string> neededNames,
        IEnumerable<SourceObject> sourceObjects,
        string repoRoot)
    {
        string projectRoot =
            Directory.GetParent(Application.dataPath).FullName;

        string outputRoot = Path.Combine(
            projectRoot,
            AutoModelFolder
                .Substring("Assets/".Length)
                .Replace('/', Path.DirectorySeparatorChar));

        Directory.CreateDirectory(outputRoot);

        Dictionary<string, SourceObject> sourceByName =
            new Dictionary<string, SourceObject>(
                StringComparer.OrdinalIgnoreCase);

        foreach (SourceObject source in sourceObjects)
        {
            if (!source.Path.EndsWith(
                    ".gr2",
                    StringComparison.OrdinalIgnoreCase))
                continue;

            string name = Path.GetFileNameWithoutExtension(source.Path);

            if (!sourceByName.ContainsKey(name))
                sourceByName.Add(name, source);
        }

        HashSet<string> existingModels =
            AssetDatabase.FindAssets("t:Model")
                .Select(AssetDatabase.GUIDToAssetPath)
                .Select(Path.GetFileNameWithoutExtension)
                .Where(n => !string.IsNullOrWhiteSpace(n))
                .ToHashSet(StringComparer.OrdinalIgnoreCase);

        int converted = 0;
        int alreadyExisting = 0;
        int missingSource = 0;
        int failed = 0;

        foreach (string modelName in neededNames.OrderBy(
                     x => x,
                     StringComparer.OrdinalIgnoreCase))
        {
            if (existingModels.Contains(modelName) ||
                existingModels.Contains(modelName + "out"))
            {
                alreadyExisting++;
                continue;
            }

            if (!sourceByName.TryGetValue(
                    modelName,
                    out SourceObject source))
            {
                missingSource++;
                continue;
            }

            string outputFbx = Path.Combine(
                outputRoot,
                modelName + ".fbx");

            if (File.Exists(outputFbx))
            {
                converted++;
                continue;
            }

            try
            {
                // Required orientation correction:
                // -rotate 90 0 0
                string arguments =
                    $"?cmode \"{source.Path}\" \"{outputFbx}\" " +
                    "-fbxmeshmerge -rotate 90 0 0";

                UnityEngine.Debug.Log(
                    $"Noesis GR2 -> FBX: {modelName}\n" +
                    $"Source: {source.Path}\n" +
                    $"Args: {arguments}");

                using (Process process = new Process())
                {
                    process.StartInfo = new ProcessStartInfo
                    {
                        FileName = noesisPath,
                        Arguments = arguments,
                        WorkingDirectory = Path.GetDirectoryName(noesisPath),
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

                        failed++;
                        UnityEngine.Debug.LogWarning(
                            $"Noesis timeout: {modelName}");
                        continue;
                    }

                    string stdout = process.StandardOutput.ReadToEnd();
                    string stderr = process.StandardError.ReadToEnd();

                    if (process.ExitCode != 0 ||
                        !File.Exists(outputFbx))
                    {
                        failed++;

                        UnityEngine.Debug.LogWarning(
                            $"Noesis başarısız: {modelName}\n" +
                            $"ExitCode: {process.ExitCode}\n" +
                            $"STDOUT:\n{stdout}\n" +
                            $"STDERR:\n{stderr}");

                        continue;
                    }
                }

                converted++;

                EditorUtility.DisplayProgressBar(
                    "Pyungmoo GR2 -> FBX",
                    modelName,
                    converted /
                    (float)Math.Max(1, neededNames.Count));
            }
            catch (Exception ex)
            {
                failed++;

                UnityEngine.Debug.LogWarning(
                    $"GR2 -> FBX exception: {modelName}\n{ex.Message}");
            }
        }

        EditorUtility.ClearProgressBar();

        UnityEngine.Debug.Log(
            $"Pyungmoo auto-conversion: " +
            $"new={converted}, existing={alreadyExisting}, " +
            $"source-missing={missingSource}, failed={failed}");

        return new ConversionStats
        {
            Converted = converted,
            AlreadyExisting = alreadyExisting,
            MissingSource = missingSource,
            Failed = failed
        };
    }

    private static bool IsConvertible3DSource(SourceObject source)
    {
        return source.Path.EndsWith(
                   ".gr2",
                   StringComparison.OrdinalIgnoreCase) ||
               source.Path.EndsWith(
                   ".spt",
                   StringComparison.OrdinalIgnoreCase);
    }

    private static Dictionary<string, GameObject> BuildModelIndex()
    {
        var result =
            new Dictionary<string, GameObject>(
                StringComparer.OrdinalIgnoreCase);

        foreach (string guid in AssetDatabase.FindAssets("t:Model"))
        {
            string path = AssetDatabase.GUIDToAssetPath(guid);

            GameObject model =
                AssetDatabase.LoadAssetAtPath<GameObject>(path);

            if (model == null)
                continue;

            string name =
                Path.GetFileNameWithoutExtension(path);

            if (string.IsNullOrWhiteSpace(name))
                continue;

            if (!result.ContainsKey(
                    NormalizeKey(name)))
            {
                result.Add(
                    NormalizeKey(name),
                    model);
            }
        }

        UnityEngine.Debug.Log(
            $"Unity model index: {result.Count} model");

        return result;
    }

    private static bool TryFindModel(
        Dictionary<string, GameObject> index,
        string sourceModelName,
        out GameObject model)
    {
        string key = NormalizeKey(sourceModelName);

        if (index.TryGetValue(key, out model))
            return true;

        string outKey =
            NormalizeKey(sourceModelName + "out");

        if (index.TryGetValue(outKey, out model))
            return true;

        model = null;
        return false;
    }

    private static List<AreaObject> ParseAreaData(string file)
    {
        var result = new List<AreaObject>();
        string[] lines = File.ReadAllLines(file);

        for (int i = 0; i < lines.Length; i++)
        {
            if (!lines[i].Trim().StartsWith(
                    "Start Object",
                    StringComparison.OrdinalIgnoreCase))
                continue;

            Match objectMatch =
                Regex.Match(
                    lines[i].Trim(),
                    @"Start Object(\d+)",
                    RegexOptions.IgnoreCase |
                    RegexOptions.CultureInvariant);

            int objectIndex = result.Count;

            if (objectMatch.Success)
                int.TryParse(
                    objectMatch.Groups[1].Value,
                    NumberStyles.Integer,
                    CultureInfo.InvariantCulture,
                    out objectIndex);

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
                continue;

            if (!TryParseVector3(data[0], out Vector3 position))
                continue;

            if (!uint.TryParse(
                    data[1],
                    NumberStyles.Integer,
                    CultureInfo.InvariantCulture,
                    out uint propertyId))
            {
                continue;
            }

            if (!TryParseVector3(
                    data[2].Replace('#', ' '),
                    out Vector3 rotation))
            {
                rotation = Vector3.zero;
            }

            float offset = 0.0f;

            float.TryParse(
                data[3],
                NumberStyles.Float,
                CultureInfo.InvariantCulture,
                out offset);

            result.Add(
                new AreaObject
                {
                    ObjectIndex = objectIndex,
                    PropertyId = propertyId,
                    Position = position,
                    Rotation = rotation,
                    HeightOffset = offset
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

    private static Vector3 ConvertPosition(Vector3 source)
    {
        return new Vector3(
            source.x * CoordinateScale,
            source.z * CoordinateScale,
            -source.y * CoordinateScale);
    }

    private static Quaternion ConvertRotation(Vector3 source)
    {
        // AreaData is Z-up; Unity is Y-up.
        Quaternion sourceBasis =
            Quaternion.Euler(-90.0f, 0.0f, 0.0f);

        Quaternion sourceRotation =
            Quaternion.Euler(
                source.x,
                source.y,
                source.z);

        return sourceBasis *
               sourceRotation *
               Quaternion.Inverse(sourceBasis);
    }

    private static bool AddMeshColliders(GameObject root)
    {
        int added = 0;

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
            collider.convex = false;
            added++;
        }

        return added > 0;
    }

    private static uint ComputeCrc32(string file)
    {
        const uint polynomial = 0xEDB88320u;
        uint crc = 0xFFFFFFFFu;

        using (FileStream stream =
               new FileStream(
                   file,
                   FileMode.Open,
                   FileAccess.Read,
                   FileShare.Read))
        {
            byte[] buffer = new byte[1024 * 1024];
            int read;

            while ((read = stream.Read(buffer, 0, buffer.Length)) > 0)
            {
                for (int i = 0; i < read; i++)
                {
                    crc ^= buffer[i];

                    for (int bit = 0; bit < 8; bit++)
                    {
                        if ((crc & 1u) != 0)
                            crc = (crc >> 1) ^ polynomial;
                        else
                            crc >>= 1;
                    }
                }
            }
        }

        return crc ^ 0xFFFFFFFFu;
    }

    private static string FindNoesis(string repoRoot)
    {
        string userProfile =
            Environment.GetFolderPath(
                Environment.SpecialFolder.UserProfile);

        string oneDrive =
            Environment.GetEnvironmentVariable("OneDrive");

        var candidates = new List<string>
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

        string workspaceParent =
            Directory.GetParent(repoRoot)?.FullName;

        if (!string.IsNullOrEmpty(workspaceParent))
        {
            try
            {
                string found =
                    Directory.EnumerateFiles(
                        workspaceParent,
                        "Noesis.exe",
                        SearchOption.AllDirectories)
                    .FirstOrDefault();

                if (!string.IsNullOrEmpty(found))
                    return found;
            }
            catch (Exception ex)
            {
                UnityEngine.Debug.LogWarning(
                    "Noesis araması başarısız: " + ex.Message);
            }
        }

        return null;
    }

    private static void DeleteExistingObjectRoot(GameObject mapRoot)
    {
        Transform oldRoot =
            mapRoot.transform.Find(ObjectRootName);

        if (oldRoot != null)
            UnityEngine.Object.DestroyImmediate(
                oldRoot.gameObject);
    }

    private static void WriteReport(string text)
    {
        string projectRoot =
            Directory.GetParent(Application.dataPath).FullName;

        string absolute =
            Path.Combine(
                projectRoot,
                ReportPath.Substring("Assets/".Length)
                    .Replace('/', Path.DirectorySeparatorChar));

        string directory =
            Path.GetDirectoryName(absolute);

        if (!string.IsNullOrEmpty(directory))
            Directory.CreateDirectory(directory);

        File.WriteAllText(
            absolute,
            text,
            new UTF8Encoding(false));

        AssetDatabase.ImportAsset(
            ReportPath,
            ImportAssetOptions.ForceUpdate);
    }

    private static string NormalizeKey(string value)
    {
        return (value ?? string.Empty)
            .Trim()
            .Replace('\\', '/')
            .Split('/')
            .Last()
            .ToLowerInvariant();
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

    private static string Sanitize(string value)
    {
        if (string.IsNullOrWhiteSpace(value))
            return "Object";

        foreach (char c in Path.GetInvalidFileNameChars())
            value = value.Replace(c, '_');

        return value.Replace(' ', '_');
    }

    private sealed class AreaObject
    {
        public int ObjectIndex;
        public uint PropertyId;
        public Vector3 Position;
        public Vector3 Rotation;
        public float HeightOffset;
    }

    private sealed class SourceObject
    {
        public uint Crc;
        public string Path;
    }

    private sealed class ConversionStats
    {
        public int Converted;
        public int AlreadyExisting;
        public int MissingSource;
        public int Failed;
    }
}
