"""cc-P856: one-off, narrowing clearance.py after its first run: trees and pier posts beside a piece read fine in the
shots, so the camera check counts only buildings (a static with the Wall or Roof flag) on the 3 tiles south or east of
the outline, and the ring check is dropped."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
for path in (os.path.join(HERE, "find856.py"), os.path.join(HERE, "rel", "findrel.py")):
    s = open(path, encoding="utf-8").read()
    old = "                    if south_or_east and x <= x2 + 3 and y <= y2 + 3 and top >= base + 10 and sz <= base + 20:"
    new = ("                    building = B.iflags(sid) & (B.WALL | B.ROOF)\n"
           "                    if building and south_or_east and x <= x2 + 3 and y <= y2 + 3 and top >= base + 10 and sz <= base + 20:")
    assert s.count(old) == 1, path
    s = s.replace(old, new)
    old = "                    if ring and B.iflags(sid) & B.IMP and top > base and sz < base + 16:"
    assert s.count(old) == 1, path
    s = s.replace(old, "                    if False and ring:   # dropped (clearance2.py): trees and pier posts beside a piece read fine")
    open(path, "w", encoding="utf-8", newline="\n").write(s)
    print("edited", path)
