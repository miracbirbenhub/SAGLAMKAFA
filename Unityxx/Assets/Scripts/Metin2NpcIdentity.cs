using UnityEngine;

public sealed class Metin2NpcIdentity : MonoBehaviour
{
    [field: SerializeField] public int Vnum { get; private set; }
    [field: SerializeField] public string DisplayName { get; private set; }
    [field: SerializeField] public Vector2Int MapCoordinate { get; private set; }

    public void Initialize(int vnum, string displayName, Vector2Int mapCoordinate)
    {
        Vnum = vnum;
        DisplayName = displayName;
        MapCoordinate = mapCoordinate;
    }
}
