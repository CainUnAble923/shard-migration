"""cc-P725: renders stretches of the isle's coast from a built map folder (isorender, the client's layout).
    python -P shore_shots.py <map folder> <out folder> <prefix> [name=x1,y1,x2,y2 ...] [--scale f]"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'scripts'))
from mapbuild import isorender as R, uofiles as U

STRETCHES = {'wake': (6624, 3976, 6658, 4006), 'nw': (6670, 3940, 6704, 3974), 'north': (6712, 3926, 6746, 3960),
             'sw': (6650, 3994, 6684, 4022), 'south': (6700, 3994, 6734, 4022), 'east': (6800, 3964, 6836, 3998)}
folder, outdir, prefix = sys.argv[1:4]
args = sys.argv[4:]
scale = 1.0
if '--scale' in args:
    scale = float(args[args.index('--scale') + 1]); args = args[:args.index('--scale')]
pick = dict((a.split('=')[0], tuple(int(v) for v in a.split('=')[1].split(','))) for a in args if '=' in a) or STRETCHES
art = R.Art()
os.makedirs(outdir, exist_ok=True)
for name, (x1, y1, x2, y2) in pick.items():
    mf = U.MapFile(folder, 1)
    land = mf.region(x1 - 1, y1 - 1, x2 + 2, y2 + 2)
    st = [(x, y, z, t) for (x, y, z, t) in U.statics_in(folder, 1, x1, y1, x2, y2)]
    im = R.render(R.Scene(land, st), x1, y1, x2, y2, art=art)
    if scale != 1.0:
        im = im.resize((int(im.width * scale), int(im.height * scale)))
    out = os.path.join(outdir, '%s-%s.jpg' % (prefix, name))
    im.convert('RGB').save(out, quality=85)
    print(out, im.size)
