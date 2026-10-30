"""cc-P734: the in-game proof for the six practice builds on The Fold's Green Acres stretch (x 5700-5779, y 1170-1224,
flat grass at Z 0, empty: plot_scan.py). Writes:
  - place.json: the Admin's commands that place every build ([PlaceBuild practice-<name> x y z on TheFold);
  - shots.json: one TazUO shot per view (outside from the north-west, inside each room, the stair, both bridge ends);
  - walks.json and Walk<Name>.py: a real character walks each door, gate, stair, bridge and dock both ways, step by
    step (the client's own moves; a closed door or gate in the way is opened by double-click, as a player would).
Usage: python -P notes/cc-P734-tools/make_walks.py <work folder for the walk logs> [walk,walk: only these, to walks-again.json]"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = sys.argv[1] if len(sys.argv) > 1 else r'D:\UO\golems\Iron\p734-proof'
MAP = 'TheFold'
ORIGIN = {'farmhouse': (5700, 1170), 'bank': (5720, 1170), 'lodge': (5740, 1170),
          'dock': (1550, 612), 'market': (5722, 1195), 'twostory': (5742, 1195)}
# Review round 1: the dock moved to a real lake on The Fold (x 1550-1576, y 612-634; banks Z 1 west and east of the
# bridge rows, Z 6 south of the pier), since water statics over grass block nothing.


def at(name, dx, dy, z=0):
    ox, oy = ORIGIN[name]
    return (ox + dx, oy + dy, z)


def move(p):
    loc = '(%d,%d,%d)' % p
    return ['[global set Map %s where playermobile Name == "{player}"' % MAP,
            '[global set Location %s where playermobile Name == "{player}"' % loc,
            '[global set LogoutMap %s where playermobile Name == "{player}"' % MAP,
            '[global set LogoutLocation %s where playermobile Name == "{player}"' % loc]


def shot(name, p, settle=15, legion='Clear734.py', **kw):
    s = {'name': name, 'character': 'Iron the Tester', 'commands': move(p), 'settle': settle, 'legion': legion}
    s.update(kw)
    return s


# Views: outside from the plot's north-west corner (the subject lower right, as the proof shots do), and inside each
# room (the client hides a roof over a player inside it).
SHOTS = [
    shot('farmhouse-outside', at('farmhouse', 1, 1)), shot('farmhouse-front', at('farmhouse', 4, 10)),
    shot('farmhouse-inside', at('farmhouse', 4, 5)),
    shot('bank-outside', at('bank', 1, 1)), shot('bank-front', at('bank', 5, 11)), shot('bank-inside', at('bank', 6, 6)),
    shot('lodge-outside', at('lodge', 1, 1)), shot('lodge-front', at('lodge', 6, 12)), shot('lodge-inside', at('lodge', 6, 8)),
    shot('dock-west-end', at('dock', 3, 7, 1)), shot('dock-east-end', at('dock', 24, 7, 1)), shot('dock-pier', at('dock', 16, 22, 6)),
    shot('market-outside', at('market', 0, 0)), shot('market-square', at('market', 8, 10)),
    shot('twostory-outside', at('twostory', 1, 1)), shot('twostory-front', at('twostory', 4, 11)),
    shot('twostory-ground', at('twostory', 5, 7)), shot('twostory-stair-foot', at('twostory', 7, 7)),
    shot('twostory-upper', at('twostory', 6, 5, 20)),
]

# Walks: legs of (direction, axis 0/1, '<=' or '>=', absolute target).
WALKS = {
    # In by the south door to the chair in front of the table (the table at y 4 blocks a straight line), and out.
    'farmhouse': (at('farmhouse', 5, 9), [('north', 1, '<=', at('farmhouse', 0, 5)[1]), ('south', 1, '>=', at('farmhouse', 0, 9)[1])]),
    # Through the field gate (west side of the fence, y 5) into the garden and back.
    'farmgate': (at('farmhouse', 9, 5), [('east', 0, '>=', at('farmhouse', 12, 0)[0]), ('west', 0, '<=', at('farmhouse', 9, 0)[0])]),
    'bank': (at('bank', 6, 10), [('north', 1, '<=', at('bank', 0, 5)[1]), ('south', 1, '>=', at('bank', 0, 10)[1])]),
    'lodge': (at('lodge', 7, 11), [('north', 1, '<=', at('lodge', 0, 8)[1]), ('south', 1, '>=', at('lodge', 0, 11)[1])]),
    # Across the bridge on its middle row and back; then from the south bank out along the pier's middle column to
    # its free end (the rail across the end at row 15 stops a walker at row 16) and back.
    'dock': (at('dock', 2, 7, 1), [('east', 0, '>=', at('dock', 25, 0)[0]), ('west', 0, '<=', at('dock', 2, 0)[0])]),
    'pier': (at('dock', 16, 23, 6), [('north', 1, '<=', at('dock', 0, 16)[1]), ('south', 1, '>=', at('dock', 0, 23)[1])]),
    'market': (at('market', 0, 10), [('east', 0, '>=', at('market', 15, 0)[0]), ('west', 0, '<=', at('market', 0, 0)[0])]),
    'twostory': (at('twostory', 4, 10), [('north', 1, '<=', at('twostory', 0, 7)[1]), ('east', 0, '>=', at('twostory', 8, 0)[0]),
                                         ('north', 1, '<=', at('twostory', 0, 3)[1]), ('south', 1, '>=', at('twostory', 0, 7)[1]),
                                         ('west', 0, '<=', at('twostory', 4, 0)[0]), ('south', 1, '>=', at('twostory', 0, 10)[1])]),
}

WALK = '''# cc-P734: a real character walks the practice %(name)s, step by step in TazUO (the client's own movement, the server's
# own checks; no teleport). A closed door or gate in the way is double-clicked open, as a player would. Made by
# notes/cc-P734-tools/make_walks.py.
import API

LOG = r"%(log)s"
LEGS = %(legs)r
DOORS = set(range(0x0675, 0x06F5)) | set(range(0x0839, 0x0849))


def say(text):
    API.SysMsg("Walk %(name)s: " + text)
    with open(LOG, "a") as f:
        f.write(text + "\\n")


def where():
    p = API.Player
    return (p.X, p.Y, p.Z)


def done(pos, axis, op, value):
    return pos[axis] >= value if op == ">=" else pos[axis] <= value


def open_door():
    for it in API.GetItemsOnGround(2) or []:
        if it.Graphic in DOORS:
            API.UseObject(it.Serial)
            say("opened a door or gate 0x%%04X at %%d,%%d,%%d" %% (it.Graphic, it.X, it.Y, it.Z))
            API.Pause(1)
            return True
    return False


API.Pause(8)
open(LOG, "w").close()
say("start %%s" %% (where(),))
for direction, axis, op, value in LEGS:
    last = where()
    stuck = 0
    opened = False
    for i in range(40):
        API.Walk(direction)
        API.Pause(0.6)
        now = where()
        say("%%s step %%d: %%s" %% (direction, i, now))
        if done(now, axis, op, value):
            say("%%s: reached %%s" %% (direction, now))
            break
        # No progress along the leg's axis counts as stuck (a side-step shuffle is not progress).
        stuck = stuck + 1 if (now[axis] - last[axis]) * (1 if op == ">=" else -1) <= 0 else 0
        last = now
        if stuck >= 2 and not opened:
            opened = open_door()
            stuck = 0
        if stuck >= 4:
            say("%%s: STUCK at %%s" %% (direction, now))
            break
    API.Pause(1)
say("end %%s" %% (where(),))
'''

CLEAR = '''# cc-P734 (P724's Clear724.py): closes the server's login windows (patch notes, achievements) so the shot shows the
# build, then stays idle.
import API

for _ in range(4):
    API.Pause(3)
    for g in API.GetAllGumps():
        try:
            g.Dispose()
        except Exception:
            pass
'''

if __name__ == '__main__':
    os.makedirs(WORK, exist_ok=True)
    place = []
    for name, (ox, oy) in ORIGIN.items():
        place.append('[PlaceBuild practice-%s %d %d 0' % (name, ox, oy))
    admin = ['[global set Map %s where playermobile Name == "{golem}"' % MAP,
             '[global set Location (5690,1165,0) where playermobile Name == "{golem}"'] + place
    json.dump(admin, open(os.path.join(HERE, 'place.json'), 'w'), indent=1)
    json.dump(SHOTS, open(os.path.join(HERE, 'shots.json'), 'w'), indent=1)
    walks = []
    for name, (start, legs) in WALKS.items():
        fn = 'Walk%s.py' % name.capitalize()
        with open(os.path.join(HERE, fn), 'w', encoding='ascii', newline='\n') as f:
            f.write(WALK % {'name': name, 'log': os.path.join(WORK, 'walk-%s.log' % name), 'legs': legs})
        if len(sys.argv) > 2 and name not in sys.argv[2].split(','):
            continue
        walks.append({'name': 'walk-' + name, 'character': 'Iron the Tester', 'commands': move(start), 'legion': fn,
                      'settle': 12, 'frames': 70, 'frameMs': 1000})
    json.dump(walks, open(os.path.join(HERE, 'walks.json' if len(sys.argv) <= 2 else 'walks-again.json'), 'w'), indent=1)
    with open(os.path.join(HERE, 'Clear734.py'), 'w', encoding='ascii', newline='\n') as f:
        f.write(CLEAR)
    print('place.json %d commands, shots.json %d shots, walks.json %d walks' % (len(admin), len(SHOTS), len(walks)))
