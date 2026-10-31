"""cc-P741: renders of the Wakening Isle from built map files, with the server's pieces drawn in (the farm layout, the
lesson props and signposts, P724's addons) read from the code copy by build_isle.server_items().

    python -P render741.py <map folder> <out.jpg> x1 y1 x2 y2 [--scale 0.5] [--no-items] [--cut Z]

Set PYTHONPATH=scripts, MAPBUILD_CLIENT=D:/UO/UltimaOnlineVanilla, SL_CODE=<code copy>."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, 'scripts'))
sys.path.insert(0, os.path.join(REPO, 'notes', 'cc-P662-tools'))
from mapbuild import isorender as iso, uofiles  # noqa: E402
import build_isle as B  # noqa: E402
from PIL import Image  # noqa: E402


def items_on(folder, rect):
    farm, props, pts, door = B.server_items()
    x1, y1, x2, y2 = rect
    mf = uofiles.MapFile(folder, 1)
    land = mf.region(x1 - 2, y1 - 2, x2 + 2, y2 + 2)
    out = []
    for (x, y, z, tid, what) in farm:
        out.append((x, y, z, tid))
    extra = getattr(B, 'EXTRA_RENDER', [])
    for (x, y, z, tid, what) in props + extra:
        if z is None:
            z = land.get((x, y), (0, 0))[1]
        out.append((x, y, z, tid))
    return [s for s in out if x1 <= s[0] <= x2 and y1 <= s[1] <= y2]


def main():
    a = sys.argv[1:]
    folder, out = a[0], a[1]
    x1, y1, x2, y2 = (int(v) for v in a[2:6])
    scale = float(a[a.index('--scale') + 1]) if '--scale' in a else 1.0
    sc = iso.Scene.from_map(folder, 1, x1, y1, x2, y2)
    if '--no-items' not in a:
        sc.statics += items_on(folder, (x1, y1, x2, y2))
    if '--cut' in a:
        # the cut-away: no statics at or above this Z (roofs, gables, the upper wall courses)
        cut = int(a[a.index('--cut') + 1])
        sc.statics = [s for s in sc.statics if s[2] < cut]
    im = iso.render(sc, x1, y1, x2, y2).convert('RGB')
    if scale != 1.0:
        im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    im.save(out, quality=85)
    print(out, im.size, os.path.getsize(out))


if __name__ == '__main__':
    main()
