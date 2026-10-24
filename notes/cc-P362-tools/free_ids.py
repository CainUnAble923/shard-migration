"""cc-P362: free gump and art ID runs for the skins (scripts\find-free-art.py's rules, on the shard's client data).
    python -P free_ids.py GUMPS ART"""
import argparse, importlib.util, sys
spec = importlib.util.spec_from_file_location('ffa', r'D:\UO\golems\Iron\ShatteredLegacy\scripts\find-free-art.py')
ffa = importlib.util.module_from_spec(spec); spec.loader.exec_module(ffa)
ng, na = int(sys.argv[1]), int(sys.argv[2])
a = argparse.Namespace(data=r'D:\UO\UltimaOnlineVanilla', pinned=ffa.DEFAULT_PINNED, registry=ffa.REGISTRY,
                       tazuo=r'D:\UO\cc-p40-work\tazuo-3212623f\src', placeholder=False, lo=0x400, hi=0xFFFF)
w = ffa.World(a)
def gump_runs(lo, hi, n, top=5):
    out, start = [], None
    for g in range(lo, hi):
        if not w.gump_reasons(g):
            start = g if start is None else start
            if g - start + 1 == n:
                out.append(start); start = None
                if len(out) >= top: break
        else:
            start = None
    return out
for lo in (22470, 23000, 40000):
    print('gump runs of %d from %d: %s' % (ng, lo, gump_runs(lo, 0x10000, ng)))
print('art runs of %d:' % na, w.runs(na, 0x400, 0x3FFF, False)[:8] if hasattr(w, 'runs') else ffa.runs(w, na, 0x400, 0x3FFF, False)[:8])
