r"""cc-P813: put the Claude Design gump art into the player package's art vendor folder.

    python -P add_package_rows.py <ShatteredLegacy root> <cut gumps dir> <banner 44x88 png>

Copies gumps 23211-23222 to vendor\shattered-legacy-art\gumps\, the banner to art\46710.png, appends one registry.csv
row each, and appends the banner's tiledata record to records.json (OSI's hanging banner 0x1586's values). Refuses to
run twice (an ID already registered) and checks every PNG's size.
"""

import csv
import io
import json
import os
import shutil
import sys

from PIL import Image

SOURCE = ("Chase (Shattered Legacy), made with Claude Design: canvas \"\"Shattered Legacy gump art\"\" (2026-11-01, "
          "approved 2026-11-05), {board}; rendered at true size by headless Edge and cut by shard-migration "
          "notes\\cc-P813-tools\\render_gump_art.py{cut}")
LICENSE = "ours"

GUMPS = [
    (23211, 340, 280, "Pet choice scroll window (cc-P813, P762's PetChoiceGump): background, no text (the server draws it)",
     "Main.dc.html", "; text and tiles hidden"),
    (23212, 143, 96, "Pet choice scroll (cc-P813): Dog tile with its icon, the button's normal look (the server draws the word)",
     "Main.dc.html", "; text hidden"),
    (23213, 143, 96, "Pet choice scroll (cc-P813): Dog tile, pressed (the design's tile one step darker)",
     "Main.dc.html", "; text hidden, tile #ddcfa6 and border #5c4110"),
    (23214, 143, 96, "Pet choice scroll (cc-P813): Cat tile with its icon, the button's normal look (the server draws the word)",
     "Main.dc.html", "; text hidden"),
    (23215, 143, 96, "Pet choice scroll (cc-P813): Cat tile, pressed (the design's tile one step darker)",
     "Main.dc.html", "; text hidden, tile #ddcfa6 and border #5c4110"),
    (23216, 400, 136, "Moongate skip achievement popup (cc-P813, P762's \"\"Didn't Read the Sign\"\" in AchievementEarnedGump): background, no text",
     "Achievement.dc.html", "; text hidden"),
    (23217, 560, 420, "Reward store window (cc-P813, the League shop, LeagueShopGump): background (panel, border, header rule), no text, tabs or rows",
     "RewardStore.dc.html", "; text, buttons and rows hidden"),
    (23218, 8, 1, "Reward store window (cc-P813): the row rule, 8 x 1, tiled under each row",
     "RewardStore.dc.html", "; the first row's bottom border"),
    (23219, 104, 32, "Reward store window (cc-P813): a tab, inactive (one width for every label; the server draws the word)",
     "RewardStore.dc.html", "; text hidden, tabs 104 px wide"),
    (23220, 104, 32, "Reward store window (cc-P813): a tab, active (the design's \"\"Gear\"\" tab) and the pressed look",
     "RewardStore.dc.html", "; text hidden, tabs 104 px wide"),
    (23221, 72, 28, "Reward store window (cc-P813): the Buy button (the server draws the word)",
     "RewardStore.dc.html", "; text hidden"),
    (23222, 72, 28, "Reward store window (cc-P813): the Buy button, pressed",
     "RewardStore.dc.html", "; text hidden, button #2a2317"),
]

BANNER = 46710
BANNER_ROW = (BANNER, "Hall of Finishers banner (cc-P813): a hanging banner with a sword snapped across the blade, 44 x 88, "
                      "decor ([add FinishersBanner); has our tiledata record (OSI's banner 0x1586's)",
              "Banner.dc.html", "; exported by the overseer at true size as finishers-banner-44x88.png (D:\\UO\\overseer\\gump-art-20261105), unchanged")
BANNER_RECORD = {"id": BANNER, "name": "banner", "flags": "0x00044000", "weight": 255, "layer": 0, "count": 0,
                 "animId": 0, "hue": 0, "light": 0, "height": 0}


def line(id_, what, board, cut, kind):
    src = SOURCE.format(board=board, cut=cut)
    return f'{id_},0x{id_:04X},"{what}","{src}",{LICENSE},{kind}\n'


def main():
    root, cut_dir, banner = sys.argv[1:4]
    vendor = os.path.join(root, "player-package", "vendor", "shattered-legacy-art")
    reg_path = os.path.join(vendor, "registry.csv")
    with open(reg_path, encoding="utf-8", newline="") as f:
        reg_text = f.read()
    rows = list(csv.DictReader(io.StringIO("\n".join(l for l in reg_text.splitlines() if not l.startswith("#")))))
    taken = {int(r["id"]) for r in rows}
    wanted = [g[0] for g in GUMPS] + [BANNER]
    clash = [i for i in wanted if i in taken]
    if clash:
        raise SystemExit(f"already registered: {clash}")

    add = []
    for gid, w, h, what, board, cut in GUMPS:
        src = os.path.join(cut_dir, f"{gid}.png")
        im = Image.open(src)
        if im.size != (w, h) or im.mode != "RGBA":
            raise SystemExit(f"{src}: {im.size} {im.mode}, wanted {(w, h)} RGBA")
        shutil.copyfile(src, os.path.join(vendor, "gumps", f"{gid}.png"))
        add.append(line(gid, what, board, cut, "gump"))

    im = Image.open(banner)
    if im.size != (44, 88):
        raise SystemExit(f"{banner}: {im.size}, wanted 44 x 88")
    shutil.copyfile(banner, os.path.join(vendor, "art", f"{BANNER}.png"))
    add.append(line(BANNER, BANNER_ROW[1], BANNER_ROW[2], BANNER_ROW[3], "art"))

    nl = "\r\n" if "\r\n" in reg_text else "\n"
    if not reg_text.endswith(("\n", "\r\n")):
        reg_text += nl
    reg_text += "".join(a.replace("\n", nl) for a in add)
    with open(reg_path, "w", encoding="utf-8", newline="") as f:
        f.write(reg_text)

    rec_path = os.path.join(vendor, "records.json")
    with open(rec_path, encoding="utf-8") as f:
        raw = f.read()
    json.loads(raw)
    if '"id": 46710,' in raw:
        raise SystemExit("records.json already has 46710")
    # The file keeps one record per line, so the record goes in as text after the last tiledata record (46709).
    last = '"id": 46709, "name": "archery butte", "flags": "0x00008040", "weight": 255, "layer": 0, "count": 0, "animId": 0, "hue": 0, "light": 0, "height": 10 }'
    end = last + "\n  ],"
    if raw.count(end) != 1:
        raise SystemExit("records.json: the tiledata list no longer ends with 46709")
    r = BANNER_RECORD
    rec_line = ("    { " + ", ".join(f'"{k}": {json.dumps(v)}' for k, v in r.items()) + " }")
    raw = raw.replace(end, last + ",\n" + rec_line + "\n  ],", 1)
    about_end = raw.index('",\n  "tiledata"')
    raw = raw[:about_end] + (" cc-P813, the Hall of Finishers banner 46710: OSI's hanging banner 0x1586's record "
                             "(banner, ArticleA | PartialHue, weight 255, height 0); the server's copy is "
                             "FinishersBannerArt.") + raw[about_end:]
    rec = json.loads(raw)
    assert rec["tiledata"][-1] == BANNER_RECORD
    with open(rec_path, "w", encoding="utf-8", newline="") as f:
        f.write(raw)
    print(f"added {len(add)} registry rows, {len(GUMPS)} gumps, art {BANNER} and its record")


if __name__ == "__main__":
    main()
