r"""cc-P678 part 6, offline: P289's route (a new character's start to the banker and back) and the Rootdeep way in on the
SoS files, by the playbook's walk with every blocking prop of our layouts in place (crosscheck.rows). The live run needs
the server reading SoS (S2); this is the map's side of it.
    python -P route.py > out/route.txt
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import crosscheck  # noqa: E402
import soswalk  # noqa: E402

START = (3634, 2586)
BANKER = (3620, 2617)          # the Second Bank's banker spawner (pinned uoml Vendors.json); Sarsmea Smythe 3624,2616
SARSMEA = (3624, 2616)
HATCH, LANDING = crosscheck.HATCH, crosscheck.LANDING


def main():
    f = soswalk.files()
    rows = crosscheck.rows()
    blocking = [(r[2], r[3], r[4], r[5]) for r in rows if r[1] == "prop" and r[5] is not None
                and f["items"][r[5]]["flags"] & soswalk.IMP]
    w = soswalk.Walk(crosscheck.BOX, extra=blocking + [(HATCH[0], HATCH[1], -1, 0x3E65)])
    fails = 0
    for name, a, b in (("start to the banker", START, BANKER), ("the banker back to the start", BANKER, START),
                       ("start to Sarsmea Smythe", START, SARSMEA),
                       ("start to the cellar hatch", START, HATCH), ("the ladder's landing to the start", LANDING, START),
                       ("the ladder's landing to the hatch", LANDING, HATCH)):
        p = w.path(a, b)
        if p is None:
            print("NO PATH", name)
            fails += 1
            continue
        zs = [w.stand[t] for t in p]
        print("%-36s %3d steps, Z %d..%d, via %s" % (name, len(p) - 1, min(zs), max(zs), " ".join("%d,%d" % t for t in p[::8] + [p[-1]])))
    print("the hatch stands the walker at Z %s (the floor is 0; a step of 2 is allowed)" % w.stand[HATCH])
    print("FAILURES", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
