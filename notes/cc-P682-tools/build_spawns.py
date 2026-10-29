r"""cc-P682 (SoS swap S10): people for the author's new towns and keeps, and wild creatures on his new land.

    python -P build_spawns.py          writes the spawn files into the code copy (server\data\Spawns\sos\...) and the
                                        survey, ledger and density figures into out\

The author ships no spawns. Everything placed here is a stock ModernUO spawner record, in pinned's spawn JSON, so the
shard builds it with the stock [GenerateSpawners (the console's fresh-world order runs Data/Spawns/sos/**/*.json).

TOWNS (one file each, both facets): the town's buildings are the roofed tiles of its P676 region (a non-foliage static
10 or more above the standing Z), joined 4-way into components of 9 or more tiles. Each building is scored by the trade
fittings among its statics (forge and anvil for a smith, loom and spinning wheel for a tailor, oven for a baker...).
P695's roster (rosters.json, Verite's draft from P672's cast) says which trades a town has and how many. The bank goes in
the building holding the author's go-menu Bank point when there is one; every other trade goes to the free building
whose fittings score best for it, and a trade with no fitting in town takes the largest free building. A vendor stands on
the building's deepest interior tile, reachable on foot from the town's go point. Guards are stock OrderGuard posts (the
type and the 1-count, range-0 record of Serpent's Hold's posts, shared/trammel/TownsPeople.json): stock spawns no
WarriorGuard; a guarded town's guards still come from its region (S3), as in every stock town. Townsfolk are the stock
town mixes: a town crier, the EscortableMage/Noble/SeekerOfAdventure walkers, and Bird/Cat/Dog/Rat, sized so the town's
spawn density per 100 dry tiles meets stock's town median.

KEEPS: a small OrderGuard garrison at the five keeps (P695's counts; Castle Dunbain 2 at its gate, P695 holding its
quest's hired guards), half at the outdoor tiles nearest the author's point, half inside the keep's largest building.

WILD (the named areas: their land new or changed since stock): stock's terrain-to-spawn table, measured from stock itself: every stock wild encounter and wildlife spawner on the
surface (P681's ledger kinds), grouped by the terrain class of its home on the stock map (P681 sosgrid classes). The
rate is the stock creatures per 100 dry outdoor tiles of that class outside towns. On the new land (the author's
Nujelm Desert and Moonglow Forest regions, the new continent; Glimmerwood; the 59 surface components of P669's 65 new
islands, the six dungeon strips being S18's) each class gets stock's rate, by copying stock spawners of that class
(entries, count, ranges, delays), on tiles not in a town (+10), a closure (S14), a dungeon region, within 12 of an
author dungeon entrance, or already in range of a stock wild spawner S9 kept or moved. Felucca's table is Felucca's.
"""
import collections
import csv
import json
import math
import os
import random
import sys
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402
from common import np, NONE, W, H  # noqa: E402

ROSTERS = os.path.join(common.HERE, "rosters.json")          # P695's, copied from golem/Verite/P695 f8c5099
LEDGER = os.path.join(common.NOTES, "cc-P681-tools", "out", "ledger.csv")
SPOTS = os.path.join(common.NOTES, "cc-P669-tools", "out", "spots.csv")
ISLANDS = os.path.join(common.NOTES, "cc-P669-tools", "out", "new-islands.csv")
SPAWNS_OUT = os.path.join(common.SHARD, "server", "data", "Spawns", "sos")
NS = uuid.UUID("5d0c6f2e-82a1-4b7e-9c3d-6820a0f1c682")
FACETS = ["Trammel", "Felucca"]
FOLIAGE = ("leaves", "tree", "branch", "vines", "foliage", "fern", "palm", "willow", "bamboo", "canopy")

# trade fittings: substring of the tiledata name -> weight
FITTINGS = {
    "Blacksmith": {"forge": 5, "anvil": 5, "bellows": 3, "ingots": 1, "forged metal": 2, "hammer": 1},
    "Armorer": {"platemail": 1, "chainmail": 1, "ringmail": 1, "helm": 1, "shield": 1, "decorative armor": 1},
    "Tailor": {"loom": 5, "spinning wheel": 5, "bolt": 2, "cloth": 1, "scissors": 2, "dress form": 3, "thread": 2, "yarn": 2},
    "Baker": {"oven": 5, "flour": 3, "bread": 2, "dough": 3, "pie": 1, "rolling pin": 2},
    "Cook": {"oven": 3, "cauldron": 2, "plate of food": 1, "kettle": 2, "pot": 1, "skillet": 2},
    "Carpenter": {"woodworker's bench": 5, "saw": 3, "wood curls": 2, "nails": 1, "cooper's bench": 3, "lumber": 2, "logs": 1},
    "Tinker": {"tinker": 5, "clock": 3, "gears": 3, "springs": 3, "tool": 1, "hinge": 2, "axle": 2},
    "Alchemist": {"empty jars": 3, "jar": 1, "bottle": 1, "flask": 2, "mortar": 3, "retort": 3, "magical crystal": 1},
    "Bowyer": {"bow": 3, "arrow": 2, "fletching": 4, "shafts": 3, "feathers": 2, "archery butte": 4},
    "InnKeeper": {"bed": 2, "bar": 2, "keg": 2, "wine": 1, "cider": 1, "mug": 1, "fireplace": 1},
    "Fisherman": {"fishing net": 4, "fish": 2, "net": 1, "anchor": 1},
    "Shipwright": {"anchor": 2, "rope": 1, "ship": 2, "hull": 3},
    "Farmer": {"hay": 2, "sheaf": 2, "basket": 1, "crops": 2, "wheat": 2},
    "AnimalTrainer": {"trough": 4, "hay": 2, "saddle": 3, "horse": 1},
    "Scribe": {"bookcase": 2, "pen and ink": 3, "book": 1, "scroll": 2, "globe": 1, "writing table": 3},
    "Mapmaker": {"map": 3, "globe": 2, "writing table": 1},
    "Provisioner": {"crate": 1, "barrel": 1, "sack": 1, "display case": 1, "shelves": 1, "shelf": 1, "counter": 1},
    "Banker": {"metal chest": 2, "counter": 1, "gold": 2, "strongbox": 3},
    "Healer": {"bandage": 3, "ankh": 4, "bed": 1, "wash basin": 1, "herb": 1},
}
CORE = ("Banker", "Healer", "Blacksmith", "Provisioner")
VENDOR_DELAY = ("00:05:00", "00:10:00")
STOCK_GUARD = "OrderGuard"
PEOPLE = ["EscortableMage", "Noble", "SeekerOfAdventure"]
TOWN_PETS = ["Bird", "Cat", "Dog", "Rat"]
KEEPS = {  # name -> (P669 spots.csv name, garrison) ; P695's counts, Dunbain's from the prompt
    "Fort Whitestone": 4, "Castle Dunbain": 2, "Fort Stormhammer": 4, "Tigerclaw Fortress": 2, "Khalahandra Keep": 6,
}
WILD_KINDS = {"wild encounter", "wildlife"}
WILD_AREAS = {"NujelmContinent": ["Nujelm Desert", "Moonglow Forest"], "Glimmerwood": ["Glimmerwood"]}
DUNGEON_STRIPS = {357, 370, 349, 365, 348, 395}
# P698's B3 tier ("isolated from towns and travel ... after review") and stock's non-creature wild entries (treasure
# chests, camps): no new-land spawner copies a stock spawner holding one
HELD = {"daemon", "dragon", "drake", "wyvern", "whitewyrm", "ancientwyrm", "balron", "lich", "lichlord", "titan",
        "efreet", "cyclops", "skeletaldragon", "kraken", "deepseaserpent", "shadowwyrm", "poisonelemental",
        "bloodelemental", "iceelemental", "snowelemental"}


def held(entry):
    e = entry.lower()
    return e in HELD or "treasurechest" in e or e.endswith("camp")


# Old Haven's undead field, the ML trainers' training ground (P678 ClusterFHavenTownSpawns.RuinFieldGuid): not a wild mix
HAVEN_TRAINING_FIELD = "1af71e9c-8891-43d9-940a-bdbd94560583"
MAX_RANGE = 30   # a new wild spawner's widest range; stock's wider fields are scaled down to it at their density
TERRAIN_HOMES = ("grass", "forest", "jungle", "swamp", "sand", "snow", "rock", "dirt", "lava")


_fit = {}


def fitting(nm):
    """The trade weights one static name carries (cached)."""
    if nm not in _fit:
        c = collections.Counter()
        for trade, words in FITTINGS.items():
            for wd, wt in words.items():
                if wd in nm and not (wd == "bow" and ("elbow" in nm or "bowl" in nm)) and not (wd == "bar" and "barrel" in nm):
                    c[trade] += wt
        _fit[nm] = c
    return _fit[nm]


_stock_grids = {}


def stock_grid(facet):
    if facet not in _stock_grids:
        _stock_grids[facet] = common.sosgrid.load(facet.lower())
    return _stock_grids[facet]


def guid(*parts):
    return str(uuid.uuid5(NS, "/".join(str(p) for p in parts)))


def record(g, name, x, y, z, facet, count, entries, home, walk, delays=VENDOR_DELAY, team=0):
    return {
        "$type": "Spawner", "guid": g, "name": name, "location": [int(x), int(y), int(z)], "map": facet,
        "count": int(count), "minDelay": delays[0], "maxDelay": delays[1], "team": team,
        "homeRange": int(home), "walkingRange": int(walk),
        "entries": [{"name": n, "maxCount": int(c), "probability": 100} for n, c in entries],
    }


# ------------------------------------------------------------------------------------------------ map helpers

class Town:
    """A town's (or keep's) box, its buildings and its walkable reach from a start tile."""

    def __init__(self, name, rects, start, margin=0):
        g = common.grid()
        self.name, self.rects = name, rects
        self.x1 = max(0, min(r[0] for r in rects) - margin)
        self.y1 = max(0, min(r[1] for r in rects) - margin)
        self.x2 = min(W, max(r[2] for r in rects) + margin)
        self.y2 = min(H, max(r[3] for r in rects) + margin)
        sl = (slice(self.x1, self.x2), slice(self.y1, self.y2))
        self.stand = g["stand"][sl].astype(np.int32)
        self.inside = np.zeros(self.stand.shape, dtype=bool)
        for x1, y1, x2, y2 in rects:
            self.inside[max(0, x1 - self.x1):max(0, x2 - self.x1), max(0, y1 - self.y1):max(0, y2 - self.y1)] = True
        self.terrain = g["terrain"][sl]
        self._roofs()
        self.reach = self._reach(start)
        self.buildings = self._buildings()

    def _roofs(self):
        names = common.item_names()
        sx, sy, sz, sid = common.statics_in_box(self.x1, self.y1, self.x2, self.y2)
        lx, ly = sx - self.x1, sy - self.y1
        st = self.stand[lx, ly]
        foliage = np.array([any(w in names[int(i)] for w in FOLIAGE) for i in sid], dtype=bool)
        roof = (st != NONE) & (sz >= st + 10) & ~foliage
        self.roofed = np.zeros(self.stand.shape, dtype=bool)
        self.roofed[lx[roof], ly[roof]] = True
        self.statics = (lx, ly, sz, sid)

    def _reach(self, start):
        """Tiles a player walks to: the walkable component (4-way and diagonal steps of at most 8 Z, as stairs climb)
        holding `start` (the author's Bank point or the region's go point, where recall and the go-menu land), and the
        component with the most tiles on the survey box's edge (the land around, where the roads come in). Both,
        because each alone misses one town: Valunstead's box edge is all water, and Fort Yondall's go point is inside
        a keep its portcullis statics seal from the courtyard (out\\build-log.txt names such towns)."""
        s = self.stand
        w, h = s.shape
        lab = np.zeros(s.shape, dtype=np.int32)
        n = 0
        edge = collections.Counter()
        for x0, y0 in zip(*np.nonzero(s != NONE)):
            if lab[x0, y0]:
                continue
            n += 1
            lab[x0, y0] = n
            stack = [(x0, y0)]
            while stack:
                x, y = stack.pop()
                if x == 0 or y == 0 or x == w - 1 or y == h - 1:
                    edge[n] += 1
                z = s[x, y]
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and not lab[nx, ny] and s[nx, ny] != NONE and abs(int(s[nx, ny]) - int(z)) <= 8:
                        lab[nx, ny] = n
                        stack.append((nx, ny))
        sx, sy = start[0] - self.x1, start[1] - self.y1
        at_start = 0
        for r in range(0, 6):   # the point may sit on a tile no one stands on: the nearest standable within 5
            for dx in range(-r, r + 1):
                for dy in range(-r, r + 1):
                    x, y = sx + dx, sy + dy
                    if not at_start and 0 <= x < w and 0 <= y < h and lab[x, y]:
                        at_start = int(lab[x, y])
        best = max(edge, key=lambda k: edge[k]) if edge else 0
        self.split = bool(at_start and best and at_start != best)
        return ((lab == at_start) & (at_start > 0)) | ((lab == best) & (best > 0))

    def _buildings(self):
        names = common.item_names()
        m = self.roofed & (self.stand != NONE) & self.inside
        lab = np.zeros(m.shape, dtype=np.int32)
        out = []
        n = 0
        for x0, y0 in zip(*np.nonzero(m)):
            if lab[x0, y0]:
                continue
            n += 1
            tiles, stack = [], [(x0, y0)]
            lab[x0, y0] = n
            while stack:
                x, y = stack.pop()
                tiles.append((x, y))
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < m.shape[0] and 0 <= ny < m.shape[1] and m[nx, ny] and not lab[nx, ny]:
                        lab[nx, ny] = n
                        stack.append((nx, ny))
            if len(tiles) >= 9:
                out.append({"id": n, "tiles": tiles})
        lx, ly, sz, sid = self.statics
        at = collections.defaultdict(list)
        for x, y, i in zip(lx.tolist(), ly.tolist(), sid.tolist()):
            at[(x, y)].append(names[i])
        for b in out:
            ts = set(b["tiles"])
            # depth: Chebyshev rings to the building's edge
            depth = {}
            ring = [t for t in ts if any((t[0] + dx, t[1] + dy) not in ts for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
            d, frontier, left = 1, ring, set(ts)
            while frontier:
                for t in frontier:
                    depth[t] = d
                    left.discard(t)
                d += 1
                frontier = [t for t in left if any((t[0] + dx, t[1] + dy) in depth for dx in (-1, 0, 1) for dy in (-1, 0, 1))]
            b["depth"] = depth
            b["reach"] = [t for t in b["tiles"] if self.reach[t]]
            b["fit"] = collections.Counter()
            b["names"] = collections.Counter()
            # fittings: statics on the building's tiles or one tile out (counters and forges stand at walls)
            near = ts | {(x + dx, y + dy) for x, y in ts for dx in (-1, 0, 1) for dy in (-1, 0, 1)}
            for t in near:
                for nm in at.get(t, ()):
                    b["names"][nm] += 1
                    b["fit"].update(fitting(nm))
            b["cx"] = sum(t[0] for t in b["tiles"]) / len(b["tiles"]) + self.x1
            b["cy"] = sum(t[1] for t in b["tiles"]) / len(b["tiles"]) + self.y1
        # only buildings a player can walk into
        return [b for b in out if b["reach"]]

    def spot_in(self, b, taken, apart=3):
        """The building's deepest reachable tile not within `apart` of a taken spot; (x, y, z, depth) world."""
        cands = sorted(b["reach"], key=lambda t: (-b["depth"].get(t, 1),
                                                  abs(t[0] + self.x1 - b["cx"]) + abs(t[1] + self.y1 - b["cy"])))
        for t in cands:
            wx, wy = t[0] + self.x1, t[1] + self.y1
            if all(max(abs(wx - a), abs(wy - c)) >= apart for a, c in taken):
                return wx, wy, int(self.stand[t]), b["depth"].get(t, 1)
        return None

    def outdoor(self):
        """Reachable, unroofed tiles inside the region (world x, y)."""
        m = self.reach & ~self.roofed & self.inside
        xs, ys = np.nonzero(m)
        return [(int(x) + self.x1, int(y) + self.y1) for x, y in zip(xs, ys)]

    def z(self, x, y):
        return int(self.stand[x - self.x1, y - self.y1])

    def dry_tiles(self):
        return int(((self.stand != NONE) & self.inside).sum())


def farthest(points, k, seeds=(), rng=None):
    """k points spread out: each the candidate farthest from those already chosen (and from the seeds)."""
    if not points or k <= 0:
        return []
    pts = np.array(points, dtype=np.int32)
    chosen = []
    d = np.full(len(pts), 10 ** 9, dtype=np.int64)
    for s in seeds:
        d = np.minimum(d, np.maximum(np.abs(pts[:, 0] - s[0]), np.abs(pts[:, 1] - s[1])))
    if not seeds:
        i = (rng or random).randrange(len(pts))
        chosen.append(tuple(pts[i]))
        d = np.minimum(d, np.maximum(np.abs(pts[:, 0] - pts[i, 0]), np.abs(pts[:, 1] - pts[i, 1])))
    while len(chosen) < k:
        i = int(np.argmax(d))
        if d[i] <= 0:
            break
        chosen.append(tuple(pts[i]))
        d = np.minimum(d, np.maximum(np.abs(pts[:, 0] - pts[i, 0]), np.abs(pts[:, 1] - pts[i, 1])))
    return [(int(a), int(b)) for a, b in chosen]


# ------------------------------------------------------------------------------------------------ stock figures

def stock_files(facet):
    """Every stock spawner the shard imports on the facet (post-uoml/** and shared/**), by guid."""
    out = {}
    for root in ("post-uoml", "shared"):
        base = os.path.join(common.PINNED, "Spawns", root)
        for dp, _, fs in os.walk(base):
            for f in fs:
                if f.endswith(".json"):
                    for s in json.load(open(os.path.join(dp, f))):
                        if s.get("map") == facet:
                            s["_file"] = os.path.relpath(os.path.join(dp, f), os.path.join(common.PINNED, "Spawns")).replace("\\", "/")
                            out[s["guid"]] = s
    return out


def ledger():
    rows = list(csv.DictReader(open(LEDGER)))
    return rows


def stock_town_regions(facet):
    """Pinned regions.json's named TownRegions on the facet (the stock towns), as exclusive rectangles."""
    out = {}
    for r in json.load(open(os.path.join(common.PINNED, "regions.json"))):
        if r.get("$type") == "TownRegion" and r.get("Map") == facet and r.get("Name"):
            rects = []
            for a in r.get("Area", []):
                if "x1" in a:
                    rects.append((a["x1"], a["y1"], a["x2"], a["y2"]))
                elif "x" in a:
                    rects.append((a["x"], a["y"], a["x"] + a["width"], a["y"] + a["height"]))
            out.setdefault(r["Name"], []).extend(rects)
    return out


def town_density_stock(facet, rows):
    """Stock spawned people and town animals per 100 dry tiles in each stock town of the facet (stock map)."""
    g = stock_grid(facet)
    stand = g["stand"]
    towns = stock_town_regions(facet)
    kinds = {"town service", "town animals", "town NPC or prop"}
    out = {}
    for name, rects in towns.items():
        if any(w in name.lower() for w in ("field", "farm", "orchard", "graveyard", "cemetery")) or len(name) < 3:
            continue
        m = common.rect_mask(rects)
        dry = int(((stand != NONE) & m).sum())
        if dry < 1500:
            continue
        n = 0
        for r in rows:
            if r["facet"] == facet and r["kind"] in kinds and common.in_rects(int(r["x"]), int(r["y"]), rects):
                n += int(r.get("_count") or 1)
        if n:
            out[name] = (n, dry, 100.0 * n / dry)
    return out


# ------------------------------------------------------------------------------------------------ towns

def load_rosters():
    d = json.load(open(ROSTERS, encoding="utf-8"))
    return {s["name"]: s for s in d["settlements"]}


def author_points():
    out = collections.defaultdict(dict)
    for r in csv.DictReader(open(SPOTS, encoding="utf-8")):
        parts = [p.strip() for p in r["group"].split("/")]
        out[parts[-1]][r["name"]] = (int(r["x"]), int(r["y"]), int(r["z"]))
    return out


def build_town(name, roster, regs, recs, points, facet, rng, density_target, log):
    rects = regs[name]
    rec = next(r for r in recs if r.get("Name") == name)
    go = rec["GoLocation"]
    bankpt = points.get(name, {}).get("Bank")
    start = bankpt[:2] if bankpt else (go["x"], go["y"])
    t = Town(name, rects, start, margin=20)
    if t.split:
        log.append(f"{facet} {name}: the land around and the {'Bank' if bankpt else 'go'} point are not joined on foot")
    roles = []  # (trade type, count, core)
    roles.append(("Banker", roster["bank"]["count"] if roster["bank"]["available"] else 1))
    roles.append(("Healer", roster["healer"]["count"] if roster["healer"]["available"] else 1))
    for v in roster["vendors"]:
        roles.append((v["type"].split(".")[-1], v["count"]))
    for c in CORE:
        if not any(r[0] == c for r in roles):
            roles.append((c, 1))
    free = list(t.buildings)
    taken, out, placed = [], [], []

    def take(b):
        if b in free:
            free.remove(b)

    def place(trade, count, b, why):
        sp = t.spot_in(b, taken)
        if sp is None:
            return False
        x, y, z, depth = sp
        taken.append((x, y))
        walk = 2 if depth >= 3 else (1 if depth == 2 else 0)
        g = guid(facet, name, "vendor", trade)
        out.append(record(g, f"{name} {trade}", x, y, z, facet, count, [(trade, count)], 0, walk))
        placed.append(dict(town=name, facet=facet, role=trade, count=count, x=x, y=y, z=z, building=b["id"],
                           tiles=len(b["tiles"]), why=why, fit=b["fit"].get(trade, 0), indoor=True))
        return True

    order = sorted(roles, key=lambda r: (r[0] != "Banker", r[0] not in CORE, -max((b["fit"].get(r[0], 0) for b in t.buildings), default=0)))
    for trade, count in order:
        b, why = None, None
        if trade == "Banker" and bankpt:
            bx, by = bankpt[0], bankpt[1]
            near = sorted(t.buildings, key=lambda b: min(max(abs(x + t.x1 - bx), abs(y + t.y1 - by)) for x, y in b["tiles"]))
            if near and min(max(abs(x + t.x1 - bx), abs(y + t.y1 - by)) for x, y in near[0]["tiles"]) <= 6:
                b, why = near[0], "the author's Bank point"
        if b is None:
            scored = sorted((bb for bb in free if bb["fit"].get(trade, 0) > 0), key=lambda bb: (-bb["fit"][trade], -len(bb["tiles"])))
            if scored:
                b, why = scored[0], "fittings: " + ", ".join(f"{k}" for k, v in scored[0]["names"].most_common() if any(w in k for w in FITTINGS[trade]))[:120] if trade in FITTINGS else "fittings"
        if b is None and free:
            b, why = max(free, key=lambda bb: len(bb["tiles"])), "no fitting in town: the largest free building"
        if b is None:
            # every building has a trade: share the largest building that still has room
            for bb in sorted(t.buildings, key=lambda bb: -len(bb["tiles"])):
                if t.spot_in(bb, taken) is not None:
                    b, why = bb, "shares a building (no free building left)"
                    break
        if b is None or not place(trade, count, b, why):
            log.append(f"{facet} {name}: no room for {trade}")
            continue
        take(b)
    # guards: stock OrderGuard posts, the first by the bank, the rest spread over the town's reachable streets
    outdoor = t.outdoor()
    gcount = roster["guards"]["count"] or 0
    bank = next((p for p in placed if p["role"] == "Banker"), None)
    seeds = []
    posts = []
    if gcount and outdoor:
        if bank:
            first = min(outdoor, key=lambda p: max(abs(p[0] - bank["x"]), abs(p[1] - bank["y"])))
            posts.append(first)
            seeds = [first]
        posts += farthest(outdoor, gcount - len(posts), seeds=seeds or (), rng=rng)
    for i, (x, y) in enumerate(posts[:gcount]):
        out.append(record(guid(facet, name, "guard", i), f"{name} guard post {i + 1}", x, y, t.z(x, y), facet, 1,
                          [(STOCK_GUARD, 1)], 0, 1))
        placed.append(dict(town=name, facet=facet, role=STOCK_GUARD, count=1, x=x, y=y, z=t.z(x, y), building="", tiles="",
                           why="guard post", fit="", indoor=False))
    # townsfolk: crier by the bank, walkers, town animals
    people = []
    if outdoor:
        crier = min(outdoor, key=lambda p: max(abs(p[0] - bank["x"]), abs(p[1] - bank["y"])) if bank else 0)
        crier = next((p for p in sorted(outdoor, key=lambda p: max(abs(p[0] - crier[0]), abs(p[1] - crier[1]))) if p not in posts), crier)
        out.append(record(guid(facet, name, "crier"), f"{name} town crier", crier[0], crier[1], t.z(*crier), facet, 1,
                          [("TownCrier", 1)], 1, 5))
        people.append(("TownCrier", 1, crier))
        dry = t.dry_tiles()
        walkers = max(1, round(dry / 15000))
        for i, (x, y) in enumerate(farthest(outdoor, walkers, seeds=[crier] + posts, rng=rng)):
            out.append(record(guid(facet, name, "people", i), f"{name} townspeople {i + 1}", x, y, t.z(x, y), facet, 3,
                              [(n, 3) for n in PEOPLE], 10, 20))
            people.append(("people", 3, (x, y)))
        so_far = sum(p["count"] for p in placed) + sum(c for _, c, _ in people)
        want = math.ceil(density_target * dry / 100.0)
        pets = max(0, want - so_far)
        if pets:
            n = max(1, math.ceil(pets / 24))
            per = math.ceil(pets / n)
            rng_ = min(50, max(10, (min(t.x2 - t.x1, t.y2 - t.y1) // 4)))
            for i, (x, y) in enumerate(farthest(outdoor, n, seeds=[crier] + posts, rng=rng)):
                out.append(record(guid(facet, name, "pets", i), f"{name} town animals {i + 1}", x, y, t.z(x, y), facet, per,
                                  [(n_, per) for n_ in TOWN_PETS], rng_, rng_))
                people.append(("pets", per, (x, y)))
    for kind, c, (x, y) in people:
        placed.append(dict(town=name, facet=facet, role=kind, count=c, x=x, y=y, z=t.z(x, y), building="", tiles="",
                           why="townsfolk", fit="", indoor=False))
    survey = [dict(town=name, building=b["id"], tiles=len(b["tiles"]), reachable=len(b["reach"]),
                   cx=round(b["cx"]), cy=round(b["cy"]), fit=dict(b["fit"].most_common(4))) for b in t.buildings]
    return out, placed, survey, t


def build_keep(name, garrison, point, facet, rng, log):
    x0, y0, _ = point
    t = Town(name, [(x0 - 40, y0 - 40, x0 + 41, y0 + 41)], (x0, y0))
    if t.split:
        log.append(f"{facet} {name}: the land around and the author's point are not joined on foot")
    out, placed = [], []
    outdoor = t.outdoor()
    n_out = (garrison + 1) // 2
    gate = sorted(outdoor, key=lambda p: max(abs(p[0] - x0), abs(p[1] - y0)))
    posts = []
    for p in gate:
        if len(posts) >= n_out:
            break
        if all(max(abs(p[0] - q[0]), abs(p[1] - q[1])) >= 3 for q in posts):
            posts.append(p)
    inside = []
    blds = sorted([b for b in t.buildings if b["reach"]], key=lambda b: -len(b["tiles"]))
    if blds and name != "Castle Dunbain":   # Dunbain: P695 keeps its rooms for the Open Ledger's encounter (P672-06)
        taken = []
        for i in range(garrison - len(posts)):
            sp = t.spot_in(blds[0], taken)
            if sp is None:
                break
            taken.append(sp[:2])
            inside.append(sp[:2])
    if len(posts) + len(inside) < garrison:   # no building to hold them: the rest outdoors too
        for p in gate:
            if len(posts) + len(inside) >= garrison:
                break
            if p not in posts and all(max(abs(p[0] - q[0]), abs(p[1] - q[1])) >= 3 for q in posts):
                posts.append(p)
    for i, (x, y) in enumerate(posts + inside):
        out.append(record(guid(facet, name, "garrison", i), f"{name} garrison {i + 1}", x, y, t.z(x, y), facet, 1,
                          [(STOCK_GUARD, 1)], 0, 1))
        placed.append(dict(town=name, facet=facet, role=STOCK_GUARD, count=1, x=x, y=y, z=t.z(x, y), building="",
                           tiles="", why="garrison (inside)" if (x, y) in inside else "garrison (gate)", fit="",
                           indoor=(x, y) in inside))
    if len(out) < garrison:
        log.append(f"{facet} {name}: garrison {len(out)} of {garrison}")
    return out, placed


# ------------------------------------------------------------------------------------------------ wild

def kind_of(rows, facet):
    return {r["guid"]: r for r in rows if r["facet"] == facet}


def stock_table(facet, stock, rows):
    """terrain class -> (templates, creatures per 100 dry outdoor tiles), from stock on the stock map."""
    g = stock_grid(facet)
    stand, cov, ter = g["stand"], g["covered"], g["terrain_" + facet.lower()]
    towns = common.rect_mask([r for rs in stock_town_regions(facet).values() for r in rs])
    surface = np.zeros((W, H), dtype=bool)
    surface[:5120, :] = True
    dry = (stand != NONE) & ~cov & ~towns & surface
    classes = common.sosgrid.CLASS_NAMES
    lk = kind_of(rows, facet)
    tmpl = collections.defaultdict(list)
    creatures = collections.Counter()
    for gid, s in stock.items():
        r = lk.get(gid)
        if not r or r["kind"] not in WILD_KINDS:
            continue
        x, y, _ = s["location"]
        if x >= 5120 or not (0 <= x < W and 0 <= y < H) or towns[x, y]:
            continue
        c = classes[int(ter[x, y])]
        creatures[c] += int(s["count"])
        if s.get("spawnBounds") or s.get("region") or gid == HAVEN_TRAINING_FIELD or any(held(e["name"]) for e in s["entries"]):
            continue
        tmpl[c].append(s)
    out = {}
    for c in TERRAIN_HOMES:
        k = classes.index(c)
        n = int((dry & (ter == k)).sum())
        out[c] = (tmpl.get(c, []), 100.0 * creatures[c] / n if n else 0.0, n, creatures[c])
    return out


def retained_cover(facet, stock, rows):
    """Tiles already within range of a stock wild spawner S9 kept or moved (its SoS home)."""
    cover = np.zeros((W, H), dtype=bool)
    for r in rows:
        if r["facet"] != facet or r["kind"] not in WILD_KINDS | {"graveyard", "town-edge encounter"} or r["action"] not in ("keep", "move"):
            continue
        x, y = (int(r["nx"]), int(r["ny"])) if r["action"] == "move" and r["nx"] else (int(r["x"]), int(r["y"]))
        rr = max(int(r["home_range"] or 0), 5)
        cover[max(0, x - rr):min(W, x + rr + 1), max(0, y - rr):min(H, y + rr + 1)] = True
    return cover


def wild_mask():
    """Where S10's wild spawns may stand on SoS (both facets read the same file): the new land, less what is not wild."""
    g = common.grid()
    regs = common.regions()
    recs = common.region_records()
    stand, cov, wet = g["stand"], g["covered"], g["wet"]
    areas = {k: common.rect_mask([r for n in v for r in regs[n]]) for k, v in WILD_AREAS.items()}
    stock_t = stock_grid("Trammel")["stand"]
    newly = (stand != NONE) & (stock_t == NONE)
    isl = np.zeros((W, H), dtype=np.int32)
    for r in csv.DictReader(open(ISLANDS)):
        if r["verdict"] != "new" or int(r["id"]) in DUNGEON_STRIPS:
            continue
        x1, y1, x2, y2 = int(r["x1"]), int(r["y1"]), int(r["x2"]) + 1, int(r["y2"]) + 1
        sub = newly[x1:x2, y1:y2]
        isl[x1:x2, y1:y2] = np.where(sub & (isl[x1:x2, y1:y2] == 0), int(r["id"]), isl[x1:x2, y1:y2])
    bad = np.zeros((W, H), dtype=bool)
    for r in recs:
        rects = [(a["x1"], a["y1"], a["x2"], a["y2"]) for a in r.get("Area", [])]
        if r["$type"] in ("TownRegion", "GuardedRegion"):
            bad |= common.rect_mask([(a - 10, b - 10, c + 10, d + 10) for a, b, c, d in rects])
        elif r["$type"] == "DungeonRegion" or "Dungeon" in r["$type"]:
            bad |= common.rect_mask(rects)
    for x1, y1, x2, y2 in common.CLOSURES.values():
        bad[x1:x2 + 1, y1:y2 + 1] = True
    for r in csv.DictReader(open(SPOTS, encoding="utf-8")):
        if "/ Dungeons /" in r["group"]:
            x, y = int(r["x"]), int(r["y"])
            bad[max(0, x - 12):x + 13, max(0, y - 12):y + 13] = True
    bad[5120:, :] = True
    ok = (stand != NONE) & ~cov & ~wet & ~bad
    # the named areas take only what is new: land that was sea or void in stock, or whose terrain changed class
    # (the author's Moonglow Forest region also holds stock Moonglow's own woods, which keep stock's spawns)
    changed = g["terrain"] != g["terrain_trammel"]
    for k in areas:
        areas[k] &= newly | changed
    return areas, isl, ok


def place_wild(facet, table, cover, areas, isl, ok, rng, log):
    g = common.grid()
    ter, stand = g["terrain"], g["stand"]
    classes = common.sosgrid.CLASS_NAMES
    files = collections.defaultdict(list)
    ledger_rows = []
    groups = []   # (file, area label, mask)
    for k, m in areas.items():
        groups.append((k, k, m & ok & ~cover))
    ids = sorted(set(np.unique(isl)) - {0})
    for i in ids:
        groups.append(("Islands", f"island {i}", (isl == i) & ok & ~cover & ~areas["NujelmContinent"] & ~areas["Glimmerwood"]))
    density = []
    for fname, label, m in groups:
        for c in TERRAIN_HOMES:
            temps, rate, _, _ = table[c]
            cm = m & (ter == classes.index(c))
            n = int(cm.sum())
            if n == 0:
                continue
            want = rate * n / 100.0
            placed = 0
            if temps and want >= 1:
                xs, ys = np.nonzero(cm)
                order = list(range(len(xs)))
                rng.shuffle(order)
                homes = []
                for j in order:
                    if placed >= want - 0.5:
                        break
                    x, y = int(xs[j]), int(ys[j])
                    s = temps[rng.randrange(len(temps))]
                    hr, cnt = int(s.get("homeRange", 10)), int(s["count"])
                    if hr > MAX_RANGE:
                        # stock's wide wildlife fields (40 deer over 100 tiles): the same density over 30
                        cnt, hr = max(2, round(cnt * (MAX_RANGE / hr) ** 2)), MAX_RANGE
                    cnt = max(1, min(cnt, 30, round(want - placed)))   # the last one makes up the target
                    sep = max(8, hr)
                    if any(abs(x - a) < sep and abs(y - b) < sep for a, b in homes):
                        continue
                    # land over a quarter of its range (P681's walk test); shrink the range until it holds
                    while hr > 3 and ok[max(0, x - hr):x + hr + 1, max(0, y - hr):y + hr + 1].mean() < 0.25:
                        hr -= 2
                    if ok[max(0, x - hr):x + hr + 1, max(0, y - hr):y + hr + 1].mean() < 0.25:
                        continue   # too little land even at the smallest range: another tile
                    homes.append((x, y))
                    walk = int(s.get("walkingRange", -1))
                    rec = record(guid(facet, "wild", label, c, x, y), f"{label} {c} {len(homes)}", x, y, int(stand[x, y]),
                                 facet, cnt, [], hr, min(walk, hr) if walk >= 0 else hr,
                                 (s["minDelay"], s["maxDelay"]), int(s.get("team", 0)))
                    rec["entries"] = [{"name": e["name"], "maxCount": min(int(e["maxCount"]), cnt),
                                       "probability": e["probability"]} for e in s["entries"]]
                    files[fname].append(rec)
                    placed += cnt
                    ledger_rows.append(dict(facet=facet, file=fname, area=label, terrain=c, x=x, y=y, z=int(stand[x, y]),
                                            count=cnt, home_range=hr, template=s["guid"], template_file=s["_file"],
                                            entries="|".join(e["name"] for e in s["entries"])))
            density.append(dict(facet=facet, file=fname, area=label, terrain=c, dry=n, stock_rate=round(rate, 3),
                                target=round(want, 1), placed=placed))
    return files, ledger_rows, density


# ------------------------------------------------------------------------------------------------ main

def main():
    os.makedirs(common.OUT, exist_ok=True)
    regs = common.regions()
    recs = common.region_records()
    rosters = load_rosters()
    points = author_points()
    rows = ledger()
    log = []
    all_placed, survey_rows, files = [], [], collections.defaultdict(list)
    dens_rows = []
    for facet in FACETS:
        rng = random.Random(f"P682-{facet}")
        stock = stock_files(facet)
        for r in rows:
            s = stock.get(r["guid"])
            r.setdefault("_count", 0)
            if s and r["facet"] == facet:
                r["_count"] = int(s["count"])
        towns_stock = town_density_stock(facet, rows)
        med = sorted(v[2] for v in towns_stock.values())[len(towns_stock) // 2]
        for name, (n, dry, d) in sorted(towns_stock.items()):
            dens_rows.append(dict(facet=facet, kind="stock town", name=name, spawned=n, dry=dry, per100=round(d, 3)))
        for name in common.TOWNS:
            out, placed, survey, t = build_town(name, rosters[name], regs, recs, points, facet, rng, med, log)
            files["towns/" + name.replace(" ", "") + ".json"] += out
            all_placed += placed
            if facet == "Trammel":
                survey_rows += survey
            n = sum(p["count"] for p in placed)
            dens_rows.append(dict(facet=facet, kind="new town", name=name, spawned=n, dry=t.dry_tiles(),
                                  per100=round(100.0 * n / t.dry_tiles(), 3)))
        for name, garrison in KEEPS.items():
            pt = points.get(name, {}).get(name) or next(iter(points.get(name, {}).values()), None)
            if name == "Khalahandra Keep":
                pt = points["Khalahandra Keep"]["Entrance"]
            if pt is None:
                pt = next(v for k, v in ((k, v) for d in points.values() for k, v in d.items()) if k == name)
            out, placed = build_keep(name, garrison, pt, facet, rng, log)
            files["keeps/" + name.replace(" ", "") + ".json"] += out
            all_placed += placed
        # wild
        table = stock_table(facet, stock, rows)
        for c, (temps, rate, n, cr) in table.items():
            dens_rows.append(dict(facet=facet, kind="stock wild", name=c, spawned=cr, dry=n, per100=round(rate, 3),
                                  templates=len(temps)))
        areas, isl, ok = wild_mask()
        cover = retained_cover(facet, stock, rows)
        wf, wl, wd = place_wild(facet, table, cover, areas, isl, ok, rng, log)
        for k, v in wf.items():
            files["wild/" + k + ".json"] += v
        with open(os.path.join(common.OUT, f"wild-ledger-{facet.lower()}.csv"), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(wl[0].keys()))
            w.writeheader()
            w.writerows(wl)
        with open(os.path.join(common.OUT, f"wild-density-{facet.lower()}.csv"), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(wd[0].keys()))
            w.writeheader()
            w.writerows(wd)
        del areas, isl, ok, cover
    # write the spawn files (sorted for a stable diff)
    for rel, recs_ in files.items():
        recs_.sort(key=lambda r: (r["map"] != "Trammel", r["name"]))
        common.write_json(os.path.join(SPAWNS_OUT, rel), recs_)
    with open(os.path.join(common.OUT, "towns-placed.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(all_placed[0].keys()))
        w.writeheader()
        w.writerows(all_placed)
    with open(os.path.join(common.OUT, "town-buildings.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(survey_rows[0].keys()))
        w.writeheader()
        w.writerows(survey_rows)
    keys = sorted({k for r in dens_rows for k in r})
    with open(os.path.join(common.OUT, "density.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(dens_rows)
    with open(os.path.join(common.OUT, "build-log.txt"), "w") as f:
        f.write("\n".join(log) + "\n")
    print("\n".join(log))
    for rel, recs_ in sorted(files.items()):
        print(rel, len(recs_), "spawners", sum(r["count"] for r in recs_), "creatures")


if __name__ == "__main__":
    main()
