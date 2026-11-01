"""cc-P749: write the release's trammel.mapops: the release's own file with P741+P746+P751's isle blocks (main
34ed792 against its parent eec3bbb) taken from main. The file keeps mapops.py's order: header, F, B lines, then each
op kind (L, S+, S-) in its own run sorted by x then y. Each run is merged by (x, y); a tile's lines all come from one
side, since a tile lies in one block.
Usage: mapops_merge.py <repo> <release rev> <out trammel.mapops>
"""
import subprocess
import sys

W, REL, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
PATH = "player-package/vendor/shattered-legacy-map/trammel.mapops"


def raw(rev):
    return subprocess.run(["git", "-C", W, "show", f"{rev}:{PATH}"], capture_output=True, text=True,
                          encoding="utf-8", check=True).stdout


def split(text):
    head, ops = [], []
    for line in text.splitlines():
        if not line or line[0] == "#" or line.startswith("F ") or line.startswith("B "):
            assert not ops, "header line after ops: " + line
            head.append(line)
        else:
            ops.append(line)
    return head, ops


def blk(line):
    p = line.split()
    return (int(p[1]) >> 3) * 512 + (int(p[2]) >> 3)


def key(line):
    p = line.split()
    return (p[0], int(p[1]), int(p[2]))


def runs(ops):
    """Kinds in file order, and whether each run is sorted by (x, y)."""
    kinds = []
    for o in ops:
        k = o.split()[0]
        if not kinds or kinds[-1] != k:
            assert k not in kinds, "kind appears twice: " + k
            kinds.append(k)
    return kinds


rel_text, par_text, new_text = raw(REL), raw("34ed792^1"), raw("34ed792")
rh, rops = split(rel_text)
ph, pops = split(par_text)
nh, nops = split(new_text)
for name, ops in (("release", rops), ("parent", pops), ("main", nops)):
    ks = [key(o) for o in ops]
    print(name, "kinds", runs(ops), "sorted by (kind run, x, y):",
          all(ks[i][0] != ks[i + 1][0] or ks[i][1:] <= ks[i + 1][1:] for i in range(len(ks) - 1)))
order = runs(rops)
assert runs(nops) == order or set(runs(nops)) <= set(order), (runs(nops), order)

changed = {blk(o) for o in set(pops) ^ set(nops)}
# void on both maps: the release's lines in the changed blocks are main's parent's
assert sorted(o for o in rops if blk(o) in changed) == sorted(o for o in pops if blk(o) in changed)
keep = [o for o in rops if blk(o) not in changed]
take = [o for o in nops if blk(o) in changed]
rank = {k: i for i, k in enumerate(order)}
merged = sorted(keep + take, key=lambda o: (rank[o.split()[0]],) + key(o)[1:])
# sorted() is stable; a tile's lines all come from one source, so each keeps its file order.
out = rh + merged
open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
print("changed blocks", len(changed), "kept", len(keep), "taken", len(take), "written", len(out), "lines")
