"""cc-P680: render a piece of Trammel on the SoS land with a decoration set placed, as the client lays it out.

    python -P render_deco.py <overlay> <decoration root> x1 y1 x2 y2 out.png [zmax]

The decoration root holds Britannia/ and Trammel/ cfgs (our server/data/Decoration, or pinned's for the "before").
Each entry is drawn as its header's art id at its x, y, z (an addon shows only its first piece), over the map's land
and statics (scripts/mapbuild/isorender.py). zmax leaves out everything above it, map and decoration alike, as the
client hides the roof and upper floors when you stand inside.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(DOCS, 'scripts'))
sys.path.insert(0, os.path.join(DOCS, 'tools', 'tests'))
from mapbuild import isorender  # noqa: E402
import test_s5_decoration as fact  # noqa: E402


def main():
    overlay, root = sys.argv[1], sys.argv[2]
    x1, y1, x2, y2 = (int(v) for v in sys.argv[3:7])
    out = sys.argv[7]
    zmax = int(sys.argv[8]) if len(sys.argv) > 8 else 999
    sc = isorender.Scene.from_map(overlay, 1, x1, y1, x2, y2)
    sc.statics = [s for s in sc.statics if s[2] <= zmax]
    n = 0
    for folder, _, header, x, y, z, _ in fact.read(root):
        if folder == 'Felucca' or not (x1 <= x <= x2 and y1 <= y <= y2) or z > zmax:
            continue
        m = re.match(r'^\S+\s+(0x[0-9A-Fa-f]+|\d+)', header)
        if m:
            sc.statics.append((x, y, z, int(m.group(1), 0)))
            n += 1
    print(out, n, 'entries', isorender.save(isorender.render(sc, x1, y1, x2, y2), out))


if __name__ == '__main__':
    main()
