"""cc-P436 step 2: free runs of gump IDs for look B's frame (scripts\\find-free-art.py's gump rules, on the shard's
client data), and the reasons for any ID asked about.
    python -P free_ids.py 9                 runs of 9 from a few starting points
    python -P free_ids.py 9 23200           the first run of 9 at or after 23200
"""
import argparse
import importlib.util
import sys

spec = importlib.util.spec_from_file_location("ffa", r"D:\UO\golems\Iron\ShatteredLegacy\scripts\find-free-art.py")
ffa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ffa)

n = int(sys.argv[1])
starts = [int(sys.argv[2])] if len(sys.argv) > 2 else [22470, 23081, 23200, 40000]
a = argparse.Namespace(data=r"D:\UO\UltimaOnlineVanilla", pinned=ffa.DEFAULT_PINNED, registry=ffa.REGISTRY,
                       tazuo=r"D:\UO\cc-p40-work\tazuo-3212623f\src", placeholder=False, lo=0x400, hi=0xFFFF)
w = ffa.World(a)


def first_run(lo, n):
    start = None
    for g in range(lo, 0x10000):
        if not w.gump_reasons(g):
            start = g if start is None else start
            if g - start + 1 == n:
                return start
        else:
            start = None
    return None


for lo in starts:
    s = first_run(lo, n)
    print("first free run of %d at or after %d: %s" % (n, lo, "%d-%d" % (s, s + n - 1) if s is not None else "none"))
    if s is not None:
        for g in range(s, s + n):
            assert not w.gump_reasons(g), g
