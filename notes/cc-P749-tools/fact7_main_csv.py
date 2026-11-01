"""cc-P749: map fact 7 (the isle is the build and nothing else) on the release's patch, read against main's builder
CSVs (notes/cc-P662-tools at origin/main): this docs branch predates P751, so its own CSVs are older.
Usage: fact7_main_csv.py <docs repo> <release trammel.mapops>
"""
import collections
import csv
import io
import subprocess
import sys

DOCS, SHIPPED = sys.argv[1], sys.argv[2]
ISLE = (6594, 3905, 6865, 4049)  # replaced by the value in main's test_mapops.py below


def show(path):
    return subprocess.run(["git", "-C", DOCS, "show", "origin/main:" + path], capture_output=True, text=True,
                          encoding="utf-8", check=True).stdout


src = show("tools/tests/test_mapops.py")
ns = {}
for line in src.splitlines():
    if line.startswith("ISLE ="):
        exec(line, ns)
ISLE = ns.get("ISLE", ISLE)


def inside(x, y, box):
    return box[0] <= x <= box[2] and box[1] <= y <= box[3]


lines = open(SHIPPED, encoding="utf-8").read().splitlines()
isle = [l.split() for l in lines if l.split() and l.split()[0] in ("L", "S+", "S-")
        and inside(int(l.split()[1]), int(l.split()[2]), ISLE)]
land = [f for f in isle if f[0] == "L"]
ok = True


def check(name, cond):
    global ok
    ok = ok and cond
    print(("ok  " if cond else "FAIL"), name)


print("ISLE box", ISLE)
check("every cell of the drawn area", (ISLE[2] - ISLE[0] + 1) * (ISLE[3] - ISLE[1] + 1) == len(land))
check("one land line per cell", len(land) == len({(f[1], f[2]) for f in land}))
want = {(int(r["land_id_hex"], 16), int(r["z"])): int(r["tiles"])
        for r in csv.DictReader(io.StringIO(show("notes/cc-P662-tools/land-summary.csv")))}
check("land counts are main's land-summary.csv", want == dict(collections.Counter((int(f[3]), int(f[4])) for f in land)))
placed = sorted("S+ %s %s %s %d 0" % (r["x"], r["y"], r["z"], int(r["id_hex"], 16))
                for r in csv.DictReader(io.StringIO(show("notes/cc-P662-tools/statics-placed.csv"))))
check("statics are main's statics-placed.csv", placed == sorted(" ".join(f) for f in isle if f[0] == "S+"))
check("no removals on the isle", [] == [f for f in isle if f[0] == "S-"])
gate = [f for f in land if (f[1], f[2]) == ("6832", "3991")]
check("the moongate stands on land", int(gate[0][3]) not in (0x00A8, 0x00A9, 0x00AA, 0x00AB))
check("nothing placed on the moongate", [] == [f for f in isle if f[0] == "S+" and (f[1], f[2]) == ("6832", "3991")])
print("ALL OK" if ok else "FAILED")
