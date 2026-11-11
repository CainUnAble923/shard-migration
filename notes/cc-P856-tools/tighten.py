"""cc-P856: one-off. Adds the render review's two checks to find856.py (main) and rel/findrel.py (release): no static
with any height on a tile a piece covers (a garden bench under the snow globe), and nothing impassable anywhere in the
piece's bounding box (a fir between the train's cars)."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
for path, facet, base_mod in ((os.path.join(HERE, "find856.py"), "R.F", "B"), (os.path.join(HERE, "rel", "findrel.py"), "F", "B")):
    s = open(path, encoding="utf-8").read()
    old = """        if not verbose and errs:
            return None, errs
    if indoor:"""
    new = """        for sid, sz in %(F)s.statics(x, y):   # cc-P856 render review: nothing standing on a covered tile
            if %(B)s.iheight(sid) > 0 and sz >= base - 2:
                errs.append("%%d,%%d has 0x%%04X %%s at z%%d" %% (x, y, sid, %(B)s.iname(sid), sz))
        if not verbose and errs:
            return None, errs
    # cc-P856 render review: nothing impassable in the bounding box, gaps included
    xs, ys = [dx for dx, _ in tiles], [dy for _, dy in tiles]
    for x in range(ox + min(xs), ox + max(xs) + 1):
        for y in range(oy + min(ys), oy + max(ys) + 1):
            for sid, sz in %(F)s.statics(x, y):
                if %(B)s.iflags(sid) & %(B)s.IMP and sz + %(B)s.iheight(sid) > base and sz < base + 16:
                    errs.append("%%d,%%d in the box: 0x%%04X %%s" %% (x, y, sid, %(B)s.iname(sid)))
                    break
    if not verbose and errs:
        return None, errs
    if indoor:""" % {"F": facet, "B": base_mod}
    assert s.count(old) == 1, path
    s = s.replace(old, new)
    open(path, "w", encoding="utf-8", newline="\n").write(s)
    print("tightened", path)
