"""cc-P844 (P741's render741.py, for P834's list): isorenders of the isle's farm gate and stop area, and of the clothes and
chat stops, from built map files, with main's server pieces drawn in. build_isle.server_items() reads the farm layout
and the lesson signposts; this adds what it does not read (the clothes table, the chat signpost, Pip's bench and
blood, the field gate and its fence piece) and swaps the layout's old gate sign arm for the isle's standing post, as
TutorialFarm.IsleArt does.

    python -P render844.py <map folder> <out.jpg> x1 y1 x2 y2 [--scale 0.5] [--cut Z]

Set PYTHONPATH=scripts, MAPBUILD_CLIENT, MAPBUILD_ART, SL_CODE=<code copy>."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, 'scripts'))
sys.path.insert(0, os.path.join(REPO, 'notes', 'cc-P662-tools'))
from mapbuild import isorender as iso, uofiles  # noqa: E402
import build_isle as B  # noqa: E402
from PIL import Image  # noqa: E402

GATE_ART = int(os.environ.get('P844_GATE_ART', '0x0843'), 16)  # LightWoodGate NorthCCW, shut (checked live: notes)

# main's pieces build_isle.server_items() does not read (TutorialCorePlacement.cs, TutorialFarm.cs on main 4ec6962)
EXTRA = [
    (6664, 3990, None, 0x0B8F, 'clothes table (Rack -1,-2)'),
    (6690, 3986, None, 0xA854, 'chat signpost (Signpost -2,-4)'),
    (6704, 3975, 7, 0x0B2C, 'Pip bench'),  # cc-P844: was 0x0B2D
    (6704, 3976, 7, 0x0B2C, 'Pip bench'),
    (6703, 3975, 7, 0x122A, 'blood'),
    (6703, 3976, 7, 0x122D, 'blood'),
    (6703, 3974, 7, 0x122C, 'blood'),
    (6695, 3978, None, 0x0837, 'field fence piece'),
    (6695, 3979, None, GATE_ART, 'field gate'),
]


def items_on(folder, rect):
    farm, props, pts, door = B.server_items()
    x1, y1, x2, y2 = rect
    mf = uofiles.MapFile(folder, 1)
    land = mf.region(x1 - 2, y1 - 2, x2 + 2, y2 + 2)
    out = []
    for (x, y, z, tid, what) in farm:
        if tid == 0x0BCF:          # the old board: the isle drops it (IsleArt)
            continue
        if tid == 0x0B97:          # the old wall arm: the isle's standing post instead
            tid = 0xA854
        out.append((x, y, z, tid))
    for (x, y, z, tid, what) in props + getattr(B, 'EXTRA_RENDER', []) + EXTRA:
        if z is None:
            z = land.get((x, y), (0, 0))[1]
        out.append((x, y, z, tid))
    seen, uniq = set(), []
    for s in out:
        if s not in seen:
            seen.add(s)
            uniq.append(s)
    return [s for s in uniq if x1 <= s[0] <= x2 and y1 <= s[1] <= y2]


def main():
    a = sys.argv[1:]
    folder, out = a[0], a[1]
    x1, y1, x2, y2 = (int(v) for v in a[2:6])
    scale = float(a[a.index('--scale') + 1]) if '--scale' in a else 1.0
    sc = iso.Scene.from_map(folder, 1, x1, y1, x2, y2)
    sc.statics += items_on(folder, (x1, y1, x2, y2))
    if '--cut' in a:
        cut = int(a[a.index('--cut') + 1])
        sc.statics = [s for s in sc.statics if s[2] < cut]
    im = iso.render(sc, x1, y1, x2, y2).convert('RGB')
    if scale != 1.0:
        im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    im.save(out, quality=85)
    print(out, im.size, os.path.getsize(out))


if __name__ == '__main__':
    main()
