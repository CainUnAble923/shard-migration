"""cc-P362: the stock gumps and art a skin stands in for: present in the client, and their sizes.
    python -P probe_stock.py [client folder]"""
import importlib.util, struct, sys
spec = importlib.util.spec_from_file_location('ffa', r'D:\UO\golems\Iron\ShatteredLegacy\scripts\find-free-art.py')
ffa = importlib.util.module_from_spec(spec); spec.loader.exec_module(ffa)
data = sys.argv[1] if len(sys.argv) > 1 else r'D:\UO\UltimaOnlineVanilla'
g = ffa.Uop(data + r'\gumpartLegacyMUL.uop')
for gid in [0x3C, 0x3D, 0x44, 0x49, 0x4A, 0x50, 9810, 9811, 50422, 60422, 0x775E, 0x775F, 0x7760, 0x7761, 0x7762, 0x7763, 0x777B, 0x777C, 0x777D]:
    d = g.get('build/gumpartlegacymul/%08d.tga' % gid)
    print('gump %5d 0x%04X: %s' % (gid, gid, 'absent' if d is None else '%dx%d' % struct.unpack('<ii', d[:8])))
