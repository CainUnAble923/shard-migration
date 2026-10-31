"""cc-P750: the shot list for shots750.ps1 (shots750.json). The Admin places the halls ([ClusterFGuildHalls place, test
shard only) and reports their status; then the Tester stands in Fort Viridian's open inner court south-west of the
Rangers' guildmaster's new post (both should show), beside the League's and the Tinkers' rehung signs, and on the
Custodians' and the Tinkers' travel stops (the cover model reads them 100% and 42% covered: a look in game). Every spot
is a standable tile at its Z on the SoS land (P708's walk), the nearest to the wanted one.
    python -P make_shots750.py   -> shots750.json
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'cc-P708-tools', 'p281sos'))
from walk import Walk  # noqa: E402

PLAN = 'D:/UO/golems/Iron/ShatteredLegacy/design/guild-halls/halls.json'
P = 'Iron the Tester'


def stand(x, y, z, near=(0, 0)):
    """The standable tile nearest (x+dx, y+dy) at about z (within 3), searching outward (P708's make_shots.py)."""
    W = Walk(1, (x - 8, y - 8, x + 8, y + 8), pad=1)
    best = None
    for r in range(0, 6):
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                tx, ty = x + near[0] + dx, y + near[1] + dy
                for h in W.heights(tx, ty):
                    if abs(h - z) <= 3 and (best is None or abs(dx) + abs(dy) < best[0]):
                        best = (abs(dx) + abs(dy), tx, ty, h)
        if best:
            return best[1:]
    raise SystemExit('no standable tile near %s' % ((x, y, z),))


def move(x, y, z):
    loc = '(%d,%d,%d)' % (x, y, z)
    return ['[global resurrect where playermobile Name == "%s"' % P,
            '[global set Blessed True where playermobile Name == "%s"' % P,
            '[global set Map Trammel where playermobile Name == "%s"' % P,
            '[global set Location %s where playermobile Name == "%s"' % (loc, P),
            '[global set LogoutMap Trammel where playermobile Name == "%s"' % P,
            '[global set LogoutLocation %s where playermobile Name == "%s"' % (loc, P)]


halls = {h['key']: h for h in json.load(open(PLAN, encoding='utf-8'))['halls']}
r, lg, tk, cu = halls['rangers'], halls['league'], halls['tinkers'], halls['custodians']
n = r['npc']
scenes = [
    {'name': 'rangers-guildmaster', 'commands': ['[ClusterFGuildHalls place', '[ClusterFGuildHalls status']
        + move(*stand(n['x'], n['y'], n['z'], near=(-3, 4)))},
    {'name': 'league-sign', 'commands': move(*stand(lg['sign']['x'], lg['sign']['y'], lg['travel']['z'], near=(-3, 3)))},
    {'name': 'tinkers-sign', 'commands': move(tk['travel']['x'], tk['travel']['y'], tk['travel']['z'])},
    {'name': 'custodians-stop', 'commands': move(cu['travel']['x'], cu['travel']['y'], cu['travel']['z'])},
    {'name': 'replace-again', 'commands': ['[ClusterFGuildHalls place'] + move(*stand(n['x'], n['y'], n['z'], near=(-3, 4)))},
]
json.dump(scenes, open(os.path.join(HERE, 'shots750.json'), 'w'), indent=1)
for s in scenes:
    print(s['name'], [c for c in s['commands'] if 'Location (' in c and 'Logout' not in c])
