"""cc-P679 (SoS swap S4, part 4): the author's go-menu (Zigholtul's Siege of Sosaria Trammel Map 3.0,
Data/Locations/trammel.xml, copied here as sos-trammel-locations.xml) in pinned's go-menu format
(Distribution/Data/Locations/<facet>.json: GoCategory name, categories, locations with name and [x, y, z]).

    python -P golocations.py <code copy>

Writes <code copy>/server/data/Locations/trammel.json and felucca.json: the same tree, named for its facet (Felucca
stands on the same SoS land, SosMaps.cs). Every <parent> becomes a category and every <child> a location, in the file's
order; names and coordinates are his, unchanged. The single top <parent name="Trammel"> is the root.
"""
import json
import os
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, 'sos-trammel-locations.xml')


def category(node):
    c = {'name': node.get('name')}
    cats = [category(p) for p in node if p.tag == 'parent']
    locs = [{'name': ch.get('name'), 'location': [int(ch.get('x')), int(ch.get('y')), int(ch.get('z'))]}
            for ch in node if ch.tag == 'child']
    if cats:
        c['categories'] = cats
    if locs:
        c['locations'] = locs
    return c


def tree():
    root = ET.parse(SOURCE).getroot()
    tops = [p for p in root if p.tag == 'parent']
    assert len(tops) == 1 and tops[0].get('name') == 'Trammel', [t.get('name') for t in tops]
    assert not [n for n in root.iter() if n.tag not in ('places', 'parent', 'child')]
    return category(tops[0])


def dump(c, ind=0):
    """Pinned's layout: one location per line."""
    pad, inner = ' ' * ind, ' ' * (ind + 2)
    parts = [inner + '"name": ' + json.dumps(c['name'], ensure_ascii=False)]
    if 'categories' in c:
        parts.append(inner + '"categories": [\n' + ',\n'.join(dump(x, ind + 4) for x in c['categories'])
                     + '\n' + inner + ']')
    if 'locations' in c:
        parts.append(inner + '"locations": [\n' + ',\n'.join(
            inner + '  ' + json.dumps(loc, ensure_ascii=False) for loc in c['locations']) + '\n' + inner + ']')
    return pad + '{\n' + ',\n'.join(parts) + '\n' + pad + '}'


def count(c):
    return len(c.get('locations', [])) + sum(count(x) for x in c.get('categories', []))


def spots(c, path=()):
    for loc in c.get('locations', []):
        yield path + (c['name'],), loc
    for x in c.get('categories', []):
        yield from spots(x, path + (c['name'],))


def main():
    code = sys.argv[1]
    out = os.path.join(code, 'server', 'data', 'Locations')
    os.makedirs(out, exist_ok=True)
    t = tree()
    for facet in ('Trammel', 'Felucca'):
        t['name'] = facet
        with open(os.path.join(out, facet.lower() + '.json'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(dump(t) + '\n')
    print('spots', count(t), 'categories', sum(1 for _ in ET.parse(SOURCE).getroot().iter('parent')))


if __name__ == '__main__':
    main()
