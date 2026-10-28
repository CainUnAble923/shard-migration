"""cc-P677 (SoS swap S8): every coordinate literal in S8's files, checked on the land the server reads.

    python -P spots.py <SoS map folder> <code copy> [--files <list file>] [--out <csv>]

The land is the SoS base with our trammel.mapops (docker/uo/Build-MapOverlay.ps1 writes it), the Trammel files Felucca
shares too (P675). Literals are P669's (geo.py's PAT): new Point3D/Point2D(x, y[, z]), new Rectangle2D/3D(x, y, ...),
bare (x, y, z) tuples, "go x y"; this keeps the Z where the literal gives one. A patch's own (+) lines only.

Each literal's facet: a Map.X on its line, else the nearest within the 15 lines before, else the file's own (P669's: it
names Trammel, Felucca, both, or neither). Literals on another facet (Ter Mur, Ilshenar, Malas, Tokuno) are not on the
SoS land and are only listed.

A spot passes when its tile has a standing surface (the land, unless it is water, impassable or void, or a Surface
static: a floor, a dock, stairs) with nothing impassable in the 16 Z above it (pinned's PersonHeight), and, for a
literal with a Z, one such surface is within 5 Z of it. The verdict is ok, or why not: water, void, land impassable,
blocked (the static that blocks), or z (the nearest standing Z).
"""
import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(DOCS, 'scripts'))
sys.path.insert(0, os.path.join(DOCS, 'notes', 'cc-P481-tools'))
from mapbuild import uofiles  # noqa: E402
import islands  # noqa: E402

IMP, WET, SURF, BRIDGE = 0x40, 0x80, 0x200, 0x400


def calc_height(it):
    # pinned ItemData.CalcHeight: a Bridge item (stairs, ramps, raised blocks) counts half its height
    return it['height'] // 2 if it['flags'] & BRIDGE else it['height']
PERSON, ZTOL = 16, 5
VOID_IDS = set(int(i) for i in islands.VOID_IDS)  # P481's void land ids
SOS_FACETS = ('Trammel', 'Felucca', 'both', 'unnamed')

PAT = [
    ('Point3D', re.compile(r"new Point3D\(\s*(\d{1,4})\s*,\s*(\d{1,4})\s*,\s*(-?\d{1,3})?")),
    ('Point2D', re.compile(r"new Point2D\(\s*(\d{1,4})\s*,\s*(\d{1,4})\s*\)")),
    ('Rectangle', re.compile(r"new Rectangle[23]D\(\s*(\d{1,4})\s*,\s*(\d{1,4})\s*,")),
    ('tuple', re.compile(r"\(\s*(\d{3,4})\s*,\s*(\d{3,4})\s*,\s*(-?\d{1,3})\s*\)")),
    ('go', re.compile(r"\bgo (\d{3,4}) (\d{3,4})")),
]
MAPREF = re.compile(r"Map\.(Trammel|Felucca|Ilshenar|Malas|Tokuno|TerMur|Internal)\b")
# ClusterFGuildHallPlacementData's records: new("key", "Guild", Kind.X, "Building", "Town", <MapIndex>,
HALL = re.compile(r'new\("[^"]+", "[^"]*", Kind\.\w+, "[^"]*", "[^"]*", (\d),')
MAP_INDEX = {0: 'Felucca', 1: 'Trammel', 2: 'Ilshenar', 3: 'Malas', 4: 'Tokuno', 5: 'TerMur'}
# Files whose literals are all on one facet that the line-by-line reading cannot see (declared above the Map.X use).
FILE_FACET = {
    'server/customizations/Services/Expansions/Time Of Legends/EodonGeneration.cs': 'TerMur',  # Eodon: Map.TerMur
}


def facet_of(lines, i, file_facet):
    """The facet of a literal on line i (0-based): a Map.X on its line, else the nearest within the 15 lines before,
    else the file's own."""
    for j in range(i, max(-1, i - 16), -1):
        m = MAPREF.findall(lines[j])
        if m:
            return m[0] if j == i else m[-1]
    return file_facet


def literals(path, rel):
    """[(rel, line, kind, x, y, z or None, text, facet)] for one file, as geo.py reads it (comment lines skipped)."""
    out = []
    lines = open(path, encoding='utf-8', errors='replace').read().splitlines()
    whole = chr(10).join(lines)
    t, fe = 'Trammel' in whole, 'Felucca' in whole
    file_facet = 'both' if t and fe else 'Trammel' if t else 'Felucca' if fe else 'unnamed'
    file_facet = FILE_FACET.get(rel, file_facet)
    record_facet = FILE_FACET.get(rel)  # a guild hall record names its facet by MapIndex (ClusterFGuildHallPlacementData)
    for i, line in enumerate(lines, 1):
        hall = HALL.search(line)
        if hall:
            record_facet = MAP_INDEX.get(int(hall.group(1)), 'other')
        elif line.strip().startswith(('new("', ']')) and record_facet and 'Kind.' not in line and line.strip() == ']),':
            record_facet = None
        if line.lstrip().startswith(('//', '///', '#')) and 'go ' not in line:
            continue
        if rel.endswith('.patch') and not line.startswith('+'):
            continue  # a patch's own lines only: context and removed lines are pinned's
        seen = set()
        for kind, p in PAT:
            for m in p.finditer(line):
                x, y = int(m.group(1)), int(m.group(2))
                if (x < 8 and y < 8) or m.start(1) in seen:
                    continue
                seen.add(m.start(1))  # one literal once: a Point3D's numbers also read as a bare tuple
                z = int(m.group(3)) if m.lastindex and m.lastindex >= 3 and m.group(3) is not None else None
                out.append((rel, i, kind, x, y, z, line.strip()[:160],
                            record_facet or facet_of(lines, i - 1, file_facet)))
    return out


class Land:
    def __init__(self, folder):
        self.folder = folder
        self.ids, self.zs = uofiles.load_land(folder, 1)
        self.land, self.items = uofiles.read_tiledata(uofiles.CLIENT)

    def avgz(self, x, y):
        """pinned Map.GetAverageZ (Map.cs:243-285): the diagonal with the smaller slope, halved toward zero (as P678's
        soswalk.py)."""
        zs = self.zs
        t, l, r, b = int(zs[x, y]), int(zs[x, min(4095, y + 1)]), int(zs[min(7167, x + 1), y]), int(zs[min(7167, x + 1), min(4095, y + 1)])
        return int((l + r) / 2) if abs(t - b) > abs(l - r) else int((t + b) / 2)

    def surfaces(self, x, y):
        """(standing Zs on this tile, statics on it, land reason), every level kept."""
        lid, lz = int(self.ids[x, y]), int(self.zs[x, y])
        lf = self.land[lid][0]
        sts = [(s[2], s[3]) for s in uofiles.statics_in(self.folder, 1, x, y, x, y)]
        tops, why = [], None
        if lid in VOID_IDS:
            why = 'void'
        elif lf & WET:
            why = 'water'
        elif lf & IMP:
            why = 'land impassable'
        else:
            tops.append(self.avgz(x, y))  # pinned stands a mobile on land at Map.GetAverageZ, not the tile's own Z
        for sz, i in sts:
            it = self.items[i]
            if it['flags'] & SURF:
                tops.append(sz + calc_height(it))
        return sorted(set(tops)), sts, why

    def open_tops(self, x, y):
        """The standing Zs on this tile a person fits on (check's rule), exactly."""
        if not (0 <= x < 7168 and 0 <= y < 4096):
            return []
        tops, sts, why = self.surfaces(x, y)
        return [t for t in tops if not any(
            self.items[i]['flags'] & (IMP | SURF)
            and not (self.items[i]['flags'] & SURF and sz + calc_height(self.items[i]) <= t)
            and sz < t + PERSON and sz + max(calc_height(self.items[i]), 1) > t for sz, i in sts)]

    def check(self, x, y, z):
        if not (0 <= x < 7168 and 0 <= y < 4096):
            return 'off map'
        tops, sts, why = self.surfaces(x, y)
        if not tops:
            return why or 'no surface'
        open_tops, block = [], None
        for t in tops:
            # pinned Movement's fit test: an impassable or a surface static filling part of the 16 Z above the
            # standing Z blocks (a ceiling, a platform round you), but not the floor you stand on (its top is t)
            hit = next(((sz, i) for sz, i in sts
                        if self.items[i]['flags'] & (IMP | SURF)
                        and not (self.items[i]['flags'] & SURF and sz + calc_height(self.items[i]) <= t)
                        and sz < t + PERSON and sz + max(calc_height(self.items[i]), 1) > t), None)
            if hit:
                block = block or hit
            else:
                open_tops.append(t)
        if not open_tops:
            return 'blocked by 0x%04X %s z%d' % (block[1], self.items[block[1]]['name'], block[0])
        if z is None:
            return 'ok'
        near = min(open_tops, key=lambda t: abs(t - z))
        return 'ok' if abs(near - z) <= ZTOL else 'z: stands at %d' % near


def skip(verdict):
    return verdict in ('ok', 'gone', 'area corner') or verdict.startswith('not on SoS')


def run(folder, code, files):
    land = Land(folder)
    rows = []
    for rel in files:
        path = os.path.join(code, rel)
        if not os.path.exists(path):
            rows.append((rel, 0, 'file', 0, 0, None, '(file no longer exists)', 'gone', ''))
            continue
        for (r, i, kind, x, y, z, text, facet) in literals(path, rel):
            if facet not in SOS_FACETS:
                v = 'not on SoS (%s)' % facet
            elif 'Rectangle' in text or kind == 'Rectangle' or (z is None and ('MinZ' in text or 'MaxZ' in text)):
                v = 'area corner'  # a rectangle's corner bounds an area; it is not a spot anything stands on
            else:
                v = land.check(x, y, z)
            rows.append((r, i, kind, x, y, z, text, v, facet))
    return rows


def main():
    folder, code = sys.argv[1], sys.argv[2]
    args = sys.argv[3:]
    files = [l.strip() for l in open(args[args.index('--files') + 1]) if l.strip() and not l.startswith('#')]
    out = args[args.index('--out') + 1] if '--out' in args else os.path.join(HERE, 'out-spots.csv')
    rows = run(folder, code, files)
    with open(out, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['file', 'line', 'kind', 'x', 'y', 'z', 'text', 'verdict', 'facet'])
        w.writerows(rows)
    print('literals', len(rows), 'not ok', sum(1 for r in rows if not skip(r[7])),
          'not on SoS', sum(1 for r in rows if r[7].startswith('not on SoS')))
    per = {}
    for r in rows:
        per.setdefault(r[0], [0, 0])[0] += 1
        if not skip(r[7]):
            per[r[0]][1] += 1
    for k, (n, b) in sorted(per.items()):
        print('  %4d literals %4d not ok  %s' % (n, b, k))


if __name__ == '__main__':
    main()
