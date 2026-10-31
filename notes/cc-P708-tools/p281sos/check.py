# cc-P281: checks every hall in design/guild-halls/halls.json against the client files and pinned's world data, by the
# rules in the notes (read only). Exit 1 on any failure. Writes check.out.txt (the notes table).
#   python -P check.py [key ...]
#
# Per hall:
#   npc     the tile fits a person at its z; no door, door swing or pinned spawner within 2 tiles; no pinned decoration
#           item on it; and blocking it leaves every tile reachable that was reachable before (it cuts no walk).
#   travel  standable, not under a roof, reaches the edge of the 8-tile box around the hall (so the town), and reaches a
#           tile beside the npc.
#   sign    not on a door tile (a swing tile is where OSI hangs its own signs).
#   decor   every piece's tile is standable at its z, 2 or more tiles from doors and spawners, off decoration items;
#           with every piece counted as a blocker, the npc is still reachable and no other tile is cut off.
#   new     the multi's footprint (its components, the steps included) is clear of statics (low ground cover allowed), decoration and spawners,
#           its land within 3 of the building's z, and its front steps and doors open onto standable ground.
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hallbase as H  # noqa: E402
import multidump  # noqa: E402
from walk import Walk  # noqa: E402

CODE = 'D:/UO/golems/Iron/ShatteredLegacy'
PLAN = os.environ.get('HALLS_JSON', CODE + '/design/guild-halls/halls.json')
TEMPLATES = CODE + '/server/customizations/GuildHallDecor/GuildHallDecorTemplates.cs'
GUILD_HOUSE_DOORS = [(-1, 6, 7), (0, 6, 7), (-3, -1, 7), (3, -1, 7)]  # pinned Houses.cs GuildHouse
SWING = {'WestCW': (-1, 1), 'EastCCW': (1, 1), 'WestCCW': (-1, 0), 'EastCW': (1, -1), 'SouthCW': (1, 1),
         'NorthCCW': (1, -1), 'SouthCCW': (0, 0), 'NorthCW': (0, -1)}


def cheb(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def templates():
    """{(set, group): [(dx, dy, dz, id, name)]} from the generated C# table."""
    src = open(TEMPLATES).read()
    out, cur_set, cur_group = {}, None, None
    for line in src.split('\n'):
        m = re.match(r'\s*new\("([a-z-]+)", "[^"]*", "Decor\w+",', line)
        if m:
            cur_set = m.group(1)
            continue
        m = re.match(r'\s*new\("([a-z0-9-]+)", "', line)
        if m and cur_set:
            cur_group = m.group(1)
            out[(cur_set, cur_group)] = []
            continue
        m = re.match(r'\s*new\(0x([0-9A-F]+), "([^"]*)", (-?\d+), (-?\d+), (-?\d+), (\d+), "', line)
        if m and cur_group:
            out[(cur_set, cur_group)].append((int(m.group(3)), int(m.group(4)), int(m.group(5)), int(m.group(1), 16), m.group(2)))
    return out


def door_zone(W):
    """Door tiles and the tiles their leaves swing onto."""
    z = set(W.door_tiles())
    for (x, y), (dz, f) in W.gen_doors.items():
        sx, sy = SWING[f]
        z.add((x + sx, y + sy))
    return z


def standable(W, x, y, z, tol=1):
    return any(abs(h - z) <= tol for h in W.heights(x, y))


def reach_xy(W, start):
    return {(x, y) for (x, y, z) in W.flood(start)}


def check(h, T):
    fails, notes = [], []
    fi, rect = h['facet'], h['rect']
    W = Walk(fi, rect, pad=8)
    F = W.F
    fname = H.FNAME[fi]
    doors = door_zone(W)
    spawns = [(s[1], s[2], s[3]) for s in H.spawns_in(fname, *W.box)]
    deco = {(d[0], d[1]) for d in H.decoration_in(fi, *W.box)}
    n, t = h['npc'], h['travel']
    npc = (n['x'], n['y'])
    stop = (t['x'], t['y'], t['z'])

    building = h.get('building')
    floor_extra = {}
    if building:
        bx, by, bz = building['x'], building['y'], building['z']
        comps = multidump.components(building['multi'])
        foot = {(bx + c[0], by + c[1]) for c in comps}
        bad = []
        for (x, y) in sorted(foot):
            # grass, leaves and flowers under 3 high that block nothing are covered by the floor (7 above the ground)
            st = [sid for sid, sz in F.statics(x, y)
                  if H.iheight(sid) > 2 or H.iflags(sid) & (H.IMP | H.SURF | H.WALL | H.ROOF)]
            if st:
                bad.append('%d,%d static %s' % (x, y, F.describe(x, y)))
            if (x, y) in deco:
                bad.append('%d,%d decoration' % (x, y))
            if abs(F.avgz(x, y) - bz) > 3:
                bad.append('%d,%d land z %d' % (x, y, F.avgz(x, y)))
            if any(cheb((x, y), (s[0], s[1])) <= 2 for s in spawns):
                bad.append('%d,%d within 2 of a spawner' % (x, y))
        if bad:
            fails.append('new building footprint: ' + '; '.join(bad[:6]) + (' (+%d)' % (len(bad) - 6) if len(bad) > 6 else ''))
        else:
            notes.append('footprint %d tiles clear, land within 3 of z%d' % (len(foot), bz))
        # the steps' foot: the row south of the steps (y + 8) must be standable ground for x -2..1
        for dx in (-2, -1, 0, 1):
            if not standable(W, bx + dx, by + 8, bz, 3):
                fails.append('the steps do not open onto standable ground at %d,%d' % (bx + dx, by + 8))
        # walls and floor of the multi block the outside walk around it: add them as blockers for the travel check
        for (x, y) in foot:
            W.extra.setdefault((x, y), []).append((bz, bz + 60))
        npc_ok = (n['x'] - bx, n['y'] - by)
        if not (-6 <= npc_ok[0] <= 5 and 0 <= npc_ok[1] <= 5) or npc_ok[1] == -1:
            fails.append('npc offset %s is not on the guild house front room floor (x -6..5, y 0..5)' % (npc_ok,))
        if any(cheb((n['x'], n['y']), (bx + d[0], by + d[1])) < 2 for d in GUILD_HOUSE_DOORS):
            fails.append('npc within 1 of a guild house door')
        if n['z'] != bz + 7:
            fails.append('npc z %d is not the guild house floor z%d' % (n['z'], bz + 7))
        floor_extra = foot

    # travel stop
    hs = W.heights(stop[0], stop[1])
    if not any(abs(z - stop[2]) <= 1 for z in hs):
        fails.append('travel stop %s not standable (heights %s)' % (stop, hs))
    elif any(F.roof_over(stop[0], stop[1], z) for z in hs if abs(z - stop[2]) <= 1):
        fails.append('travel stop %s is under a roof' % (stop,))
    reach = reach_xy(W, stop)
    x1, y1, x2, y2 = W.box
    if not any(x in (x1, x2) or y in (y1, y2) for (x, y) in reach):
        fails.append('travel stop does not reach the edge of the box (the town)')
    else:
        notes.append('stop reaches the town (%d tiles in the box)' % len(reach))

    if not building:
        # npc
        if not standable(W, n['x'], n['y'], n['z']):
            fails.append('npc %d,%d,%d does not fit (heights %s)' % (n['x'], n['y'], n['z'], W.heights(*npc)))
        near_door = [d for d in doors if cheb(npc, d) < 2]
        if near_door:
            fails.append('npc within 1 of a door or swing %s' % near_door)
        near_sp = [s for s in spawns if cheb(npc, s) <= 2]
        if near_sp:
            fails.append('npc within 2 of a pinned spawner %s' % near_sp)
        if npc in deco:
            fails.append('npc on a pinned decoration item')
        # beside the npc at its own floor (the ground under a raised floor does not count)
        beside = {(n['x'] + dx, n['y'] + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy}
        reach3 = W.flood(stop)
        if not any((x, y) in beside and abs(z - n['z']) <= 3 for (x, y, z) in reach3):
            fails.append('npc not reachable from the travel stop')
        else:
            notes.append('npc reachable from the stop')
        # cut test: block the npc tile
        W.extra[npc] = [(n['z'] - 5, n['z'] + 20)]
        reach2 = W.flood(stop)
        lost = {(x, y) for (x, y, z) in reach3 - reach2 if (x, y) != npc}
        if lost:
            fails.append('blocking the npc cuts off %d tile(s), e.g. %s' % (len(lost), sorted(lost)[:4]))
        else:
            notes.append('npc cuts no walk')
    else:
        notes.append('npc on the guild house floor (walk checked in game)')

    # sign
    s = h.get('sign')
    if s:
        # a hanging sign blocks nothing, and OSI hangs signs on door-swing tiles (Jhelom's 1368,3713): only the door itself
        if (s['x'], s['y']) in W.door_tiles():
            fails.append('sign on a door tile')

    # decor
    for d in h.get('decor', []):
        rows = T.get((d['set'], d['group']))
        if rows is None:
            fails.append('no decor template %s/%s' % (d['set'], d['group']))
            continue
        bad = []
        for (dx, dy, dz, iid, name) in rows:
            x, y, z = d['x'] + dx, d['y'] + dy, d['z']
            if dz:
                continue  # stacked on another row of the same group
            if (x, y) in floor_extra:
                ox, oy = x - building['x'], y - building['y']
                if z != building['z'] + 7 or not (-6 <= ox <= 5 and (0 <= oy <= 5 or -6 <= oy <= -2)):
                    bad.append('%s at offset %d,%d z%d is not on the guild house floor' % (name, ox, oy, z))
                if any(cheb((ox, oy), (gd[0], gd[1])) < 2 for gd in GUILD_HOUSE_DOORS):
                    bad.append('%s at offset %d,%d beside a guild house door' % (name, ox, oy))
                if cheb((x, y), npc) < 2:
                    bad.append('%s beside the npc' % name)
                continue
            elif not standable(W, x, y, z, 2):
                bad.append('%s at %d,%d not on floor z%d (%s)' % (name, x, y, z, W.heights(x, y)))
            if any(cheb((x, y), dd) < 2 for dd in doors):
                bad.append('%s at %d,%d by a door' % (name, x, y))
            if any(cheb((x, y), sp) < 2 for sp in spawns):
                bad.append('%s at %d,%d by a spawner' % (name, x, y))
            if (x, y) in deco:
                bad.append('%s at %d,%d on a decoration item' % (name, x, y))
            if cheb((x, y), npc) < 1:
                bad.append('%s on the npc' % name)
        if bad:
            fails.append('decor %s/%s: %s' % (d['set'], d['group'], '; '.join(bad)))
        before = W.flood(stop)
        tiles = {(d['x'] + r[0], d['y'] + r[1]) for r in rows}
        for (x, y) in tiles:
            W.extra.setdefault((x, y), []).append((d['z'] - 5, d['z'] + 30))
        after = W.flood(stop)
        lost = {(x, y) for (x, y, z) in before - after if (x, y) not in tiles}
        if lost:
            fails.append('decor %s/%s cuts off %d tile(s), e.g. %s' % (d['set'], d['group'], len(lost), sorted(lost)[:4]))
        else:
            notes.append('decor %s/%s (%d pieces) on clear floor, cuts no walk' % (d['set'], d['group'], len(rows)))
    return fails, notes


def main(keys):
    plan = json.load(open(PLAN))
    T = templates()
    lines, bad = ['| Hall | Result | Checked |', '|---|---|---|'], 0
    for h in plan['halls']:
        if keys and h['key'] not in keys:
            continue
        fails, notes = check(h, T)
        bad += bool(fails)
        lines.append('| %s | %s | %s |' % (h['key'], 'FAIL: ' + ' / '.join(fails) if fails else 'ok', '; '.join(notes)))
        print(h['key'], 'FAIL' if fails else 'ok')
        for f in fails:
            print('   ', f)
    if not keys:
        open(os.path.join(HERE, 'check.out.txt'), 'w').write('\n'.join(lines) + '\n')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(set(sys.argv[1:])))
