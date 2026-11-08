"""cc-P838 (P828 review item 1, guide 11.2): the iron fence pieces 0x0821, 0x0822 and 0x0823 drawn beside the cell gate
0x0828 in an east-west row, one row each, on flat stock land near the jail, to read which piece closes an east-west line.

    python -u -P -W ignore notes/cc-P838-tools/bar_test838.py out.jpg
"""
import os
import sys

DOCS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(DOCS, 'notes', 'cc-P708-tools', 'p281sos'))
import hallbase as H

H.CLIENT = H.uofiles.CLIENT = 'D:/UO/tool-trials/client-data-copy'
F = H.Facet(1)
ox, oy, fz = 3469, 2597, 11
extra = []
for row, bar in enumerate((0x0821, 0x0822, 0x0823)):
    y = oy + 2 + row * 3
    for x in range(1, 8):
        extra.append((0x0519, ox + x, y, fz))
        extra.append((0x0828 if x == 4 else bar, ox + x, y, fz))
print(row, H.render(F, ox - 2, oy - 2, ox + 10, oy + 12, extra=extra, grid=0, out=sys.argv[1]))
