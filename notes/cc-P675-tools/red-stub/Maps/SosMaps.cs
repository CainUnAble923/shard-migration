// cc-P675 red stub: the same public names as server/customizations/Maps/SosMaps.cs and no behaviour (Felucca stays on
// file index 0). Mounted over the builder image for the red run only; never shipped.
namespace Server;

public static class SosMaps
{
    public const int FeluccaIndex = 0;
    public const int SosFileIndex = 1;
    public static bool FeluccaOnSos => false;

    [CallPriority(3)]
    public static void Configure()
    {
    }
}
