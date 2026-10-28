"""cc-P676: the SoS author's Regions.xml (ServUO format, read only), summarised: python -I authorregions.py <Regions.xml>"""
import collections, sys
import xml.etree.ElementTree as ET


def regions(path):
    """[(facet, type, name, parent names, [(x1, y1, x2, y2)], go, entrance, music, priority)] for every region."""
    root = ET.parse(path).getroot()
    out = []

    def walk(el, facet, parents):
        for r in el.findall('region'):
            rects = []
            for rect in r.findall('rect'):
                a = rect.attrib
                if 'width' in a:
                    x, y = int(a['x']), int(a['y'])
                    rects.append((x, y, x + int(a['width']) - 1, y + int(a['height']) - 1))
                else:
                    rects.append((int(a['x']), int(a['y']), int(a['x2']) - 1, int(a['y2']) - 1) if 'x2' in a else None)
            go = r.find('go'); ent = r.find('entrance'); mus = r.find('music')
            out.append((facet, r.get('type', ''), r.get('name', ''), tuple(parents), rects,
                        go.attrib if go is not None else None, ent.attrib if ent is not None else None,
                        mus.get('name') if mus is not None else None, r.get('priority')))
            walk(r, facet, parents + [r.get('name', '')])
    for f in root.findall('Facet'):
        walk(f, f.get('name'), [])
    return out


if __name__ == '__main__':
    rs = regions(sys.argv[1])
    print(collections.Counter(r[0] for r in rs))
    for facet in sorted({r[0] for r in rs}):
        sub = [r for r in rs if r[0] == facet]
        print(facet, collections.Counter(r[1] for r in sub))
    tr = [r for r in rs if r[0] == 'Trammel']
    for r in tr[:400]:
        if not r[3]:
            print('%-16s %-34s rects %3d go %s' % (r[1], r[2][:34], len(r[4]), r[5]))
