"""cc-P363: quest markers, gem tokens and quest keys, and four coloured moongates, IDs 46592-46663 (0xB600-0xB647).

    python -P p363_art.py registry <registry.csv>           append the 72 rows (before any PNG); refuses a taken ID
    python -P p363_art.py png <src> <ShatteredLegacy repo>  convert each BMP through scripts\\anchor-art-frames.py
    python -P p363_art.py records <records.json>            append the tiledata and animdata records (as lines)

<src> is a copy of the packs, made first (the prompt: never build or run from D:\\UO\\third-party), laid out as
    <src>\\quest-markers\\E1.bmp ...           D:\\UO\\third-party\\quest-markers\\Quest Marker\\
    <src>\\token-keys\\<gem> Token.bmp ...     D:\\UO\\third-party\\token-keys\\Quest or Item Key and Tokens\\
    <src>\\token-keys\\Quest or Item Keys\\... the same folder's key subfolder
    <src>\\moongate-<colour>\\*.bmp            D:\\UO\\third-party\\moongate-<colour>\\

Three community sets (each folder's SOURCE.txt):
  RedRooster's quest markers   "!" E1-E3 and "?" Q1-Q3, three frames each, 1,2,3,2 at frame rate 3 (his words). No terms;
                               credit him in the shard credits, which he asks for.
  Hestia's tokens and keys     12 gem tokens and 34 keys: "use however you want, drops, gate keys, items keys".
  Carl Hamilton's moongates    blue, red, black, white, five frames each. Made to replace OSI's moongate images: here
                               they are NEW IDs, and OSI's moongates (0xF6C, 0xDDA, 0x1FD4 and their frames) are untouched.
None is EA-derived or ripped.

Pixels: BMP to PNG with pure black transparent. The tokens, keys and gates keep their canvas (--keep-geometry): each
author drew them for a tile already. The markers are cut to the union of their frames and stood 92 pixels above the
tile's front tip (--bottom-pad 92): the pack's canvas puts the mark 60 pixels up, on a person's chest; drawn as an
effect on an NPC (QuestMarkers.cs) the mark must clear the head. Nothing else is changed.
"""
import csv
import io
import json
import os
import subprocess
import sys

FIRST = 46592

MARKER = ("RedRooster (Steven Armstrong)", '"Quest Markers" (servuo.dev 1823)',
          "none stated; community work: credit RedRooster in the shard credits (he asks to be listed), ship only inside "
          "the player package or the private repo, do not repost (D:\\UO\\third-party\\quest-markers\\SOURCE.txt)")
HESTIA = ("Hestia", '"Quest, Item, Token Keys" (servuo.dev 1809)',
          "use however you want, drops, gate keys, items keys (the author's page); credit Hestia in the shard credits, "
          "ship only inside the player package or the private repo (D:\\UO\\third-party\\token-keys\\SOURCE.txt)")


def carl(colour, n):
    return ("Carl Hamilton", f'"NEW {colour} Spinning Moongate" (servuo.dev {n})',
            "none stated; community work: credit Carl Hamilton in the shard credits, ship only inside the player package "
            "or the private repo, do not repost; made to replace OSI's moongate, registered here under NEW IDs "
            f"(D:\\UO\\third-party\\moongate-{colour.lower()}\\SOURCE.txt)")


# Tiledata. Only an animation's base ID has a record (Build-UoOverrides.ps1 skips an animation whose other frames
# have records of their own). Read from the client's tiledata.mul 2026-10-23:
#   blue moongate 0xF6C: 0x05804000 (ArticleA | LightSource | Animation | 0x04000000), weight 255, height 0
#   copper key 0x100E: ArticleA, weight 1, height 1
ANIM_MARK = (0x01000000, 255, 0)   # Animation: an effect drawn over an NPC, never placed
GATE = (0x05804000, 255, 0)
TOKEN = (0x00004000, 1, 1)
KEY = (0x00004000, 1, 1)
KEY_PH = (0x00044000, 1, 1)        # the author's "Blank Partial Hue" key
# Animdata (frame offsets from the base, interval): the markers 1,2,3,2 at 3 (RedRooster's words); the gates spin
# 1-5 at 2, a turn of the vortex per second (OSI's moongates swing 0..4..0 at 3 and 4; these are drawn as one turn).
ANIM_MARK_FRAMES = ([0, 1, 2, 1], 3)
GATE_FRAMES = ([0, 1, 2, 3, 4], 2)

TOKENS = ["Amber  Token", "Amethyst Token", "Citrine  Token", "Diamond Token", "Emerald Token", "Opal Token",
          "Pearl Token", "Rose Quartz  Token", "Ruby Token", "Sapphire Token", "Star Sapphire Token", "Tourmaline Token"]
GATES = [("blue", "Blue", 2309), ("red", "Red", 2310), ("black", "Black", 2312), ("white", "White", 2313)]

# (id, tiledata name or None, what, relative file, credit, record or None, animdata or None, group)
PIECES = []


def add(name, what, rel, credit, record, anim, group):
    PIECES.append((FIRST + len(PIECES), name, what, rel, credit, record, anim, group))


for mark, label, files in (("!", "a quest to offer", "E"), ("?", "a quest ready to turn in", "Q")):
    for i in (1, 2, 3):
        base = i == 1
        add("quest marker" if base else None, f'quest marker "{mark}" ({label}), frame {i} of 3' + (" (base ID)" if base else ""),
            os.path.join("quest-markers", f"{files}{i}.bmp"), MARKER, ANIM_MARK if base else None,
            ANIM_MARK_FRAMES if base else None, "marker")
for colour, Colour, n in GATES:
    for i in range(1, 6):
        base = i == 1
        add(f"{colour} moongate" if base else None, f"{colour} spinning moongate, frame {i} of 5" + (" (base ID)" if base else ""),
            os.path.join(f"moongate-{colour}", f"{Colour} Spinning Portal {i}.bmp"), carl(Colour, n),
            GATE if base else None, GATE_FRAMES if base else None, "gate")
for t in TOKENS:
    gem = " ".join(t.split()[:-1]).lower()
    add(f"{gem} token", f"gem token: {gem}", os.path.join("token-keys", f"{t}.bmp"), HESTIA, TOKEN, None, "token")
for i in range(1, 35):
    f = "Item Key 1 Blank Partial Hue.bmp" if i == 1 else f"Item Key {i}.bmp"
    add("quest key", f"quest key {i}" + (" (blank, partial hue)" if i == 1 else ""),
        os.path.join("token-keys", "Quest or Item Keys", f), HESTIA, KEY_PH if i == 1 else KEY, None, "key")


def check(src=None):
    ids = [p[0] for p in PIECES]
    assert ids == list(range(46592, 46664)), (ids[0], ids[-1], len(ids))
    for p in PIECES:
        assert p[1] is None or (len(p[1]) <= 19 and p[1].isascii()), p[1]
        if src:
            assert os.path.isfile(os.path.join(src, p[3])), p


def cmd_registry(path):
    check()
    with open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    taken = {line.split(",", 1)[0] for line in text.splitlines() if line and not line.startswith("#")}
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    for gid, name, what, rel, (author, pack, terms), rec, anim, group in PIECES:
        if str(gid) in taken:
            sys.exit(f"{gid} is already registered")
        w.writerow([str(gid), f"0x{gid:04X}", f"cc-P363 {what}",
                    f"{author}, {pack}: {os.path.basename(rel)}; black made transparent"
                    + ("; cut to the frames' union and stood 92 px up (--bottom-pad 92)" if group == "marker" else ", nothing else changed"),
                    terms, "art"])
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text if text.endswith("\n") else text + "\n")
        f.write(buf.getvalue())
    print(f"appended {len(PIECES)} rows")


def run(tool, files, first, out, keep):
    args = [sys.executable, "-P", tool, "--files", *files, "--black-transparent", "--first-id", str(first), "--out", out]
    args += ["--keep-geometry"] if keep else ["--bottom-pad", "92"]
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"{first}: {r.stdout}{r.stderr}")
    print(first, len(files), "->", r.stdout.strip().splitlines()[0] if r.stdout.strip() else "")


def cmd_png(src, repo):
    check(src)
    tool = os.path.join(repo, "scripts", "anchor-art-frames.py")
    out = os.path.join(repo, "player-package", "vendor", "shattered-legacy-art", "art")
    # The markers go as one run per mark, so all three frames share one cut and stay registered on each other.
    for start in (0, 3):
        run(tool, [os.path.join(src, p[3]) for p in PIECES[start:start + 3]], PIECES[start][0], out, False)
    for p in PIECES[6:]:
        run(tool, [os.path.join(src, p[3])], p[0], out, True)


def cmd_records(path):
    check()
    with open(path, encoding="utf-8") as f:
        text = f.read()
    rec = json.loads(text)
    have = {int(t["id"]) for t in rec["tiledata"]} | {int(a["id"]) for a in rec["animdata"]}
    tiles, anims = [], []
    for gid, name, what, rel, credit, record, anim, group in PIECES:
        assert gid not in have, gid
        if record:
            flags, weight, height = record
            tiles.append(f'    {{ "id": {gid}, "name": "{name}", "flags": "0x{flags:08X}", "weight": {weight}, "layer": 0, '
                         f'"count": 0, "animId": 0, "hue": 0, "light": 0, "height": {height} }}')
        if anim:
            frames, interval = anim
            anims.append(f'    {{ "id": {gid}, "frames": [{", ".join(str(x) for x in frames)}], "interval": {interval}, "start": 0 }}')
    for key, lines in (("tiledata", tiles), ("animdata", anims)):
        head = text.index(f'  "{key}": [')
        close = text.index("\n  ]", head)
        text = text[:close] + ",\n" + ",\n".join(lines) + text[close:]
    out = json.loads(text)
    assert len(out["tiledata"]) == len(rec["tiledata"]) + len(tiles)
    assert len(out["animdata"]) == len(rec["animdata"]) + len(anims)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print(f"appended {len(tiles)} tiledata and {len(anims)} animdata records")


if __name__ == "__main__":
    {"registry": lambda: cmd_registry(sys.argv[2]), "png": lambda: cmd_png(sys.argv[2], sys.argv[3]),
     "records": lambda: cmd_records(sys.argv[2])}[sys.argv[1]]()
