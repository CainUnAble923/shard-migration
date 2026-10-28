r"""cc-P681: ML New Haven's four outlying vendors move into the author's town by their hall's new home (P678), instead
of being dropped (the prompt's "or a new spot in the town"; and SpawnerImportVerification's count of
post-uoml/trammel/Vendors.json, which P678 also rewrites, stays as it is).
    python -P edit_outlying.py
"""
P = "regrade.py"
s = open(P).read()

REPS = [
    ('''        elif (r["facet"] == "Trammel" and r["source"] == "Spawns/post-uoml/trammel/Vendors.json"
              and in_box(x, y, HAVEN_ISLAND) and not in_box(x, y, HAVEN_TOWN)
              and stock_pass.get(r["facet"] + "/" + r["guid"], True)):
            out.update(action="drop", reason="ML New Haven's outlying hall or camp, forest or rock on SoS; S7 (P678) moved "
                                             "the guilds into the author's town, S8 owns the mine camp")''',
     '''        elif (r["facet"] == "Trammel" and r["source"] == "Spawns/post-uoml/trammel/Vendors.json"
              and in_box(x, y, HAVEN_ISLAND) and not in_box(x, y, HAVEN_TOWN)
              and stock_pass.get(r["facet"] + "/" + r["guid"], True)):
            found = outlying(gr, r, hr)
            if found:
                nx, ny, nz, why = found
                out.update(action="move", nx=nx, ny=ny, nz=nz, reason="ML New Haven's outlying hall, forest or rock on SoS; " + why)
            else:
                out.update(action="drop", reason="ML New Haven's outlying hall, forest or rock on SoS; no floor by its hall's new home")'''),
    ('''def ring(x, y, d):''', '''# ML New Haven's outlying vendors (post-uoml/trammel/Vendors.json, by the halls S7 moved into the author's town): the
# entry, and the hall's new home in P678's homes table (p678-homes.csv, copied from golem/Iron/P678) or the stock shop
OUTLYING = {
    "holymage": ("Haven Magery School", (3647, 2472)),
    "evilwanderinghealer": ("the east house (Keepers of the Last Door)", (3732, 2636)),
    "actor": ("the Bardic Guild in Haven", (3667, 2537)),
    "miner": ("the Mystic Mines of Haven", (3754, 2703)),
}


def p678_tiles():
    with open(os.path.join(HERE, "p678-homes.csv")) as f:
        return {(int(r["x"]), int(r["y"])) for r in csv.DictReader(f)}


def outlying(gr, r, hr):
    names = [e.strip().lower() for e in r["entries"].split("|")]
    hit = next((OUTLYING[n] for n in names if n in OUTLYING), None)
    if not hit:
        return None
    hall, (ax, ay) = hit
    taken = p678_tiles() | {tuple(a[:2]) for a in haven_anchors().values()}
    for d in range(0, 7):
        for (cx, cy) in ([(ax, ay)] if d == 0 else ring(ax, ay, d)):
            s = int(gr.stand[cx, cy])
            if s == NONE or (cx, cy) in taken or not gr.cov[cx, cy]:
                continue
            f = gr.floor(cx, cy, s)
            if f is not None and gr.passes(cx, cy, f, hr, False):
                return cx, cy, f, "into the author's town by its hall's new home, %s (P678)" % hall
    return None


def ring(x, y, d):'''),
]
for a, b in REPS:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
open(P, "w").write(s)
print("ok")
