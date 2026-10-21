"""cc-P241: append the ten achievement category icon rows (gumps 22459-22468) to the art registry, before any PNG.

Each icon's author is the game-icons.net folder that serves it (https://game-icons.net/1x1/<author>/<name>.html,
looked up 2026-10-21; Praxiiz's set has no per-author folders). Refuses to add a row whose ID is already registered.
Run: python -P registry_rows.py <path to registry.csv>
"""
import csv
import io
import sys

ICONS = [
    (22459, "Combat", "crossed-swords", "Lorc", "lorc"),
    (22460, "Skills", "open-book", "Lorc", "lorc"),
    (22461, "Exploration", "compass", "Lorc", "lorc"),
    (22462, "Mining", "mining", "Lorc", "lorc"),
    (22463, "Crafting", "anvil", "Lorc", "lorc"),
    (22464, "Legacy", "scroll-unfurled", "Lorc", "lorc"),
    (22465, "Discovery", "magnifying-glass", "Lorc", "lorc"),
    (22466, "Collection", "swap-bag", "Lorc", "lorc"),
    (22467, "League", "laurel-crown", "Lorc", "lorc"),
    (22468, "Mischief", "imp-laugh", "Lorc", "lorc"),
]


def rows():
    for gid, cat, name, author, slug in ICONS:
        what = f"Achievement category icon: {cat} (cc-P241; AchievementsGump draws it beside the category's heading)"
        if cat == "Mischief":
            what = ("Achievement category icon: Mischief, the hidden joke achievements (cc-P241; AchievementsGump draws "
                    "it beside the category's heading)")
        source = (f'Praxiiz "1000+ Custom Spell Icons" 1.1.0 (servuo.dev resource 258), bmp\\{name}.bmp, '
                  f"converted from game-icons.net/1x1/{slug}/{name}.html; black made transparent, nothing else changed")
        license_ = (f"CC BY 3.0, Icons made by {author} (game-icons.net); conversion by Praxiiz; "
                    f"credit both (D:\\UO\\third-party\\spell-icons-1000\\SOURCE.txt)")
        yield [str(gid), f"0x{gid:04X}", what, source, license_, "gump"]


def main(path):
    with open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    taken = {line.split(",", 1)[0] for line in text.splitlines() if line and not line.startswith("#")}
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    for r in rows():
        if r[0] in taken:
            sys.exit(f"{r[0]} is already registered")
        w.writerow(r)
    if not text.endswith("\n"):
        text += "\n"
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text + buf.getvalue())
    print(f"appended {len(ICONS)} rows to {path}")


if __name__ == "__main__":
    main(sys.argv[1])
