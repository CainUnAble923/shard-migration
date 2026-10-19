"""The wall rule, corners and doorway frames (cc-P180 research in notes/uo-wall-orientation.md; cc-P181 frames;
cc-P185 the run-topology rule, sections 9-12 of that note).

A wall piece's art stands on its own tile's SOUTH edge (the "ew" piece, running along x) or EAST edge (the "ns"
piece, running along y); the corner piece carries both slabs; the post marks the tile's south-east corner point.
Which piece a wall tile takes is decided by the runs through it, i.e. which of its four orthogonal neighbours are
wall tiles (wall_role): a free end takes the run's piece, an L takes post / ew / ns / corner by which two runs meet,
a T takes the through run's piece plus the branch's slab only when the branch comes from the west or the north.
The wall tiles themselves are the 8-neighbour ring of non-floor tiles round the floor (ring_of). Openings
(doorways, gaps) are floor: the run ends either side of them.
Marble doorways (OSI Nujel'm and Magincia): the wall before the gap keeps its run piece, the arch top (0x0114 /
0x0116, passable) goes on the first open tile, the pier (0x0113 / 0x0115) replaces the run piece on the wall tile
after the gap. A pier on the tile before leaves half a tile of nothing between the run and the pier (P181's gap).

A wall set is a dict such as plan-sets.json's:
    {"ew": "0x01D0", "ns": "0x01D1", "corner": "0x01CF", "post": "0x01D2",
     "frameNS": {"first": "0x01D8", "mid": null, "after": "0x01D9", "before": null},
     "frameEW": {"first": "0x01D6", "mid": null, "after": "0x01D7", "before": null}}
frameNS frames a gap that runs along y (a north-south wall), frameEW a gap along x: "first" goes on the first open
tile (north or west end), "mid" on the other open tiles (or nothing), "after" replaces the wall piece on the wall
tile past the gap (south or east), "before" replaces the one before it (north or west); "replaces": false keeps the
run piece beside the jamb (the dungeon set does that on OSI's map). Measured on OSI:
    stone   N-S: Terathan Keep column 5431, y 3132-3134 (0x01D8 open, 0x01D9 jamb after); E-W: 5436-5438, 3131
    dungeon E-W: Deceit row 535, x 5209-5212 (0x0245, 0x0247, 0x0247, 0x0249 jamb); N-S: column 5183, y 541-543
            (0x0248 on the open tiles, 0x024A on the wall tile after, beside its run piece)
    marble  E-W: Nujel'm row 1323, x 3737-3740 (0x0113 pier, 0x0114 half arch, open, 0x0113 pier);
            N-S: Magincia column 3716, y 2064-2067 (0x0115 pier, 0x0116, open, 0x0115)
"""
import collections


def hx(v):
    return int(v, 16) if isinstance(v, str) else int(v)


def wall_role(Wt, x, y):
    """The role of the wall tile (x, y) by the RUN-TOPOLOGY rule (cc-P185, measured on 9,744 OSI wall tiles in nine
    dungeons and two towns: 98.0 percent agreement, against 91.1 for P180's floor rule). Wt(c) is true for a tile that
    carries a wall (a ring tile of a walled floor, a walled pillar); cave rock, void and floor are not wall tiles.
    What decides the piece is which orthogonal neighbours are wall tiles (which runs pass through the tile), not where
    the floor is:
      one wall neighbour (a run's free end, at a doorway, a passage or rock): the run's own piece, nothing added
      two opposite: the run's piece (a wall between two floors, a ring row or column)
      two adjacent (an L, the outline turning): W+S -> ew (NE corner), E+S -> post (NW corner), N+E -> ns (SW corner),
        N+W -> corner (SE corner); the same four whether the floor is inside the L or outside it (a solid block's
        corner with floor on two sides takes the same piece as a room's corner)
      three (a T): the through run's piece, plus the branch's slab when the branch comes from the west (its line must
        reach the through line: corner) or from the north (corner); a branch from the east or south stops at the
        junction tile's corner point on its own (ns, ew)
      four (a cross) or none (a one-tile pillar): corner
    Returns ew, ns, corner or post."""
    wN, wE, wS, wW = Wt((x, y - 1)), Wt((x + 1, y)), Wt((x, y + 1)), Wt((x - 1, y))
    n = wN + wE + wS + wW
    if n == 1:
        return "ns" if (wN or wS) else "ew"
    if n == 2:
        if wN and wS:
            return "ns"
        if wE and wW:
            return "ew"
        if wW and wS:
            return "ew"
        if wE and wS:
            return "post"
        if wN and wE:
            return "ns"
        return "corner"          # wN and wW
    if n == 3:
        if not wW:
            return "ns"
        if not wN:
            return "ew"
        return "corner"          # the branch comes from the west (no east) or from the north (no south)
    return "corner"


def wall_pieces(Wt, x, y, ws):
    """Pieces for the wall tile (x, y) by wall_role: [(tileId, role)]. A set without a corner piece gets both runs."""
    role = wall_role(Wt, x, y)
    if role == "corner" and not ws.get("corner"):
        return [(hx(ws["ew"]), "ew"), (hx(ws["ns"]), "ns")]
    return [(hx(ws[role]), role)]


def wall_pieces_p180(F, x, y, ws):
    """P180's floor rule, kept so the junction check can show what it placed (cc-P181's build): a slab wherever floor
    lies across the tile's north/south or east/west, plus diagonal corner terms. Right on 91.1 percent of OSI wall
    tiles; wrong at run ends (a stub across the end), at outer corners with floor on two sides (a corner piece where
    OSI uses a post or a run piece) and at a corridor leaving a room (stubs into the mouth)."""
    N, S, E, W = F((x, y - 1)), F((x, y + 1)), F((x + 1, y)), F((x - 1, y))
    NE, NW, SE, SW = F((x + 1, y - 1)), F((x - 1, y - 1)), F((x + 1, y + 1)), F((x - 1, y + 1))
    needS = N or S or (SW and not W and not S) or (NW and not W and not N)
    needE = E or W or (NE and not N and not E) or (NW and not N and not W)
    if needS and needE:
        if ws.get("corner"):
            return [(hx(ws["corner"]), "corner")]
        return [(hx(ws["ew"]), "ew"), (hx(ws["ns"]), "ns")]
    if needS:
        return [(hx(ws["ew"]), "ew")]
    if needE:
        return [(hx(ws["ns"]), "ns")]
    if SE:
        return [(hx(ws["post"]), "post")]
    return []


def ring_of(floor):
    """The 8-neighbour ring of non-floor tiles around a floor set (these carry the walls)."""
    ring = set()
    for (x, y) in floor:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if (x + dx, y + dy) not in floor:
                    ring.add((x + dx, y + dy))
    return ring


def walls_for(floor, openings, ws, z=0):
    """Wall statics [(x, y, z, id, role)] for a floor set, plus the ring (the wall tiles; openings are floor)."""
    ring = ring_of(floor)
    Wt = lambda c: c in ring
    out = []
    for (x, y) in sorted(ring):
        for tid, role in wall_pieces(Wt, x, y, ws):
            out.append((x, y, z, tid, role))
    return out, ring


# ------------------------------------------------------------------------------------------------ corners

DIAG = ((-1, -1, "NW"), (1, -1, "NE"), (-1, 1, "SW"), (1, 1, "SE"))


def concave_corners(floor, solid, skip=()):
    """Floor tiles in an inner corner: solid straight north or south AND straight east or west.
    Returns [(x, y, name)] with name the corner's direction (NW: solid to the N and W)."""
    out = []
    for (x, y) in sorted(floor):
        if (x, y) in skip:
            continue
        for dx, dy, nm in DIAG:
            if solid((x + dx, y)) and solid((x, y + dy)):
                out.append((x, y, nm))
    return out


def convex_corners(floor, solid, skip=()):
    """Floor tiles wrapping round a solid corner: the diagonal is solid, both orthogonals are floor.
    Returns [(x, y, name)] with name the direction of the solid diagonal."""
    out = []
    for (x, y) in sorted(floor):
        if (x, y) in skip:
            continue
        for dx, dy, nm in DIAG:
            if solid((x + dx, y + dy)) and not solid((x + dx, y)) and not solid((x, y + dy)):
                out.append((x, y, nm))
    return out


def visible_strip_tiles(corner, solid):
    """The wall tiles whose top face the player sees at an inner corner: the one south of the floor tile and the one
    east of it (a wall tile's slab stands on its far edge, so the south and east ring tiles show floor; the north and
    west ones hide behind their slab). corner = (x, y, name)."""
    x, y, nm = corner
    out = []
    if "S" in nm and solid((x, y + 1)):
        out.append((x, y + 1))
    if "E" in nm and solid((x + 1, y)):
        out.append((x + 1, y))
    if nm == "SE" and solid((x + 1, y + 1)):
        out.append((x + 1, y + 1))
    return out


# ------------------------------------------------------------------------------------------------ openings and frames

def opening_groups(openings, solid):
    """Group opening tiles into straight gaps. Each group: dict(tiles, axis ('y' for a gap running along y through
    a north-south wall, 'x' through an east-west wall), before, after) where before/after are the wall tiles at the
    two ends of the gap line (north/south or west/east)."""
    left = set(openings)
    groups = []
    while left:
        start = min(left)
        x, y = start
        # which way does the gap run: along y if the tile north or south is also an opening, or if the tiles east
        # and west are solid (a one-tile gap in a north-south wall)
        along_y = (x, y + 1) in left or (x, y - 1) in left or (solid((x - 1, y)) and solid((x + 1, y)) and not solid((x, y + 1)))
        tiles = [start]
        left.discard(start)
        dx, dy = (0, 1) if along_y else (1, 0)
        cx, cy = x + dx, y + dy
        while (cx, cy) in left:
            tiles.append((cx, cy)); left.discard((cx, cy)); cx, cy = cx + dx, cy + dy
        first, last = tiles[0], tiles[-1]
        before = (first[0] - dx, first[1] - dy)
        after = (last[0] + dx, last[1] + dy)
        groups.append(dict(tiles=tiles, axis="y" if along_y else "x", before=before, after=after,
                           before_solid=solid(before), after_solid=solid(after)))
    return groups


def frame_pieces(group, ws):
    """[(x, y, id, role, replaces_wall)] framing one opening group with the wall set's frame rule, or [] if the set
    has none for that axis. replaces_wall is true for the jamb or pier on a wall tile (its run piece goes)."""
    rule = ws.get("frameNS" if group["axis"] == "y" else "frameEW")
    if not rule:
        return []
    out = []
    tiles = group["tiles"]
    if rule.get("first"):
        out.append((tiles[0][0], tiles[0][1], hx(rule["first"]), "frame first", False))
    if rule.get("mid"):
        for t in tiles[1:]:
            out.append((t[0], t[1], hx(rule["mid"]), "frame mid", False))
    rep = rule.get("replaces", True)
    if rule.get("after") and group["after_solid"]:
        out.append((group["after"][0], group["after"][1], hx(rule["after"]), "frame jamb", rep))
    if rule.get("before") and group["before_solid"]:
        out.append((group["before"][0], group["before"][1], hx(rule["before"]), "frame jamb", rep))
    return out


# ------------------------------------------------------------------------------------------------ checks

def check_wall_tiles(statics, items, allow_double=()):
    """Every tile should carry at most one wall-flagged piece (the corner piece is one piece); returns the tiles
    that carry more, except those in allow_double (a dungeon-set jamb sits beside its run piece on OSI's map)."""
    WALL = 1 << 4
    per = collections.defaultdict(list)
    for s in statics:
        x, y, z, tid = s[0], s[1], s[2], s[3]
        if items[tid]["flags"] & WALL:
            per[(x, y)].append(tid)
    return sorted((c, v) for c, v in per.items() if len(v) > 1 and c not in allow_double)
