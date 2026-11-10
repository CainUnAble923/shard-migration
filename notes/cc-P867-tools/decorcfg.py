"""cc-P867: read P855's decor addon files (server/data/Decoration/Addons/*.cfg, pinned's [Decorate text plus #! headers)
and summarise or render them. ASCII only.

  python -P decorcfg.py summary                      one line per design: pieces, bbox, facing, tall pieces by side
  python -P decorcfg.py room <out.jpg> <design> <wall> [ox oy]
        render the design standing in a mock fieldstone room against <wall> (north|west|south|east, nw|se for a corner, or none), by the guide's wall rule
        (post NW, "south" pieces on the north row to the NE tile and the south row, "east" pieces down the west column
        to the SW tile and the east column, L corner SE; floor at the wall Z under the south row and east column).
        The design's origin goes to (ox, oy) inside the room (default: picked so its back row is the first floor row).
  python -P decorcfg.py sheet <out.jpg> <design>:<wall> ...   several room renders on one sheet

Env: SL_ADDONS (default the Iron code copy's server/data/Decoration/Addons), MAPBUILD_CLIENT.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("MAPBUILD_CLIENT", r"D:\UO\tool-trials\client-data-copy")
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
ADDONS = os.environ.get("SL_ADDONS", r"D:\UO\golems\Iron\ShatteredLegacy\server\data\Decoration\Addons")


def read(design):
    path = os.path.join(ADDONS, design + ".cfg")
    head, pieces, cur = {}, [], None
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if line.startswith("#!"):
            k, _, v = line[2:].partition(":")
            head[k.strip()] = v.strip()
            continue
        if not line or line.startswith("#"):
            continue
        m = re.match(r"Static (0x[0-9A-Fa-f]+)", line)
        if m:
            cur = int(m.group(1), 16)
            continue
        x, y, z = (int(v) for v in line.split())
        pieces.append((cur, x, y, z))
    return head, pieces


def designs():
    return sorted(f[:-4] for f in os.listdir(ADDONS) if f.endswith(".cfg"))


def summary():
    from mapbuild import uofiles
    _, items = uofiles.read_tiledata(os.environ["MAPBUILD_CLIENT"])
    for d in designs():
        head, p = read(d)
        xs = [c[1] for c in p]
        ys = [c[2] for c in p]
        tall = [(c[1], c[2]) for c in p if items[c[0]]["height"] >= 15]
        print("%-40s %3d pieces  x %d..%d  y %d..%d  facing %-12s tall %s" % (
            d, len(p), min(xs), max(xs), min(ys), max(ys), head.get("facing", "?"), sorted(set(tall))))


# fieldstone set (guide 2.2): post 0x001D, south piece 0x001C, east piece 0x001B, corner 0x001A
POST, SOUTH, EAST, CORNER = 0x001D, 0x001C, 0x001B, 0x001A
if os.environ.get("ROOM") == "plaster":       # guide 2.2: post 0x012A, south 0x0133, east 0x0134, corner 0x0132
    POST, SOUTH, EAST, CORNER = 0x012A, 0x0133, 0x0134, 0x0132
FLOOR = 0x0519


def room_scene(design, wall, ox=None, oy=None, size=9):
    """A size x size wall box at Z 0 with the design against its north or west wall."""
    from mapbuild import isorender as iso
    _, p = read(design)
    x0, y0 = 0, 0
    x1, y1 = size - 1, size - 1
    statics = []
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            if (x, y) == (x0, y0):
                tid = POST
            elif (x, y) == (x1, y1):
                tid = CORNER
            elif y == y0 or (y == y1 and x0 < x < x1):
                tid = SOUTH
            elif x == x0 or (x == x1 and y0 < y < y1):
                tid = EAST
            else:
                tid = None
            if tid:
                statics.append((x, y, 0, tid))
            if x > x0 and y > y0:
                statics.append((x, y, 0, FLOOR))
    xs = [c[1] for c in p]
    ys = [c[2] for c in p]
    if ox is None:
        mx = (x0 + x1) // 2 - (min(xs) + max(xs)) // 2
        my = (y0 + y1) // 2 - (min(ys) + max(ys)) // 2
        # back row on the first floor row inside that wall (the north row and west column are wall tiles; the south row
        # and east column carry their wall on the far edge, so their own tiles are floor)
        ox = {"west": x0 + 1 - min(xs), "east": x1 - max(xs), "nw": x0 + 1 - min(xs), "se": x1 - max(xs)}.get(wall, mx)
        oy = {"north": y0 + 1 - min(ys), "south": y1 - max(ys), "nw": y0 + 1 - min(ys), "se": y1 - max(ys)}.get(wall, my)
    clash = []
    # the north row and west column are wall-only tiles; the south row and east column are floor with the wall on
    # their far edge, so furniture may share them (OSI's multis do)
    wall_tiles = {(x, y0) for x in range(x0, x1 + 1)} | {(x0, y) for y in range(y0, y1 + 1)}
    for tid, dx, dy, dz in p:
        x, y = ox + dx, oy + dy
        statics.append((x, y, dz + 1, tid))
        if (x, y) in wall_tiles:
            clash.append((tid, x, y))
    land = {(x, y): (0x0003, 0) for x in range(x0 - 2, x1 + 4) for y in range(y0 - 2, y1 + 4)}
    return iso, iso.Scene(land, statics), (x0 - 1, y0 - 1, x1 + 2, y1 + 2), (ox, oy), clash


def render_room(design, wall, ox=None, oy=None):
    iso, scene, box, at, clash = room_scene(design, wall, ox, oy)
    im = iso.render(scene, *box, art=iso.Art())
    return im, at, clash


def sheet(out, specs):
    from PIL import Image, ImageDraw
    tiles = []
    for spec in specs:
        design, wall = spec.split(":")
        im, at, clash = render_room(design, wall)
        title = "%s on the %s wall, origin %d,%d%s" % (design, wall, at[0], at[1],
                                                      ", ON WALL TILES: %d" % len(clash) if clash else "")
        print(title)
        tiles.append((title, im))
    cols = min(3, len(tiles))
    cw, ch = 520, 460
    rows = (len(tiles) + cols - 1) // cols
    sh = Image.new("RGB", (cols * cw + 20, rows * ch + 20), (27, 27, 27))
    d = ImageDraw.Draw(sh)
    for i, (title, im) in enumerate(tiles):
        im = im.convert("RGB")
        im.thumbnail((cw - 20, ch - 40))
        x, y = 20 + (i % cols) * cw, 10 + (i // cols) * ch
        d.text((x, y), title, fill=(240, 198, 116))
        sh.paste(im, (x, y + 22))
    sh.save(out, quality=85)
    print(out, sh.size)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "summary":
        summary()
    elif cmd == "room":
        out, design, wall = sys.argv[2:5]
        rest = [int(v) for v in sys.argv[5:7]]
        im, at, clash = render_room(design, wall, *(rest or [None, None]))
        im.convert("RGB").save(out, quality=88)
        print(out, at, "clash", clash)
    elif cmd == "sheet":
        sheet(sys.argv[2], sys.argv[3:])
