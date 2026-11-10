"""cc-P856: one-off. The walk check counted a tile inside a piece's own bounding box (a gap between the train's cars)
as cut off; such a tile is part of the piece, not the town. Both finders and main's validator now leave the pieces'
boxes out of the cut-off count."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def box(tiles, ox, oy):
    xs, ys = [dx for dx, _ in tiles], [dy for _, dy in tiles]
    return {(x, y) for x in range(ox + min(xs), ox + max(xs) + 1) for y in range(oy + min(ys), oy + max(ys) + 1)}


def edit(path, pairs):
    s = open(path, encoding="utf-8").read()
    for old, new in pairs:
        assert s.count(old) == 1, (path, old)
        s = s.replace(old, new)
    open(path, "w", encoding="utf-8", newline="\n").write(s)
    print("edited", path)


edit(os.path.join(HERE, "find856.py"), [
    ("""    cut = sorted(R.REACH - after - block)
    if cut:""", """    # a tile inside the piece's own box (a gap between its parts) is the piece's, not cut off from the town
    xs, ys = [dx for dx, _ in tiles], [dy for _, dy in tiles]
    inside = {(x, y) for x in range(ox + min(xs), ox + max(xs) + 1) for y in range(oy + min(ys), oy + max(ys) + 1)}
    cut = sorted(R.REACH - after - block - inside)
    if cut:"""),
])
edit(os.path.join(HERE, "validate856.py"), [
    ("""    block = set()
    for key, area, design, x, y, z, name in rs:
        block |= {(x + dx, y + dy) for dx, dy in F.design_tiles(design)}""",
     """    block, inside = set(), set()
    for key, area, design, x, y, z, name in rs:
        tiles = F.design_tiles(design)
        block |= {(x + dx, y + dy) for dx, dy in tiles}
        xs, ys = [dx for dx, _ in tiles], [dy for _, dy in tiles]   # gaps inside a piece's box are the piece's
        inside |= {(i, j) for i in range(x + min(xs), x + max(xs) + 1) for j in range(y + min(ys), y + max(ys) + 1)}"""),
    ("""    cut = sorted(F.R.REACH - after - block)""", """    cut = sorted(F.R.REACH - after - block - inside)"""),
])
edit(os.path.join(HERE, "rel", "findrel.py"), [
    ("""    cut = walk_cut({(ox + dx, oy + dy) for dx, dy in tiles})""",
     """    xs, ys = [dx for dx, _ in tiles], [dy for _, dy in tiles]   # gaps inside the piece's box are the piece's
    inside = {(x, y) for x in range(ox + min(xs), ox + max(xs) + 1) for y in range(oy + min(ys), oy + max(ys) + 1)}
    cut = [t for t in walk_cut({(ox + dx, oy + dy) for dx, dy in tiles}) if t not in inside]"""),
    ("""        block |= {(x + dx, y + dy) for dx, dy in design_tiles(design)}
    cut = walk_cut(block)""", """        block |= {(x + dx, y + dy) for dx, dy in design_tiles(design)}
        tiles = design_tiles(design)
        xs, ys = [dx for dx, _ in tiles], [dy for _, dy in tiles]
        inside |= {(i, j) for i in range(x + min(xs), x + max(xs) + 1) for j in range(y + min(ys), y + max(ys) + 1)}
    cut = [t for t in walk_cut(block) if t not in inside]"""),
    ("""    bad, lines, block = 0, [], set()""", """    bad, lines, block, inside = 0, [], set(), set()"""),
])
