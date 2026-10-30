r"""cc-P688 (SoS swap S15) part 2: every fixed point the play-test bot and the isle route use, on the swapped land.

The land is the SoS map with the shipped trammel.mapops applied (the Burrows, Rootdeep, the isle and the rest of our
patch), built by `mapops.py apply` into a work folder outside the repos. Each point is read off walkgrid's grid:
standable (and at what Z), and which walk area it is in. Points a check walks between must share an area (or reach
it one way, for a step down); points the bot only [go]es to need only to be standable.

    python -P bot_points.py <code copy> <patched map folder>     -> out/bot-points.csv; exit 1 on a bad point
"""
import collections
import csv
import hashlib
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import walkgrid  # noqa: E402
import islands  # noqa: E402  (walkgrid put cc-P481-tools on the path)

ISLE_ROUTE = os.path.join(walkgrid.NOTES, "cc-P732-tools", "isle.py")   # main's (SoS New Haven) isle route


def literal(path, name):
    """A tuple constant from a source file, by name (the file is read, never imported: the bot needs its client)."""
    s = open(path, encoding="utf-8").read()
    m = re.search(r"^%s\s*=\s*(\(.*?\))\s*(#.*)?$" % re.escape(name), s, re.M | re.S)
    return eval(m.group(1), {})


def points(code):
    """(source, name, facet, x, y, walk group or '') for each point."""
    bot = os.environ.get("P688_UOBOT") or os.path.join(code, "tools", "playtest-bot", "uobot")   # a red run's copy
    out = []
    g = os.path.join(bot, "checks_p224_guilds.py")
    s = open(g, encoding="utf-8").read()
    for key, x, y, _z in re.findall(r'"(\w+)": \("\w+", \((\d+), (\d+), (-?\d+)\)', s):
        out.append(("checks_p224_guilds", key + " guildmaster", "Trammel", int(x), int(y), "haven"))
    hunt = re.search(r"move_player\(a, p, (\d+), (\d+), -?\d+\)", s)
    out.append(("checks_p224_guilds", "the hunting yard", "Trammel", int(hunt.group(1)), int(hunt.group(2)), "haven"))
    t39 = re.search(r"dist = max\(abs\(x - (\d+)\), abs\(y - (\d+)\)\)", open(os.path.join(bot, "checks.py"), encoding="utf-8").read())
    out.append(("checks T-039", "the board it measures from", "Trammel", int(t39.group(1)), int(t39.group(2)), "haven"))
    v = os.path.join(bot, "checks_p224_vbuild.py")
    sx, sy, _ = literal(v, "SQUARE")
    dx, dy = literal(v, "BOX_DX, BOX_DY")
    out.append(("checks_p224_vbuild", "the square", "Trammel", sx, sy, "haven"))
    out.append(("checks_p224_vbuild", "the work box", "Trammel", sx + dx, sy + dy, "haven"))
    m = os.path.join(bot, "checks_p224_mule.py")
    x, y, _ = literal(m, "DESPISE")
    out.append(("checks_p224_mule", "Despise go spot", "Trammel", x, y, ""))
    t = os.path.join(bot, "checks_p224_thieves.py")
    for name in ("TRAMMEL_DESPISE", "FELUCCA_SHAME", "BURROWS"):
        f, x, y, _ = literal(t, name)
        out.append(("checks_p224_thieves", name, f, x, y, ""))
    for i, (f, x, y, _) in enumerate(literal(t, "CHAMPION_SPOTS")):
        out.append(("checks_p224_thieves", "champion altar %d" % (i + 1), f, x, y, ""))
    r = os.path.join(bot, "checks_p224_rootdeep.py")
    for name in ("DOORWAY", "ADMIN_SPOT", "ADMIN_ASIDE", "CRAWLWAY_MOUTH", "CRAWLWAY_EXIT", "STAND"):
        x, y = literal(r, name)
        out.append(("checks_p224_rootdeep", name, "Trammel", x, y, "rootdeep"))
    for name in ("ROOK_EXIT", "HAVEN_START"):
        x, y = literal(ISLE_ROUTE, name)
        out.append(("isle route (P732)", name, "Trammel", x, y, "haven"))
    for name in ("BEACH", "BLUE_TILE", "CAMP", "SIGN", "WREN", "RAT", "BANK_STOP", "LODGE", "STONES", "BANK_FLOOR",
                 "GATE"):
        x, y = literal(ISLE_ROUTE, name)
        out.append(("isle route (P732)", name, "Trammel", x, y, "isle"))
    # the places the bot's own Haven steps lean on (HavenSpots.cs): the bank and the healer
    hs = open(os.path.join(code, "server", "customizations", "Tutorial", "HavenSpots.cs"), encoding="utf-8").read()
    for name in ("Bank", "Healer", "Rook", "QuestBoard"):
        mm = re.search(r"Point3D %s\s*(?:\{[^}]*\})?\s*=\s*new\((\d+), (\d+), (-?\d+)\)" % name, hs)
        out.append(("HavenSpots", name, "Trammel", int(mm.group(1)), int(mm.group(2)), "haven"))
    return out


def main():
    code, folder = sys.argv[1], sys.argv[2]
    islands.MAPS["sos-patched"] = ("uop", folder, 1, walkgrid.W, walkgrid.H, None)
    # the patched map's grid and walk areas, cached by the folder and its statics' time (a red run reuses a green one's)
    key = hashlib.sha256(("%s|%s" % (os.path.abspath(folder), os.path.getmtime(os.path.join(folder, "staidx1.mul"))))
                         .encode()).hexdigest()[:12]
    cache = os.path.join(os.path.dirname(walkgrid.CACHE), "p688-patched-%s.npz" % key)
    if os.path.exists(cache):
        d = np.load(cache)
        stand, lab = d["stand"], d["lab"]
    else:
        stand, low, top = walkgrid.build("sos-patched")
        lab, _, _ = walkgrid.areas(walkgrid.steps(stand, low, top))
        np.savez(cache, stand=stand, lab=lab)
    size = collections.Counter(lab[lab >= 0].tolist())
    rows, bad = [], []
    for src, name, facet, x, y, group in points(code):
        z = int(stand[x, y])
        a = int(lab[x, y])
        rows.append(dict(source=src, point=name, facet=facet, x=x, y=y, z="" if z == walkgrid.NONE else z,
                         area=a, area_tiles=size.get(a, 0), group=group))
        if z == walkgrid.NONE:
            bad.append("%s %s %d,%d: nobody stands there" % (src, name, x, y))
    board = next(r for r in rows if r["point"] == "QuestBoard")
    for r in rows:
        if r["source"] == "checks T-039" and max(abs(r["x"] - board["x"]), abs(r["y"] - board["y"])) > 1:
            bad.append("checks T-039 measures from %d,%d; the board is at HavenSpots.QuestBoard %d,%d"
                       % (r["x"], r["y"], board["x"], board["y"]))
    for group in sorted({r["group"] for r in rows if r["group"]}):
        areas = collections.Counter(r["area"] for r in rows if r["group"] == group and r["z"] != "")
        main_area = areas.most_common(1)[0][0]
        for r in rows:
            if r["group"] == group and r["z"] != "" and r["area"] != main_area:
                bad.append("%s %s %d,%d: not in the %s walk area (area %d of %d tiles)"
                           % (r["source"], r["point"], r["x"], r["y"], group, r["area"], r["area_tiles"]))
    os.makedirs(walkgrid.OUT, exist_ok=True)
    with open(os.path.join(walkgrid.OUT, "bot-points.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print("%-22s %-20s %-8s %4d,%4d z %4s area %9d (%d tiles) %s" % (r["source"], r["point"], r["facet"], r["x"],
              r["y"], r["z"], r["area"], r["area_tiles"], r["group"]))
    print("\n%d points, %d bad" % (len(rows), len(bad)))
    for b in bad:
        print("BAD", b)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
