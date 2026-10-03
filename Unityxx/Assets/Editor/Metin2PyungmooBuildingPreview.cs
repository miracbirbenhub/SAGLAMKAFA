using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;

public static class Metin2PyungmooBuildingPreview
{
    private const string ScenePath = "Assets/Scenes/Pyungmoo.unity";
    private const string Folder = "Assets/Metin2Imported/Building";
    private const string RootName = "BuildingFBXPreview";

    [MenuItem("Metin2/Pyungmoo/Preview All Building FBX On Map")]
    public static void Preview()
    {
        Scene scene = SceneManager.GetActiveScene();

        if (!string.Equals(scene.path, ScenePath, StringComparison.OrdinalIgnoreCase))
            scene = EditorSceneManager.OpenScene(ScenePath, OpenSceneMode.Single);

        GameObject mapRoot = GameObject.Find("Pyungmoo");
        if (mapRoot == null)
            throw new InvalidOperationException("Pyungmoo GameObject'i bulunamadı.");

        Transform oldRoot = mapRoot.transform.Find(RootName);
        if (oldRoot != null)
            UnityEngine.Object.DestroyImmediate(oldRoot.gameObject);

        Transform root = new GameObject(RootName).transform;
        root.SetParent(mapRoot.transform, false);

        AssetDatabase.Refresh();

        string[] guids = AssetDatabase.FindAssets("t:Model", new[] { Folder });
        var models = new List<GameObject>();

        foreach (string guid in guids)
        {
            string path = AssetDatabase.GUIDToAssetPath(guid);
            if (!path.EndsWith(".fbx", StringComparison.OrdinalIgnoreCase))
                continue;

            GameObject model = AssetDatabase.LoadAssetAtPath<GameObject>(path);
            if (model != null)
                models.Add(model);
        }

        models = models
            .GroupBy(m => Path.GetFileNameWithoutExtension(m.name), StringComparer.OrdinalIgnoreCase)
            .Select(g => g.First())
            .OrderBy(m => m.name, StringComparer.OrdinalIgnoreCase)
            .ToList();

        const int columns = 8;
        const float spacing = 45f;

        for (int i = 0; i < models.Count; i++)
        {
            int col = i % columns;
            int row = i / columns;

            GameObject instance =
                PrefabUtility.InstantiatePrefab(models[i]) as GameObject;

            if (instance == null)
                continue;

            instance.name =
                "PREVIEW_" +
                Regex.Replace(models[i].name, @"[^A-Za-z0-9_-]", "_");

            instance.transform.SetParent(root, false);
            instance.transform.localPosition =
                new Vector3(col * spacing, 5f, row * spacing);
            instance.transform.localRotation = Quaternion.identity;
        }

        Selection.activeGameObject = root.gameObject;

        EditorSceneManager.MarkSceneDirty(scene);
        EditorSceneManager.SaveScene(scene, ScenePath);

        EditorUtility.DisplayDialog(
            "Building Preview",
            "Preview olarak sahneye yerleştirilen FBX: " + models.Count +
            "\n\nHierarchy: Pyungmoo/BuildingFBXPreview",
            "Tamam");
    }
}
