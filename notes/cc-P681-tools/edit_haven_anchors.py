r"""cc-P681: a failing town spawner in the author's Haven town (either facet) goes to the shop of its trade, where pinned's
pre-UOML Haven data puts that trade (uoml/trammel/Vendors.json, S7's source), before any nearest-building search.
    python -P edit_haven_anchors.py
"""
P = "regrade.py"
s = open(P).read()

REPS = [
    ('''def ring(x, y, d):''', '''_anchors = None


def haven_anchors():
    """{entry name (lower case): (x, y, z)} of pinned's pre-UOML Haven spawners inside the town (S7's shops)."""
    global _anchors
    if _anchors is None:
        _anchors = {}
        for s in json.load(open(os.path.join(PINNED, "Spawns", "uoml", "trammel", "Vendors.json"))):
            x, y, z = s["location"]
            if in_box(x, y, HAVEN_TOWN):
                for e in s["entries"]:
                    _anchors.setdefault(e["name"].lower(), (x, y, z))
    return _anchors


def ring(x, y, d):'''),
    ('''def search(gr, r, x, y, z, hr, kind, facet):
    sea = kind == "sea life"''', '''def search(gr, r, x, y, z, hr, kind, facet):
    sea = kind == "sea life"
    if kind in CIVIC and in_box(x, y, HAVEN_TOWN):
        # the author's Haven is pre-UOML Haven rebuilt: the shop of the trade, as pinned's pre-UOML data places it
        for name in (e.split(":")[0].strip().lower() for e in r["entries"].split("|")):
            a = haven_anchors().get(name)
            if a:
                for d in range(0, 4):
                    for (cx, cy) in ([(a[0], a[1])] if d == 0 else ring(a[0], a[1], d)):
                        f = gr.floor(cx, cy, a[2])
                        if f is not None and gr.passes(cx, cy, f, hr, False):
                            return cx, cy, f, "town: the Haven shop of its trade (pinned's pre-UOML %s, %d,%d)" % (name, a[0], a[1])'''),
]
for a, b in REPS:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
open(P, "w").write(s)
print("ok")
