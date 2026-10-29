"""cc-P684: the code copy's edits by exact text (TreasureMap.cs ValidateLocation, the Dockerfile's treasure.cfg line)."""
import sys

ROOT = "D:/UO/golems/Iron/ShatteredLegacy/"


def edit(rel, old, new):
    p = ROOT + rel
    s = open(p, encoding="utf-8", newline="").read()
    if "\r\n" in s:
        old, new = old.replace("\n", "\r\n"), new.replace("\n", "\r\n")
    if s.count(old) != 1:
        sys.exit(f"{rel}: expected one match, found {s.count(old)}")
    open(p, "w", encoding="utf-8", newline="").write(s.replace(old, new))
    print("edited", rel)


edit("server/patches/TreasureMap.cs",
     """//   - OnChestOpened tells ClusterFAchievementSystem (the shard's "dug up a treasure map chest" trigger, built waiting for it).
""",
     """//   - OnChestOpened tells ClusterFAchievementSystem (the shard's "dug up a treasure map chest" trigger, built waiting for it).
//   - ValidateLocation refuses ClusterFSosTreasureLand's tiles (cc-P684, SoS swap S11): S14's unfinished land, and on
//     Felucca Trammel's towns and dungeons (the same SoS land, before S13 redraws Felucca's regions).
""")

edit("server/patches/TreasureMap.cs",
     """    public static bool ValidateLocation(int x, int y, Map map)
    {
        var lt = map.Tiles.GetLandTile(x, y);
""",
     """    public static bool ValidateLocation(int x, int y, Map map)
    {
        var lt = map.Tiles.GetLandTile(x, y);

        if (ClusterFSosTreasureLand.Refused(x, y, lt.Z, map))
        {
            return false;
        }
""")

edit("docker/uo/Dockerfile",
     "COPY server/data/Decoration/ /build/modernuo/Distribution/Data/ShatteredLegacy/Decoration/\n",
     "COPY server/data/Decoration/ /build/modernuo/Distribution/Data/ShatteredLegacy/Decoration/\n"
     "# cc-P684 (SoS swap S11): pinned's treasure.cfg decided for the SoS land, with spots on the new land, in its place\n"
     "# (TreasureMap's level-0 and classic spots, TreasureMapProtection's no-housing squares; made by shard-migration\n"
     "# notes/cc-P684-tools/treasure.py).\n"
     "COPY server/data/treasure.cfg /build/modernuo/Distribution/Data/treasure.cfg\n")
