r"""cc-P681: add the purpose checks to regrade.py (one-off edit script, kept for the record).
    python -P edit_fit.py
"""
P = "regrade.py"
s = open(P).read()

REPS = [
    ('''NE_SNOW = (4224, 4479, 256, 767)            # P673's S14 closure, P698's drops
''', '''NE_SNOW = (4224, 4479, 256, 767)            # P673's S14 closure, P698's drops

# The author's new towns S10 peoples (P673's list), their TownRegion rectangles from his Regions.xml (reference only;
# notes/sos-author-data): a wild spawner inside one moves out (P698: civic space is S10's).
NEW_TOWNS = ("Valunstead", "Hammerhill", "Kameron Kove", "Elmhaven", "Kettleburg", "Fort Yondall", "Elandrim Nur Shaz")


def new_town_rects():
    import re
    xml = open(os.path.join(os.path.dirname(HERE), "sos-author-data", "Regions.xml"), encoding="utf-8", errors="replace").read()
    out = []
    for m in re.finditer(r'<region type="TownRegion" name="([^"]+)">(.*?)</region>', xml, re.S):
        if m.group(1) in NEW_TOWNS:
            for r in re.finditer(r'<rect x="(\\d+)" y="(\\d+)" width="(\\d+)" height="(\\d+)"', m.group(2)):
                x, y, w, h = (int(v) for v in r.groups())
                out.append((m.group(1), x, y, x + w - 1, y + h - 1))
    return out
'''),
    ('''        self.surf = sosgrid.Surfaces(name)
''', '''        self.surf = sosgrid.Surfaces(name)
        self.towns = new_town_rects()
        self.stock = {}

    def stock_grid(self, facet):
        if facet not in self.stock:
            g = sosgrid.load(facet.lower())
            self.stock[facet] = {"covered": g["covered"], "terrain": g["terrain"]}
        return self.stock[facet]

    def new_town(self, x, y):
        return next((t[0] for t in self.towns if t[1] <= x <= t[3] and t[2] <= y <= t[4]), None)

    def unfit(self, x, y, hr, kind, facet):
        """Why a home that passes the walk no longer serves its purpose on SoS, or None (P698's purpose rules)."""
        st = self.stock_grid(facet)
        if kind in CIVIC and hr <= 1 and st["covered"][x, y] and not self.cov[x, y]:
            return "its building is gone (indoors on the stock map, outdoors on SoS)"
        if kind in WILD:
            town = self.new_town(x, y)
            if town:
                return "inside the author's new town %s (S10's civic space)" % town
            want = GROUP.get(self.names[int(st["terrain"][x, y])], "other")
            have = self.group(self.terr, x, y)
            if want in HABITATS and have != want:
                return "its habitat changed (%s on the stock map, %s on SoS)" % (want, have)
        return None
'''),
    ('''GROUP = {''', '''HABITATS = {"green", "sand", "snow", "swamp", "rock", "lava"}
GROUP = {'''),
    # the search keeps wild spawners out of the new towns
    ('''            if gr.group(gr.terr, cx, cy) != want or gr.cov[cx, cy]:''',
     '''            if gr.group(gr.terr, cx, cy) != want or gr.cov[cx, cy] or gr.new_town(cx, cy):'''),
    # main: a passing home that no longer fits is searched for
    ('''        elif gr.passes(x, y, z, hr, kind == "sea life"):''',
     '''        elif gr.passes(x, y, z, hr, kind == "sea life") and not gr.unfit(x, y, hr, kind, r["facet"]):'''),
    ('''            found = search(gr, r, x, y, z, hr, kind, r["facet"])
            if found:
                nx, ny, nz, why = found
                out.update(action="move", nx=nx, ny=ny, nz=nz, reason=why)
            else:
                out.update(action="drop", reason="fails on SoS and nothing matching within %d" % (SERVICE_SEARCH if r["_role"] else SEARCH))''',
     '''            first = gr.unfit(x, y, hr, kind, r["facet"]) if gr.passes(x, y, z, hr, kind == "sea life") else "fails the walk"
            found = search(gr, r, x, y, z, hr, kind, r["facet"])
            if found:
                nx, ny, nz, why = found
                out.update(action="move", nx=nx, ny=ny, nz=nz, reason="%s; %s" % (first, why))
            else:
                out.update(action="drop", reason="%s; nothing matching within %d" % (first, SERVICE_SEARCH if r["_role"] else SEARCH))'''),
    ('''A FAILING home is searched for,''', '''A home that passes but no longer FITS its purpose is searched for too (P698's rules): a standing town NPC that was
indoors on the stock map and is outdoors on SoS (its building is gone); a wild spawner inside one of the author's seven
new towns (S10's civic space); a wild spawner whose land changed habitat (green, sand, snow, swamp, rock, lava).

A FAILING home is searched for,'''),
]
for a, b in REPS:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
open(P, "w").write(s)
print("ok")
