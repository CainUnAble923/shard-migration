"""cc-P743: writes shots743.json, the private-shard shot scenes (the P750/P753 runner's shape): the admin seeds the
tutorial first (its reply shows the New Haven line), then each scene moves the Tester to a spot and logs both windows.

    python -P notes/cc-P743-tools/make_shots743.py
"""
import json
import os

T = 'Iron the Tester'
SCENES = [
    ('rook-bench', (3669, 2633, 0), ['[ClusterFSeedTutorial']),
    ('proving-grounds', (3731, 2585, 40), []),
    ('mountain-path-sign', (3703, 2748, 30), []),
    ('mining-cave', (3612, 2744, 9), []),
    ('stables-stall', (3605, 2617, 0), []),
    ('bardic-hall', (3663, 2532, 0), []),
    ('magery-hall', (3651, 2477, 0), []),
    ('housing-stop1', (3709, 2595, 20), []),
    ('old-farm-site', (3390, 2611, 27), ['[ClusterFSeedTutorialFarm dryrun']),
]


def move(x, y, z):
    loc = '(%d,%d,%d)' % (x, y, z)
    who = 'where playermobile Name == "%s"' % T
    return [
        '[global resurrect ' + who,
        '[global set Blessed True ' + who,
        '[global set Map Trammel ' + who,
        '[global set Location %s %s' % (loc, who),
        '[global set LogoutMap Trammel ' + who,
        '[global set LogoutLocation %s %s' % (loc, who),
    ]


out = [{'name': n, 'commands': pre + move(*at)} for n, at, pre in SCENES]
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shots743.json')
json.dump(out, open(path, 'w'), indent=1)
print('wrote', path, len(out), 'scenes')
