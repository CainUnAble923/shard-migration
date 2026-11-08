"""cc-P845: the farmhouse and its doorstep from the built isle map, with the server's pieces drawn in: P741's render741.py
(the farm layout, the lesson signposts, the addons) plus Pip's bench and blood (TutorialFarm.PipProps), which
build_isle.server_items() does not read. Pip himself is a mobile: a red dot marks his tile when --pip is given.

    python -P render845.py <map folder> <out.jpg> x1 y1 x2 y2 [--scale S] [--cut Z] [--pip] [--bench 0x0B2D] [--walls-off]

--bench draws the bench with another piece (the before render). Set PYTHONPATH=scripts,
MAPBUILD_CLIENT=D:/UO/tool-trials/client-data-copy, MAPBUILD_ART=<art.mul folder>, SL_CODE=<code copy>."""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, 'scripts'))
sys.path.insert(0, os.path.join(REPO, 'notes', 'cc-P662-tools'))
sys.path.insert(0, os.path.join(REPO, 'notes', 'cc-P741-tools'))
from mapbuild import isorender as iso  # noqa: E402
import render741 as R  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402


def pip_props(bench=None):
    code = os.environ['SL_CODE']
    src = open(os.path.join(code, 'server', 'customizations', 'Tutorial', 'TutorialFarm.cs'), encoding='utf-8-sig').read()
    bench_id = int(re.search(r'const int BenchId = (0x[0-9A-Fa-f]+);', src).group(1), 16)
    body = re.search(r'PipProps =\s*\[(.*?)\];', src, re.S).group(1)
    out = []
    for m in re.finditer(r'\((BenchId|0x[0-9A-Fa-f]+), new Point3D\((\d+), (\d+), (-?\d+)\), "([^"]+)"\)', body):
        tid = bench_id if m.group(1) == 'BenchId' else int(m.group(1), 16)
        if bench is not None and m.group(1) == 'BenchId':
            tid = bench
        out.append((int(m.group(2)), int(m.group(3)), int(m.group(4)), tid, m.group(5)))
    pip = re.search(r'Point3D PipBench = new\((\d+), (\d+), (-?\d+)\)', src).groups()
    return out, tuple(int(v) for v in pip)


def main():
    a = sys.argv[1:]
    folder, out = a[0], a[1]
    x1, y1, x2, y2 = (int(v) for v in a[2:6])
    scale = float(a[a.index('--scale') + 1]) if '--scale' in a else 1.0
    bench = int(a[a.index('--bench') + 1], 16) if '--bench' in a else None
    sc = iso.Scene.from_map(folder, 1, x1, y1, x2, y2)
    sc.statics += R.items_on(folder, (x1, y1, x2, y2))
    props, pip = pip_props(bench)
    sc.statics += [(x, y, z, t) for (x, y, z, t, _) in props if x1 <= x <= x2 and y1 <= y <= y2]
    if '--cut' in a:
        cut = int(a[a.index('--cut') + 1])
        sc.statics = [s for s in sc.statics if s[2] < cut]
    art = iso.Art()
    if '--walls-off' in a:
        # the cut-away inside: no wall pieces standing on the floor (Z 7 and up), so the room shows from above
        sc.statics = [s for s in sc.statics if not (s[2] >= 7 and art.item_data[s[3]]['flags'] & iso.FLAG_WALL)]
    im = iso.render(sc, x1, y1, x2, y2, art=art)
    if '--pip' in a:
        px, py = iso.tile_px(im, pip[0], pip[1])
        py += 22 - pip[2] * 4
        ImageDraw.Draw(im).ellipse((px - 4, py - 4, px + 4, py + 4), outline=(255, 0, 0, 255), width=2)
    im = im.convert('RGB')
    if scale != 1.0:
        im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    im.save(out, quality=85)
    for p in props:
        print('placed', '0x%04X' % p[3], '%d,%d,%d' % p[:3], p[4])
    print(out, im.size, os.path.getsize(out))


if __name__ == '__main__':
    main()
