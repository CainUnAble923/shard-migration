"""cc-P362: the optional UI skins (Chase's look book "Like" picks): backpack, bag, metal chest (and the bank box), crate
and spell scroll looks, each under NEW IDs. Stock IDs keep stock art; our TazUO patch remaps a stock ID to one of these
only for a player who picks that skin (client side, per profile).

    python -P skins.py registry <registry.csv>      append the 93 rows (29 gumps, 64 art); refuses a taken ID
    python -P skins.py png <ShatteredLegacy repo>    convert each source through scripts\\anchor-art-frames.py
    python -P skins.py manifest <skins.json> <SkinTable.cs>   write the skin table (data, and the client's C# copy)

Pixels: BMP to PNG with pure black made transparent and the canvas kept (anchor-art-frames.py --black-transparent
--keep-geometry). Nothing else is changed.

Sources (each folder's SOURCE.txt under D:\\UO\\third-party; never built or run from there, only read):
  fancy-backpack, gothic-backpack   Carl Hamilton, community work
  backpack-sets                     Safera: Bloody is his own; Celtic and Dragon are UO Desktop themes and the leather
                                    "Fancy" set is EA-derived (likely his KR Strappy conversion): those ship only as
                                    our own PNG under new IDs, never as an EA file. Primitive, Snowy and Strappy are
                                    EA's own alternate backpacks (gumps 30558-30563), which the client already has and
                                    TazUO already offers (Options, Containers, backpack style): nothing of them ships.
  bag-gumps                         Castiel, community work (styled after EA's backpacks)
  erads-custom-content              Erachiro: "Everything you see in this pack is free to use."
  magic-scrolls                     CorvaeOboro: CC0 1.0 (his GitHub repository ultima_online_mods, the repository-wide
                                    license; checked 2026-10-23); credited anyway
"""
import csv
import io
import json
import os
import subprocess
import sys

TP = r"D:\UO\third-party"
FANCY = os.path.join(TP, "fancy-backpack")
GOTHIC = os.path.join(TP, "gothic-backpack")
SETS = os.path.join(TP, "backpack-sets")
BAGS = os.path.join(TP, "bag-gumps")
ERAD = os.path.join(TP, "erads-custom-content", "Erad's Custom UO Content", "Client", "Containers")
SCROLLS = os.path.join(TP, "magic-scrolls", "ART_MagicScrolls")

COMMUNITY = ("none stated; community work: credit {who} in the shard credits, ship only inside the player package or the "
             "private repo, do not repost ({src}); an optional skin under new IDs, stock IDs keep stock art")
CARL = ("Carl Hamilton", COMMUNITY.format(who="Carl Hamilton", src=r"D:\UO\third-party\{f}\SOURCE.txt"))
SAFERA = ("Safera", COMMUNITY.format(who="Safera", src=r"D:\UO\third-party\backpack-sets\SOURCE.txt"))
SAFERA_EA = ("Safera", COMMUNITY.format(who="Safera", src=r"D:\UO\third-party\backpack-sets\SOURCE.txt")
             + "; EA-derived ({why}): ships only as our PNG override under a new ID, never as an EA file")
CASTIEL = ("Castiel", COMMUNITY.format(who="Castiel", src=r"D:\UO\third-party\bag-gumps\SOURCE.txt"))
ERACHIRO = ("Erachiro", 'Erachiro: "Everything you see in this pack is free to use." Credit Erachiro in the shard credits, '
            r"ship only inside the player package or the private repo, do not repost (D:\UO\third-party\erads-custom-content\SOURCE.txt); "
            "an optional skin under new IDs, stock IDs keep stock art")
CORVAE = ("CorvaeOboro", "CC0 1.0 (github.com/CorvaeOboro/ultima_online_mods, the repository's license, checked 2026-10-23); "
          r"credited in the shard credits anyway (D:\UO\third-party\magic-scrolls\SOURCE.txt); an optional skin under new "
          "art IDs, stock scroll art stays")

# The stock gumps a skin stands in for (pinned Distribution\Data\containers.cfg; TazUO ContainerManager and
# PaperDollInteractable): the backpack's open gump, its minimized icon, the backpack drawn on a man's paperdoll; the
# bag; the metal chest (also every bank box, item 0xE7C); the crate.
BACKPACK, ICON, ON_PAPERDOLL, BAG, METAL_CHEST, CRATE = 0x3C, 0x50, 0xC4F6, 0x3D, 0x4A, 0x44

FIRST_GUMP = 23052
FIRST_ART = 13049

# Gump pieces: (key, what, folder, file, credit, terms-format). In ID order from FIRST_GUMP.
GUMPS = [
    ("fancy.open", "Fancy backpack: open backpack (full)", FANCY, "Gump 60 Fancy Backpack FULL Container.bmp", CARL, "fancy-backpack"),
    ("fancy.icon", "Fancy backpack: minimized backpack", FANCY, "Gump 80 Fancy Backpack Minimized 1.bmp", CARL, "fancy-backpack"),
    ("fancy.paperdoll", "Fancy backpack: on the paperdoll", FANCY, "Gump 50422 Fancy Backpack  on Paperdoll Window.bmp", CARL, "fancy-backpack"),
    ("fancy.compact", "Fancy backpack: open backpack (compact)", FANCY, "Gump 60 Fancy Backpack Mini Container.bmp", CARL, "fancy-backpack"),
    ("gothic.open", "Gothic backpack: open backpack (full)", GOTHIC, "Gump 60 Gothic Backpack Full Container.bmp", CARL, "gothic-backpack"),
    ("gothic.icon", "Gothic backpack: minimized backpack", GOTHIC, "Gump 80 Gothic Backpack Minimized 1.bmp", CARL, "gothic-backpack"),
    ("gothic.paperdoll", "Gothic backpack: on the paperdoll", GOTHIC, "Gump 50422 Gothic Backpack on Paperdoll Window.bmp", CARL, "gothic-backpack"),
    ("gothic.compact", "Gothic backpack: open backpack (compact)", GOTHIC, "Gump 60 Gothic Backpack Mini Container.bmp", CARL, "gothic-backpack"),
    ("bloody.open", "Bloody backpack: open backpack", os.path.join(SETS, "Bloody"), "BloodpackOpen.bmp", SAFERA, None),
    ("bloody.paperdoll", "Bloody backpack: on the paperdoll", os.path.join(SETS, "Bloody"), "Gump 50422_bloodybackpack.bmp", SAFERA, None),
    ("celtic.open", "Celtic backpack: open backpack", os.path.join(SETS, "Celtic"), "0x3c.bmp", SAFERA_EA, "a UO Desktop theme"),
    ("celtic.icon", "Celtic backpack: minimized backpack", os.path.join(SETS, "Celtic"), "0x50.bmp", SAFERA_EA, "a UO Desktop theme"),
    ("celtic.paperdoll", "Celtic backpack: on the paperdoll", os.path.join(SETS, "Celtic"), "0xc4f6.bmp", SAFERA_EA, "a UO Desktop theme"),
    ("dragon.open", "Dragon backpack: open backpack", os.path.join(SETS, "Dragon"), "0x3c.bmp", SAFERA_EA, "a UO Desktop theme"),
    ("dragon.icon", "Dragon backpack: minimized backpack", os.path.join(SETS, "Dragon"), "0x50.bmp", SAFERA_EA, "a UO Desktop theme"),
    ("dragon.paperdoll", "Dragon backpack: on the paperdoll", os.path.join(SETS, "Dragon"), "0xc4f6.bmp", SAFERA_EA, "a UO Desktop theme"),
    ("leather.open", "Leather backpack: open backpack", os.path.join(SETS, "Fancy"), "OpenPack.bmp", SAFERA_EA, "likely the KR client's strappy backpack"),
    ("leather.icon", "Leather backpack: minimized backpack", os.path.join(SETS, "Fancy"), "Gump 9811.bmp", SAFERA_EA, "likely the KR client's strappy backpack"),
    ("leather.paperdoll", "Leather backpack: on the paperdoll", os.path.join(SETS, "Fancy"), "Backpack_Paperdoll.bmp", SAFERA_EA, "likely the KR client's strappy backpack"),
    ("bag.celtic", "Celtic bag: open bag", BAGS, "Celtic Bag.bmp", CASTIEL, None),
    ("bag.primitive", "Primitive bag: open bag", BAGS, "Primitive Bag.bmp", CASTIEL, None),
    ("bag.snowy", "Snowy bag: open bag", BAGS, "Snowy Bag.bmp", CASTIEL, None),
    ("chest.blue", "Metal chest and bank box: blue lining", os.path.join(ERAD, "Chests"), "Bankchest Blue Lining.bmp", ERACHIRO, None),
    ("chest.pink", "Metal chest and bank box: pink lining", os.path.join(ERAD, "Chests"), "Bankchest Pink Lining.bmp", ERACHIRO, None),
    ("chest.red", "Metal chest and bank box: red lining", os.path.join(ERAD, "Chests"), "Bankchest Red Lining.bmp", ERACHIRO, None),
    ("chest.teal", "Metal chest and bank box: teal lining", os.path.join(ERAD, "Chests"), "Bankchest Teal Lining.bmp", ERACHIRO, None),
    ("chest.yellow", "Metal chest and bank box: yellow lining", os.path.join(ERAD, "Chests"), "Bankchest Yellow Lining.bmp", ERACHIRO, None),
    ("crate.refurbished", "Crate: refurbished", os.path.join(ERAD, "Crates"), "Refurbished Crate.bmp", ERACHIRO, None),
    ("crate.weathered", "Crate: weathered", os.path.join(ERAD, "Crates"), "Weathered Crate.bmp", ERACHIRO, None),
]
GUMP_ID = {k: FIRST_GUMP + i for i, (k, *_rest) in enumerate(GUMPS)}

# Skins: (kind, key, label, credit line, {stock id: piece key}). A backpack skin without a minimized icon keeps stock's.
KINDS = [("backpack", "Backpack", "gump"), ("bag", "Bags", "gump"), ("chest", "Metal chests and the bank box", "gump"),
         ("crate", "Crates", "gump"), ("scroll", "Spell scrolls", "art")]
SKINS = [
    ("backpack", "fancy", "Fancy", "Carl Hamilton", {BACKPACK: "fancy.open", ICON: "fancy.icon", ON_PAPERDOLL: "fancy.paperdoll"}),
    ("backpack", "fancy-compact", "Fancy, compact", "Carl Hamilton", {BACKPACK: "fancy.compact", ICON: "fancy.icon", ON_PAPERDOLL: "fancy.paperdoll"}),
    ("backpack", "gothic", "Gothic", "Carl Hamilton", {BACKPACK: "gothic.open", ICON: "gothic.icon", ON_PAPERDOLL: "gothic.paperdoll"}),
    ("backpack", "gothic-compact", "Gothic, compact", "Carl Hamilton", {BACKPACK: "gothic.compact", ICON: "gothic.icon", ON_PAPERDOLL: "gothic.paperdoll"}),
    ("backpack", "bloody", "Bloody", "Safera", {BACKPACK: "bloody.open", ON_PAPERDOLL: "bloody.paperdoll"}),
    ("backpack", "celtic", "Celtic", "Safera", {BACKPACK: "celtic.open", ICON: "celtic.icon", ON_PAPERDOLL: "celtic.paperdoll"}),
    ("backpack", "dragon", "Dragon", "Safera", {BACKPACK: "dragon.open", ICON: "dragon.icon", ON_PAPERDOLL: "dragon.paperdoll"}),
    ("backpack", "leather", "Leather", "Safera", {BACKPACK: "leather.open", ICON: "leather.icon", ON_PAPERDOLL: "leather.paperdoll"}),
    ("bag", "celtic", "Celtic", "Castiel", {BAG: "bag.celtic"}),
    ("bag", "primitive", "Primitive", "Castiel", {BAG: "bag.primitive"}),
    ("bag", "snowy", "Snowy", "Castiel", {BAG: "bag.snowy"}),
    ("chest", "blue", "Blue lining", "Erachiro", {METAL_CHEST: "chest.blue"}),
    ("chest", "pink", "Pink lining", "Erachiro", {METAL_CHEST: "chest.pink"}),
    ("chest", "red", "Red lining", "Erachiro", {METAL_CHEST: "chest.red"}),
    ("chest", "teal", "Teal lining", "Erachiro", {METAL_CHEST: "chest.teal"}),
    ("chest", "yellow", "Yellow lining", "Erachiro", {METAL_CHEST: "chest.yellow"}),
    ("crate", "refurbished", "Refurbished", "Erachiro", {CRATE: "crate.refurbished"}),
    ("crate", "weathered", "Weathered", "Erachiro", {CRATE: "crate.weathered"}),
]


def scroll_files():
    """The 64 Magery scrolls, by stock item ID (0x1F2D-0x1F6C), each from the file that names that ID."""
    out = []
    for f in sorted(os.listdir(SCROLLS)):
        if f.startswith("item_scroll_") and f.endswith(".bmp"):
            stock = int(f.rsplit("_", 1)[1][:-4], 16)
            out.append((stock, f))
    out.sort()
    assert [s for s, _ in out] == list(range(0x1F2D, 0x1F6D)), [hex(s) for s, _ in out]
    return out


def art_rows():
    rows = []
    for i, (stock, f) in enumerate(scroll_files()):
        spell = f[len("item_scroll_"):].rsplit("_", 1)[0]          # "1_Clumsy"
        circle, name = spell.split("_", 1)
        rows.append((FIRST_ART + i, stock, f, f"Magic Scrolls skin: {name} scroll (circle {circle}), for stock art 0x{stock:04X}"))
    return rows


def check():
    assert len(GUMPS) == 29 and len(set(GUMP_ID)) == 29
    for k, what, folder, fname, credit, fmt in GUMPS:
        assert os.path.isfile(os.path.join(folder, fname)), (k, fname)
    for kind, key, label, who, m in SKINS:
        assert kind in [k for k, _, _ in KINDS]
        for stock, piece in m.items():
            assert piece in GUMP_ID, piece
            assert stock not in GUMP_ID.values()
    used = {p for *_x, m in SKINS for p in m.values()}
    assert used == set(GUMP_ID), set(GUMP_ID) - used
    assert len(art_rows()) == 64


def registry_rows():
    rows = []
    for k, what, folder, fname, (author, terms), fmt in GUMPS:
        gid = GUMP_ID[k]
        pack = os.path.basename(folder) if folder not in (FANCY, GOTHIC, BAGS) else os.path.basename(folder)
        lic = terms.format(f=fmt) if author == "Carl Hamilton" else (terms.format(why=fmt) if fmt else terms)
        rows.append([str(gid), f"0x{gid:04X}", f"UI skin (cc-P362): {what}",
                     f"{author}: {os.path.relpath(os.path.join(folder, fname), TP)}; black made transparent, nothing else changed",
                     lic, "gump"])
    for aid, stock, f, what in art_rows():
        rows.append([str(aid), f"0x{aid:04X}", f"UI skin (cc-P362): {what}",
                     f"CorvaeOboro: magic-scrolls\\ART_MagicScrolls\\{f}; black made transparent, nothing else changed",
                     CORVAE[1], "art"])
    return rows


def cmd_registry(path):
    check()
    with open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    taken = {line.split(",", 1)[0] for line in text.splitlines() if line and not line.startswith("#")}
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    for r in registry_rows():
        if r[0] in taken:
            sys.exit(f"{r[0]} is already registered")
        w.writerow(r)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text if text.endswith("\n") else text + "\n")
        f.write(buf.getvalue())
    print("appended %d rows" % len(registry_rows()))


def convert(tool, src, first_id, out):
    r = subprocess.run([sys.executable, "-P", tool, "--files", src, "--black-transparent", "--keep-geometry",
                        "--first-id", str(first_id), "--out", out], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"{first_id} {src}: {r.stdout}{r.stderr}")


def cmd_png(repo):
    check()
    tool = os.path.join(repo, "scripts", "anchor-art-frames.py")
    vendor = os.path.join(repo, "player-package", "vendor", "shattered-legacy-art")
    for k, what, folder, fname, credit, fmt in GUMPS:
        convert(tool, os.path.join(folder, fname), GUMP_ID[k], os.path.join(vendor, "gumps"))
    for aid, stock, f, what in art_rows():
        convert(tool, os.path.join(SCROLLS, f), aid, os.path.join(vendor, "art"))
    print("converted %d gumps and %d art" % (len(GUMPS), len(art_rows())))


def manifest():
    kinds = [{"key": k, "label": label, "space": space} for k, label, space in KINDS]
    skins = [{"kind": kind, "key": key, "label": label, "author": who,
              "map": {str(stock): GUMP_ID[piece] for stock, piece in sorted(m.items())}}
             for kind, key, label, who, m in SKINS]
    skins.append({"kind": "scroll", "key": "magic-scrolls", "label": "Magic Scrolls", "author": "CorvaeOboro",
                  "map": {str(stock): aid for aid, stock, f, what in art_rows()}})
    return {"comment": "cc-P362: optional UI skins. map: stock ID -> our ID (gump IDs, or art IDs for the scroll kind). "
                       "Written by shard-migration notes/cc-P362-tools/skins.py; the client's copy is SlSkins.cs.",
            "kinds": kinds, "skins": skins}


def csharp(m):
    lines = []
    for s in m["skins"]:
        pairs = ", ".join(f"[{k}] = {v}" for k, v in s["map"].items())
        lines.append(f'            new("{s["kind"]}", "{s["key"]}", "{s["label"]}", "{s["author"]}", new Dictionary<uint, uint> {{ {pairs} }}),')
    return "\n".join(lines)


def cmd_manifest(path, cs_out):
    check()
    m = manifest()
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(m, f, indent=2)
        f.write("\n")
    with open(cs_out, "w", encoding="utf-8", newline="\n") as f:
        f.write(csharp(m) + "\n")
    print("wrote %s (%d skins) and %s" % (path, len(m["skins"]), cs_out))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "registry":
        cmd_registry(sys.argv[2])
    elif cmd == "png":
        cmd_png(sys.argv[2])
    elif cmd == "manifest":
        cmd_manifest(sys.argv[2], sys.argv[3])
    elif cmd == "check":
        check(); print("ok", GUMP_ID)
