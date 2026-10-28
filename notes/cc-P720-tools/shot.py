"""cc-P720: isometric renders of an isle spot, from a built map folder plus the server items the seeder places (the farm
addon from TutorialIsleFarmLayout.cs, the lesson props, the doors, the station markers), read from the code copy.

    python -P shot.py <map folder> <out.png> x1 y1 x2 y2 [--noroof] [--label text] [--layout <file.cs>]

--noroof drops statics 20 or more above the floor's land (as the client hides a roof over a player inside).
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, 'scripts'))
sys.path.insert(0, os.path.join(REPO, 'notes', 'cc-P662-tools'))
from PIL import Image, ImageDraw  # noqa: E402
from mapbuild import isorender, uofiles  # noqa: E402
import build_isle as B  # noqa: E402

CODE = os.path.join(B.SL_CODE, 'server', 'customizations', 'Tutorial')


def farm_pieces(layout):
    text = open(layout, encoding='utf-8').read()
    return [(int(x), int(y), int(z), int(t, 16)) for t, x, y, z in
            re.findall(r'\((0x[0-9A-Fa-f]+), (\d+), (\d+), (-?\d+)\), //', text)]


def extras(mf, layout):
    farm, props, pts, door = B.server_items()
    out = farm_pieces(layout)
    for (x, y, z, tid, what) in props:
        out.append((x, y, mf.get(x, y)[1], tid))
    return out, pts


def main():
    a = sys.argv[1:]
    folder, png = a[0], a[1]
    x1, y1, x2, y2 = (int(v) for v in a[2:6])
    layout = a[a.index('--layout') + 1] if '--layout' in a else os.path.join(CODE, 'TutorialIsleFarmLayout.cs')
    label = a[a.index('--label') + 1] if '--label' in a else ''
    extra_file = a[a.index('--extra') + 1] if '--extra' in a else None
    mf = uofiles.MapFile(folder, 1)
    sc = isorender.Scene.from_map(folder, 1, x1, y1, x2, y2)
    ex, pts = extras(mf, layout)
    if extra_file:
        for line in open(extra_file):
            f = line.split()
            if len(f) >= 4 and not line.startswith('#'):
                ex.append((int(f[0]), int(f[1]), int(f[2]), int(f[3], 16)))
    for (x, y, z, tid) in ex:
        if x1 - 1 <= x <= x2 + 1 and y1 - 1 <= y <= y2 + 1:
            sc.statics.append((x, y, z, tid))
    if '--noroof' in a:
        sc.statics = [s for s in sc.statics if s[2] - mf.get(s[0], s[1])[1] < 20]
    im = isorender.render(sc, x1, y1, x2, y2).convert('RGB')
    if im.width > 1600:
        im = im.resize((1600, int(im.height * 1600 / im.width)), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, im.width, 20], fill=(0, 0, 0))
    d.text((6, 4), '%s  x %d-%d, y %d-%d' % (label, x1, x2, y1, y2), fill=(255, 255, 255))
    im.save(png)
    print(png, im.size)


if __name__ == '__main__':
    main()
