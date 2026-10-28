"""cc-P677 (S8 item 3): the mine camp's tents on the Siege of Sosaria land (design/mine-camp-tents/layout.json).

SoS's mountain reaches further north and west than stock's: the Survey Archivist's tent (3492-3497, 2752-2756) is on
rock, and only a pocket of open ground (3493-3501, 2733-2747, Z 1-7) is left at the mountain's foot. The Miners'
Compact tent stays where it is; the Archivist's tent moves (+2, -16) into the pocket's north end, one free row above
the Miners' tent. Every component keeps its height above the ground: new Z = design Z - stock's GetAverageZ at its old
tile + SoS's at its new tile (both tents, so the Miners' tent also sits on SoS's ground). The Archivist's NPC "to" spot
moves with her tent. Checks every component's new tile is open on SoS (spots.Land) and lies inside the pocket.

    python -P replace_camp.py <SoS map folder> <stock client folder> <code copy> [--write]
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import spots  # noqa: E402

SHIFT = {'MinersCompactTent': (0, 0), 'SurveyArchivistTent': (2, -16)}
NPC_TENT = {'SurveyArchivist': 'SurveyArchivistTent', 'MinersCompactLiaison': 'MinersCompactTent'}


def main():
    sos, stock, code = sys.argv[1], sys.argv[2], sys.argv[3]
    path = os.path.join(code, 'design', 'mine-camp-tents', 'layout.json')
    raw = open(path, 'rb').read().decode('ascii')
    nl = '\r\n' if '\r\n' in raw else '\n'
    d = json.loads(raw)
    new_land, old_land = spots.Land(sos), spots.Land(stock)
    bad, taken = [], {}
    for addon in d['addons']:
        dx, dy = SHIFT[addon['name']]
        for c in addon['components']:
            x, y = c['x'] + dx, c['y'] + dy
            z = c['z'] - old_land.avgz(c['x'], c['y']) + new_land.avgz(x, y)
            if not new_land.open_tops(x, y):
                bad.append((addon['name'], c['name'], x, y, 'not open on SoS'))
            taken.setdefault((x, y), []).append(addon['name'])
            print('%-20s %-14s %d,%d,%d -> %d,%d,%d' % (addon['name'], c['name'], c['x'], c['y'], c['z'], x, y, z))
            c['x'], c['y'], c['z'] = x, y, z
    for n in d['npcs']:
        dx, dy = SHIFT[NPC_TENT[n['type']]]
        if (dx, dy) == (0, 0):
            print('npc %-20s to %s (its tent stays; unchanged)' % (n['type'], n['to']))
            continue
        x, y = n['to'][0] + dx, n['to'][1] + dy
        z = new_land.open_tops(x, y)
        if not z:
            bad.append((n['type'], 'to', x, y, 'not open on SoS'))
        else:
            n['to'] = [x, y, min(z, key=lambda t: abs(t - n['to'][2]))]
        print('npc %-20s to %s' % (n['type'], n['to']))
    mixed = [k for k, v in taken.items() if len(set(v)) > 1]
    if mixed:
        bad.append(('tiles shared by both tents', mixed))
    d['source'] = d['source'] + ('; cc-P677: on the Siege of Sosaria land the Archivist\'s tent moved (+2, -16) to the '
                                 'open ground at the mountain\'s foot and every z was re-measured there '
                                 '(shard-migration notes/cc-P677-tools/replace_camp.py)')
    print('problems:', bad)
    if bad:
        sys.exit(1)
    if '--write' in sys.argv:
        text = json.dumps(d, indent=1).replace('\n', nl) + nl
        open(path, 'wb').write(text.encode('ascii'))
        print('wrote', path)


if __name__ == '__main__':
    main()
