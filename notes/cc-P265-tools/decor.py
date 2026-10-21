"""cc-P265: the guild hall decor packs, IDs 0x6D70 on (28016 on), registered for the halls but placed nowhere.

    python -P decor.py check                       every source file exists, IDs are a free consecutive block
    python -P decor.py registry <registry.csv>     append one row per ID (before any PNG); refuses a taken ID
    python -P decor.py png <ShatteredLegacy repo>  convert every source through scripts\\anchor-art-frames.py
    python -P decor.py records <records.json>      append the tiledata and animdata records (as lines)
    python -P decor.py cs <ShatteredLegacy repo>   write server\\customizations\\GuildHallDecorArt.cs (generated)
    python -P decor.py table                       the piece table for the notes (markdown)

The packs (D:\\UO\\third-party, art library section 5 "Guild halls"; each folder's SOURCE.txt):
  Order of the Alembic  bubble-vat (Hestia), creature-tanks (RedRooster, CREDIT), partialhue-flasks (Ems, EA),
                        rooster-crystal-ball (RedRooster, CREDIT)
  Society of Smiths     blacksmith-shop (Apocalypse, EA), mrriots-firepit (MrRiots)
  Artificers            floating-crystals (MrRiots), arc-orb-fx (otimpyre)
  Hall structure        marble-railings (OUTLANDSOwyn), hestia-large/medium/small/white-brick/white-column-tower (Hestia)

Pixels: format, and the background made transparent, nothing else. A black-background BMP goes through
anchor-art-frames.py --black-transparent (pure black (0,0,0) only, as cc-P34). Six sources were drawn on pure white
instead (the large tower's top and turret, the white towers' domes, the arc orb gate, the blacksmith): for those, the
white connected to the image border is made transparent (a flood fill of pure (255,255,255) from the edge; white inside
the art is kept), written to a staging PNG, and that PNG goes through the same tool. Every canvas is kept as its author
drew it (--keep-geometry): the authors placed the art for a tile.

Records copy a named OSI tile read from the client's tiledata.mul (D:\\UO\\tool-trials\\client-data-copy, 2026-10-21),
or the author's own recommendation (RedRooster's two .txt files), as each row says. Animated pieces: the base ID has the
tiledata record (with Animation) and the animdata; its frames are the IDs that follow it, registered, with no record.
"""
import csv
import io
import json
import os
import shutil
import subprocess
import sys

import numpy as np
from PIL import Image

TP = r"D:\UO\third-party"
FIRST = 0x6D70

# TileFlag bits (pinned Server/TileData.cs).
TRANSP, TRANSL, WALL, IMP, SURF, BRIDGE, NOSHOOT = 0x4, 0x8, 0x10, 0x40, 0x200, 0x400, 0x2000
ART_A, ART_AN, PH, LIGHT, ANIM, UNK3, ROOF = 0x4000, 0x8000, 0x40000, 0x800000, 0x1000000, 0x4000000, 0x10000000


def pack(folder, author, title, url, terms, ea=None):
    return dict(folder=folder, author=author, title=title, url=url, terms=terms, ea=ea)


COMMUNITY = ("none stated; community work: credit {a} in the shard credits, ship only inside the player package or "
             "the private repo, do not repost")
VAT = pack("bubble-vat", "Hestia", '"Hueable Anim Bubble Vat"', "https://www.servuo.dev/archive/hueable-anim-bubble-vat.2145/", COMMUNITY.format(a="Hestia"))
TANKS = pack("creature-tanks", "RedRooster", '"Rooster\'s Creature Tank\'s"', "https://www.servuo.dev/archive/roosters-creature-tanks.1999/",
             "CREDIT: RedRooster asks to be added to the shard credits list (his page); otherwise none stated, ship "
             "only inside the player package or the private repo, do not repost")
FLASKS = pack("partialhue-flasks", "Ems", '"Partialhue flasks"', "https://www.servuo.dev/archive/partialhue-flasks.1995/", COMMUNITY.format(a="Ems"),
              ea="EA-derived (partial-hue edits of EA flask art, the files named by stock item IDs): ships only as our "
                 "PNG override, never as an EA file")
BALL = pack("rooster-crystal-ball", "RedRooster", '"Rooster\'s Crystal Ball" 1.0', "https://www.servuo.dev/archive/roosters-crystal-ball.2000/",
            "CREDIT: RedRooster asks to be added to the shard credits list (his page); otherwise none stated, ship "
            "only inside the player package or the private repo, do not repost")
SMITH = pack("blacksmith-shop", "Apocalypse", '"Shop Additions: Blacksmith"', "https://www.servuo.dev/archive/shop-additions-blacksmith.986/",
             COMMUNITY.format(a="Apocalypse"),
             ea="EA-derived (frames cut from the EA human body 400 animation, its file names say so): ships only as "
                "our PNG override, never as an EA file")
FIREPIT = pack("mrriots-firepit", "MrRiots", '"[MrRiots] New Firepit"', "https://www.servuo.dev/archive/mrriots-new-firepit.2098/",
               '"Use and edit as you wish" (his page): credit MrRiots, ship inside the player package, do not repost '
               "the raw files")
CRYSTALS = pack("floating-crystals", "MrRiots", '"[MrRiots] Floating Crystals (Lightsource)"', "https://www.servuo.dev/archive/mrriots-floating-crystals-lightsource.2317/",
                '"Use them as you please" (his page): credit MrRiots')
ORB = pack("arc-orb-fx", "otimpyre", '"Arc-Orb FX"', "https://www.servuo.dev/archive/arc-orb-fx.94/",
           COMMUNITY.format(a="otimpyre") + " (he shares his source files for remixing)")
RAILS = pack("marble-railings", "OUTLANDSOwyn (Outlands)", '"Marble Railings, Bannisters, Ladder"', "https://www.servuo.dev/archive/marble-railings-bannisters-ladder.2663/",
             '"Feel free to use them in your own projects ... Please credit Outlands if you use these assets." (his '
             "page, read 2026-10-21): credit Outlands in the shard credits, ship inside the player package",
             ea='EA-derived ("based on the existing wooden assets", his words: marble recolours of OSI\'s wooden '
                "rails): ships only as our PNG override, never as an EA file")


def hestia(folder, title, url):
    return pack(folder, "Hestia", title, url, COMMUNITY.format(a="Hestia"))


LARGE = hestia("hestia-large-brick-tower", '"Large Brick Tower"', "https://www.servuo.dev/archive/large-brick-tower.2498/")
MEDIUM = hestia("hestia-medium-brick-tower", '"Medium Brick Tower"', "https://www.servuo.dev/archive/medium-brick-tower.2497/")
SMALL = hestia("hestia-small-brick-tower", '"Small Brick Tower"', "https://www.servuo.dev/archive/small-brick-tower.2496/")
WBRICK = hestia("hestia-white-brick-tower", '"White Brick Tower Large"', "https://www.servuo.dev/archive/white-brick-tower-large.2504/")
WCOL = hestia("hestia-white-column-tower", '"White Column Tower Large"', "https://www.servuo.dev/archive/white-column-tower-large.2505/")

# Records: (flags, height, weight, light) and where they come from.
R_VAT = (PH | IMP | ART_A, 8, 255, 0, "OSI's vat 0x1550 (Impassable | ArticleA, height 8), plus PartialHue: the pack "
         "is hueable, its liquid is grey (Hestia)")
R_STAND = (IMP | ART_A, 5, 255, 0, "RedRooster's own recommendation (Impassable, height 5), ArticleA")
R_TANK = (ANIM | ART_A, 5, 255, 0, "RedRooster's own recommendation (Animation on the first frame, height 5), ArticleA")
R_FLASK = (PH | ART_A, 1, 1, 0, "OSI's flask 0x182A (ArticleA, weight 1, height 1), plus PartialHue as Ems made them")
R_CLOTH = (ART_A, 1, 255, 0, "RedRooster's own recommendation (height 1, no flags), ArticleA")
R_BALL_OFF = (TRANSL | PH | ANIM | ART_A, 1, 10, 0, "RedRooster's recommendation (Translucent | PartialHue | "
              "Animation, height 1), weight 10 as OSI's crystal ball 0xE2D")
R_BALL_ON = (TRANSL | PH | ANIM | LIGHT | ART_A, 1, 10, 2, "as the unlit ball, plus LightSource and light 2 as OSI's "
             "lit crystal ball 0xE2E")
R_SMITH = (ANIM | PH | IMP | ART_A, 15, 255, 0, "Apocalypse's description (Animation | PartialHue: the skin takes "
           "a hue); ours: Impassable, height 15 (a standing figure), ArticleA")
R_PIT_LIT = (ANIM | LIGHT | NOSHOOT | SURF | IMP | ART_A, 0, 255, 0, "OSI's fire pit 0x29FD (0x01806240, height "
             "0), as cc-P34's raised firepit")
R_PIT_COLD = (NOSHOOT | SURF | IMP | ART_A, 0, 255, 0, "OSI's fire pit 0x29FD without Animation and LightSource")
R_PILLAR = (IMP | ART_A, 17, 255, 0, "OSI's brazier 0x19AA (Impassable | ArticleA, height 17) without LightSource")
R_CRYSTAL = (ANIM | LIGHT | IMP | ART_A, 17, 255, 1, "OSI's brazier 0x19AA (LightSource | Impassable | ArticleA, "
             "light 1, height 17), plus Animation (MrRiots: added as light sources)")
R_ORB_GATE = (ANIM | LIGHT | ART_AN, 0, 255, 29, "OSI's blue moongate 0xF6C (Animation | LightSource, light 29, "
              "height 0) without Unknown3, ArticleAn")
R_ORB_FLOOR = R_ORB_GATE[:4] + ("as the arc orb gate (OSI's moongate 0xF6C): walk-through, lit",)
R_ORB_ITEM = (ANIM | LIGHT | ART_AN, 1, 10, 2, "OSI's lit crystal ball 0xE2E (Animation | LightSource, light 2, "
              "weight 10, height 1), ArticleAn")
R_RAIL = (IMP | TRANSP | ART_A, 5, 255, 0, "OSI's wooden banister 0x08AE and wooden rail 0x087E (both Impassable | "
          "Transparent | ArticleA, height 5), as cc-P237's railings")
R_LADDER = (BRIDGE | SURF | ART_A, 35, 20, 0, "OSI's tall ladder 0x2FDE (Bridge | Surface | ArticleA, weight 20, "
            "height 35)")
R_TWALL = (IMP | WALL | NOSHOOT | ART_A, 20, 255, 0, "OSI's stone wall 0x001B (Impassable | Wall | NoShoot | "
           "ArticleA, height 20)")
R_TTOP = (ROOF | ART_A, 0, 255, 0, "ours: Roof | ArticleA, height 0 (it sits on the walls; TazUO hides roofs over "
          "the player)")
R_TCAP = (ROOF | PH | ART_A, 0, 255, 0, "ours: Roof | ArticleA, height 0, plus PartialHue (Hestia: a hueable turret)")

ANIM_VAT = ([0, 1, 2, 3], 3, "ours: the pack gives no timing (4 frames, interval 3, as RedRooster's tanks)")


def bmp(folder, *rel):
    return os.path.join(TP, folder, *rel)


PIECES = []   # dict: key, guild, name, what, files [base, frames...], rec, anim, pack


def add(key, guild, name, what, files, rec, src, anim=None):
    PIECES.append(dict(key=key, guild=guild, name=name, what=what, files=files, rec=rec, anim=anim, pack=src))


# ---------------------------------------------------------------- Order of the Alembic
V = ("bubble-vat", "Anim water vat hue")
for n in range(1, 9):
    add(f"vat-{n}", "alembic", "bubbling vat", f"bubbling vat, part {n} of 9 (4 frames)",
        [bmp(*V, f"bubble vat {n}{c}.bmp") for c in "abcd"], R_VAT, VAT, ANIM_VAT)
add("vat-front", "alembic", "bubbling vat", "bubbling vat, the hueable front band (part 9 of 9)",
    [bmp(*V, "Vat Hue 1i.bmp")], R_VAT, VAT)

T = ("creature-tanks", "Rooster'sCreatureCages")
add("stand-s1", "alembic", "tank stand", "tank stand, south facing, east half", [bmp(*T, "0.TankStand", "TankStandS1.bmp")], R_STAND, TANKS)
add("stand-s2", "alembic", "tank stand", "tank stand, south facing, west half", [bmp(*T, "0.TankStand", "TankStandS2.bmp")], R_STAND, TANKS)
add("stand-e1", "alembic", "tank stand", "tank stand, east facing, south half", [bmp(*T, "0.TankStand", "TankStandE1.bmp")], R_STAND, TANKS)
add("stand-e2", "alembic", "tank stand", "tank stand, east facing, north half", [bmp(*T, "0.TankStand", "TankStandE2.bmp")], R_STAND, TANKS)
# (folder, file stem, frame count, RedRooster's frames (1-based), his frame delay)
CREATURES = [("Fish", "Fish ", 4, [1, 2, 3, 4], 3), ("Frog", "Frog", 3, [1, 2, 3, 2, 1, 2, 1, 2], 3),
             ("Hamster", "Hamster", 2, [1, 2], 2), ("Lobster", "lobster", 2, [1, 2], 3),
             ("Scorpion", "scorpion", 2, [1, 1, 1, 1, 1, 2], 3), ("Snake", "snake", 2, [1, 2], 1),
             ("Tarantula", "Tarantula", 2, [1, 2], 3), ("Turtle", "Turtle ", 2, [1, 1, 1, 1, 2], 3)]
for folder, stem, count, seq, delay in CREATURES:
    for facing, way in (("South", "s"), ("East", "e")):
        add(f"tank-{folder.lower()}-{way}", "alembic", f"{folder.lower()} tank",
            f"creature tank: {folder.lower()}, {facing.lower()} facing ({count} frames)",
            [bmp(*T, folder, facing, f"{stem}{i}.bmp") for i in range(1, count + 1)], R_TANK, TANKS,
            ([s - 1 for s in seq], delay, "RedRooster's own (Tiledata.Animdata.txt)"))
for i, h in enumerate(range(0x3A9C, 0x3AA4)):
    add(f"flask-{i + 1}", "alembic", "flask", f"partial-hue flask {i + 1} of 8",
        [bmp("partialhue-flasks", f"Item 0x{h:04X}.bmp")], R_FLASK, FLASKS)
B = ("rooster-crystal-ball", "Rooster'sCrystalBall")
add("ball-cloth", "alembic", "ritual cloth", "crystal ball: the base cloth", [bmp(*B, "Base.bmp")], R_CLOTH, BALL)
add("ball-off", "alembic", "crystal ball", "crystal ball: unlit (4 frames)", [bmp(*B, f"off{i}.bmp") for i in range(1, 5)],
    R_BALL_OFF, BALL, ([0, 1, 2, 3], 4, "RedRooster's own (Teledata.animdata.txt)"))
add("ball-on", "alembic", "crystal ball", "crystal ball: lit (4 frames)", [bmp(*B, f"on{i}.bmp") for i in range(1, 5)],
    R_BALL_ON, BALL, ([0, 1, 2, 3], 4, "RedRooster's own (Teledata.animdata.txt)"))

# ---------------------------------------------------------------- Society of Smiths
add("blacksmith", "smiths", "blacksmith", "a blacksmith at work (3 frames)",
    [bmp("blacksmith-shop", f) for f in ("1.bmp", "anim1_400_11_3_2.bmp", "anim1_400_11_3_3.bmp")], R_SMITH, SMITH,
    ([0, 1, 2], 3, "ours: the pack gives no timing"))
add("firepit-lit", "smiths", "fire pit", "fire pit, burning (7 frames)",
    [bmp("mrriots-firepit", f"{i}.bmp") for i in range(1, 8)], R_PIT_LIT, FIREPIT,
    ([0, 1, 2, 3, 4, 5, 6], 2, "interval 2 as OSI's fire 0x19AB, cc-P34's fires"))
add("firepit-cold", "smiths", "fire pit", "fire pit, cold", [bmp("mrriots-firepit", "NewFirepit.bmp")], R_PIT_COLD, FIREPIT)

# ---------------------------------------------------------------- Artificers
add("crystal-pillar", "artificers", "crystal pillar", "crystal pillar, without its crystal", [bmp("floating-crystals", "Pillar.bmp")], R_PILLAR, CRYSTALS)
for colour in ("Green", "Purple"):
    add(f"crystal-{colour.lower()}", "artificers", "floating crystal", f"floating crystal: {colour.lower()} (9 frames)",
        [bmp("floating-crystals", colour, f"{i}.bmp") for i in range(1, 10)], R_CRYSTAL, CRYSTALS,
        (list(range(9)), 3, "ours: the pack gives no timing"))
O = ("arc-orb-fx", "[Custom Art] Arc Orb")
add("orb-gate", "artificers", "arc orb gate", "arc orb, gate version (9 frames)",
    [bmp(*O, "Moongate Version", f"{i}.bmp") for i in range(1, 10)], R_ORB_GATE, ORB, (list(range(9)), 2, "ours: "
    "the pack gives no timing (its GIF previews run fast)"))
add("orb-floor", "artificers", "arc orb field", "arc orb, floor version (9 frames)",
    [bmp(*O, "Floor Version", f"{i}.bmp") for i in range(1, 10)], R_ORB_FLOOR, ORB, (list(range(9)), 2, "as the gate"))
add("orb-item", "artificers", "arc orb", "arc orb, item version (9 frames)",
    [bmp(*O, "Item Version", f"{i}.bmp") for i in range(1, 10)], R_ORB_ITEM, ORB, (list(range(9)), 2, "as the gate"))

# ---------------------------------------------------------------- hall structure
# 70321 and 70324 are registered already (cc-P237: 15503 and 15504); the template uses those IDs.
RAILS_TAKEN = {70321: 15503, 70324: 15504}
for n in list(range(70290, 70360)) + [70388, 70389]:
    if n in RAILS_TAKEN:
        continue
    kind, name, rec = (("rail", "marble railing", R_RAIL) if n <= 70310 else ("banister", "marble banister", R_RAIL)
                       if n <= 70347 else ("post", "marble post", R_RAIL) if n <= 70359 else ("ladder", "marble ladder", R_LADDER))
    add(f"marble-{n}", "structure", name, f"marble {kind} (his Item-{n})",
        [bmp("marble-railings", "marblerailings", f"Item-{n}.png")], rec, RAILS)

L = ("hestia-large-brick-tower", "Large Brick Tower")
for f in ["2a", "2b", "2c", "2d", "2e", "2h", "2J", "2k", "a2f", "a2g", "a2i", "a2La", "a2ma", "a2Na", "2Q", "a2p"]:
    what = {"2Q": "large brick tower wall with a door", "a2p": "large brick tower wall with a window"}.get(f, "large brick tower wall")
    add(f"large-{f.lower()}", "structure", "brick tower", f"{what} (his DW {f})", [bmp(*L, f"DW {f}.bmp")], R_TWALL, LARGE)
add("large-top", "structure", "tower top", "large brick tower: the top floor (his temp 23a)", [bmp(*L, "temp 23a.bmp")], R_TTOP, LARGE)
add("large-turret", "structure", "tower turret", "large brick tower: the hueable turret (his temp 28)", [bmp(*L, "temp 28.bmp")], R_TCAP, LARGE)
M = ("hestia-medium-brick-tower", "Med Brick Tower")
for c in "abcdefgh":
    what = {"g": "medium brick tower wall with a window", "h": "medium brick tower wall with a door"}.get(c, "medium brick tower wall")
    add(f"medium-1{c}", "structure", "brick tower", f"{what} (his 1{c})", [bmp(*M, f"Brick tower med 1{c}.bmp")], R_TWALL, MEDIUM)
add("medium-turret", "structure", "tower turret", "medium brick tower: the turret (his i)", [bmp(*M, "Brick turret med i.bmp")], R_TCAP, MEDIUM)
S = ("hestia-small-brick-tower", "Small Brick Tower")
for f, what in [("a1b", "front"), ("a2a", "back"), ("a3", "west edge"), ("a4", "east edge"), ("a6b", "front with a window"),
                ("a8", "front with a door")]:
    add(f"small-{f}", "structure", "brick tower", f"small brick tower: {what} (his DW51 {f})", [bmp(*S, f"DW51 {f}.bmp")], R_TWALL, SMALL)
add("small-top", "structure", "tower top", "small brick tower: the crenellated top (his DW51 a7)", [bmp(*S, "DW51 a7.bmp")], R_TTOP, SMALL)
W = ("hestia-white-brick-tower", "Wht Brick Tower Lg")
for n in range(1, 13):
    what = {11: "white brick tower wall with a window", 12: "white brick tower wall with a door"}.get(n, "white brick tower wall")
    add(f"wbrick-{n}", "structure", "white tower", f"{what} (his {n})", [bmp(*W, f"Brick Wht Tower {n}.bmp")], R_TWALL, WBRICK)
add("wbrick-dome", "structure", "tower dome", "white brick tower: the hueable dome (his template 31)",
    [bmp(*W, "white tower template 31.bmp")], R_TCAP, WBRICK)
C = ("hestia-white-column-tower", "Wht Tower Columns Large")
for n in range(1, 12):
    what = "white column tower wall with a door" if n == 11 else "white column tower wall"
    add(f"wcol-{n}", "structure", "white tower", f"{what} (his {n})", [bmp(*C, f"a white tower {n}.bmp")], R_TWALL, WCOL)
add("wcol-top", "structure", "tower top", "white column tower: the top floor (his template 13)", [bmp(*C, "white tower template 13.bmp")], R_TTOP, WCOL)
add("wcol-dome", "structure", "tower dome", "white column tower: the hueable round turret (his template 22)",
    [bmp(*C, "white tower template 22.bmp")], R_TCAP, WCOL)

# ---------------------------------------------------------------- IDs
_next = FIRST
for p in PIECES:
    p["id"] = _next
    _next += len(p["files"])
LAST = _next - 1
BY_KEY = {p["key"]: p for p in PIECES}


def ids():
    for p in PIECES:
        for i, f in enumerate(p["files"]):
            yield p["id"] + i, p, i, f


def check():
    keys = [p["key"] for p in PIECES]
    assert len(keys) == len(set(keys)), "duplicate key"
    for gid, p, i, f in ids():
        assert os.path.isfile(f), f
        assert len(p["name"]) <= 19 and p["name"].isascii(), p["name"]
        if p["anim"]:
            assert max(p["anim"][0]) < len(p["files"]), p["key"]
    assert LAST < 0x71F3, hex(LAST)   # the free empty run 0x6D61-0x71F3 (find-free-art.py, 2026-10-21)


def white_background(rgb):
    w = (rgb == 255).all(2)
    border = np.concatenate([w[0], w[-1], w[:, 0], w[:, -1]])
    return border.mean() > 0.5


def unwhite(src, dst):
    """Pure white connected to the border becomes alpha 0; every other pixel is kept exactly (opaque)."""
    import cv2
    rgb = np.asarray(Image.open(src).convert("RGB"))
    w = (rgb == 255).all(2).astype(np.uint8)
    h, wd = w.shape
    mask = np.zeros((h + 2, wd + 2), np.uint8)
    for x, y in [(x, 0) for x in range(wd)] + [(x, h - 1) for x in range(wd)] + [(0, y) for y in range(h)] + \
            [(wd - 1, y) for y in range(h)]:
        if w[y, x] == 1:
            cv2.floodFill(w, mask, (x, y), 2)
    t = w == 2
    out = np.dstack([rgb, np.where(t, 0, 255).astype(np.uint8)])
    out[t, :3] = 0
    Image.fromarray(out).save(dst)


def credit(p):
    k = p["pack"]
    return f"{k['author']}, {k['title']} ({k['url']})"


def license_text(p):
    k = p["pack"]
    t = f"{k['terms']} (D:\\UO\\third-party\\{k['folder']}\\SOURCE.txt)"
    return t + ("; " + k["ea"] if k["ea"] else "")


def guild_label(g):
    return {"alembic": "Order of the Alembic", "smiths": "Society of Smiths", "artificers": "Artificers",
            "structure": "hall structure"}[g]


def cmd_check(_=None):
    check()
    print(f"{len(PIECES)} pieces, {LAST - FIRST + 1} IDs, 0x{FIRST:04X}-0x{LAST:04X} ({FIRST}-{LAST})")
    for g in ("alembic", "smiths", "artificers", "structure"):
        ps = [p for p in PIECES if p["guild"] == g]
        print(f"  {g}: {len(ps)} pieces, {sum(len(p['files']) for p in ps)} IDs")


def cmd_registry(path):
    check()
    with open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    taken = {line.split(",", 1)[0] for line in text.splitlines() if line and not line.startswith("#")}
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    for gid, p, i, f in ids():
        if str(gid) in taken:
            sys.exit(f"{gid} is already registered")
        n = len(p["files"])
        frame = "" if n == 1 else (f", frame {i + 1} of {n}" + (" (base ID: has our tiledata and animdata record)" if i == 0 and p["anim"] else ""))
        how = "background made transparent, nothing else changed"
        w.writerow([str(gid), f"0x{gid:04X}", f"Guild hall decor (cc-P265, {guild_label(p['guild'])}): {p['what']}{frame}",
                    f"{credit(p)}: {os.path.relpath(f, os.path.join(TP, p['pack']['folder']))}; {how}",
                    license_text(p), "art"])
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text if text.endswith("\n") else text + "\n")
        f.write(buf.getvalue())
    print(f"appended {LAST - FIRST + 1} rows")


def cmd_png(repo):
    check()
    tool = os.path.join(repo, "scripts", "anchor-art-frames.py")
    out = os.path.join(repo, "player-package", "vendor", "shattered-legacy-art", "art")
    stage = os.path.join(os.environ.get("TEMP", "."), "p265-stage")
    shutil.rmtree(stage, ignore_errors=True)
    os.makedirs(stage)
    for gid, p, i, f in ids():
        rgb = np.asarray(Image.open(f).convert("RGB"))
        args = [sys.executable, "-P", tool, "--keep-geometry", "--first-id", str(gid), "--out", out]
        if white_background(rgb):
            staged = os.path.join(stage, f"{gid}.png")
            unwhite(f, staged)
            args += ["--files", staged]
        elif f.lower().endswith(".png"):
            args += ["--files", f]                 # the railings: UOFiddler exports with their own alpha
        else:
            args += ["--files", f, "--black-transparent"]
        r = subprocess.run(args, capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit(f"{gid} {f}: {r.stdout}{r.stderr}")
    print(f"wrote {LAST - FIRST + 1} PNGs to {out}")


def flags_of(p):
    """The record's flags; an animated piece's base ID always carries Animation (the client animates only then)."""
    return p["rec"][0] | (ANIM if p["anim"] else 0)


def records():
    """(tiledata rows, animdata rows) for records.json: one tiledata row per piece (its base ID)."""
    tiles, anims = [], []
    for p in PIECES:
        _, height, weight, light, _ = p["rec"]
        flags = flags_of(p)
        tiles.append(dict(id=p["id"], name=p["name"], flags=flags, weight=weight, light=light, height=height))
        if p["anim"]:
            anims.append(dict(id=p["id"], frames=p["anim"][0], interval=p["anim"][1]))
    return tiles, anims


def cmd_records(path):
    check()
    with open(path, encoding="utf-8") as f:
        text = f.read()
    rec = json.loads(text)
    have = {int(t["id"]) for t in rec["tiledata"]}
    tiles, anims = records()
    tl = []
    for t in tiles:
        assert t["id"] not in have, t["id"]
        # the layer byte carries the light shape for a light source (cc-P237's lantern and campfire)
        tl.append(f'    {{ "id": {t["id"]}, "name": "{t["name"]}", "flags": "0x{t["flags"]:08X}", "weight": {t["weight"]}, '
                  f'"layer": {t["light"]}, "count": 0, "animId": 0, "hue": 0, "light": 0, "height": {t["height"]} }}')
    al = [f'    {{ "id": {a["id"]}, "frames": {json.dumps(a["frames"]).replace(",", ", ").replace(",  ", ", ")}, '
          f'"interval": {a["interval"]}, "start": 0 }}' for a in anims]
    for section, lines in (("tiledata", tl), ("animdata", al)):
        head = text.index(f'  "{section}": [')
        close = text.index("\n  ]", head)
        text = text[:close] + ",\n" + ",\n".join(lines) + text[close:]
    out = json.loads(text)
    assert len(out["tiledata"]) == len(rec["tiledata"]) + len(tl)
    assert len(out["animdata"]) == len(rec["animdata"]) + len(al)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print(f"appended {len(tl)} tiledata and {len(al)} animdata records")


FLAG_NAMES = [(TRANSP, "Transparent"), (TRANSL, "Translucent"), (WALL, "Wall"), (IMP, "Impassable"),
              (SURF, "Surface"), (BRIDGE, "Bridge"), (NOSHOOT, "NoShoot"), (ART_A, "ArticleA"), (ART_AN, "ArticleAn"),
              (PH, "PartialHue"), (LIGHT, "LightSource"), (ANIM, "Animation"), (UNK3, "Unknown3"), (ROOF, "Roof")]


def flag_expr(v):
    parts = [f"TileFlag.{n}" for b, n in FLAG_NAMES if v & b]
    assert sum(b for b, n in FLAG_NAMES if v & b) == v, hex(v)
    return " | ".join(parts) if parts else "TileFlag.None"


def cmd_cs(repo):
    check()
    lines = []
    for p in PIECES:
        _, height, weight, light, _ = p["rec"]
        flags = flags_of(p)
        lines.append(f'        new("{p["key"]}", 0x{p["id"]:04X}, {len(p["files"])}, "{p["name"]}", {flag_expr(flags)}, {weight}, {light}, {height}),')
    body = "\n".join(lines).rstrip(",")
    src = f"""// Generated by shard-migration notes/cc-P265-tools/decor.py (cs). Do not edit by hand: change the catalogue there
// and re-run it. The values are records.json's (player-package\\tests\\Build-UoOverrides.Tests.ps1 compares them).
//
// cc-P265: the guild hall decor packs (art library section 5): IDs 0x{FIRST:04X}-0x{LAST:04X} ({FIRST}-{LAST}), {len(PIECES)} pieces.
// One record per piece, on its base ID; an animated piece's frames are the Frames - 1 IDs after it (no record).

namespace Server;

public static class GuildHallDecorArt
{{
    public sealed record Piece(string Key, int Id, int Frames, string Name, TileFlag Flags, int Weight, int Light, int Height);

    public const int FirstId = 0x{FIRST:04X};
    public const int LastId = 0x{LAST:04X};

    public static readonly Piece[] Pieces =
    [
{body}
    ];

    public static Piece Find(string key)
    {{
        foreach (var p in Pieces)
        {{
            if (p.Key == key)
            {{
                return p;
            }}
        }}

        return null;
    }}

    /// <summary>Writes the records into the server's in-memory TileData.ItemTable (the server reads EA's tiledata,
    /// where these are empty slots); the light shape goes in the quality byte, as the client reads it.</summary>
    public static void Apply()
    {{
        foreach (var p in Pieces)
        {{
            TileData.ItemTable[p.Id] = new ItemData(p.Name, p.Flags, p.Weight, p.Light, 0, 0, 0, p.Height);
        }}
    }}
}}
"""
    path = os.path.join(repo, "server", "customizations", "GuildHallDecor", "GuildHallDecorArt.cs")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(src)
    print("wrote", path)


def cmd_table(repo=None):
    """The notes' piece table: every registered piece, its IDs, credit, and the template groups that use it."""
    check()
    used = {}
    if repo:
        _, _, d = load_design(repo)
        for s in d["sets"]:
            for g in s["groups"]:
                for r in g["rows"]:
                    if "piece" in r:
                        used.setdefault(r["piece"], set()).add(f"{s['key']}/{g['key']}")
    print("| Pack | Piece | New ID(s) | Credit | Used | Record copies |")
    print("|---|---|---|---|---|---|")
    for p in PIECES:
        r = f"0x{p['id']:04X}" + (f"-0x{p['id'] + len(p['files']) - 1:04X} ({len(p['files'])} frames)" if len(p["files"]) > 1 else "")
        u = ", ".join(sorted(used.get(p["key"], []))) or "registered, not in a template yet"
        src = p["rec"][4].split(" (")[0].replace("|", "\\|")
        print(f"| {p['pack']['folder']} | {p['what']} | {r} | {p['pack']['author']}"
              f"{' (EA-derived)' if p['pack']['ea'] else ''} | {u} | {src} |")




# ---------------------------------------------------------------- templates (design/guild-hall-decor/templates.json)
def load_design(repo):
    path = os.path.join(repo, "design", "guild-hall-decor", "templates.json")
    with open(path, encoding="utf-8") as f:
        text = f.read()
    d = json.loads(text)
    for s in d["sets"]:
        gkeys = [g["key"] for g in s["groups"]]
        assert len(gkeys) == len(set(gkeys)), s["key"]
        spots = set()      # across the whole set: placing every group never puts two rows on one tile at one z
        for g in s["groups"]:
            for r in g["rows"]:
                assert ("piece" in r) != ("item" in r), r
                if "piece" in r:
                    assert r["piece"] in BY_KEY or r["piece"] in ("marble-70321", "marble-70324"), r
                spot = (r["dx"], r["dy"], r["dz"])
                assert spot not in spots, (s["key"], g["key"], spot)   # two rows on one tile at one z
                spots.add(spot)
    return path, text, d


def row_id(r):
    if "item" in r:
        return int(r["item"], 16)
    if r["piece"].startswith("marble-") and int(r["piece"][7:]) in RAILS_TAKEN:
        return RAILS_TAKEN[int(r["piece"][7:])]
    return BY_KEY[r["piece"]]["id"]


def row_name(r):
    return r["name"] if "item" in r else (BY_KEY[r["piece"]]["name"] if r["piece"] in BY_KEY else "marble railing")


def cs_str(v):
    return '"' + v.replace("\\", "\\\\").replace('"', '\\"') + '"'


def cmd_layout(repo):
    """Write GuildHallDecorTemplates.cs (the server's copy of the design file) and the test's copy of the design."""
    import hashlib
    path, text, d = load_design(repo)
    # the hash is of the file without its final newline: the test's raw string literal holds exactly that
    text = text.replace("\r\n", "\n").rstrip("\n")
    sha = hashlib.sha256(text.encode("ascii")).hexdigest()
    sets = []
    for s in d["sets"]:
        groups = []
        for g in s["groups"]:
            rows = ",\n".join(
                f"                new(0x{row_id(r):04X}, {cs_str(row_name(r))}, {r['dx']}, {r['dy']}, {r['dz']}, "
                f"{r.get('hue', 0)}, {cs_str(r.get('piece', r.get('item')))})" for r in g["rows"])
            groups.append(f"            new({cs_str(g['key'])}, {cs_str(g['about'])},\n            [\n{rows}\n            ])")
        sets.append(f"        new({cs_str(s['key'])}, {cs_str(s['guild'])}, {cs_str(s['command'])},\n        [\n"
                    + ",\n".join(groups) + "\n        ])")
    src = f"""// Generated by shard-migration notes/cc-P265-tools/decor.py (layout) from design/guild-hall-decor/templates.json.
// Do not edit by hand: change the design file and re-run the generator. The test
// GuildHallDecorVerification.TheTemplatesAreTheDesignFile compares this table with the design file.
//
// A C# table, not a data file, because the build installs only .cs files from server/customizations (as
// ClusterFMineCampLayout). Offsets are tiles from the point staff target: dx east, dy south, dz up.

namespace Server;

public static class GuildHallDecorTemplates
{{
    public const string DesignFile = "design/guild-hall-decor/templates.json";
    public const string DesignSha256 = "{sha}";

    /// <summary>One item: its art ID, name, offset from the target point, hue, and the design row's piece (or stock item).</summary>
    public sealed record Row(int ItemId, string Name, int Dx, int Dy, int Dz, int Hue, string Piece);

    public sealed record Group(string Key, string About, Row[] Rows);

    public sealed record Set(string Key, string Guild, string Command, Group[] Groups);

    public static readonly Set[] Sets =
    [
{",\n".join(sets)}
    ];

    public static Set Find(string key)
    {{
        foreach (var s in Sets)
        {{
            if (s.Key == key)
            {{
                return s;
            }}
        }}

        return null;
    }}
}}
"""
    out = os.path.join(repo, "server", "customizations", "GuildHallDecor", "GuildHallDecorTemplates.cs")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(src)
    assert '"""' not in text
    copy = f"""// Generated by shard-migration notes/cc-P265-tools/decor.py (layout): a byte copy of {"design/guild-hall-decor/templates.json"}
// for GuildHallDecorVerification (the test host has no design folder). Do not edit by hand.

namespace ShatteredLegacy.Tests;

public static class GuildHallDecorDesignCopy
{{
    public const string Sha256 = "{sha}";

    public const string Json = \"\"\"\"
{text.rstrip(chr(10))}
\"\"\"\";
}}
"""
    tpath = os.path.join(repo, "server", "tests", "Misc", "GuildHallDecorDesignCopy.cs")
    with open(tpath, "w", encoding="utf-8", newline="\n") as f:
        f.write(copy)
    print("wrote", out, "and", tpath, "sha", sha)


def compose_rows(rows, repo, floor=True):
    """A client-geometry render (isorender's rules: x+y, then z, then height order; art bottom on the tile's bottom
    tip, 4 px per z) of rows [(id, x, y, z)], with our PNGs from the package and stock art from the client."""
    sys.path.insert(0, r"D:\UO\golems\Iron\shard-migration\scripts")
    from mapbuild import isorender
    art = isorender.Art()
    adir = os.path.join(repo, "player-package", "vendor", "shattered-legacy-art", "art")
    def img(i):
        p = os.path.join(adir, f"{i}.png")
        return Image.open(p).convert("RGBA") if os.path.exists(p) else art.static(i).convert("RGBA")
    items = [(i, x, y, z, img(i)) for i, x, y, z in rows]
    boxes = []
    for i, x, y, z, im in items:
        cx = (x - y) * 22; by = (x + y) * 22 + 44 - 4 * z
        boxes.append((cx - im.width // 2, by - im.height, cx - im.width // 2 + im.width, by))
    tiles = set()
    if floor:
        for i, x, y, z, im in items:
            for ax in range(-1, 2):
                for ay in range(-1, 2):
                    tiles.add((x + ax, y + ay))
        for x, y in tiles:
            cx = (x - y) * 22; ty = (x + y) * 22
            boxes.append((cx - 22, ty, cx + 22, ty + 44))
    L = min(b[0] for b in boxes) - 8; T = min(b[1] for b in boxes) - 8
    R = max(b[2] for b in boxes) + 8; B = max(b[3] for b in boxes) + 8
    out = Image.new("RGBA", (R - L, B - T), (24, 24, 30, 255))
    from PIL import ImageDraw
    dr = ImageDraw.Draw(out)
    for x, y in tiles:
        cx = (x - y) * 22 - L; ty = (x + y) * 22 - T
        dr.polygon([(cx, ty), (cx + 22, ty + 22), (cx, ty + 44), (cx - 22, ty + 22)], fill=(92, 88, 80, 255),
                   outline=(70, 66, 60, 255))
    order = sorted(range(len(items)), key=lambda k: (items[k][1] + items[k][2], items[k][3], k))
    for k in order:
        i, x, y, z, im = items[k]
        l, t, _, _ = boxes[k]
        out.alpha_composite(im, (l - L, t - T))
    return out


def cmd_preview(repo):
    _, _, d = load_design(repo)
    outdir = os.environ.get("P265_OUT", ".")
    for s in d["sets"]:
        rows = [(row_id(r), r["dx"], r["dy"], r["dz"]) for g in s["groups"] for r in g["rows"]]
        im = compose_rows(rows, repo)
        p = os.path.join(outdir, f"preview-{s['key']}.png")
        im.save(p)
        print(p, im.size)

def cmd_source(path):
    """Append this set's section to the package's SOURCE.txt (the package credits file)."""
    check()
    with open(path, encoding="utf-8") as f:
        text = f.read()
    assert "(cc-P265)" not in text, "the section is there already"
    title = f"Guild hall decor, art {FIRST}-{LAST} (0x{FIRST:04X}-0x{LAST:04X}) (cc-P265)"
    out = ["", title, "-" * len(title)]
    packs = []
    for p in PIECES:
        if p["pack"] not in packs:
            packs.append(p["pack"])
    for k in packs:
        ps = [p for p in PIECES if p["pack"] is k]
        lo, hi = ps[0]["id"], ps[-1]["id"] + len(ps[-1]["files"]) - 1
        out.append(f"  {lo}-{hi}  {k['author']}, {k['title']}, {k['url']}")
        out.append("               (D:\\UO\\third-party\\" + k["folder"] + f"\\). {len(ps)} pieces, {hi - lo + 1} IDs. "
                   f"Terms: {k['terms']}.")
        if k["ea"]:
            out.append(f"               {k['ea'][:10].upper()}{k['ea'][10:]}.")
    out += [
        "Not shipped: mad-scientist (its readme credits an unknown original author); arc-orb-fx's \"My Source Files\" and",
        "             the GIF previews; the preview JPGs; the large tower's Corel auto-save copy of DW a2ma. Marble railings",
        "             70321 and 70324 were shipped by cc-P237 (15503, 15504) and are not registered twice.",
        "Pixels:      background made transparent, nothing else: pure black (0,0,0) for the BMPs drawn on black",
        "             (scripts\\anchor-art-frames.py --black-transparent --keep-geometry); for the six drawn on white (the",
        "             large tower's top and turret, both white towers' domes, the arc orb gate, the blacksmith) the white",
        "             touching the image border, then the same tool without the black switch. The railings are UOFiddler",
        "             PNG exports with their own alpha: re-encoded only. Canvases kept as drawn. Made by shard-migration",
        "             notes\\cc-P265-tools\\decor.py, which also names the OSI tile (or the author's own note) each record copies.",
        "Records:     one tiledata record per piece on its base ID (179); animdata for the 33 animated pieces (the vat's",
        "             eight parts, sixteen creature tanks, the crystal ball lit and unlit, the blacksmith, the burning fire",
        "             pit, two floating crystals, three arc orbs). Server copy: GuildHallDecorArt.Pieces (generated).",
        "Placed by:   nothing yet. Staff seeders [DecorAlembicHall, [DecorSmithsHall, [DecorArtificersHall and",
        "             [DecorHallStructure place a template (design\\guild-hall-decor\\templates.json) on the test shard only.",
        "",
    ]
    with open(path, "a", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out))
    print("appended", len(out), "lines")


if __name__ == "__main__":
    cmd = sys.argv[1]
    {"check": cmd_check, "registry": cmd_registry, "png": cmd_png, "records": cmd_records, "cs": cmd_cs,
     "table": cmd_table, "preview": cmd_preview,
     "source": cmd_source, "layout": cmd_layout}[cmd](sys.argv[2] if len(sys.argv) > 2 else None)
