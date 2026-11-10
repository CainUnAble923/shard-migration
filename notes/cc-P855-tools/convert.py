"""cc-P855: turn the nine downloads' YAAAG addon component lists into our decoration data (ShardDecorAddon files).

Reads only the component numbers out of each download's .cs (item ID, x, y, z, and for the "complex" ones hue, light
and name). No code is copied: the output is pinned's [Decorate text, one "Static 0x.... (params)" list per look, with
"#!" header lines our ShardDecorAddon reads (name, credit, source) and pinned's reader skips as comments.

  python -P convert.py <third-party code folder> <output folder>

Writes <output>/<key>.cfg for every piece in PIECES, and prints each piece's component count against the source's.
"""

import os
import re
import sys

LIGHTS = None  # filled from pinned's LightType order below

# pinned Projects/Server/Items/LightType.cs, in order (only the ones these files use are checked in main()).
LIGHT_NAMES = {0: "ArchedWindowEast", 1: "Circle225", 29: "Circle300"}

# (folder, file inside it, our key, display name, credit line). Facings: the file names' where they give one; the two
# harpsichords' files do not, so their art names do (tiledata "Harpsichord SOUTH" in pianomodern, "EAST" in pianomodern2).
PIECES = [
    ("grey-fireplaces", "GreySmallFPEastAddon.cs", "grey-fireplace-small-east", "a small grey stone fireplace (east)", "Diesel"),
    ("grey-fireplaces", "GreySmallFPSouthAddon.cs", "grey-fireplace-small-south", "a small grey stone fireplace (south)", "Diesel"),
    ("grey-fireplaces", "GreyLowFPEastAddon.cs", "grey-fireplace-low-east", "a low grey stone fireplace (east)", "Diesel"),
    ("grey-fireplaces", "GreyLowFPSouthAddon.cs", "grey-fireplace-low-south", "a low grey stone fireplace (south)", "Diesel"),
    ("grey-fireplaces", "GreyMedFPEastAddon.cs", "grey-fireplace-medium-east", "a grey stone fireplace (east)", "Diesel"),
    ("grey-fireplaces", "GreyMedFPSouthAddon.cs", "grey-fireplace-medium-south", "a grey stone fireplace (south)", "Diesel"),
    ("grey-fireplaces", "GreyLargeFPEastAddon.cs", "grey-fireplace-large-east", "a large grey stone fireplace (east)", "Diesel"),
    ("grey-fireplaces", "GreyLargeFPSouthAddon.cs", "grey-fireplace-large-south", "a large grey stone fireplace (south)", "Diesel"),
    ("grey-fireplaces", "GreyGrandFPEastAddon.cs", "grey-fireplace-grand-east", "a grand grey stone fireplace (east)", "Diesel"),
    ("grey-fireplaces", "GreyGrandFPSouthAddon.cs", "grey-fireplace-grand-south", "a grand grey stone fireplace (south)", "Diesel"),
    ("lagatha-holiday-fireplace", "holidayfireplaceAddon.cs", "holiday-fireplace", "a holiday fireplace",
     "Lagatha, after Gwenivere (Knights of the Round Table shard)"),
    ("olorin-feasting-tables", "FeastingTable1Addon.cs", "feasting-table-1", "a festival feasting table", "Olórin"),
    ("olorin-feasting-tables", "FeastingTable2Addon.cs", "feasting-table-2", "a festival feasting table", "Olórin"),
    ("olorin-feasting-tables", "FeastingTable3Addon.cs", "feasting-table-3", "a festival feasting table", "Olórin"),
    ("manwitch-buffet-table", "BuffetTableE2WAddon.cs", "buffet-table-east-west", "a Hunt Master's buffet table (east-west)", "manwitch"),
    ("manwitch-buffet-table", "BuffetTableN2SAddon.cs", "buffet-table-north-south", "a Hunt Master's buffet table (north-south)", "manwitch"),
    ("manwitch-formal-dining", "FormalDiningTableE2WAddon.cs", "formal-dining-table-east-west", "a Hunt Master's formal dining table (east-west)", "manwitch"),
    ("manwitch-formal-dining", "FormalDiningTableN2SAddon.cs", "formal-dining-table-north-south", "a Hunt Master's formal dining table (north-south)", "manwitch"),
    ("lagatha-pianos", "piano's/pianomodernAddon.cs", "harpsichord-south", "a harpsichord (south)", "Lagatha"),
    ("lagatha-pianos", "piano's/pianomodern2Addon.cs", "harpsichord-east", "a harpsichord (east)", "Lagatha"),
    ("lagatha-kitchens-bbq", "kitchen and BarBQ/KitchenNWAddon.cs", "small-kitchen-northwest", "a small kitchen", "Lagatha"),
    ("lagatha-kitchens-bbq", "kitchen and BarBQ/KitchenSEAddon.cs", "small-kitchen-southeast", "a small kitchen", "Lagatha"),
    ("lagatha-kitchens-bbq", "kitchen and BarBQ/BarBQSteakSAddon.cs", "barbecue-south", "a barbecue (south)", "Lagatha"),
    ("lagatha-kitchens-bbq", "kitchen and BarBQ/BarBQSteaksEAddon.cs", "barbecue-east", "a barbecue (east)", "Lagatha"),
    ("lagatha-new-kitchen", "NewKitchenEastAddon.cs", "country-kitchen-east", "a country kitchen (east)", "Lagatha"),
    ("lagatha-new-kitchen", "NewKitchenSouthAddon.cs", "country-kitchen-south", "a country kitchen (south)", "Lagatha"),
    ("blue-couches", "BlueCouchEastAddon.cs", "blue-couch-east", "a blue couch (east)", "Diesel"),
    ("blue-couches", "BlueCouchNorthAddon.cs", "blue-couch-north", "a blue couch (north)", "Diesel"),
    ("blue-couches", "BlueCouchSouthAddon.cs", "blue-couch-south", "a blue couch (south)", "Diesel"),
    ("blue-couches", "BlueCouchWestAddon.cs", "blue-couch-west", "a blue couch (west)", "Diesel"),
]

# Each piece's deed group (one deed per group; the deed asks which facing) and its facing's label.
GROUPS = {}
for _key in [p[2] for p in PIECES]:
    _m = re.match(r"^(.*?)-(east-west|north-south|northwest|southeast|east|south|north|west)$", _key)
    if _key == "holiday-fireplace":
        GROUPS[_key] = (_key, "as made")
    elif _key.startswith("feasting-table-"):
        GROUPS[_key] = ("feasting-table", "style " + _key[-1])
    else:
        GROUPS[_key] = (_m.group(1), _m.group(2))

SIMPLE = re.compile(r"\{\s*(\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*\}")
COMPLEX = re.compile(r"AddComplexComponent\(\s*\(BaseAddon\)\s*this\s*,([^;]*)\)\s*;")


def source_url(folder):
    with open(os.path.join(folder, "SOURCE.txt"), encoding="utf-8-sig") as f:
        for line in f:
            if line.startswith("http"):
                return line.strip()
    return ""


def parse(path):
    text = open(path, encoding="utf-8", errors="replace").read()
    pieces = []
    m = re.search(r"m_AddOnSimpleComponents\s*=\s*new int\[,\]\s*\{(.*?)\};", text, re.S)
    if m:
        for g in SIMPLE.findall(m.group(1)):
            pieces.append((int(g[0]), int(g[1]), int(g[2]), int(g[3]), 0, -1, ""))
    for args in COMPLEX.findall(text):
        parts = [a.strip() for a in args.split(",")]
        item, x, y, z, hue, light = (int(p) for p in parts[:6])
        name = parts[6].strip('"') if len(parts) > 6 else ""
        amount = int(parts[7]) if len(parts) > 7 else 1
        if amount != 1:
            raise ValueError(f"{path}: amount {amount}")
        pieces.append((item, x, y, z, hue, light, name))
    expected = len(re.findall(r"AddComplexComponent\(\s*\(BaseAddon\)", text)) + (len(SIMPLE.findall(m.group(1))) if m else 0)
    return pieces, expected


def header(item, hue, light, name):
    params = []
    if hue:
        params.append(f"Hue={hue}")
    if light != -1:
        params.append(f"Light={LIGHT_NAMES[light]}")
    if name:
        params.append(f"Name={name}")
    return f"Static 0x{item:04X}" + (f" ({'; '.join(params)})" if params else "")


def main():
    src, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    for folder, file, key, display, credit in PIECES:
        pieces, expected = parse(os.path.join(src, folder, file))
        assert len(pieces) == expected, (file, len(pieces), expected)
        groups = {}
        for item, x, y, z, hue, light, name in pieces:
            groups.setdefault(header(item, hue, light, name), []).append((x, y, z))
        lines = [
            f"# cc-P855: {display}, a ShardDecorAddon piece (stock art only). Made from the component list of {folder}/{file}",
            f"# ({source_url(os.path.join(src, folder))}) by shard-migration notes/cc-P855-tools/convert.py; no code was taken.",
            "# Offsets are from the addon's own tile (where the deed is targeted). Do not edit by hand: rerun the script.",
            f"#! name: {display}",
            f"#! credit: {credit}",
            f"#! group: {GROUPS[key][0]}",
            f"#! facing: {GROUPS[key][1]}",
            "",
        ]
        for h, points in groups.items():
            lines.append(h)
            for x, y, z in points:
                lines.append(f"{x} {y} {z}")
            lines.append("")
        with open(os.path.join(out, key + ".cfg"), "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(lines))
        lights = sorted({p[5] for p in pieces if p[5] != -1})
        print(f"{key}: {len(pieces)} components, {len(groups)} lists, lights {lights}")


if __name__ == "__main__":
    main()
