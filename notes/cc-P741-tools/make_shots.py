"""cc-P741: the shot list (shots.json, walks.json) for isle-shots.ps1: Iron the Tester moved beside each subject, Z
from the built map's ground (build_isle.Walker), default camera. python -P make_shots.py <edited folder>"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'scripts')); sys.path.insert(0, os.path.join(HERE, '..', 'cc-P662-tools'))
import build_isle as B
w = B.Walker(sys.argv[1], B.shifted(*B.AREA[:2]) + B.shifted(*B.AREA[2:]))
SPOTS = [
    ('coast-wreck', 6633, 3992, None), ('coast-west', 6631, 4001, None), ('coast-southwest', 6662, 4003, None),
    ('coast-north', 6700, 3944, None), ('coast-northeast', 6745, 3946, None), ('coast-yard-south', 6740, 4013, None),
    ('coast-east', 6803, 3973, None), ('coast-dock', 6812, 3993, None),
    ('sign-1-movement', 6646, 3992, None), ('sign-4-chat', 6690, 3990, None), ('sign-6-death', 6736, 3992, None),
    ('sign-11-travel', 6810, 3991, None),
    ('farm', 6688, 3987, None), ('farm-gate', 6697, 3981, None), ('farmhouse-inside', 6702, 3976, 7),
    ('bank-front', 6762, 3985, None), ('bank-inside', 6762, 3979, None),
    ('lodge-front', 6782, 3991, None), ('lodge-inside', 6782, 3997, None),
]
TESTER = 'where playermobile Name == "Iron the Tester"'
out = []
for name, x, y, z in SPOTS:
    z = w.ground(x, y) if z is None else z
    loc = '(%d,%d,%d)' % (x, y, z)
    out.append({'name': name, 'character': 'Iron the Tester',
                'commands': ['[global set Map TheFold ' + TESTER, '[global set Location %s %s' % (loc, TESTER),
                             '[global set LogoutMap TheFold ' + TESTER, '[global set LogoutLocation %s %s' % (loc, TESTER)],
                'settle': 18, 'legion': 'Clear741.py'})
json.dump(out, open(os.path.join(HERE, 'shots.json'), 'w'), indent=1)
x, y = 6629, 4003
loc = '(%d,%d,%d)' % (x, y, w.ground(x, y))
walk = [{'name': 'beach-walk', 'character': 'Iron the Tester',
         'commands': ['[global set Map TheFold ' + TESTER, '[global set Location %s %s' % (loc, TESTER),
                      '[global set LogoutMap TheFold ' + TESTER, '[global set LogoutLocation %s %s' % (loc, TESTER)],
         'legion': 'BeachWalk741.py', 'settle': 12, 'frames': 50, 'frameMs': 2000}]
json.dump(walk, open(os.path.join(HERE, 'walks.json'), 'w'), indent=1)
print(len(out), 'shots; walk from', loc)
