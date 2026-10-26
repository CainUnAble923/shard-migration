r"""cc-P670 part 1: vendor Zigholtul's redrawn statics into the player package, only those that fit.

Reads the download as data (never runs anything from it), fit.py's verdicts (out\fit.csv, run on the download), and
copies each PNG whose verdict is ok, byte for byte, to player-package\vendor\zigholtul-redrawn-statics\art\<id>.png.
Writes manifest.csv beside it: every file in the download with its verdict, the reason, and for the shipped ones
the SHA-256 (the package gate checks the zip against it).
    python -P vendor.py "<download folder>"
"""
import csv
import hashlib
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fit  # noqa: E402

REASON = {
    "ok": "ships",
    "shifted": "left out: does not stand where the stock art does (fit.py: bottom or base off by more than its kind allows)",
    "water": "left out: water statics draw another blue than stock water land, a patchwork of squares",
    "partial set": "left out: a tree set the pack covers only in part (a redrawn trunk with a stock crown looks crooked)",
    "no stock": "left out: the stock client has no art for this ID",
    "ours": "left out: one of our own art IDs or a UI skin's",
    "animated": "left out: not every frame of its animation is redrawn",
}


def main():
    src = sys.argv[1]
    dest_root = os.path.dirname(fit.VENDOR)
    if os.path.isdir(fit.VENDOR):
        shutil.rmtree(fit.VENDOR)
    os.makedirs(fit.VENDOR)
    verdicts = {int(r["id"]): r for r in csv.DictReader(open(os.path.join(fit.OUT, "fit.csv")))}
    rows, shipped, total = [], 0, 0
    for name in sorted(os.listdir(src), key=lambda n: (len(n), n)):
        if not name.lower().endswith(".png"):
            continue
        m = re.fullmatch(r"(\d+)\.png", name)
        if not m:
            rows.append([name, "", "not an ID", "left out: not named by a plain decimal art ID (TazUO itself would not "
                         "load it; an alternate drawing beside its numbered file)", ""])
            continue
        tid = int(m.group(1))
        r = verdicts[tid]
        sha = ""
        if r["verdict"] == "ok":
            data = open(os.path.join(src, name), "rb").read()
            sha = hashlib.sha256(data).hexdigest()
            open(os.path.join(fit.VENDOR, name), "wb").write(data)
            shipped += 1
            total += len(data)
        rows.append([name, tid, r["verdict"], REASON[r["verdict"]] + ("" if not r["set"] else " (tree set %s)" % r["set"]), sha])
    with open(os.path.join(dest_root, "manifest.csv"), "w", newline="\n", encoding="ascii") as f:
        f.write("# cc-P670: every file of Zigholtul's UO Art Static Replacements for TazUO 2.0, and what became of it.\n")
        f.write("# Written by shard-migration notes/cc-P670-tools/vendor.py from fit.py's verdicts; never edited by hand.\n")
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["file", "itemId", "verdict", "reason", "sha256"])
        w.writerows(rows)
    print(len(rows), "files listed;", shipped, "shipped,", total, "bytes")


if __name__ == "__main__":
    main()
