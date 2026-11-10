"""cc-P856: one-off, after the first TazUO shots. Two more checks in both finders:
  - camera: nothing tall (a static reaching 10 or more above the base: walls, roofs, trees, posts) on the 3 tiles south
    or east of the piece's outline, where the client draws it over the piece (the hall's roof hid main's snowman bench,
    a building's roof main's snow globe; the guide's "a tall wall hides the tile west or north of it");
  - room: nothing impassable on the ring of tiles round the outline (release's snowman bench stood against an ankh,
    lamp posts and a fence)."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
for path, F in ((os.path.join(HERE, "find856.py"), "R.F"), (os.path.join(HERE, "rel", "findrel.py"), "F")):
    s = open(path, encoding="utf-8").read()
    old = """    if not verbose and errs:
        return None, errs
    if indoor:"""
    new = """    if not verbose and errs:
        return None, errs
    # cc-P856 after the first shots: camera and room (clearance.py)
    x1, x2, y1, y2 = ox + min(xs), ox + max(xs), oy + min(ys), oy + max(ys)
    if not indoor:
        for x in range(x1 - 1, x2 + 4):
            for y in range(y1 - 1, y2 + 4):
                south_or_east = x > x2 or y > y2
                ring = x in (x1 - 1, x2 + 1) or y in (y1 - 1, y2 + 1)
                if not (south_or_east or ring):
                    continue
                for sid, sz in %(F)s.statics(x, y):
                    top = sz + B.iheight(sid)
                    if south_or_east and x <= x2 + 3 and y <= y2 + 3 and top >= base + 10 and sz <= base + 20:
                        errs.append("camera: %%d,%%d has 0x%%04X %%s (top z%%d) south or east of the piece" %% (x, y, sid, B.iname(sid), top))
                        break
                    if ring and B.iflags(sid) & B.IMP and top > base and sz < base + 16:
                        errs.append("room: %%d,%%d has 0x%%04X %%s against the piece" %% (x, y, sid, B.iname(sid)))
                        break
    if not verbose and errs:
        return None, errs
    if indoor:""" % {"F": F}
    assert s.count(old) == 1, path
    s = s.replace(old, new)
    open(path, "w", encoding="utf-8", newline="\n").write(s)
    print("edited", path)
