"""cc-P869 (P865 review, item 5): the keep-clear rule both finders were missing.

The building guide (section 5, "Keep clear", and checklist 1.4) keeps trees 3 tiles from server items and landmarks,
and a piece must read from the default camera. P865 found map trees against three of the main pieces and the release
train, and P678's own winter rows (a decorated tree, a snow pile) one or two tiles off the main globe. This module
gives both finders one check: no tree (a map static named tree, leaves, sapling, palm, pine, fir and the like) and none of P678's winter rows
within RADIUS tiles (Chebyshev; "tree" by its tiledata name, pines and firs included) of any tile a piece covers.

  trees_near(statics, iname, tiles, radius)  -> ["x,y 0xID name", ...]
  rows_near(rows, tiles, radius)             -> ["x,y key", ...]   rows: iterable of (x, y, key)
"""
import re

RADIUS = 3
TREE = re.compile(r"\b(tree|trees|leaves|sapling|palm|pine|fir|cypress|yew|spruce|birch|bamboo)\b", re.I)
NOT_TREE = re.compile(r"\b(roof|stump|potted)\b", re.I)   # a palm-frond roof, a stump, a potted tree are not trees


def ring(tiles, radius=RADIUS):
    """Every tile within radius of a covered tile (the covered tiles included)."""
    out = set()
    for x, y in tiles:
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                out.add((x + dx, y + dy))
    return out


def is_tree(iname, sid):
    name = iname(sid)
    return bool(TREE.search(name)) and not NOT_TREE.search(name)


def trees_near(statics, iname, tiles, radius=RADIUS):
    hits = []
    for x, y in sorted(ring(tiles, radius)):
        for sid, sz in statics(x, y):
            if is_tree(iname, sid):
                hits.append("%d,%d 0x%04X %s" % (x, y, sid, iname(sid)))
                break
    return hits


def rows_near(rows, tiles, radius=RADIUS):
    near = ring(tiles, radius)
    return ["%d,%d %s" % (x, y, k) for x, y, k in rows if (x, y) in near]
