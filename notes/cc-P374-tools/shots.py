# cc-P374: writes the decor proof's shot list for notes/cc-P265-tools/proof.ps1 (read only).
#   python -P shots.py <out.json> [refusal]
# Each shot: the Golem's Admin goes to Trammel and the anchor, seeds there ("place <group> here"), then puts the
# Player (Iron the Tester) on a free tile about 12 tiles of screen west of the set's middle (the camera centres on
# the Player, and the first login's patch-notes and paperdoll gumps cover the left of the window). The three empty spots P265 found are reused: the
# structure set goes on the Alembic and Smiths spots after those sets are shot and cleared.
import json
import sys

DESIGN = 'D:/UO/golems/Iron/ShatteredLegacy/design/guild-hall-decor/templates.json'
CMD = {'alembic': 'DecorAlembicHall', 'smiths': 'DecorSmithsHall', 'artificers': 'DecorArtificersHall',
       'structure': 'DecorHallStructure'}
ALEMBIC, SMITHS, ARTIFICERS = (1135, 1791, 0), (1199, 1823, 0), (1231, 1889, 0)


def move(p):
    at = '(%d,%d,%d)' % tuple(p)
    who = ' where playermobile Name == "{player}"'
    return ['[global set LogoutMap Trammel%s' % who, '[global set LogoutLocation %s%s' % (at, who),
            '[global set Map Trammel%s' % who, '[global set Location %s%s' % (at, who)]


def go(p):
    return ['[global set Map Trammel where playermobile Name == "{golem}"', '[go %d %d %d' % p]


def occupied(sets, key, groups):
    s = next(s for s in sets if s['key'] == key)
    return {(r['dx'], r['dy']) for g in s['groups'] if g['key'] in groups for r in g['rows']}


def stand(anchor, want, taken):
    """The free tile nearest the wanted offset (not under a piece)."""
    best = min(((abs(dx) + abs(dy), dx, dy) for dx in range(-4, 5) for dy in range(-4, 5)
                if (want[0] + dx, want[1] + dy) not in taken))
    return (anchor[0] + want[0] + best[1], anchor[1] + want[1] + best[2], anchor[2])


def main(out, refusal=False):
    sets = json.load(open(DESIGN))['sets']
    allg = {s['key']: [g['key'] for g in s['groups']] for s in sets}
    shots = []

    def shot(name, key, anchor, groups, want, pre=(), place=True):
        cmds = list(pre) + go(anchor)
        if place:
            cmds += ['[%s place %s here' % (CMD[key], g) for g in groups] if groups != allg[key] \
                else ['[%s place here' % CMD[key]]
        cmds += ['[%s status' % CMD[key]]
        p = stand(anchor, want, occupied(sets, key, groups))
        cmds += move(p)
        shots.append({'name': name, 'commands': cmds, 'at': list(p)})

    if refusal:
        cmds = go(ARTIFICERS) + ['[DecorArtificersHall place here', '[DecorArtificersHall clear all',
                                 '[DecorArtificersHall status']
        p = stand(ARTIFICERS, (0, 4), set())
        shots.append({'name': 'refusal', 'commands': cmds + move(p), 'at': list(p)})
    else:
        shot('1-alembic', 'alembic', ALEMBIC, allg['alembic'], (-7, 7))
        shot('2-smiths', 'smiths', SMITHS, allg['smiths'], (-4, 6))
        shot('3-artificers', 'artificers', ARTIFICERS, allg['artificers'], (-4, 7))
        a = (ALEMBIC[0] - 4, ALEMBIC[1] - 3, 0)
        shot('4-structure-towers-and-balustrade', 'structure', a, ['tower-large', 'tower-medium', 'balustrade'],
             (-1, 10), pre=go(ALEMBIC) + ['[DecorAlembicHall clear', '[DecorAlembicHall status'])
        b = (SMITHS[0] - 17, SMITHS[1] + 15, 0)
        shot('5-structure-small-and-white-towers', 'structure', b,
             ['tower-small', 'tower-white-brick', 'tower-white-column'], (12, -8),
             pre=go(SMITHS) + ['[DecorSmithsHall clear', '[DecorSmithsHall status'])
        shot('6-structure-white-column-tower', 'structure', b, ['tower-white-column'], (17, -12), place=False)
    json.dump(shots, open(out, 'w'), indent=1)
    for s in shots:
        print(s['name'], s['at'])
        for c in s['commands']:
            print('   ', c)


if __name__ == '__main__':
    main(sys.argv[1], len(sys.argv) > 2 and sys.argv[2] == 'refusal')
