"""cc-P720: tiledata item search: python -P tdfind.py <regex> [lo hi]"""
import os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'scripts'))
from mapbuild import uofiles
td = uofiles.read_tiledata(uofiles.CLIENT)[1]
lo = int(sys.argv[2], 16) if len(sys.argv) > 2 else 0
hi = int(sys.argv[3], 16) if len(sys.argv) > 3 else 0x4000
for i in range(lo, min(hi, len(td))):
    d = td[i]
    if d['name'] and re.search(sys.argv[1], d['name'], re.I):
        print('0x%04X %-28s h%-3d flags %x' % (i, d['name'], d['height'], d['flags']))
