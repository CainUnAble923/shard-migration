"""Generate CraftBulkEntries.cs from ServUO pub57's Data/Bulk Orders/<craft>/*.cfg (six 2016 crafts)."""
import os, sys

SRC = r"D:\UO\ServUO-pub57\Data\Bulk Orders"
OUT = sys.argv[1]

CRAFTS = ["Alchemy", "Carpentry", "Cooking", "Fletching", "Inscription", "Tinkering"]

# ServUO type name -> the pinned type of the same item (renamed upstream)
RENAMED = {
    "FlameStrikeScroll": "FlamestrikeScroll",
    "MagicUntrapScroll": "MagicUnTrapScroll",
    "TelekinisisScroll": "TelekinesisScroll",
    "SmithyHammer": "SmithHammer",
}
# ServUO types with no item in pinned or ours: dropped, as ServUO's loader drops a type it cannot find
MISSING = {"NexusCore", "SweetCocoaButter", "EnchantedApple", "WrathGrapes", "GrapesOfWrath", "ThreeTieredCake",
           "RunicAtlas", "Clippers", "MetalContainerEngraver"}

# ServUO's property names (SmallBulkEntry.cs :53-116, LargeBulkEntry.cs :174-440)
SMALL_NAMES = {
    ("Tinkering", "smalls"): "TinkeringSmalls", ("Tinkering", "smallsregular"): "TinkeringSmallsRegular",
    ("Carpentry", "smalls"): "CarpentrySmalls", ("Inscription", "smalls"): "InscriptionSmalls",
    ("Cooking", "smalls"): "CookingSmalls", ("Cooking", "smallsregular"): "CookingSmallsRegular",
    ("Fletching", "smalls"): "FletchingSmalls", ("Fletching", "smallsregular"): "FletchingSmallsRegular",
    ("Alchemy", "smalls"): "AlchemySmalls",
}
ALCH_LARGE = {"largeexplosive": "LargeExplosive", "largegreater": "LargeGreater", "largelesser": "LargeLesser",
              "largeregular": "LargeRegular", "largetoxic": "LargeToxic"}

dropped = []
lines = []
total = 0
for craft in CRAFTS:
    d = os.path.join(SRC, craft)
    lines.append(f"    // -- {craft} " + "-" * (100 - len(craft)))
    lines.append("")
    for fn in sorted(os.listdir(d), key=lambda s: (not s.startswith("small"), s.lower())):
        stem = fn[:-4]
        name = SMALL_NAMES.get((craft, stem)) or ALCH_LARGE.get(stem) or stem
        rows = []
        for raw in open(os.path.join(d, fn), encoding="utf-8"):
            line = raw.strip()
            if not line or line.startswith("#"):
                if line.startswith("#") and rows and line[1:].strip():
                    rows.append(("comment", line[1:].strip()))
                continue
            parts = [p.strip() for p in line.split(",")]
            t = parts[0]
            graphic = parts[1]
            cliloc = parts[2] if len(parts) >= 3 else None
            total += 1
            if t in MISSING:
                dropped.append(f"{craft}/{fn}: {t}")
                rows.append(("comment", f"{t}: not on the shard (dropped, as ServUO drops a type it cannot find)"))
                continue
            t2 = RENAMED.get(t, t)
            note = f" // ServUO {t}" if t2 != t else ""
            args = f"typeof({t2}), {graphic}" + (f", {cliloc}" if cliloc else "")
            rows.append(("entry", f"E({args}),{note}"))
        lines.append(f"    /// <summary>ServUO {craft}/{fn}.</summary>")
        lines.append(f"    public static readonly SmallBulkEntry[] {name} =")
        lines.append("    [")
        for kind, text in rows:
            lines.append(f"        // {text}" if kind == "comment" else f"        {text}")
        lines.append("    ];")
        lines.append("")

import textwrap
WRAPPED = chr(10).join("// " + l for l in textwrap.wrap(f"Not on the shard, so dropped where ServUO lists them ({len(dropped)} of {total} rows): " + ", ".join(sorted(set(d.split(": ")[1] for d in dropped))) + ". A large deed keeps the rest of its list.", 117))
header = f"""// cc-P123: the six 2016 crafts' bulk order entries, generated from ServUO pub57's Data/Bulk Orders/<craft>/*.cfg by
// shard-migration notes/cc-P123-tools/gen_entries.py (not edited by hand). ServUO loads these files at run time; this
// shard's image carries pinned's Data folder only (Blacksmith and Tailoring), so the six crafts' lists are compiled in.
//
// Each row is ServUO's: the item type, its graphic and, where the file names one, its cliloc; a row with no cliloc
// gets the graphic's name as ServUO's loader gives it (SmallBulkEntry.cs:200). ServUO's fourth column, the graphic's
// hue in the deed gump, is not carried: pinned's SmallBulkEntry and deed gumps have no hue (a potion shows an
// uncoloured bottle, named by its cliloc).
//
// Renamed upstream, mapped to pinned's type: FlameStrikeScroll -> FlamestrikeScroll, MagicUntrapScroll ->
// MagicUnTrapScroll, TelekinisisScroll -> TelekinesisScroll, SmithyHammer -> SmithHammer (pinned has one smith's
// hammer).
{WRAPPED}

using System;
using Server.Items;

namespace Server.Engines.BulkOrders;

public static class CraftBulkEntries
{{
    private static SmallBulkEntry E(Type type, int graphic, int number = 0) =>
        new(type, number != 0 ? number : graphic < 0x4000 ? 1020000 + graphic : 1078872 + graphic, graphic);

"""
open(OUT, "w", encoding="utf-8", newline="\n").write(header + "\n".join(lines).rstrip() + "\n}\n")
print(total, "rows,", len(dropped), "dropped")
for x in dropped:
    print("  ", x)
