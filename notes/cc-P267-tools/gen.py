# cc-P267 WRITES placement.json: one Halloween template per bank, picked by rule from the map and then re-checked by
# validate.py (which reads placement.json back without trusting anything here). Deterministic: one random.Random per
# bank, seeded from its key, so a rerun gives the same rows.
#
# What a template holds, and the rules (the prompt: pumpkins, candles, bone decor, cobwebs and lanterns around the
# bank, kept off doors, banker paths, teleporters and roads):
#   outside   the ground tiles that touch the bank's outer wall (so a road tile is only ever used at the wall's foot,
#             never in the way): pumpkins, carved pumpkins, hay, bones, skulls; two lanterns flank each door, two
#             tiles along the wall from it; one centrepiece (a cauldron, a scarecrow or a gravestone) at a convex
#             corner on grass or dirt, never on a road
#   corner    inside, the floor tile in an inner corner (walls on two sides): a cobweb
#   indoor    inside, a floor tile against a wall: bones or a skull (passable pieces only)
#   table     on a counter or table top inside: a skull with a candle, a candle, a small pumpkin
# Protected (never used, and not even next to, where the rule says so): the door tiles pinned DoorGenerator would
# place and their swing tiles (BaseDoor.GetOffset), two tiles either side of every doorway, map statics flagged
# Door and their neighbours, the shortest path from every door to every banker (and its neighbours), every pinned
# spawner in the box (and its home range, capped at 2), every pinned Decoration cfg item in the box, every
# teleporter end in the box.
import json, random, collections, sys, os
import bankbase as B

HERE = os.path.dirname(os.path.abspath(__file__))

# The banks. z is the floor the bankers stand on (their spawner's z). box is the search area. bankers come from
# pinned Distribution/Data/Spawns (shared + post-uoml Vendors.json). open=True: no roof, no interior search.
BANKS = [
    dict(key='new-haven', name='New Haven', facet='Trammel', z=20, bankers=[(3484, 2570), (3484, 2576)]),
    dict(key='britain', name='Britain (west bank)', facet='Trammel', z=0, bankers=[(1425, 1690)]),
    dict(key='moonglow', name='Moonglow', facet='Trammel', z=0, bankers=[(4471, 1156)]),
    dict(key='trinsic', name='Trinsic', facet='Trammel', z=10, bankers=[(1897, 2684)]),
    dict(key='vesper', name='Vesper', facet='Trammel', z=0, bankers=[(2881, 684)]),
    dict(key='minoc', name='Minoc', facet='Trammel', z=0, bankers=[(2503, 552)]),
    dict(key='yew', name='Yew', facet='Trammel', z=0, bankers=[(652, 820)], radius=7),
    dict(key='skara-brae', name='Skara Brae', facet='Trammel', z=0, bankers=[(587, 2146)]),
    dict(key='jhelom', name='Jhelom', facet='Trammel', z=0, bankers=[(1317, 3773)]),
    dict(key='luna', name='Luna', facet='Malas', z=-50, bankers=[(989, 520)]),
    dict(key='umbra', name='Umbra', facet='Malas', z=-85, bankers=[(2048, 1343)], radius=7),
    # Zento's banker stands on the ground (z25) at the north-west corner of the market deck (boards at z30), by its stall.
    dict(key='zento', name='Zento', facet='Tokuno', z=25, bankers=[(729, 1249)], open=True, radius=6),
    dict(key='royal-city', name='Royal City', facet='TerMur', z=-20, bankers=[(833, 3439), (843, 3439)]),
]
# Felucca twins of the Britannia banks (same buildings on map0; every tile is re-checked on map0 by this script and by
# validate.py). New Haven is left out: pinned spawns no Felucca banker there.
for b in list(BANKS):
    if b['facet'] == 'Trammel' and b['key'] != 'new-haven':
        BANKS.append(dict(b, key=b['key'] + '-fel', name=b['name'] + ' (Felucca)', facet='Felucca'))

R = 20   # half-size of the search box around the bankers

# Pieces (stock art; every ID checked against the client's tiledata and art by validate.py).
PUMPKINS = [(0x0C6A, 'a pumpkin', 3), (0x0C6B, 'a pumpkin', 3), (0x0C6C, 'a pumpkin', 2), (0x0C64, 'a gourd', 1)]
CARVED = [(0x4691, 'a carved pumpkin', 1), (0x4695, 'a carved pumpkin', 1)]      # lit; Impassable, height 5
GROUND_BONES = [(0x0ECA, 'bones', 1), (0x0ECD, 'bones', 1), (0x0ED0, 'bones', 1), (0x1ADA, 'a pile of skulls', 1), (0x1AE0, 'a skull', 1), (0x1AE2, 'a skull', 1)]
HAY = [(0x0F34, 'hay', 1), (0x0F35, 'hay', 1), (0x1A92, 'hay', 1), (0x1A94, 'hay', 1)]
CENTRE = [(0x0974, 'a cauldron', 2), (0x1E34, 'a scarecrow', 2), (0x1E35, 'a scarecrow', 1), (0x0ED5, 'a gravestone', 1), (0x0EDB, 'a gravestone', 1)]
WEBS = {'nw': 0x0EE3, 'ne': 0x0EE4, 'se': 0x0EE5, 'sw': 0x0EE6}   # spiderweb corners (checked on a render, notes section B)
INDOOR = [(0x0ECA, 'bones', 1), (0x0ECB, 'bones', 1), (0x0ECE, 'bones', 1), (0x1ADD, 'a pile of skulls', 1), (0x1AE1, 'a skull', 1), (0x1AE3, 'a skull', 1), (0x10D2, 'a small web', 1), (0x10D4, 'a small web', 1)]
TABLE = [(0x1854, 'a skull with a candle', 3), (0x1858, 'a skull with a candle', 2), (0x0A0F, 'a candle', 2), (0x0C6C, 'a pumpkin', 2)]
LANTERN = (0x0A22, 'a lantern')
ALL_IDS = sorted({i for t in (PUMPKINS, CARVED, GROUND_BONES, HAY, CENTRE, INDOOR, TABLE) for i, _, _ in t} | set(WEBS.values()) | {LANTERN[0]})
NAMES = {i: n for t in (PUMPKINS, CARVED, GROUND_BONES, HAY, CENTRE, INDOOR, TABLE) for i, n, _ in t}
NAMES.update({v: 'a cobweb' for v in WEBS.values()}); NAMES[LANTERN[0]] = LANTERN[1]


def weighted(rng, table, avoid=()):
    pool = [(i, n) for i, n, w in table for _ in range(w) if i not in avoid]
    if not pool: pool = [(i, n) for i, n, w in table for _ in range(w)]
    return rng.choice(pool)


def neighbours4(x, y): return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
def neighbours8(x, y): return [(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy]


class Bank:
    def __init__(self, spec):
        self.spec = spec
        self.F = FACETS.setdefault(spec['facet'], B.Facet(B.FACET[spec['facet']]))
        F = self.F
        self.fz = spec['z']
        self.open = spec.get('open', False)
        self.radius = spec.get('radius', 24)
        xs = [p[0] for p in spec['bankers']]; ys = [p[1] for p in spec['bankers']]
        self.box = (min(xs) - R, min(ys) - R, max(xs) + R, max(ys) + R)
        x0, y0, x1, y1 = self.box
        self.protected = {}
        P = lambda x, y, why: self.protected.setdefault((x, y), []).append(why)
        # doors
        self.doors = B.generated_doors(F, x0 - 2, y0 - 2, x1 + 2, y1 + 2)
        for (x, y, z, facing) in self.doors:
            P(x, y, 'door'); dx, dy = B.SWING[facing]; P(x + dx, y + dy, 'door swing')
            if facing in ('WestCW', 'EastCCW'):     # a doorway in an east-west wall: the walk is north-south
                for k in (1, 2): P(x, y - k, 'in front of a door'); P(x, y + k, 'in front of a door')
            else:
                for k in (1, 2): P(x - k, y, 'in front of a door'); P(x + k, y, 'in front of a door')
        self.static_doors = B.static_doors(F, x0, y0, x1, y1)
        for (x, y, z, sid) in self.static_doors:
            P(x, y, 'door static 0x%04X' % sid)
            for nx, ny in neighbours8(x, y): P(nx, ny, 'beside a door static')
            for k in (2,):
                for nx, ny in ((x, y - k), (x, y + k), (x - k, y), (x + k, y)): P(nx, ny, 'in front of a door static')
        # spawners, decoration items, teleporters
        for s in B.spawns_in(F.name, x0, y0, x1, y1):
            r = min(2, s[4])
            for dx in range(-r, r + 1):
                for dy in range(-r, r + 1):
                    P(s[1] + dx, s[2] + dy, 'spawner %s' % ','.join(n for n in s[5] if n))
            for nx, ny in neighbours8(s[1], s[2]): P(nx, ny, 'beside spawner %s' % ','.join(n for n in s[5] if n))
        for d in B.decoration_in(F.fi, x0, y0, x1, y1):
            P(d[0], d[1], 'decoration %s %s (%s)' % (d[3], d[4], d[5]))
        for t in B.teleporters_in(F.name, x0, y0, x1, y1):
            P(t[0], t[1], 'teleporter %s' % t[3])
            for nx, ny in neighbours8(t[0], t[1]): P(nx, ny, 'beside a teleporter')
        # the building: floor tiles reachable from the bankers at the floor z, under a roof
        self.interior = self.flood()
        self.walls = {}
        for (x, y) in list(self.interior):
            for nx, ny in neighbours4(x, y):
                if F.wall_at(nx, ny, self.fz): self.walls[(nx, ny)] = True
        # The structure the decor hugs: the walls, and for an open-air or arched bank (few Wall-flagged pieces) the tall
        # impassable pieces near the bankers too (a stall's counters, pillars, arches).
        self.structure = dict(self.walls)
        if self.open or len(self.walls) < 20:
            FOLIAGE = 1 << 17
            r = 5 if self.open else 8
            for bx, by in spec['bankers']:
                for dx in range(-r, r + 1):
                    for dy in range(-r, r + 1):
                        x, y = bx + dx, by + dy
                        for s, sz in F.statics(x, y):
                            f = B.iflags(s)
                            if f & (FOLIAGE | B.WET): continue
                            tall = f & B.IMP and not f & B.WALL and B.iheight(s) >= 5 and self.fz - 3 <= sz <= self.fz + 3
                            raised = f & B.SURF and self.fz + 3 <= sz + B.calch(s) <= self.fz + 10   # a deck or platform edge
                            if tall or raised: self.structure[(x, y)] = True
        # banker paths: from each door tile to each banker, shortest over the floor
        for (x, y, z, facing) in self.doors + [(d[0], d[1], d[2], None) for d in self.static_doors]:
            for bx, by in spec['bankers']:
                path = self.path((x, y), (bx, by))
                for px, py in path:
                    P(px, py, 'banker path')
                    for nx, ny in neighbours4(px, py): P(nx, ny, 'beside a banker path')

    def floor_ok(self, x, y):
        F = self.F; fz = self.fz
        s = F.top_surface(x, y, fz + 2)
        return s is not None and abs(s - fz) <= 2 and not F.blocked(x, y, s) and not F.wall_at(x, y, fz)

    def roofed(self, x, y):
        if self.open:   # an open-air bank: any floor at the floor z within the radius counts (see near)
            return True
        return any(sz > self.fz + 8 for s, sz in self.F.statics(x, y))

    def near(self, x, y):
        return min(max(abs(x - bx), abs(y - by)) for bx, by in self.spec['bankers']) <= self.radius

    def flood(self):
        F = self.F; x0, y0, x1, y1 = self.box
        seen = set(); q = collections.deque()
        for bx, by in self.spec['bankers']:
            for sx, sy in [(bx, by)] + neighbours4(bx, by):
                if self.floor_ok(sx, sy) and self.roofed(sx, sy): seen.add((sx, sy)); q.append((sx, sy))
        doors = {(d[0], d[1]) for d in self.doors} | {(d[0], d[1]) for d in self.static_doors}
        while q:
            x, y = q.popleft()
            if (x, y) in doors: continue
            for nx, ny in neighbours4(x, y):
                if (nx, ny) in seen or not (x0 <= nx <= x1 and y0 <= ny <= y1) or not self.near(nx, ny): continue
                if self.floor_ok(nx, ny) and (self.roofed(nx, ny) or (nx, ny) in doors):
                    seen.add((nx, ny)); q.append((nx, ny))
        return seen

    def path(self, a, b):
        """Shortest walk over interior floor tiles (door tiles allowed) from a to b, or []."""
        allowed = set(self.interior) | {a, b}
        if a not in allowed or b not in allowed: return []
        prev = {a: None}; q = collections.deque([a])
        while q:
            cur = q.popleft()
            if cur == b: break
            for n in neighbours4(*cur):
                if n in allowed and n not in prev: prev[n] = cur; q.append(n)
        if b not in prev: return []
        out = []; cur = b
        while cur: out.append(cur); cur = prev[cur]
        return out

    # ---- candidates
    def rim(self):
        """Open-air bank: platform tiles at its edge (a 4-neighbour off the platform and lower), or touching a piece
        of the stall."""
        F = self.F; out = []
        for (x, y) in self.interior:
            edge = False
            for nx, ny in neighbours4(x, y):
                if (nx, ny) in self.structure: edge = True; break
                if (nx, ny) in self.interior: continue
                s = F.top_surface(nx, ny, self.fz + 2)
                if s is None or s < self.fz - 1: edge = True; break
            if edge: out.append((x, y))
        return sorted(out)

    def outside_candidates(self):
        """Ground tiles touching the structure (an outer wall, or for an open-air bank a stall piece or pillar) at the
        floor z, not inside, not protected, with a surface near the floor and nothing in the way.
        Returns [(x, y, z, walkway, wall_dir)]."""
        F = self.F; out = []
        if self.open:
            for (x, y) in self.rim():
                if (x, y) in self.protected: continue
                s = F.top_surface(x, y, self.fz + 2)
                if s is None or abs(s - self.fz) > 2 or F.blocked(x, y, s): continue
                if any(B.iflags(i) & B.BRIDGE for i, _ in F.statics(x, y)): continue   # not on the steps
                out.append((x, y, s, '', 'rim'))
            return sorted(set(out))
        for (wx, wy) in self.structure:
            for nx, ny in neighbours4(wx, wy):
                if (not self.open and (nx, ny) in self.interior) or (nx, ny) in self.structure or (nx, ny) in self.protected: continue
                # Only the faces the client shows: the tile south or east of the wall. A piece north or west of a wall
                # is drawn before the wall and hidden behind it (P34's wall-art rule, the same reason).
                if (wx, wy) not in ((nx, ny - 1), (nx - 1, ny)): continue
                if F.wall_at(nx, ny, self.fz): continue
                s = F.top_surface(nx, ny, self.fz + 2)
                if s is None or s > self.fz + 2 or s < self.fz - 10: continue
                if F.blocked(nx, ny, s): continue
                if self.roofed(nx, ny) and any(B.iflags(i) & B.ROOF and sz > s + 8 for i, sz in F.statics(nx, ny)) and (nx, ny) not in self.interior:
                    pass   # under an eave is fine
                d = 'n' if (wx, wy) == (nx, ny + 1) else 's' if (wx, wy) == (nx, ny - 1) else 'w' if (wx, wy) == (nx + 1, ny) else 'e'
                out.append((nx, ny, s, B.walkway(F, nx, ny, s), d))
        return sorted(set(out))

    def corner_candidates(self):
        """Interior floor tiles with walls on two orthogonal sides, with the corner's name (nw, ne, se, sw)."""
        F = self.F; out = []
        for (x, y) in self.interior:
            if (x, y) in self.protected: continue
            n, s, w, e = F.wall_at(x, y - 1, self.fz), F.wall_at(x, y + 1, self.fz), F.wall_at(x - 1, y, self.fz), F.wall_at(x + 1, y, self.fz)
            for name, cond in (('nw', n and w), ('ne', n and e), ('se', s and e), ('sw', s and w)):
                if cond: out.append((x, y, name))
        return sorted(out)

    def wallside_candidates(self):
        F = self.F; out = []
        for (x, y) in self.interior:
            if (x, y) in self.protected: continue
            if any(F.wall_at(nx, ny, self.fz) for nx, ny in neighbours4(x, y)):
                out.append((x, y))
        return sorted(out)

    def table_candidates(self):
        """Surface + Impassable static tops (counters, tables) inside the building at the floor z, with the top z."""
        F = self.F; out = []
        tiles = set()
        for (x, y) in self.interior:
            for nx, ny in neighbours4(x, y): tiles.add((nx, ny))
        for (x, y) in tiles | set(self.interior):
            if (x, y) in self.protected or (x, y) in self.walls: continue
            for sid, sz in F.statics(x, y):
                f = B.iflags(sid)
                if f & B.SURF and f & B.IMP and self.fz - 3 <= sz <= self.fz + 3 and B.iheight(sid) >= 4 and (self.open or self.roofed(x, y)):
                    out.append((x, y, sz + B.calch(sid), sid))
        return sorted(set(out))

    def door_flank_spots(self):
        """Two tiles along the outer wall either side of each door, on the outside: lantern spots. Open-air bank: the
        platform's corners."""
        F = self.F; spots = []
        cands = {(c[0], c[1]): c for c in self.outside_candidates()}
        if self.open:   # no doors: up to four lanterns spread along the platform's edge
            return pick_spaced(random.Random('lanterns ' + self.spec['key']), list(cands.values()), 4, [], 4)
        for (x, y, z, facing) in self.doors:
            if facing in ('WestCW', 'EastCCW'):   # doorway in an east-west wall: flank along x, on the outside row
                for side in (-1, 1):
                    for k in (2, 3):
                        for oy in (-1, 1):
                            c = cands.get((x + side * k, y + oy))
                            if c and (x + side * k, y + oy) not in self.interior: spots.append(c); break
                        else: continue
                        break
            else:
                for side in (-1, 1):
                    for k in (2, 3):
                        for ox in (-1, 1):
                            c = cands.get((x + ox, y + side * k))
                            if c and (x + ox, y + side * k) not in self.interior: spots.append(c); break
                        else: continue
                        break
        return spots

    def convex_corners(self):
        """Outside tiles diagonal to a wall corner (a wall tile with walls on two orthogonal sides), not protected,
        on ground that is not a road: centrepiece spots."""
        F = self.F; out = []
        for (wx, wy) in self.walls:
            n, s, w, e = [(nx, ny) in self.walls for nx, ny in ((wx, wy - 1), (wx, wy + 1), (wx - 1, wy), (wx + 1, wy))]
            for (cx, cy), cond in (((wx - 1, wy - 1), s and e), ((wx + 1, wy - 1), s and w), ((wx - 1, wy + 1), n and e), ((wx + 1, wy + 1), n and w)):
                if not cond or (cx, cy) in self.interior or (cx, cy) in self.walls or (cx, cy) in self.protected: continue
                if F.wall_at(cx, cy, self.fz): continue
                sz = F.top_surface(cx, cy, self.fz + 2)
                if sz is None or sz > self.fz + 2 or sz < self.fz - 10 or F.blocked(cx, cy, sz): continue
                if B.walkway(F, cx, cy, sz): continue
                open_sides = sum(1 for nx, ny in neighbours4(cx, cy) if not F.wall_at(nx, ny, sz) and not F.blocked(nx, ny, sz) and F.top_surface(nx, ny, sz + 2) is not None)
                if open_sides >= 3: out.append((cx, cy, sz))
        return sorted(set(out))


FACETS = {}


def pick_spaced(rng, cands, n, used, mind=2):
    """Up to n candidates, each at least mind (Chebyshev) from every used tile."""
    out = []
    cands = list(cands); rng.shuffle(cands)
    for c in cands:
        if len(out) >= n: break
        if all(max(abs(c[0] - u[0]), abs(c[1] - u[1])) >= mind for u in used): out.append(c); used.append((c[0], c[1]))
    return out


def generate(spec):
    bank = Bank(spec)
    rng = random.Random('cc-P267 ' + spec['key'].replace('-fel', ''))   # the Felucca twin gets the same picks
    rows = []; used = []
    key = spec['key']
    def row(k, x, y, z, item, name, mode, why):
        rows.append(dict(key='%s/%s' % (key, k), bank=key, bankName=spec['name'], facet=spec['facet'], x=x, y=y, z=z, itemId=item, name=name, mode=mode, why=why))
    # 1. lanterns flanking the doors
    for i, c in enumerate(bank.door_flank_spots()):
        if (c[0], c[1]) in used: continue
        row('lantern-%d' % (i + 1), c[0], c[1], c[2], LANTERN[0], LANTERN[1], 'outside', 'at the edge of the market deck' if bank.open else 'two tiles along the outer wall from a door, lighting the way in')
        used.append((c[0], c[1]))
    # 2. pumpkins and the rest round the outer wall
    oc = bank.outside_candidates()
    quiet = [c for c in oc if not c[3]]; road = [c for c in oc if c[3]]
    want = max(6, min(10, len(oc) // 6))
    picks = pick_spaced(rng, quiet, want, used, 2)
    if len(picks) < want: picks += pick_spaced(rng, road, want - len(picks), used, 2)
    last = None
    for i, c in enumerate(picks):
        x, y, z, wk, d = c
        open_sides = sum(1 for nx, ny in neighbours4(x, y) if not bank.F.wall_at(nx, ny, z) and not bank.F.blocked(nx, ny, z) and bank.F.top_surface(nx, ny, z + 2) is not None)
        table = PUMPKINS + GROUND_BONES[:3] + HAY[:2]
        if not wk and open_sides >= 3 and rng.random() < 0.35: table = CARVED
        item, name = weighted(rng, table, avoid=(last,))
        last = item
        where = 'at the edge of the market deck' if d == 'rim' else 'at the foot of the %s outer wall%s' % ({'n': 'north', 's': 'south', 'w': 'west', 'e': 'east'}[{'n': 's', 's': 'n', 'w': 'e', 'e': 'w'}[d]], '' if not wk else ' (a street tile, against the wall)')
        row('out-%d' % (i + 1), x, y, z, item, name, 'outside', where)
    # 3. a centrepiece at a convex corner, off the road
    cc = [c for c in bank.convex_corners() if all(max(abs(c[0] - u[0]), abs(c[1] - u[1])) >= 2 for u in used)]
    if cc:
        c = rng.choice(cc)
        item, name = weighted(rng, CENTRE)
        row('centre', c[0], c[1], c[2], item, name, 'outside', 'at an outer corner of the bank, on ground that is not a road')
        used.append((c[0], c[1]))
    # 4. cobwebs in the inner corners
    corners = bank.corner_candidates()
    seen = set(); byname = {}
    for (x, y, cname) in corners:
        byname.setdefault((x, y), cname)
    cused = []
    for i, c in enumerate(pick_spaced(rng, sorted(byname), 6, cused, 3)):
        seen.add(c)
        row('web-%d' % (i + 1), c[0], c[1], bank.fz, WEBS[byname[c]], 'a cobweb', 'corner', 'inner corner (%s) of the hall' % byname[c])
    # 5. bones and skulls along the inner walls
    ws = [c for c in bank.wallside_candidates() if c not in seen]
    for i, c in enumerate(pick_spaced(rng, ws, max(2, min(5, len(ws) // 6)), used, 3)):
        item, name = weighted(rng, INDOOR)
        row('in-%d' % (i + 1), c[0], c[1], bank.fz, item, name, 'indoor', 'on the floor against an inner wall, out of the walk')
    # 6. candles and skulls on the counters
    tc = bank.table_candidates()
    for i, c in enumerate(pick_spaced(rng, tc, max(2, min(5, len(tc) // 3)), used, 2)):
        item, name = weighted(rng, TABLE)
        row('table-%d' % (i + 1), c[0], c[1], c[2], item, name, 'table', 'on a counter top (0x%04X at z%d)' % (c[3], c[2] - B.calch(c[3])))
    return bank, rows


if __name__ == '__main__':
    only = sys.argv[1:]
    allrows = []; report = []
    for spec in BANKS:
        if only and spec['key'] not in only: continue
        bank, rows = generate(spec)
        allrows += rows
        report.append('%-16s %-8s floor z%-4d interior %3d tiles, walls %3d, doors %2d (+%d static), protected %3d tiles, rows %2d' % (
            spec['key'], spec['facet'], bank.fz, len(bank.interior), len(bank.walls), len(bank.doors), len(bank.static_doors), len(bank.protected), len(rows)))
    if not only:
        json.dump(allrows, open(os.path.join(HERE, 'placement.json'), 'w'), indent=1)
        print('wrote placement.json:', len(allrows), 'rows')
    print('\n'.join(report))
