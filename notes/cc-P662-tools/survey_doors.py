"""cc-P662: what OSI's map holds at a door in a stone building (wall set 0x001A-0x001D), and what it puts on the
roof. Doors are server items (ModernUO's Decoration cfg); this reads their spots from the Britannia cfgs, then the
Trammel statics on the door tile and on its neighbours along the wall line.

    python -P survey_doors.py <client folder> <decoration folder>
"""
import collections, glob, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), 'scripts'))
from mapbuild import uofiles  # noqa: E402

STONE = {0x001A, 0x001B, 0x001C, 0x001D, 0x0080, 0x0081, 0x0082}


def doors(deco):
    out = []
    for path in glob.glob(os.path.join(deco, 'Britannia', '*.cfg')):
        typ = None
        for line in open(path, encoding='utf-8', errors='replace'):
            line = line.strip()
            m = re.match(r'(\w*Door\w*) (0x[0-9A-Fa-f]+)(?: \((.*)\))?', line)
            if m:
                typ = (m.group(1), m.group(3) or '')
                continue
            if not line or line.startswith('#'):
                if not line:
                    typ = None
                continue
            if typ and re.match(r'-?\d+ -?\d+ -?\d+$', line):
                x, y, z = (int(v) for v in line.split())
                out.append((typ, x, y, z))
            elif not re.match(r'-?\d+ ', line):
                typ = None
    return out


def main():
    folder, deco = sys.argv[1], sys.argv[2]
    items = uofiles.read_tiledata(folder)[1]
    ds = doors(deco)
    print('doors read', len(ds))
    at_door = collections.Counter()
    beside = collections.Counter()
    above = collections.Counter()
    facing = collections.Counter()
    n = 0
    examples = []
    for (typ, x, y, z) in ds:
        st = uofiles.statics_in(folder, 1, x - 1, y - 1, x + 1, y + 1)
        near = [s for s in st if s[3] in STONE and abs(s[2] - z) <= 2]
        if not near:
            continue
        n += 1
        facing[typ[1]] += 1
        here = [s for s in st if s[0] == x and s[1] == y]
        for s in here:
            if s[2] <= z + 1:
                at_door[(s[3], items[s[3]]['name'], s[2] - z)] += 1
            else:
                above[(s[3], items[s[3]]['name'], s[2] - z)] += 1
        for s in st:
            if (s[0], s[1]) != (x, y) and (s[0] == x or s[1] == y) and abs(s[2] - z) <= 2:
                beside[(s[3], items[s[3]]['name'])] += 1
        if len(examples) < 6:
            examples.append((typ, x, y, z))
    print('doors beside a 0x001A-0x001D wall:', n, dict(facing))
    print('on the door tile at floor level:', [('0x%04X' % t, nm, dz, c) for (t, nm, dz), c in at_door.most_common(12)])
    print('on the door tile above it:', [('0x%04X' % t, nm, dz, c) for (t, nm, dz), c in above.most_common(12)])
    print('on its orthogonal neighbours:', [('0x%04X' % t, nm, c) for (t, nm), c in beside.most_common(16)])
    print('examples:', examples)


if __name__ == '__main__':
    main()
