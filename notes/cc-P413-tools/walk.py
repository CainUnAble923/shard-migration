"""cc-P413: on a PRIVATE test shard reading the new map (proof-shard.ps1, 127.0.0.1:2596), with the playtest bot's client:
seed the way in, walk from New Haven's east edge to the burrow on foot, then step down from every mouth tile and climb
the rope ladder back up each time. The server decides every step (a 0x22 accept or a 0x21 refusal), so this is the walk
on the shard, not on our reading of the files.

    python -P walk.py --bot <work copy>\\tools\\playtest-bot --map <build_anthill work>\\edited --client <pristine>
        --out <folder> [--port 2596]

Paths come from the same flood fill as build_anthill.py (cc-P188's Walk over the edited files); a path back to a mouth
tile never crosses another mouth tile, so each tile is the one that takes the player down.
"""
import argparse, collections, json, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.dirname(HERE)
ap = argparse.ArgumentParser()
ap.add_argument('--bot', required=True)
ap.add_argument('--map', required=True)
ap.add_argument('--client', required=True)
ap.add_argument('--out', required=True)
ap.add_argument('--port', type=int, default=2596)
a = ap.parse_args()

sys.path.insert(0, os.path.join(os.path.dirname(NOTES), 'scripts'))
from mapbuild import uofiles  # noqa: E402
uofiles.CLIENT = a.client
sys.path.insert(0, os.path.join(NOTES, 'cc-P188-tools'))
import build_way_in as bwi  # noqa: E402
bwi.CLIENT = a.client
sys.path.insert(0, a.bot)
from uobot.client import Client, Cliloc, Transcript  # noqa: E402
from uobot import checks, golemcheck  # noqa: E402

MOUTH = [(x, y) for y in range(2617, 2621) for x in range(3617, 3620)]
ARRIVAL = (5193, 1138)
LADDER_FOOT = (5193, 1132)
BESIDE_MOUND = (3619, 2623)
NEW_HAVEN_EDGE = bwi.NEW_HAVEN_EDGE
DIR = {(0, -1): 0, (1, -1): 1, (1, 0): 2, (1, 1): 3, (0, 1): 4, (-1, 1): 5, (-1, 0): 6, (-1, -1): 7}

W = bwi.Walk(a.map, bwi.OVERVIEW_RECT)


def path(start, goal, avoid=()):
    """Orthogonal steps over the flood fill's open tiles, never through a tile in avoid (but the goal)."""
    q, prev = collections.deque([start]), {start: None}
    while q:
        c = q.popleft()
        if c == goal:
            break
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (c[0] + dx, c[1] + dy)
            if n in prev or W.stand.get(n) is None or W.stand[n] - W.stand[c] > bwi.STEP or (n in avoid and n != goal):
                continue
            prev[n] = c
            q.append(n)
    if goal not in prev:
        return None
    out, c = [], goal
    while c is not None:
        out.append(c)
        c = prev[c]
    return out[::-1]


def main():
    os.makedirs(a.out, exist_ok=True)
    tr = Transcript(os.path.join(a.out, 'transcript.txt'))
    cl = Cliloc(golemcheck.CLILOC if os.path.exists(golemcheck.CLILOC) else None)

    def enter(role):
        user, pw = golemcheck.account('Iron', role)
        c = Client(user, pw, tr, cl, label='iron-' + role, test_target=('127.0.0.1', a.port))
        chars = c.login()
        c.play(chars.index(golemcheck.character_name('Iron', role)))
        return c

    def follow(c, steps):
        """Walk a path tile by tile (a turn first when the direction changes). Returns (reached, where it stopped)."""
        for nxt in steps[1:]:
            here = c.pos[:2]
            d = DIR[(nxt[0] - here[0], nxt[1] - here[1])]
            for _ in range(3):
                if c.walk(d, 1, pause=0.12) != 1:
                    return False, c.pos[:3]
                if c.pos[:2] == nxt:
                    break
            if c.pos[:2] != nxt:
                return False, c.pos[:3]
        return True, c.pos[:3]

    def arrived_at(c, where, timeout=5):
        return c.wait(lambda: c.pos and c.pos[:2] == where, timeout)

    res = {}
    admin = enter('admin')
    player = enter('player')
    try:
        dry = admin.command('[ClusterFSeedRootdeep dryrun', settle=2.0)
        real = admin.command('[ClusterFSeedRootdeep', settle=3.0)
        res['seed dry run'] = [m['text'] for m in dry if 'Rootdeep' in (m['text'] or '')]
        res['seed'] = [m['text'] for m in real if 'Rootdeep' in (m['text'] or '')]

        start = NEW_HAVEN_EDGE if W.stand[NEW_HAVEN_EDGE] is not None else W.nearest_open(NEW_HAVEN_EDGE)
        checks.staff_target(admin, '[set Map Trammel', player)
        checks.staff_target(admin, '[set Location (%d,%d,%d)' % (start[0], start[1], W.stand[start]), player)
        player.wait(lambda: player.pos and player.pos[:2] == start, 8)
        res['start'] = player.pos
        first = min((path(start, t, set(MOUTH)) for t in MOUTH), key=lambda p: len(p) if p else 10 ** 9)
        ok, at = follow(player, first[:-1])
        res['walk to the mound'] = {'planned steps': len(first) - 1, 'reached the last tile before the mouth': ok, 'at': at}
        ok, at = follow(player, first[-2:])   # the step onto the mouth: the teleporter takes it
        res['walk to the mound']['down from'] = first[-1]
        res['walk to the mound']['landed'] = arrived_at(player, ARRIVAL) and player.pos[:3]

        tiles = []
        for t in MOUTH:
            row = {'tile': t}
            if not (player.pos and player.pos[:2] == ARRIVAL):
                row['problem'] = 'not on the arrival before climbing: %s' % (player.pos,)
                tiles.append(row)
                break
            up = [(5193, y) for y in range(ARRIVAL[1], LADDER_FOOT[1] - 1, -1)]
            follow(player, up[:-1])
            follow(player, up[-2:])
            row['ladder landed'] = bool(arrived_at(player, BESIDE_MOUND)) and player.pos[:3]
            p = path(BESIDE_MOUND, t, set(MOUTH))
            row['steps from the landing'] = len(p) - 1 if p else None
            if p:
                ok, at = follow(player, p[:-1])
                follow(player, p[-2:])
            else:
                # An inner tile: every neighbour is a mouth tile, so no walk reaches it without going down first. Stand
                # the player on the neighbour to the west by staff command (a move by [set fires no teleporter), then
                # step east onto the tile.
                n = (t[0] - 1, t[1])
                checks.staff_target(admin, '[set Location (%d,%d,%d)' % (n[0], n[1], W.stand[n]), player)
                row['placed on'] = n if player.wait(lambda: player.pos and player.pos[:2] == n, 8) else player.pos
                follow(player, [n, t])
            row['down'] = bool(arrived_at(player, ARRIVAL))
            row['at'] = player.pos[:3]
            tiles.append(row)
            print(row, flush=True)
        res['every mouth tile'] = tiles
        res['all down'] = len(tiles) == len(MOUTH) and all(r.get('down') for r in tiles)
        res['every ladder landing beside the mound'] = all(r.get('ladder landed') for r in tiles)
        res['first path'] = first
    finally:
        for c in (admin, player):
            try:
                c.close()
            except Exception:
                pass
    with open(os.path.join(a.out, 'walk-result.json'), 'w') as f:
        json.dump(res, f, indent=1, default=str)
    print(json.dumps({k: v for k, v in res.items() if k not in ('first path', 'every mouth tile')}, indent=1, default=str))


main()
