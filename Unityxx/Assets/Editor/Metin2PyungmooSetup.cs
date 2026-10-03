using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;

/// <summary>
/// Pyungmoo için tek tuşluk kurulum:
///   Arazi (yoksa) + harita objeleri/ağaçlar + FINAL binalar + FINAL NPC'ler.
///
/// Ayrıca Noesis yolunu yönetir. Noesis, Türkçe karakter içeren klasörlerde
/// (örn. "Masaüstü") Python modülünü başlatamıyor; bu yüzden Noesis klasörü
/// ASCII-only bir yola kopyalanıp oradan çalıştırılır.
/// </summary>
[InitializeOnLoad]
public static class Metin2PyungmooSetup
{
    public const string DefaultNoesisPath =
        @"C:\Users\roxy\OneDrive\Masaüstü\shared_3d_exporting\noesis\noesis\Noesis.exe";

    private const string ScenePath = "Assets/Scenes/Pyungmoo.unity";
    private const string PlaceholderFolder = "Assets/Metin2Generated/Pyungmoo/Placeholders";
    private const string MenuRoot = "Metin2/Pyungmoo/";
    private const string TogglePlaceholderMenu = MenuRoot + "Toggle Placeholder Trees";

    private const string NoesisPrefKey = "SAGLAMKAFA.NoesisPath";
    private const string PlaceholderPrefKey = "SAGLAMKAFA.PlaceholderTrees";
    private const string AutoPromptDisabledKey = "SAGLAMKAFA.AutoPromptDisabled";
    private const string AutoPromptSessionKey = "SAGLAMKAFA.AutoPromptShown";

    private const int VillageGuardVnum = 20355;

    static Metin2PyungmooSetup()
    {
        EditorApplication.delayCall += MaybePromptOnLoad;
    }

    // ------------------------------------------------------------------
    // Ayarlar
    // ------------------------------------------------------------------

    public static bool UsePlaceholderTrees
    {
        get { return EditorPrefs.GetBool(PlaceholderPrefKey, true); }
        set { EditorPrefs.SetBool(PlaceholderPrefKey, value); }
    }

    /// <summary>shared_3d_exporting klasörü (Noesis yolundan türetilir).</summary>
    public static string SharedExportingDir
    {
        get
        {
            try
            {
                string exe = EditorPrefs.GetString(NoesisPrefKey, DefaultNoesisPath);
                // ...\shared_3d_exporting\noesis\noesis\Noesis.exe
                string dir = Path.GetDirectoryName(exe);               // ...\noesis\noesis
                dir = string.IsNullOrEmpty(dir) ? null : Path.GetDirectoryName(dir);   // ...\noesis
                dir = string.IsNullOrEmpty(dir) ? null : Path.GetDirectoryName(dir);   // ...\shared_3d_exporting
                if (!string.IsNullOrEmpty(dir))
                    return dir;
            }
            catch
            {
            }

            return Path.GetDirectoryName(DefaultNoesisPath);
        }
    }

    [MenuItem(MenuRoot + "Set Noesis Path...", priority = 1)]
    public static void SetNoesisPathMenu()
    {
        string current = EditorPrefs.GetString(NoesisPrefKey, DefaultNoesisPath);
        string startDir = string.Empty;

        try
        {
            string dir = Path.GetDirectoryName(current);
            if (!string.IsNullOrEmpty(dir) && Directory.Exists(dir))
                startDir = dir;
        }
        catch
        {
        }

        string picked = EditorUtility.OpenFilePanel("Noesis.exe seç", startDir, "exe");
        if (string.IsNullOrEmpty(picked))
            return;

        EditorPrefs.SetString(NoesisPrefKey, picked.Replace('/', Path.DirectorySeparatorChar));
        Debug.Log("Pyungmoo: Noesis yolu ayarlandı: " + picked);
    }

    [MenuItem(TogglePlaceholderMenu, priority = 2)]
    public static void TogglePlaceholderTreesMenu()
    {
        UsePlaceholderTrees = !UsePlaceholderTrees;
    }

    [MenuItem(TogglePlaceholderMenu, true)]
    private static bool TogglePlaceholderTreesValidate()
    {
        Menu.SetChecked(TogglePlaceholderMenu, UsePlaceholderTrees);
        return true;
    }

    // ------------------------------------------------------------------
    // Noesis
    // ------------------------------------------------------------------

    /// <summary>
    /// Noesis.exe'yi bulur. Yol Türkçe/ASCII-dışı karakter içeriyorsa tüm Noesis
    /// klasörünü ASCII-only bir konuma kopyalar ve oradaki exe'yi döndürür.
    /// Bulunamazsa null.
    /// </summary>
    public static string PrepareNoesis()
    {
        string exe = ResolveNoesisExe();
        if (string.IsNullOrEmpty(exe))
            return null;

        if (IsAscii(exe))
            return exe;

        try
        {
            string sourceDir = Path.GetDirectoryName(exe);
            string mirrorDir = Path.Combine(PickAsciiMirrorRoot(), "SAGLAMKAFA_NoesisTool");
            string mirrorExe = Path.Combine(mirrorDir, Path.GetFileName(exe));
            string markerPath = Path.Combine(mirrorDir, ".mirror_stamp");

            var exeInfo = new FileInfo(exe);
            string stamp = exeInfo.Length + "|" + exeInfo.LastWriteTimeUtc.Ticks;

            bool upToDate =
                File.Exists(mirrorExe) &&
                File.Exists(markerPath) &&
                File.ReadAllText(markerPath) == stamp;

            if (!upToDate)
            {
                Debug.Log(
                    "Pyungmoo: Noesis ASCII-only yola kopyalanıyor (Python modülü " +
                    "Türkçe karakterli yolda başlatılamıyor):\n" +
                    sourceDir + "\n -> " + mirrorDir);

                CopyDirectory(sourceDir, mirrorDir);
                File.WriteAllText(markerPath, stamp);
            }

            return mirrorExe;
        }
        catch (Exception ex)
        {
            Debug.LogWarning(
                "Pyungmoo: Noesis ASCII kopyası oluşturulamadı, orijinal yol " +
                "kullanılacak (Python modülü başlatılamayabilir):\n" + ex.Message);
            return exe;
        }
    }

    private static string ResolveNoesisExe()
    {
        var candidates = new List<string>
        {
            EditorPrefs.GetString(NoesisPrefKey, string.Empty),
            DefaultNoesisPath
        };

        string projectRoot = Directory.GetParent(Application.dataPath).FullName;
        string repoRoot = Directory.GetParent(projectRoot).FullName;
        string[] tail = { "shared_3d_exporting", "noesis", "noesis", "Noesis.exe" };

        candidates.Add(Path.Combine(new[] { repoRoot }.Concat(tail).ToArray()));
        candidates.Add(Path.Combine(
            new[] { Directory.GetParent(repoRoot)?.FullName ?? repoRoot }.Concat(tail).ToArray()));

        string oneDrive = Environment.GetEnvironmentVariable("OneDrive");
        if (!string.IsNullOrEmpty(oneDrive))
        {
            candidates.Add(Path.Combine(new[] { oneDrive, "Masaüstü" }.Concat(tail).ToArray()));
            candidates.Add(Path.Combine(new[] { oneDrive, "Desktop" }.Concat(tail).ToArray()));
        }

        foreach (string candidate in candidates)
        {
            if (!string.IsNullOrWhiteSpace(candidate) && File.Exists(candidate))
                return candidate;
        }

        return null;
    }

    private static string PickAsciiMirrorRoot()
    {
        string[] roots =
        {
            Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
            Path.GetTempPath(),
            @"C:\"
        };

        foreach (string root in roots)
        {
            if (!string.IsNullOrEmpty(root) && IsAscii(root))
                return root;
        }

        return @"C:\";
    }

    private static bool IsAscii(string value)
    {
        foreach (char c in value)
        {
            if (c > 127)
                return false;
        }

        return true;
    }

    private static void CopyDirectory(string source, string destination)
    {
        Directory.CreateDirectory(destination);

        foreach (string file in Directory.GetFiles(source))
        {
            string target = Path.Combine(destination, Path.GetFileName(file));
            File.Copy(file, target, true);
        }

        foreach (string dir in Directory.GetDirectories(source))
        {
            CopyDirectory(dir, Path.Combine(destination, Path.GetFileName(dir)));
        }
    }

    // ------------------------------------------------------------------
    // Geçici ağaç (SPT -> FBX dönüşümü olmayan ağaçlar için)
    // ------------------------------------------------------------------

    public static GameObject CreateTreePlaceholder(string modelName)
    {
        Material trunkMaterial = GetPlaceholderMaterial("TreeTrunk", new Color(0.36f, 0.24f, 0.13f));
        Material crownMaterial = GetPlaceholderMaterial("TreeCrown", new Color(0.18f, 0.45f, 0.16f));

        if (trunkMaterial == null || crownMaterial == null)
            return null;

        // Aynı model adı her zaman aynı boyu versin (0.8x - 1.4x).
        uint hash = 2166136261u;
        foreach (char c in modelName ?? string.Empty)
            hash = unchecked((hash ^ c) * 16777619u);
        float variation = 0.8f + (hash % 600u) / 1000.0f;

        var root = new GameObject("TreePlaceholder");

        GameObject trunk = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
        trunk.name = "Trunk";
        trunk.transform.SetParent(root.transform, false);
        trunk.transform.localScale = new Vector3(0.8f, 3.0f * variation, 0.8f);
        trunk.transform.localPosition = new Vector3(0.0f, 3.0f * variation, 0.0f);
        trunk.GetComponent<Renderer>().sharedMaterial = trunkMaterial;

        GameObject crown = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        crown.name = "Crown";
        crown.transform.SetParent(root.transform, false);
        crown.transform.localScale = new Vector3(6.0f, 6.0f, 6.0f) * variation;
        crown.transform.localPosition = new Vector3(0.0f, 7.5f * variation, 0.0f);
        crown.GetComponent<Renderer>().sharedMaterial = crownMaterial;

        Collider crownCollider = crown.GetComponent<Collider>();
        if (crownCollider != null)
            UnityEngine.Object.DestroyImmediate(crownCollider);

        return root;
    }

    private static Material GetPlaceholderMaterial(string name, Color color)
    {
        string path = PlaceholderFolder + "/" + name + ".mat";

        Material existing = AssetDatabase.LoadAssetAtPath<Material>(path);
        if (existing != null)
            return existing;

        if (!AssetDatabase.IsValidFolder(PlaceholderFolder))
            AssetDatabase.CreateFolder("Assets/Metin2Generated/Pyungmoo", "Placeholders");

        Shader shader =
            Shader.Find("Universal Render Pipeline/Lit") ??
            Shader.Find("Standard");

        if (shader == null)
            return null;

        var material = new Material(shader) { name = name, color = color };
        if (material.HasProperty("_BaseColor"))
            material.SetColor("_BaseColor", color);
        if (material.HasProperty("_Smoothness"))
            material.SetFloat("_Smoothness", 0.0f);

        AssetDatabase.CreateAsset(material, path);
        return material;
    }

    // ------------------------------------------------------------------
    // Tek tuşluk tam kurulum
    // ------------------------------------------------------------------

    [MenuItem(MenuRoot + "0 - BUILD EVERYTHING (Map + Trees + Buildings + NPCs)", priority = 0)]
    public static void BuildEverythingMenu()
    {
        RunBuildEverything(true);
    }

    public static void RunBuildEverything(bool interactive)
    {
        try
        {
            if (!EditorSceneManager.SaveCurrentModifiedScenesIfUserWantsTo())
                return;

            EditorUtility.DisplayProgressBar("Pyungmoo", "1/4 Arazi kontrol ediliyor...", 0.05f);

            if (!SceneHasTerrain())
            {
                // Terrain importer kendi diyaloğunu gösterir.
                Metin2PyungmooImporter.ImportPyungmoo();

                if (!SceneHasTerrain())
                    throw new InvalidOperationException(
                        "Arazi oluşturulamadı. Console'daki hata mesajına bak.");
            }

            EditorUtility.DisplayProgressBar(
                "Pyungmoo",
                "2/4 Objeler/ağaçlar (Noesis dönüşümü uzun sürebilir)...",
                0.25f);
            Metin2PyungmooObjectImporter.ImportMapObjectsAuto(false);

            EditorUtility.DisplayProgressBar("Pyungmoo", "3/4 Binalar + NPC'ler + doğrulama...", 0.7f);
            string finalResult = Metin2PyungmooFinalImporter.RunPipeline();

            EditorUtility.DisplayProgressBar("Pyungmoo", "4/4 Oyuncu köye taşınıyor...", 0.95f);
            PlacePlayerAtVillage();

            Scene scene = SceneManager.GetActiveScene();
            EditorSceneManager.MarkSceneDirty(scene);
            EditorSceneManager.SaveScene(scene, ScenePath);
            AssetDatabase.SaveAssets();

            EditorUtility.ClearProgressBar();

            CountMapObjects(out int realObjects, out int placeholderTrees);

            string summary =
                "HARİTA + OBJELER + BİNALAR + NPC'LER HAZIR\n\n" +
                finalResult + "\n\n" +
                "Harita objesi (gerçek model): " + realObjects + "\n" +
                "Geçici ağaç (placeholder): " + placeholderTrees + "\n\n" +
                "Play'e basınca oyuncu köy meydanındaki gardiyanın yanında başlar.";

            Debug.Log("Pyungmoo BUILD EVERYTHING:\n" + summary);

            if (interactive)
                EditorUtility.DisplayDialog("Pyungmoo hazır", summary, "Tamam");
        }
        catch (Exception ex)
        {
            EditorUtility.ClearProgressBar();
            Debug.LogException(ex);

            if (interactive)
                EditorUtility.DisplayDialog("Pyungmoo kurulum hatası", ex.Message, "Tamam");
            else
                throw;
        }
    }

    private static bool SceneHasTerrain()
    {
        if (AssetDatabase.LoadAssetAtPath<SceneAsset>(ScenePath) == null)
            return false;

        Scene scene = SceneManager.GetActiveScene();
        if (!string.Equals(scene.path, ScenePath, StringComparison.OrdinalIgnoreCase))
            scene = EditorSceneManager.OpenScene(ScenePath, OpenSceneMode.Single);

        GameObject mapRoot = GameObject.Find("Pyungmoo");
        if (mapRoot == null)
            return false;

        Transform terrain = mapRoot.transform.Find("Terrain");
        return terrain != null && terrain.childCount > 0;
    }

    private static void CountMapObjects(out int realObjects, out int placeholderTrees)
    {
        realObjects = 0;
        placeholderTrees = 0;

        GameObject mapRoot = GameObject.Find("Pyungmoo");
        Transform objects = mapRoot != null ? mapRoot.transform.Find("MapObjects") : null;
        if (objects == null)
            return;

        foreach (Transform chunk in objects)
        {
            foreach (Transform child in chunk)
            {
                if (child.name.StartsWith("TREE_PLACEHOLDER_", StringComparison.Ordinal))
                    placeholderTrees++;
                else
                    realObjects++;
            }
        }
    }

    private static void PlacePlayerAtVillage()
    {
        GameObject player = GameObject.Find("TemporaryPlayer");
        if (player == null)
            return;

        Metin2NpcIdentity[] npcs =
            UnityEngine.Object.FindObjectsByType<Metin2NpcIdentity>(FindObjectsSortMode.None);

        if (npcs.Length == 0)
            return;

        Metin2NpcIdentity guard =
            npcs.FirstOrDefault(n => n.Vnum == VillageGuardVnum) ?? npcs[0];

        Vector3 guardPosition = guard.transform.position;
        Vector3 spawn = guardPosition + new Vector3(0.0f, 0.0f, -10.0f);

        Physics.SyncTransforms();

        RaycastHit[] hits = Physics.RaycastAll(
            new Vector3(spawn.x, 5000.0f, spawn.z),
            Vector3.down,
            10000.0f);

        // Çatıya değil, araziye oturt.
        RaycastHit? terrainHit = hits
            .Where(h => h.collider != null &&
                        h.collider.name.StartsWith("Chunk_", StringComparison.Ordinal))
            .OrderByDescending(h => h.point.y)
            .Select(h => (RaycastHit?)h)
            .FirstOrDefault();

        spawn.y = terrainHit.HasValue
            ? terrainHit.Value.point.y + 1.2f
            : guardPosition.y + 2.0f;

        player.transform.position = spawn;

        Vector3 look = guardPosition - spawn;
        look.y = 0.0f;
        if (look.sqrMagnitude > 0.001f)
            player.transform.rotation = Quaternion.LookRotation(look.normalized, Vector3.up);

        SceneView view = SceneView.lastActiveSceneView;
        if (view != null)
            view.LookAt(guardPosition, Quaternion.Euler(25.0f, 0.0f, 0.0f), 40.0f);

        Selection.activeGameObject = guard.gameObject;
    }

    // ------------------------------------------------------------------
    // Proje açılınca: sahne boşsa kurulum öner
    // ------------------------------------------------------------------

    private static void MaybePromptOnLoad()
    {
        if (Application.isBatchMode || EditorApplication.isPlayingOrWillChangePlaymode)
            return;

        if (SessionState.GetBool(AutoPromptSessionKey, false))
            return;

        SessionState.SetBool(AutoPromptSessionKey, true);

        if (EditorPrefs.GetBool(AutoPromptDisabledKey, false))
            return;

        if (!SceneNeedsBuild())
            return;

        int choice = EditorUtility.DisplayDialogComplex(
            "Pyungmoo henüz tam kurulmamış",
            "Sahnede binalar / NPC'ler / harita objeleri yok.\n\n" +
            "Şimdi arazi + ağaçlar + binalar + NPC'leri tek seferde kurayım mı?\n" +
            "(Menüden her zaman: Metin2 > Pyungmoo > 0 - BUILD EVERYTHING)",
            "Şimdi kur",
            "Daha sonra",
            "Bir daha sorma");

        if (choice == 0)
            RunBuildEverything(true);
        else if (choice == 2)
            EditorPrefs.SetBool(AutoPromptDisabledKey, true);
    }

    private static bool SceneNeedsBuild()
    {
        try
        {
            string clientRoot = Path.Combine(
                Directory.GetParent(Directory.GetParent(Application.dataPath).FullName).FullName,
                "Metin2Client");

            // Kaynak veri yoksa kurulum önermenin anlamı yok.
            if (!Directory.Exists(clientRoot))
                return false;

            string sceneFile = Path.Combine(Application.dataPath, "Scenes", "Pyungmoo.unity");
            if (!File.Exists(sceneFile))
                return true;

            string text = File.ReadAllText(sceneFile);
            return !text.Contains("m_Name: FINAL_NPCs") ||
                   !text.Contains("m_Name: FINAL_Buildings");
        }
        catch
        {
            return false;
        }
    }
}
