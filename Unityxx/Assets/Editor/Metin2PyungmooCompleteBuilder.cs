using System;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;

public static class Metin2PyungmooCompleteBuilder
{
    private const string ScenePath = "Assets/Scenes/Pyungmoo.unity";

    [MenuItem("Metin2/Pyungmoo/FINALIZE - NPC + Buildings + Validate")]
    public static void BuildAndValidate()
    {
        try
        {
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

            EditorUtility.DisplayProgressBar(
                "Pyungmoo Finalize",
                "NPC modelleri ve placement'ları yenileniyor...",
                0.10f);

            Metin2PyungmooNpcImporter.ImportVillageNpcs();

            EditorUtility.DisplayProgressBar(
                "Pyungmoo Finalize",
                "AreaData / MapObjects yeniden oluşturuluyor...",
                0.30f);

            Metin2PyungmooObjectImporter.ImportMapObjects();

            EditorUtility.DisplayProgressBar(
                "Pyungmoo Finalize",
                "Gerçek Building FBX AreaData instance'ları oluşturuluyor...",
                0.50f);

            Metin2PyungmooDirectBuildingImporter.ImportExistingBuildingFbxDirect();

            EditorUtility.DisplayProgressBar(
                "Pyungmoo Finalize",
                "47/47 Building FBX sahne galerisine bağlanıyor...",
                0.70f);

            int buildingCount =
                Metin2PyungmooBuildingPreview.PreviewAll(false);

            if (buildingCount <= 0)
            {
                throw new InvalidOperationException(
                    "Building FBX galerisi boş oluştu.");
            }

            EditorUtility.DisplayProgressBar(
                "Pyungmoo Finalize",
                "Scene validation yapılıyor...",
                0.82f);

            Metin2PyungmooIntegrationValidator.ValidationResult validation =
                Metin2PyungmooIntegrationValidator.ValidateCurrentScene();

            Metin2PyungmooIntegrationValidator.WriteReport(validation);

            if (!validation.Passed)
            {
                throw new InvalidOperationException(
                    validation.ToDisplayText());
            }

            EditorUtility.DisplayProgressBar(
                "Pyungmoo Finalize",
                "Temiz Standalone Windows build testi çalıştırılıyor...",
                0.90f);

            Metin2PyungmooIntegrationValidator.ValidationResult buildValidation =
                Metin2PyungmooIntegrationValidator.ValidateAndBuildPlayer();

            Metin2PyungmooIntegrationValidator.WriteReport(buildValidation);

            if (!buildValidation.Passed)
            {
                throw new InvalidOperationException(
                    buildValidation.ToDisplayText());
            }

            Debug.Log(
                "[Pyungmoo FINALIZE] PASS - NPC + Building + MapObjects + Standalone build.");

            EditorUtility.DisplayDialog(
                "PYUNGMOO FINAL PASS",
                "NPC + Building + MapObjects doğrulandı.\n\n" +
                $"Building FBX gallery: {buildingCount}\n" +
                "Placeholder: 0\n" +
                "StandaloneWindows64 build: PASS\n\n" +
                "Ayrıntılı rapor: Assets/Metin2Generated/Pyungmoo/PyungmooCompleteValidation.txt",
                "Tamam");
        }
        catch (Exception ex)
        {
            Debug.LogError(
                "[Pyungmoo FINALIZE] FAILED\n" + ex);

            EditorUtility.DisplayDialog(
                "PYUNGMOO FINAL FAILED",
                "İşlem tamamlanmadı.\n\n" +
                ex.Message +
                "\n\nConsole ve PyungmooCompleteValidation.txt dosyasını kontrol edin.",
                "Tamam");
        }
        finally
        {
            EditorUtility.ClearProgressBar();
        }
    }
}
