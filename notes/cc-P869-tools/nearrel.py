"""cc-P869: release origins that fit every rule but the keep-clear one, fewest keep-clear hits first."""
import sys
sys.path.insert(0, r"D:\UO\golems\Iron\shard-migration\notes\cc-P856-tools\rel")
import findrel as F
key = sys.argv[1]; x1, y1, x2, y2 = (int(v) for v in sys.argv[2:6])
taken = F.taken_tiles(); out = []
for ox in range(x1, x2 + 1):
    for oy in range(y1, y2 + 1):
        ok, errs = F.fits(key, ox, oy, False, taken, verbose=True)
        if ok is None and errs and all(e.startswith(("tree within", "winter row within")) for e in errs):
            out.append((len(errs), ox, oy, F.W.stand.get((ox, oy)), errs))
out.sort()
for n, ox, oy, z, errs in out[:int(sys.argv[6]) if len(sys.argv) > 6 else 10]:
    print(n, "%d,%d,%s" % (ox, oy, z), "; ".join(errs))
