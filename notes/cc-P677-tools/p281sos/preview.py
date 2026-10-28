# cc-P281: a client-geometry render of each hall from the client files, roofs and upper storeys left out, with the
# plan's marks: G guildmaster, s sign, T travel stop, D decor anchors, M the new building's centre. Read only.
#   python -P preview.py [key ...]   -> preview-<key>.png (git-ignored)
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hallbase as H  # noqa: E402

PLAN = os.environ.get('HALLS_JSON', 'D:/UO/golems/Iron/ShatteredLegacy/design/guild-halls/halls.json')


def marks_for(h):
    m = []
    n = h['npc']
    m.append(('G ' + h['key'], n['x'], n['y'], n['z'], (255, 60, 60, 255)))
    if h.get('sign'):
        s = h['sign']
        m.append(('s', s['x'], s['y'], s['z'], (80, 200, 255, 255)))
    t = h['travel']
    m.append(('T', t['x'], t['y'], t['z'], (80, 255, 80, 255)))
    for d in h.get('decor', []):
        m.append(('D ' + d['group'], d['x'], d['y'], d['z'], (255, 200, 0, 255)))
    if h.get('building'):
        b = h['building']
        m.append(('M', b['x'], b['y'], b['z'], (255, 0, 255, 255)))
    return m


def main(keys):
    plan = json.load(open(PLAN))
    for h in plan['halls']:
        if keys and h['key'] not in keys:
            continue
        x1, y1, x2, y2 = h['rect']
        pad = 4
        F = H.Facet(h['facet'])
        cut = h['npc']['z'] + 12
        out = os.path.join(HERE, 'preview-%s.png' % h['key'])
        H.render(F, x1 - pad, y1 - pad, x2 + pad, y2 + pad, marks=marks_for(h), out=out, scale=0.6,
                 hide_roofs_above=cut, label='%s: %s (%s)' % (h['key'], h['building_name'], h['kind']))
        print(out)


if __name__ == '__main__':
    main(set(sys.argv[1:]))
