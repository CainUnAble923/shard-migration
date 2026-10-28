r"""cc-P678 read only: table statics (name has 'table', Surface) in SoS Haven, by building. python -P tables.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sosbase as B
F = B.facet()
for (x, y), l in sorted(F.st.items(), key=lambda k: (k[0][1], k[0][0])):
    for i, z in l:
        if 'table' in B.iname(i).lower() or ('counter' in B.iname(i).lower()):
            print(x, y, z, hex(i), B.iname(i), 'top', z + B.calch(i), 'surf' if B.iflags(i) & B.SURF else '-')
