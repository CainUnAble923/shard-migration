"""cc-P365: reward mounts and the evo pets' young stages. Bodies 2088-2133 (with gaps the client's own data takes), mount
items 46672-46689 (0xB650-0xB661).

    python -P p365_art.py check <src>                    every file present, sizes, SHA-256s
    python -P p365_art.py copy <src> <ShatteredLegacy>   each .vd, byte for byte, to anim-src\\bodies\\<body>.vd
    python -P p365_art.py registry <registry.csv>        append the body and mount item rows; refuses a taken ID
    python -P p365_art.py records <records.json>         append bodyAnims and the mount items' tiledata (as lines)
    python -P p365_art.py icons <ShatteredLegacy>        each mount item's icon: its ridden look's stand frame, 44 px

<src> is a copy of the packs made first (the prompt: never build or run from D:\\UO\\third-party), laid out as
    <src>\\thagoras\\<file with spaces as underscores>     D:\\UO\\third-party\\thagoras-mount-pack\\Mount Pack\\
    <src>\\uopixel\\<archive>\\<file>                      D:\\UO\\third-party\\uo-pixel-animals\\<archive>\\
    <src>\\krwolf\\Wolf.vd                                 D:\\UO\\third-party\\kr-wolf\\

Bodies and slots are validate-art.py propose's (anim7 slot by the .vd's layout: low 200-399, people 400 up); every
.vd ships byte for byte. Krazy Zacks' drake and bear ("Do not modify contents of this package!") are shipped exactly as
he made them: no recolour, no resize, no frame touched; only placed in our anim7 as every body is.
"""
import csv
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys

THAG = ("Thagoras (from Rafael Costa, UoBrazilian)", '"Mount Pack" (servuo.dev 1979)',
        "none stated; community work: credit Thagoras and Rafael Costa (UoBrazilian) in the shard credits, ship only "
        "inside the player package or the private repo, do not repost; likely ripped from World of Warcraft (the "
        "author's words): renamed in game, no Blizzard names; see SOURCE.txt")
KZ = ("Krazy Zacks", 'uo-pixel.de anim:animals, "Mountable drake and Bear" (krazy_zacks_drake_bear)',
      "\"Distribute freely. Do not modify contents of this package!\" (his readme): shipped byte for byte, no recolour, "
      "no resize; credit Krazy Zacks in the shard credits; see SOURCE.txt")
PRAPILK_PIX = ("Prapilk", "uo-pixel.de anim:animals",
               "none stated; community work: credit Prapilk in the shard credits, ship only inside the player package "
               "or the private repo, do not repost; see SOURCE.txt")
SOCRARR = ("Socrarr", 'uo-pixel.de anim:animals, "Pferdesattel" (socrarr_pferdesattel)',
           "none stated; community work: credit Socrarr in the shard credits, ship only inside the player package or "
           "the private repo, do not repost; see SOURCE.txt")
PRAPILK_KR = ("Prapilk", '"KR Wolf" (servuo.dev 1717)',
              "none stated; community work: credit Prapilk in the shard credits, ship only inside the player package "
              "or the private repo, do not repost; see SOURCE.txt")

# (body, slot, layout type, src path, credit, our name, what it is)
BODIES = [
    (2088, 209, "ANIMAL", "thagoras/Dino_Raptor_01.vd", THAG, "marsh raptor", "reward mount: a green striped raptor"),
    (2089, 210, "ANIMAL", "thagoras/Dino_Raptor_02.vd", THAG, "dusk raptor", "reward mount: a dark violet raptor"),
    (2090, 211, "ANIMAL", "thagoras/Dino_Raptor_03.vd", THAG, "sky raptor", "reward mount: a blue raptor"),
    (2091, 212, "ANIMAL", "thagoras/Horse_01.vd", THAG, "chestnut draft horse", "reward mount on the ground; ridden as 2104"),
    (2092, 213, "ANIMAL", "thagoras/Horse_02.vd", THAG, "bay draft horse", "reward mount on the ground; ridden as 2105"),
    (2093, 214, "ANIMAL", "thagoras/Horse_03.vd", THAG, "grey draft horse", "reward mount on the ground; ridden as 2106"),
    (2094, 215, "ANIMAL", "thagoras/Horse_04.vd", THAG, "palomino draft horse", "reward mount on the ground; ridden as 2108"),
    (2095, 216, "ANIMAL", "thagoras/Horse_05_Saddle.vd", THAG, "barded warhorse", "reward mount: a dark horse in barding"),
    (2096, 217, "ANIMAL", "thagoras/Horse_06_Saddle.vd", THAG, "gilded charger", "reward mount: an armoured horse, burning hooves"),
    (2097, 218, "ANIMAL", "thagoras/Horse_Unicorn_1.vd", THAG, "moonlit unicorn", "reward mount: a white unicorn"),
    (2098, 219, "ANIMAL", "thagoras/L_Horse_Death_Mount.vd", THAG, "bonewalker steed", "reward mount: a skeletal horse"),
    (2099, 220, "ANIMAL", "thagoras/L_Horse_Nightmare.vd", THAG, "emberhoof", "reward mount: a black horse, burning hooves"),
    (2100, 221, "ANIMAL", "thagoras/L_Swamp_Lizard.vd", THAG, "bog strider", "reward mount: an armoured swamp lizard"),
    (2102, 222, "ANIMAL", "thagoras/Warg1.vd", THAG, "war wolf", "reward mount: an armoured great wolf"),
    (2104, 223, "ANIMAL", "thagoras/Horse_01_Saddle.vd", THAG, "chestnut draft horse, saddled", "ridden look of 2091 (walk, run, stand, eat)"),
    (2105, 224, "ANIMAL", "thagoras/Horse_02_Saddle.vd", THAG, "bay draft horse, saddled", "ridden look of 2092"),
    (2106, 225, "ANIMAL", "thagoras/Horse_03_Saddle.vd", THAG, "grey draft horse, saddled", "ridden look of 2093"),
    (2108, 226, "ANIMAL", "thagoras/Horse_04_Saddle.vd", THAG, "palomino draft horse, saddled", "ridden look of 2094"),
    (2109, 401, "HUMAN", "uopixel/krazy_zacks_drake_bear/P_01.vd", KZ, "riding drake", "ridden look of the riding drake (people layout: the rider's mounted actions 23-29)"),
    (2110, 402, "HUMAN", "uopixel/krazy_zacks_drake_bear/P_02.vd", KZ, "riding bear", "ridden look of the riding bear (people layout)"),
    (2111, 403, "HUMAN", "uopixel/prapilk_reitwolf/P_01.vd", PRAPILK_PIX, "riding wolf", "ridden look of the riding wolf (people layout; prapilk_reitwolf)"),
    (2112, 404, "HUMAN", "uopixel/socrarr_pferdesattel/P_pferdesattel.vd", SOCRARR, "saddled horse", "ridden look of the saddled horse (people layout)"),
    (2113, 227, "ANIMAL", "uopixel/prapilk_colts/L_01.vd", PRAPILK_PIX, "dun foal", "evo young stage: a foal (prapilk_colts L_01)"),
    (2114, 228, "ANIMAL", "uopixel/prapilk_colts/L_02.vd", PRAPILK_PIX, "grey foal", "evo young stage: a foal (prapilk_colts L_02)"),
    (2115, 229, "ANIMAL", "uopixel/prapilk_colts/L_03.vd", PRAPILK_PIX, "brown foal", "evo young stage: a foal (prapilk_colts L_03)"),
    (2118, 230, "ANIMAL", "uopixel/prapilk_colts/L_04.vd", PRAPILK_PIX, "white foal", "evo young stage: a foal (prapilk_colts L_04)"),
    (2119, 231, "ANIMAL", "uopixel/prapilk_echsen/L_01.vd", PRAPILK_PIX, "young lizard", "evo young stage: a young lizard (prapilk_echsen L_01)"),
    (2125, 232, "ANIMAL", "uopixel/prapilk_echsen/L_02.vd", PRAPILK_PIX, "young lizard", "evo young stage: a young lizard (prapilk_echsen L_02)"),
    (2126, 233, "ANIMAL", "uopixel/prapilk_echsen/L_03.vd", PRAPILK_PIX, "young lizard", "evo young stage: a young lizard (prapilk_echsen L_03)"),
    (2129, 234, "ANIMAL", "uopixel/prapilk_rindviehcher/L_01.vd", PRAPILK_PIX, "brown calf", "evo young stage: a calf (prapilk_rindviehcher L_01)"),
    (2130, 235, "ANIMAL", "uopixel/prapilk_rindviehcher/L_02.vd", PRAPILK_PIX, "spotted calf", "evo young stage: a calf (prapilk_rindviehcher L_02)"),
    (2131, 236, "ANIMAL", "uopixel/prapilk_rindviehcher/L_03.vd", PRAPILK_PIX, "red calf", "evo young stage: a calf (prapilk_rindviehcher L_03)"),
    (2132, 237, "ANIMAL", "uopixel/prapilk_rindviehcher/L_04.vd", PRAPILK_PIX, "piebald calf", "evo young stage: a calf (prapilk_rindviehcher L_04)"),
    (2133, 238, "ANIMAL", "krwolf/Wolf.vd", PRAPILK_KR, "great grey wolf", "the evo dog's top stage (kr-wolf; actions 0-10 and 12)"),
]

FIRST_ITEM = 46672
# (mount item, mount key, tiledata name <= 19 ASCII, the body it draws when ridden)
ITEMS = [
    (46672, "marsh raptor", "raptor mount", 2088),
    (46673, "dusk raptor", "raptor mount", 2089),
    (46674, "sky raptor", "raptor mount", 2090),
    (46675, "chestnut draft horse", "draft horse mount", 2104),
    (46676, "bay draft horse", "draft horse mount", 2105),
    (46677, "grey draft horse", "draft horse mount", 2106),
    (46678, "palomino draft horse", "draft horse mount", 2108),
    (46679, "barded warhorse", "warhorse mount", 2095),
    (46680, "gilded charger", "charger mount", 2096),
    (46681, "moonlit unicorn", "unicorn mount", 2097),
    (46682, "bonewalker steed", "bonewalker mount", 2098),
    (46683, "emberhoof", "emberhoof mount", 2099),
    (46684, "bog strider", "bog strider mount", 2100),
    (46685, "war wolf", "war wolf mount", 2102),
    (46686, "riding drake", "drake mount", 2109),
    (46687, "riding bear", "bear mount", 2110),
    (46688, "riding wolf", "wolf mount", 2111),
    (46689, "saddled horse", "horse mount", 2112),
]


def body(n):
    return next(b for b in BODIES if b[0] == n)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def check(src=None):
    assert len({b[0] for b in BODIES}) == len(BODIES) and len({b[1] for b in BODIES}) == len(BODIES)
    assert [i[0] for i in ITEMS] == list(range(FIRST_ITEM, FIRST_ITEM + len(ITEMS)))
    for i in ITEMS:
        assert len(i[2]) <= 19 and i[2].isascii(), i
        body(i[3])
    if src:
        for b in BODIES:
            p = os.path.join(src, b[3])
            assert os.path.isfile(p), p
            assert os.path.getsize(p) < 5 * 1024 * 1024, p


def cmd_check(src):
    check(src)
    for b in BODIES:
        p = os.path.join(src, b[3])
        print(b[0], b[1], b[2], os.path.getsize(p), sha(p), b[3])


def cmd_copy(src, repo):
    check(src)
    out = os.path.join(repo, "player-package", "vendor", "shattered-legacy-art", "anim-src", "bodies")
    for b in BODIES:
        dst = os.path.join(out, f"{b[0]}.vd")
        if os.path.exists(dst):
            sys.exit(f"{dst} exists")
        shutil.copyfile(os.path.join(src, b[3]), dst)
        assert sha(dst) == sha(os.path.join(src, b[3]))
    print(f"copied {len(BODIES)} .vd files")


def cmd_registry(path, src):
    check(src)
    with open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    taken = {line.split(",", 1)[0] for line in text.splitlines() if line and not line.startswith("#")}
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    for n, slot, typ, rel, (author, pack, terms), name, what in BODIES:
        if str(n) in taken:
            sys.exit(f"{n} is already registered")
        fname = os.path.basename(rel).replace("_", " ") if rel.startswith("thagoras") else os.path.basename(rel)
        w.writerow([str(n), f"0x{n:X}", f'{name[0].upper() + name[1:]}: {what} (cc-P365); anim7 slot {slot}, {typ} 0',
                    f"{author}, {pack}: {fname}, byte for byte as anim-src/bodies/{n}.vd (sha256 {sha(os.path.join(src, rel))})",
                    terms, "body"])
    for gid, key, tname, look in ITEMS:
        if str(gid) in taken:
            sys.exit(f"{gid} is already registered")
        n, slot, typ, rel, (author, pack, terms), name, what = body(look)
        fname = os.path.basename(rel).replace("_", " ") if rel.startswith("thagoras") else os.path.basename(rel)
        frame = "action 4" if typ == "HUMAN" else "action 2"
        w.writerow([str(gid), f"0x{gid:04X}", f"{key[0].upper() + key[1:]} mount item (cc-P365): the Mount layer item; our "
                    f"tiledata record names body {look} as its Animation; its icon is that body's stand frame, scaled to 44 px",
                    f"{author}, {pack}: {fname}, {frame} direction 2 frame 0, scaled (p365_art.py icons)", terms, "art"])
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text if text.endswith("\n") else text + "\n")
        f.write(buf.getvalue())
    print(f"appended {len(BODIES)} body and {len(ITEMS)} art rows")


def cmd_records(path):
    check()
    with open(path, encoding="utf-8") as f:
        text = f.read()
    rec = json.loads(text)
    have_b = {int(b["body"]) for b in rec["bodyAnims"]}
    have_t = {int(t["id"]) for t in rec["tiledata"]}
    bl, tl = [], []
    for n, slot, typ, rel, credit, name, what in BODIES:
        assert n not in have_b, n
        bl.append(f'    {{ "body": {n}, "slot": {slot}, "type": "{typ}", "flags": 0, "vd": "anim-src/bodies/{n}.vd", '
                  f'"name": "{name} (cc-P365)" }}')
    for gid, key, tname, look in ITEMS:
        assert gid not in have_t, gid
        tl.append(f'    {{ "id": {gid}, "name": "{tname}", "flags": "0x00400000", "weight": 255, "layer": 25, "count": 0, '
                  f'"animId": {look}, "hue": 0, "light": 0, "height": 0 }}')
    for key, lines in (("tiledata", tl), ("bodyAnims", bl)):
        head = text.index(f'  "{key}": [')
        close = text.index("\n  ]", head)
        text = text[:close] + ",\n" + ",\n".join(lines) + text[close:]
    out = json.loads(text)
    assert len(out["tiledata"]) == len(rec["tiledata"]) + len(tl)
    assert len(out["bodyAnims"]) == len(rec["bodyAnims"]) + len(bl)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print(f"appended {len(bl)} bodyAnims and {len(tl)} tiledata records")


def cmd_icons(repo):
    """Render each ridden look's stand frame (validate-art.py render), then scale it to 44 px wide, keeping its shape."""
    from PIL import Image
    import tempfile
    check()
    art = os.path.join(repo, "player-package", "vendor", "shattered-legacy-art")
    tool = os.path.join(repo, "scripts", "validate-art.py")
    tmp = tempfile.mkdtemp(prefix="p365-icons-")
    for gid, key, tname, look in ITEMS:
        typ = body(look)[2]
        action = "4" if typ == "HUMAN" else "2"
        out = os.path.join(tmp, str(gid))
        r = subprocess.run([sys.executable, "-P", tool, "--data", r"D:\UO\UltimaOnlineVanilla", "render", "--vd",
                            os.path.join(art, "anim-src", "bodies", f"{look}.vd"), "--out", out, action, "2"],
                           capture_output=True, text=True)
        frames = sorted(f for f in os.listdir(out) if f.endswith("_f00.png")) if os.path.isdir(out) else []
        if r.returncode != 0 or not frames:
            sys.exit(f"{gid}: {r.stdout}{r.stderr}")
        im = Image.open(os.path.join(out, frames[0])).convert("RGBA")
        im = im.crop(im.getbbox())
        scale = 44 / max(im.width, im.height)
        im = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))), Image.LANCZOS)
        dst = os.path.join(art, "art", f"{gid}.png")
        assert not os.path.exists(dst), dst
        im.save(dst)
        print(gid, key, im.size)


if __name__ == "__main__":
    c = sys.argv[1]
    if c == "check":
        cmd_check(sys.argv[2])
    elif c == "copy":
        cmd_copy(sys.argv[2], sys.argv[3])
    elif c == "registry":
        cmd_registry(sys.argv[2], sys.argv[3])
    elif c == "records":
        cmd_records(sys.argv[2])
    elif c == "icons":
        cmd_icons(sys.argv[2])
