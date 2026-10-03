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
    private const string RootName = "BuildingFBXPreview";

    [MenuItem("Metin2/Pyungmoo/Preview All Building FBX On Map")]
    public static void Preview()
    {
        PreviewAll(true);
    }

    public static int PreviewAll(bool showDialog)
    {
        Scene scene = SceneManager.GetActiveScene();

        if (!string.Equals(scene.path, ScenePath, StringComparison.OrdinalIgnoreCase))
        {
            scene = EditorSceneManager.OpenScene(
                ScenePath,
                OpenSceneMode.Single);
        }

        GameObject mapRoot = GameObject.Find("Pyungmoo");
        if (mapRoot == null)
            throw new InvalidOperationException("Pyungmoo GameObject'i bulunamadı.");

        Transform oldRoot = mapRoot.transform.Find(RootName);
        if (oldRoot != null)
            UnityEngine.Object.DestroyImmediate(oldRoot.gameObject);

        AssetDatabase.Refresh();

        string absoluteFolder = Path.Combine(
            Application.dataPath,
            "Metin2Imported",
            "Building");

        if (!Directory.Exists(absoluteFolder))
            throw new DirectoryNotFoundException(
                "Building FBX klasörü bulunamadı: " + absoluteFolder);

        string[] physicalFiles = Directory.GetFiles(
                absoluteFolder,
                "*.fbx",
                SearchOption.AllDirectories)
            .OrderBy(p => p, StringComparer.OrdinalIgnoreCase)
            .ToArray();

        if (physicalFiles.Length == 0)
            throw new InvalidOperationException(
                "Building klasöründe hiç FBX bulunamadı.");

        var models = new List<(string AssetPath, GameObject Model)>();

        foreach (string physicalPath in physicalFiles)
        {
            string assetPath = ToAssetPath(physicalPath);

            GameObject model =
                AssetDatabase.LoadAssetAtPath<GameObject>(assetPath);

            if (model == null)
            {
                throw new InvalidOperationException(
                    "Unity Building FBX'i import edemedi: " +
                    assetPath);
            }

            if (model.GetComponentsInChildren<Renderer>(true).Length == 0)
            {
                throw new InvalidOperationException(
                    "Building FBX içinde Renderer bulunamadı: " +
                    assetPath);
            }

            models.Add((assetPath, model));
        }

        if (models.Count != physicalFiles.Length)
        {
            throw new InvalidOperationException(
                $"Building FBX sayısı uyuşmuyor. Disk={physicalFiles.Length}, Unity={models.Count}");
        }

        Transform root = new GameObject(RootName).transform;
        root.SetParent(mapRoot.transform, true);
        root.position = CalculateGalleryOrigin(mapRoot.transform);

        const int columns = 6;
        const float spacing = 90.0f;

        for (int i = 0; i < models.Count; i++)
        {
            int col = i % columns;
            int row = i / columns;

            GameObject instance =
                PrefabUtility.InstantiatePrefab(models[i].Model) as GameObject;

            if (instance == null)
            {
                throw new InvalidOperationException(
                    "Building FBX prefab instance oluşturulamadı: " +
                    models[i].AssetPath);
            }

            instance.name =
                "FBX_" +
                i.ToString("D2") +
                "_" +
                Regex.Replace(
                    models[i].Model.name,
                    @"[^A-Za-z0-9_-]",
                    "_");

            instance.transform.SetParent(root, false);
            instance.transform.localPosition =
                new Vector3(col * spacing, 0.0f, row * spacing);
            instance.transform.localRotation = Quaternion.identity;
            instance.transform.localScale = Vector3.one;
            instance.isStatic = true;
        }

        if (root.childCount != models.Count)
        {
            throw new InvalidOperationException(
                $"Building gallery child sayısı uyuşmuyor. Scene={root.childCount}, expected={models.Count}");
        }

        Selection.activeGameObject = root.gameObject;

        EditorSceneManager.MarkSceneDirty(scene);
        EditorSceneManager.SaveScene(scene, ScenePath);

        AssetDatabase.SaveAssets();
        AssetDatabase.Refresh();

        if (showDialog)
        {
            EditorUtility.DisplayDialog(
                "Building FBX Preview",
                $"Sahneye {models.Count} adet Building FBX eklendi.\n\nHierarchy: Pyungmoo/{RootName}",
                "Tamam");
        }

        return models.Count;
    }

    private static Vector3 CalculateGalleryOrigin(Transform mapRoot)
    {
        var renderers = mapRoot
            .GetComponentsInChildren<Renderer>(true)
            .Where(r => !IsInsideNamedRoot(r.transform, RootName))
            .ToArray();

        if (renderers.Length == 0)
            return new Vector3(5000.0f, 0.0f, 5000.0f);

        Bounds bounds = renderers[0].bounds;

        for (int i = 1; i < renderers.Length; i++)
            bounds.Encapsulate(renderers[i].bounds);

        return new Vector3(
            bounds.max.x + 1000.0f,
            bounds.min.y,
            bounds.max.z + 1000.0f);
    }

    private static bool IsInsideNamedRoot(Transform transform, string rootName)
    {
        Transform current = transform;

        while (current != null)
        {
            if (string.Equals(
                    current.name,
                    rootName,
                    StringComparison.Ordinal))
                return true;

            current = current.parent;
        }

        return false;
    }

    private static string ToAssetPath(string absolutePath)
    {
        string assetsRoot = Application.dataPath
            .Replace('\\', '/')
            .TrimEnd('/');

        string normalized = absolutePath.Replace('\\', '/');

        if (!normalized.StartsWith(
                assetsRoot + "/",
                StringComparison.OrdinalIgnoreCase))
        {
            throw new InvalidOperationException(
                "Assets dışı Building FBX yolu: " + absolutePath);
        }

        return "Assets/" +
            normalized.Substring(assetsRoot.Length + 1);
    }
}
