"""cc-P243: the League Hall's decor art, IDs 15592-15629 (0x3CE8-0x3D0D).

    python -P hall_art.py registry <registry.csv>       append the 38 rows (before any PNG); refuses a taken ID
    python -P hall_art.py png <ShatteredLegacy repo>    convert each BMP through scripts\\anchor-art-frames.py
    python -P hall_art.py records <records.json>        append the 38 tiledata records (as lines; the hand layout kept)

Three community sets, none with a stated license (each folder's SOURCE.txt; Chase 2026-10-21: use them, credit the
authors in the credits list):
  RedRooster's display cases   his own drawing: a shelf and a glass insert per case, which dye apart
  Hestia's statues             rendered garden statues, not EA art
  Hestia's trophies            creature heads on plaques: EA-derived (her SOURCE.txt: stock-creature trophies likely are)
  Archaaz's trophies and heads "using existing art" (his own words): EA-derived
The EA-derived pieces ship as the earlier EA-derived sets do (cc-P140's crow, registry 2071): only as our own PNG
override inside the player package, never as an EA file or part of one.

Pixels: converting BMP to PNG and making pure black transparent (scripts\\anchor-art-frames.py --black-transparent
--keep-geometry: the author placed the art on the canvas for a tile already). Nothing else is changed.
"""
import csv
import io
import json
import os
import subprocess
import sys

TP = r"D:\UO\third-party"
CASES = os.path.join(TP, "display-cases", "Rooster's Display Case's V.1.0")
HESTIA = os.path.join(TP, "hestia-trophies", "Statue, Trophys")
ARCH = os.path.join(TP, "trophies-heads", "Trophies")

ROOSTER = ("RedRooster (Steven Armstrong)", '"Rooster\'s Display Cases" V.1.0 (servuo.dev 1555)',
           "none stated; community work: credit RedRooster in the shard credits (he asks to be listed), ship only "
           "inside the player package or the private repo, do not repost (D:\\UO\\third-party\\display-cases\\SOURCE.txt)")
HESTIA_STATUE = ("Hestia", '"Trophys and Statues" (servuo.dev 1804)',
                 "none stated; community work: credit Hestia in the shard credits, ship only inside the player package "
                 "or the private repo, do not repost (D:\\UO\\third-party\\hestia-trophies\\SOURCE.txt; Chase 2026-10-21)")
HESTIA_TROPHY = ("Hestia", '"Trophys and Statues" (servuo.dev 1804)',
                 "none stated; community work: credit Hestia in the shard credits, ship only inside the player package "
                 "or the private repo, do not repost; EA-derived (a stock creature on a plaque): ships only as our PNG "
                 "override, never as an EA file (D:\\UO\\third-party\\hestia-trophies\\SOURCE.txt; Chase 2026-10-21)")
ARCHAAZ = ("Archaaz", '"New Trophies and Heads" (servuo.dev 1428)',
           "none stated; community work: credit Archaaz in the shard credits, ship only inside the player package or "
           "the private repo, do not repost; EA-derived (built from existing art, his words): ships only as our PNG "
           "override, never as an EA file (D:\\UO\\third-party\\trophies-heads\\SOURCE.txt; Chase 2026-10-21)")

# OSI's records each kind copies (read from the client's tiledata.mul 2026-10-21):
#   bookcase 0xA97: Impassable | ArticleA (| Container, not ours: a case holds nothing), height 12
#   statue 0x1224: ArticleA, plus Impassable as cc-P34's statue, height 20 as cc-P34's
#   trophy 0x1E60: ArticleA, height 0 (it hangs on the wall, nothing walks into it)
SHELF = (0x4040, 12)
INSERT = (0x4000, 0)
INSERT_PH = (0x44000, 0)   # PartialHue: the author made Book 5 and 6 partial hue
STATUE = (0x4040, 20)
TROPHY = (0x4000, 0)
HEAD = (0x4000, 2)

# (id, our tiledata name <= 19 ASCII, what, folder, file, credit, (flags, height))
PIECES = [
    (15592, "display case", "display case shelf, facing south", CASES, "Shelf1.bmp", ROOSTER, SHELF),
    (15593, "display case", "display case shelf, facing east", CASES, "Shelf2.bmp", ROOSTER, SHELF),
    (15594, "case of books", "display case insert: books, facing south", CASES, "Book 1.bmp", ROOSTER, INSERT),
    (15595, "case of books", "display case insert: books, facing east", CASES, "Book 2.bmp", ROOSTER, INSERT),
    (15596, "case of books", "display case insert: books, partial hue, facing south", CASES, "Book 5 ph.bmp", ROOSTER, INSERT_PH),
    (15597, "case of books", "display case insert: books, partial hue, facing east", CASES, "Book 6 ph.bmp", ROOSTER, INSERT_PH),
    (15598, "case of gems", "display case insert: gems, facing south", CASES, "GEM1.bmp", ROOSTER, INSERT),
    (15599, "case of gems", "display case insert: gems, facing east", CASES, "GEM2.bmp", ROOSTER, INSERT),
    (15600, "glass case", "display case insert: plain glass, facing south", CASES, "GlassInsert1.bmp", ROOSTER, INSERT),
    (15601, "glass case", "display case insert: plain glass, facing east", CASES, "GlassInsert2.bmp", ROOSTER, INSERT),
    (15602, "dragon statue", "statue: winged dragon, facing south", os.path.join(HESTIA, "Statues"), "Statue 1a.bmp", HESTIA_STATUE, STATUE),
    (15603, "dragon statue", "statue: winged dragon, facing east", os.path.join(HESTIA, "Statues"), "Statue 1b.bmp", HESTIA_STATUE, STATUE),
    (15604, "dragon statue", "statue: dark dragon, facing south", os.path.join(HESTIA, "Statues"), "Statue 2a.bmp", HESTIA_STATUE, STATUE),
    (15605, "dragon statue", "statue: dark dragon, facing east", os.path.join(HESTIA, "Statues"), "Statue 2b.bmp", HESTIA_STATUE, STATUE),
    (15606, "dragon statue", "statue: jeweled dragon (one facing)", os.path.join(HESTIA, "Statues"), "Statue 5a.bmp", HESTIA_STATUE, STATUE),
    (15607, "gargoyle statue", "statue: grinning gargoyle (one facing)", os.path.join(HESTIA, "Statues"), "Statue 6a.bmp", HESTIA_STATUE, STATUE),
    (15608, "minotaur trophy", "wall trophy: minotaur, north wall", HESTIA, "Trophy Minotaur 1b.bmp", HESTIA_TROPHY, TROPHY),
    (15609, "minotaur trophy", "wall trophy: minotaur, west wall", HESTIA, "Trophy Minotaur 1a.bmp", HESTIA_TROPHY, TROPHY),
    (15610, "sabertooth trophy", "wall trophy: sabertooth, north wall", HESTIA, "Trophy Sabertooth 1b.bmp", HESTIA_TROPHY, TROPHY),
    (15611, "sabertooth trophy", "wall trophy: sabertooth, west wall", HESTIA, "Trophy Sabertooth 1a.bmp", HESTIA_TROPHY, TROPHY),
    (15612, "troglodyte trophy", "wall trophy: troglodyte, north wall", HESTIA, "Trophy Troglodyte 1a.bmp", HESTIA_TROPHY, TROPHY),
    (15613, "troglodyte trophy", "wall trophy: troglodyte, west wall", HESTIA, "Trophy Troglodyte 1b.bmp", HESTIA_TROPHY, TROPHY),
    (15614, "skull trophy", "wall trophy: skull, north wall", HESTIA, "Trophy Skull 1b.bmp", HESTIA_TROPHY, TROPHY),
    (15615, "skull trophy", "wall trophy: skull, west wall", HESTIA, "Trophy Skull 1a.bmp", HESTIA_TROPHY, TROPHY),
    (15616, "titan trophy", "wall trophy: titan, north wall", ARCH, "Titan Trophy 2.bmp", ARCHAAZ, TROPHY),
    (15617, "titan trophy", "wall trophy: titan, west wall", ARCH, "Titan Trophy 1.bmp", ARCHAAZ, TROPHY),
    (15618, "oni trophy", "wall trophy: oni, north wall", ARCH, "Oni Trophy 1.bmp", ARCHAAZ, TROPHY),
    (15619, "oni trophy", "wall trophy: oni, west wall", ARCH, "Oni Trophy 2.bmp", ARCHAAZ, TROPHY),
    (15620, "ophidian trophy", "wall trophy: ophidian matriarch, north wall", ARCH, "Ophidian Matriarch Trophy 2.bmp", ARCHAAZ, TROPHY),
    (15621, "ophidian trophy", "wall trophy: ophidian matriarch, west wall", ARCH, "Ophidian Matriarch Trophy 1.bmp", ARCHAAZ, TROPHY),
    (15622, "terathan trophy", "wall trophy: terathan matriarch, north wall", ARCH, "Terathan Matriarch Trophy 1.bmp", ARCHAAZ, TROPHY),
    (15623, "terathan trophy", "wall trophy: terathan matriarch, west wall", ARCH, "Terathan Matriarch Trophy 2.bmp", ARCHAAZ, TROPHY),
    (15624, "paroxysmus trophy", "wall trophy: paroxysmus, north wall", ARCH, "Paroxsymus Trophy 2.bmp", ARCHAAZ, TROPHY),
    (15625, "paroxysmus trophy", "wall trophy: paroxysmus, west wall", ARCH, "Paroxsymus  Trophy 1.bmp", ARCHAAZ, TROPHY),
    (15626, "titan head", "mounted head: titan, facing south", ARCH, "Titan Head 1.bmp", ARCHAAZ, HEAD),
    (15627, "titan head", "mounted head: titan, facing east", ARCH, "Titan Head 2.bmp", ARCHAAZ, HEAD),
    (15628, "oni head", "mounted head: oni, facing south", ARCH, "Oni Head 1.bmp", ARCHAAZ, HEAD),
    (15629, "oni head", "mounted head: oni, facing east", ARCH, "Oni Head 2.bmp", ARCHAAZ, HEAD),
]


def check():
    ids = [p[0] for p in PIECES]
    assert ids == list(range(15592, 15630)), ids
    for p in PIECES:
        assert len(p[1]) <= 19 and p[1].isascii(), p[1]
        assert os.path.isfile(os.path.join(p[3], p[4])), p


def cmd_registry(path):
    check()
    with open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    taken = {line.split(",", 1)[0] for line in text.splitlines() if line and not line.startswith("#")}
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    for gid, name, what, folder, fname, (author, pack, terms), _ in PIECES:
        if str(gid) in taken:
            sys.exit(f"{gid} is already registered")
        w.writerow([str(gid), f"0x{gid:04X}", f"League Hall decor (cc-P243): {what}",
                    f"{author}, {pack}: {fname}; black made transparent, nothing else changed", f"{terms}", "art"])
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text if text.endswith("\n") else text + "\n")
        f.write(buf.getvalue())
    print(f"appended {len(PIECES)} rows")


def cmd_png(repo):
    check()
    tool = os.path.join(repo, "scripts", "anchor-art-frames.py")
    out = os.path.join(repo, "player-package", "vendor", "shattered-legacy-art", "art")
    for gid, name, what, folder, fname, credit, _ in PIECES:
        r = subprocess.run([sys.executable, "-P", tool, "--files", os.path.join(folder, fname), "--black-transparent",
                            "--keep-geometry", "--first-id", str(gid), "--out", out], capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit(f"{gid} {fname}: {r.stdout}{r.stderr}")
        print(gid, fname, "->", r.stdout.strip().splitlines()[0])


def cmd_records(path):
    check()
    with open(path, encoding="utf-8") as f:
        text = f.read()
    rec = json.loads(text)
    have = {int(t["id"]) for t in rec["tiledata"]}
    lines = []
    for gid, name, what, folder, fname, credit, (flags, height) in PIECES:
        assert gid not in have, gid
        lines.append(f'    {{ "id": {gid}, "name": "{name}", "flags": "0x{flags:08X}", "weight": 255, "layer": 0, '
                     f'"count": 0, "animId": 0, "hue": 0, "light": 0, "height": {height} }}')
    head = text.index('  "tiledata": [')
    close = text.index("\n  ]", head)
    text = text[:close] + ",\n" + ",\n".join(lines) + text[close:]
    assert len(json.loads(text)["tiledata"]) == len(rec["tiledata"]) + len(PIECES)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print(f"appended {len(PIECES)} tiledata records")


if __name__ == "__main__":
    {"registry": cmd_registry, "png": cmd_png, "records": cmd_records}[sys.argv[1]](sys.argv[2])
