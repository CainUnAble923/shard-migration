"""cc-P708: the shot list for shots708.ps1 (shots708.json). The first scene has the Admin place the halls
([ClusterFGuildHalls place, test shard only) and report their status; then, per moved hall, the Tester on its travel
stop (the door and the sign) and about 3 tiles north-west of its guildmaster (the guildmaster below him, clear of the
windows top left); and Fort Stormhammer's hall and its upper floor for the survey. Every Tester spot is a standable
tile at its Z on the SoS land (the P708 walk), the nearest to the wanted one.
    python -P make_shots.py   -> shots708.json, shots708b.json (the second pass), shots708c.json (the third)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'p281sos'))
from walk import Walk  # noqa: E402

PLAN = 'D:/UO/golems/Iron/ShatteredLegacy/design/guild-halls/halls.json'
P = 'Iron the Tester'
MOVED = ['league', 'merchants', 'healers', 'rangers', 'tinkers', 'custodians']


def stand(x, y, z, near=(0, 0)):
    """The standable tile nearest (x+dx, y+dy) at about z (within 3), searching outward."""
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
scenes = []
first = True
for key in MOVED:
    h = halls[key]
    t, n = h['travel'], h['npc']
    door = stand(t['x'], t['y'], t['z'])
    inside = stand(n['x'], n['y'], n['z'], near=(-3, -3))
    pre = ['[ClusterFGuildHalls place', '[ClusterFGuildHalls status'] if first else []
    first = False
    scenes.append({'name': key + '-door', 'commands': pre + move(*door)})
    scenes.append({'name': key + '-inside', 'commands': move(*inside)})
# Fort Stormhammer, the survey: the gate, the great hall (the Sentinels entrance in its north-west corner), the upper floor
scenes.append({'name': 'stormhammer-gate', 'commands': move(*stand(1488, 1320, 2))})
scenes.append({'name': 'stormhammer-hall', 'commands': move(*stand(1486, 1300, 2))})
scenes.append({'name': 'stormhammer-upper', 'commands': move(*stand(1488, 1302, 24))})
json.dump(scenes, open(os.path.join(HERE, 'shots708.json'), 'w'), indent=1)

# the second pass: the windows top left hid what stood north-west of the Tester; 4 tiles south-west of the subject puts
# it to the right of the Tester, clear of them (shots708b.json)
second = []
for key in MOVED:
    h = halls[key]
    n, g = h['npc'], h['sign']
    second.append({'name': key + '-guildmaster', 'commands': move(*stand(n['x'], n['y'], n['z'], near=(-4, 4)))})
    second.append({'name': key + '-sign', 'commands': move(*stand(g['x'], g['y'], h['travel']['z'], near=(-4, 4)))})
json.dump(second, open(os.path.join(HERE, 'shots708b.json'), 'w'), indent=1)
scenes = scenes + second

# the third pass, after the signs were rehung outside their walls (edit_signs.py): the Admin places again (the old signs
# are taken away), then each sign from 4 tiles south-west, and the Rangers' guildmaster from inside his court
third = [{'name': 'replace', 'commands': ['[ClusterFGuildHalls place', '[ClusterFGuildHalls status']}]
for key in MOVED:
    h = halls[key]
    g = h['sign']
    third.append({'name': key + '-sign2', 'commands': move(*stand(g['x'], g['y'], h['travel']['z'], near=(-4, 4)))})
n = halls['rangers']['npc']
third.append({'name': 'rangers-guildmaster2', 'commands': move(*stand(n['x'], n['y'], n['z'], near=(-3, 2)))})
json.dump(third[:1] + third[1:], open(os.path.join(HERE, 'shots708c.json'), 'w'), indent=1)
scenes = scenes + third
for s in scenes:
    print(s['name'], [c for c in s['commands'] if 'set Location' in c])
