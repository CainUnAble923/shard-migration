"""cc-P749: plan the release's trammel.mapops for P741+P746+P751 (main 34ed792, parent eec3bbb) on the stock land.
For every block the isle round changed, check it is void on both maps (same fingerprint on the release and on main,
and the release's lines equal main's parent's). Then write the release's file with exactly those blocks taken from
34ed792, every other block, fingerprint and header the release's own.
The file it writes keeps each block's lines together, which reorders mapops.py's x,y order: it was used only for
the checks it prints; mapops_merge.py wrote the shipped file.
Usage: mapops_plan.py <repo> <release rev> <out trammel.mapops>
"""
import subprocess
import sys
from collections import defaultdict

W, REL, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
PATH = "player-package/vendor/shattered-legacy-map/trammel.mapops"


def raw(rev):
    return subprocess.run(["git", "-C", W, "show", f"{rev}:{PATH}"], capture_output=True, text=True,
                          encoding="utf-8", check=True).stdout


def parse(text):
    blocks = defaultdict(list)
    fp = {}
    head = []
    order = []
    for line in text.splitlines():
        if not line or line.startswith("#") or line.startswith("F "):
            head.append(line)
            order.append(("h", line))
            continue
        p = line.split()
        if p[0] == "B":
            fp[int(p[1])] = p[2]
            order.append(("B", int(p[1])))
            continue
        b = (int(p[1]) >> 3) * 512 + (int(p[2]) >> 3)
        blocks[b].append(line)
        order.append(("L", b))
    return head, blocks, fp, order


rel_text = raw(REL)
stock = parse(rel_text)
par = parse(raw("34ed792^1"))
new = parse(raw("34ed792"))

changed = {b for b in set(par[1]) | set(new[1]) if par[1].get(b) != new[1].get(b)}
xs = sorted(((b // 512) * 8) for b in changed)
ys = sorted(((b % 512) * 8) for b in changed)
fp_diff = [b for b in changed if stock[2].get(b) != new[2].get(b)]
par_diff = [b for b in changed if stock[1].get(b, []) != par[1].get(b, [])]
fp_changed = [b for b in set(par[2]) | set(new[2]) if par[2].get(b) != new[2].get(b)]
print("isle blocks changed by P741+P746+P751:", len(changed), "x", xs[0], "-", xs[-1] + 7, "y", ys[0], "-", ys[-1] + 7)
print("fingerprints differing stock vs main on those blocks:", len(fp_diff), sorted(fp_diff)[:10])
print("blocks where the release's lines differ from main's parent:", len(par_diff), sorted(par_diff)[:10])
print("fingerprints the round itself changed:", len(fp_changed))
print("header same on main before/after:", par[0] == new[0])

# Write: walk the release file's own line order; replace changed blocks' lines with 34ed792's lines, in 34ed792's
# order, emitted where the block first appears (or appended in 34ed792's order if the release had none).
out_lines = []
emitted = set()
src_lines = rel_text.splitlines()
# group line order per block in new
for line in src_lines:
    if not line or line.startswith("#") or line.startswith("F "):
        out_lines.append(line)
        continue
    p = line.split()
    if p[0] == "B":
        out_lines.append(line)
        continue
    b = (int(p[1]) >> 3) * 512 + (int(p[2]) >> 3)
    if b in changed:
        if b not in emitted:
            out_lines.extend(new[1].get(b, []))
            emitted.add(b)
        continue
    out_lines.append(line)
missing = [b for b in changed if b not in emitted and new[1].get(b)]
print("changed blocks absent from the release file (appended at end):", len(missing))
for b in sorted(missing):
    out_lines.extend(new[1][b])
open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(out_lines) + ("\n" if rel_text.endswith("\n") else ""))
print("written", OUT, len(out_lines), "lines")
