"""cc-P675: an overlay folder against the re-base's edited map (SoS + the new patch): land byte for byte, statics block
by block, and Valunstead's open ground.   python -P overlay_check.py <overlay> <edited>"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scripts'))
from mapbuild import mapops, uofiles
o, e = sys.argv[1], sys.argv[2]
land_equal, bad = mapops.compare(o, e, 1)
print('overlay', o)
print('  land identical to SoS + patch:', land_equal, '; statics blocks differing:', len(bad))
print('  504,384:', '%04X@%d' % uofiles.MapFile(o, 1).get(504, 384), ' 6638,3993:', '%04X@%d' % uofiles.MapFile(o, 1).get(6638, 3993))
