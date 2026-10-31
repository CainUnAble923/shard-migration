# cc-P281: writes the proof's shot list (for notes/cc-P265-tools/proof.ps1): the first shot places every hall, then
# each shot puts the Golem's Player inside the hall two tiles from its guildmaster, on the side of the travel stop (new
# halls: inside the guild house, and a second shot from the travel stop outside). Read only.
#   python -P shots.py <out.json>
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from walk import Walk  # noqa: E402

PLAN = 'D:/UO/golems/Iron/ShatteredLegacy/design/guild-halls/halls.json'
MAPS = {0: 'Felucca', 1: 'Trammel', 3: 'Malas', 4: 'Tokuno', 5: 'TerMur'}


def cheb(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def view_tile(h):
    n, t = h['npc'], h['travel']
    if h.get('building'):
        b = h['building']
        return (b['x'] - 1, b['y'] + 3, b['z'] + 7)
    W = Walk(h['facet'], h['rect'])
    reach = W.flood((t['x'], t['y'], t['z']))
    for want in (2, 3, 1):
        best = None
        for (x, y, z) in reach:
            if cheb((x, y), (n['x'], n['y'])) == want and abs(z - n['z']) <= 3:
                d = cheb((x, y), (t['x'], t['y']))
                if best is None or d < best[0]:
                    best = (d, x, y, z)
        if best:
            return best[1:]
    raise SystemExit('%s: no view tile near the guildmaster' % h['key'])


def move(m, p):
    """Commands that put the Player at p on map m whether it stands in the world or is on the internal map (Point3D
    takes no spaces: '(1364, 3716, 0)' is refused)."""
    at = '(%d,%d,%d)' % tuple(p)
    who = ' where playermobile Name == "{player}"'
    return ['[global set LogoutMap %s%s' % (m, who), '[global set LogoutLocation %s%s' % (at, who),
            '[global set Map %s%s' % (m, who), '[global set Location %s%s' % (at, who)]


def main(out):
    plan = json.load(open(PLAN))
    shots = []
    for i, h in enumerate(plan['halls']):
        m = MAPS[h['facet']]
        v = view_tile(h)
        cmds = []
        if i == 0:
            cmds += ['[ClusterFGuildHalls place', '[ClusterFGuildHalls status']
        cmds += move(m, v)
        shots.append({'name': '%02d-%s' % (i + 1, h['key']), 'commands': cmds, 'at': list(v)})
        if h.get('building'):
            t = h['travel']
            p = (t['x'], t['y'] + 2, t['z'])
            shots.append({'name': '%02d-%s-outside' % (i + 1, h['key']), 'commands': move(m, p), 'at': list(p)})
    json.dump(shots, open(out, 'w'), indent=1)
    for s in shots:
        print(s['name'], s['at'])


if __name__ == '__main__':
    main(sys.argv[1])
