"""cc-P679: scenes.json for the TazUO shot at each moongate (P716's shots.ps1).

    python -P make_scenes.py <overlay>

The bot world was generated on stock, so its gates stand at stock's spots; an Administrator cannot run [MoonGen
(Developer). The first scene's commands list the world's gates, then move each to PMList's new spot with [global set,
matching it by its X (no gate of another facet shares one): that is what [MoonGen makes from the patched list. Each
scene puts the Player by a Trammel gate and the Admin by the Felucca one, about three tiles north-west (the nearest open
tile to that), at the tile's floor. The Player is resurrected first (the entrance walks may have left him dead). Scene 9: New Haven (Trammel) and Buccaneer's Den (Felucca).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sosland  # noqa: E402

GATES = [('moonglow', 4467, 1283, 23), ('britain', 1336, 1997, 15), ('jhelom', 1499, 3771, 5), ('yew', 771, 752, 15),
         ('minoc', 2701, 692, 20), ('trinsic', 1828, 2948, -16), ('skara-brae', 643, 2067, 5),
         ('magincia', 3563, 2139, 34)]
NEW_HAVEN, BUCS = ('new-haven', 3696, 2570, 14), ('bucs-den', 2711, 2234, 0)
# [global set lines: (stock X, the new Location)
MOVES = [(4467, (4467, 1283, 23)), (1336, (1336, 1997, 15)), (771, (771, 752, 15)), (2701, (2701, 692, 20)),
         (1828, (1828, 2948, -16)), (3563, (3563, 2139, 34)), (3450, (3696, 2570, 14))]


def stand(L, x, y, z):
    # North-west of the gate: the client draws the gate below the character, clear of the login windows that cover
    # the upper left of every shot (P716).
    for dx, dy in ((-3, -3), (-2, -3), (-3, -2), (-2, -2), (-4, -3), (-3, -4), (-1, -3), (-3, -1), (-2, -1), (-1, -2)):
        tops = L.open_tops(x + dx, y + dy)
        if tops:
            return x + dx, y + dy, min(tops, key=lambda t: abs(t - z))
    raise SystemExit('no stand tile by %d,%d' % (x, y))


def put(who, m, p):
    loc = '(%d,%d,%d)' % p
    return ['[global set Map %d where playermobile Name == "{%s}"' % (m, who),
            '[global set Location %s where playermobile Name == "{%s}"' % (loc, who),
            '[global set LogoutMap %d where playermobile Name == "{%s}"' % (m, who),
            '[global set LogoutLocation %s where playermobile Name == "{%s}"' % (loc, who)]


def main():
    L = sosland.land(sys.argv[1])
    scenes = []
    pairs = [(g, g) for g in GATES] + [(NEW_HAVEN, BUCS)]
    for i, (t, f) in enumerate(pairs, 1):
        cmds = []
        if i == 1:
            cmds.append('[global resurrect where playermobile Name == "{player}"')
            cmds.append('[global get Location where publicmoongate')
            cmds += ['[global set Location (%d,%d,%d) where publicmoongate X == %d' % (p + (x,)) for x, p in MOVES]
            cmds.append('[global get Location where publicmoongate')
        cmds += put('player', 1, stand(L, *t[1:])) + put('golem', 0, stand(L, *f[1:]))
        name = '%d-%s-trammel-player-%s-felucca-admin' % (i, t[0], f[0])
        scenes.append({'name': name, 'restart': False, 'commands': cmds})
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scenes.json')
    json.dump(scenes, open(out, 'w'), indent=2)
    print(out, len(scenes))


if __name__ == '__main__':
    main()
