"""cc-P755 (P743's make_shots743.py): writes shots755.json, the private-shard shot scenes (the P750/P753 runner's shape): the admin seeds the
tutorial first (its reply shows the New Haven line), then each scene moves the Tester to a spot and logs both windows.

    python -P notes/cc-P755-tools/make_shots755.py
"""
import json
import os

T = 'Iron the Tester'
SCENES = [
    ('mountain-path-sign', (3703, 2746, 28), ['[ClusterFSeedTutorial']),
    ('stables-sign', (3611, 2616, 0), []),
    ('housing-stop1', (3712, 2594, 20), []),
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
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shots755.json')
json.dump(out, open(path, 'w'), indent=1)
print('wrote', path, len(out), 'scenes')
