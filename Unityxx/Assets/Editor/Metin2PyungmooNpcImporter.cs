using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;

public static class Metin2PyungmooNpcImporter
{
    private const string ScenePath = "Assets/Scenes/Pyungmoo.unity";
    private const string NpcRootName = "NPCs";

    // Keep the same coordinate scale as the verified terrain importer.
    private const float MapCoordinateScaleMeters = 2.0f;
    private const float RayStartHeight = 5000.0f;
    private const float GroundOffset = 0.05f;
    private const string ImportedNpcFolder = "Assets/Metin2Imported/NPC";

    private static readonly NpcPlacement[] Placements =
    {
        // Skill teachers: placement is verified from the C1 npc.txt source.
        // root/npclist.txt maps 20340-20349 to the existing
        // jinno_patrol_spear client resource, so no additional GR2 conversion
        // is required for these NPCs at this stage.
        new(20340, "Bedensel Savaş Öğretmeni", "jinno_patrol_spear", 444, 623, 7),
        new(20341, "Zihinsel Savaş Öğretmeni", "jinno_patrol_spear", 444, 627, 7),
        new(20342, "Yakın Dövüş Öğretmeni", "jinno_patrol_spear", 444, 631, 7),
        new(20343, "Uzak Dövüş Öğretmeni", "jinno_patrol_spear", 444, 635, 7),
        new(20344, "Büyülü Silah Öğretmeni", "jinno_patrol_spear", 443, 644, 7),
        new(20345, "Kara Büyü Öğretmeni", "jinno_patrol_spear", 443, 648, 7),
        new(20346, "İyileştirme Öğretmeni", "jinno_patrol_spear", 443, 652, 7),
        new(20347, "Ejderha Gücü Öğretmeni", "jinno_patrol_spear", 443, 656, 7),

        // Village service NPCs.
        new(9001, "Silahçı", "arms", 430, 607, 8),
        new(9002, "Zırhçı", "defence", 403, 586, 1),
        new(9003, "Bakkal", "goods", 383, 693, 5),
        new(9005, "Depocu", "hotel_grandfa", 315, 560, 3),
        new(9006, "Yaşlı Kadın", "hotel_grandma", 417, 671, 6),
        new(20016, "Demirci", "blacksmith", 393, 692, 5),

        // Other fixed village NPCs from the same C1 npc.txt.
        new(20008, "Octavio", "mr_restaurant", 340, 747, 7),
        new(20023, "Soon", "bookworm", 454, 530, 0),
        new(20002, "Aranyo", "auntie", 343, 560, 0),
        new(20003, "Ah-Yu", "baby_and_mom", 378, 577, 0),
        new(20005, "Yonah", "ceramist", 292, 718, 0),
        new(20006, "Mirine", "girl_lost_elder_brother", 336, 770, 0),
        new(20011, "Uriel", "plant_researcher", 425, 716, 0),
        new(20018, "Baek-Go", "doctor", 465, 612, 0),
        new(20041, "Sarhoş", "beggar", 323, 617, 0),

        // Quest / map service NPCs.
        new(20355, "Köy Meydanı Gardiyanı", "guard_leader", 286, 639, 0),
        new(20354, "Şehir Gardiyanı", "guard_leader", 468, 714, 0),
        new(20084, "Biyolog Chaegirab", "chagirap", 285, 285, 0),
        new(20086, "Handu-Up", "handaup", 447, 928, 0),
        new(20087, "Wonda-Rim", "wondaim", 456, 936, 0),

        // Fixed landmark / interaction objects that use NPC-style vnums.
        new(20358, "İsimsiz Çiçekler", "nnflower", 771, 78, 0),
        new(20357, "Weol Anıtı", "moonstone", 114, 960, 0),

        // Stable Boy vnum 20349 is also mapped to jinno_patrol_spear
        // by root/npclist.txt in this client data set.
        new(20349, "Seyis", "jinno_patrol_spear", 396, 735, 2)
    };

    [MenuItem("Metin2/Pyungmoo/Import Village NPCs")]
    public static void ImportVillageNpcs()
    {
        try
        {
            if (!File.Exists(Path.Combine(Application.dataPath, "Scenes", "Pyungmoo.unity")))
            {
                throw new InvalidOperationException(
                    "Pyungmoo sahnesi bulunamadı: " + ScenePath);
            }

            Scene scene = SceneManager.GetActiveScene();
            if (!string.Equals(scene.path, ScenePath, StringComparison.OrdinalIgnoreCase))
            {
                scene = EditorSceneManager.OpenScene(ScenePath, OpenSceneMode.Single);
            }

            GameObject mapRoot = GameObject.Find("Pyungmoo");
            if (mapRoot == null)
                throw new InvalidOperationException("Pyungmoo kök GameObject'i bulunamadı.");

            Transform existingRoot = mapRoot.transform.Find(NpcRootName);
            if (existingRoot != null)
                UnityEngine.Object.DestroyImmediate(existingRoot.gameObject);

            var npcRoot = new GameObject(NpcRootName).transform;
            npcRoot.SetParent(mapRoot.transform, false);

            int loadedModels = 0;
            const int placeholders = 0;
            int groundMisses = 0;

            foreach (NpcPlacement placement in Placements)
            {
                Vector3 position = MapToUnityPosition(placement.MapX, placement.MapY);
                if (TryProjectToTerrain(position, out float groundY))
                    position.y = groundY + GroundOffset;
                else
                {
                    position.y = 0.0f;
                    groundMisses++;
                }

                GameObject instance = LoadModelPrefab(placement.ModelKey);

                if (instance == null)
                {
                    throw new InvalidOperationException(
                        $"NPC modeli bulunamadı: VNUM={placement.Vnum}, model={placement.ModelKey}");
                }

                instance.name =
                    $"NPC_{placement.Vnum}_{Sanitize(placement.DisplayName)}";
                loadedModels++;

                instance.transform.SetParent(npcRoot, true);
                instance.transform.position = position;
                instance.transform.rotation = Quaternion.Euler(0.0f, placement.Direction * 45.0f, 0.0f);

                Metin2NpcIdentity identity = instance.GetComponent<Metin2NpcIdentity>();
                if (identity == null)
                    identity = instance.AddComponent<Metin2NpcIdentity>();

                identity.Initialize(
                    placement.Vnum,
                    placement.DisplayName,
                    new Vector2Int(placement.MapX, placement.MapY));

                // Strict mode: missing NPC models are fatal; placeholders are never accepted.
            }

            EditorSceneManager.MarkSceneDirty(scene);
            EditorSceneManager.SaveScene(scene, ScenePath);
            AssetDatabase.SaveAssets();
            AssetDatabase.Refresh();

            Selection.activeGameObject = npcRoot.gameObject;

            EditorUtility.DisplayDialog(
                "Pyungmoo NPC yerleşimi hazır",
                $"NPC kaydı: {Placements.Length}\n" +
                $"Model bulundu: {loadedModels}\n" +
                $"Yer tutucu: {placeholders}\n" +
                $"Zemin raycast bulunamadı: {groundMisses}\n\n" +
                "Strict mode: eksik NPC modeli varsa import işlemi başarısız olur.",
                "Tamam");
        }
        catch (Exception ex)
        {
            Debug.LogException(ex);
            EditorUtility.DisplayDialog("NPC import hatası", ex.Message, "Tamam");
        }
    }

    private static Vector3 MapToUnityPosition(int mapX, int mapY)
    {
        return new Vector3(
            mapX * MapCoordinateScaleMeters,
            0.0f,
            mapY * MapCoordinateScaleMeters);
    }

    private static bool TryProjectToTerrain(Vector3 xzPosition, out float groundY)
    {
        Ray ray = new Ray(
            new Vector3(xzPosition.x, RayStartHeight, xzPosition.z),
            Vector3.down);

        if (Physics.Raycast(ray, out RaycastHit hit, RayStartHeight + 100.0f))
        {
            groundY = hit.point.y;
            return true;
        }

        groundY = 0.0f;
        return false;
    }

    private static GameObject LoadModelPrefab(string modelKey)
    {
        if (string.IsNullOrWhiteSpace(modelKey) || modelKey == "UNVERIFIED")
            return null;

        // Converted NPC files are named like "armsout.FBX", while the source
        // resource key is "arms". Accept both the exact key and the "out"
        // suffix used by the GR2 -> FBX conversion workflow.
        string[] candidateNames =
        {
            modelKey,
            modelKey + "out"
        };

        foreach (string candidateName in candidateNames)
        {
            string[] guids = AssetDatabase.FindAssets(
                $"{candidateName} t:Model",
                new[] { ImportedNpcFolder });

            foreach (string guid in guids.OrderBy(g => g, StringComparer.Ordinal))
            {
                string path = AssetDatabase.GUIDToAssetPath(guid);
                string fileName = Path.GetFileNameWithoutExtension(path);

                if (!string.Equals(
                    fileName,
                    candidateName,
                    StringComparison.OrdinalIgnoreCase))
                    continue;

                GameObject prefab = AssetDatabase.LoadAssetAtPath<GameObject>(path);
                if (prefab != null)
                    return PrefabUtility.InstantiatePrefab(prefab) as GameObject;
            }
        }

        return null;
    }

    private static string Sanitize(string name)
    {
        foreach (char c in Path.GetInvalidFileNameChars())
            name = name.Replace(c, '_');

        return name.Replace(' ', '_');
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
