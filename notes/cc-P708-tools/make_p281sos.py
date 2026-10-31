"""cc-P708 (P677's make_p281sos.py): notes/cc-P281-tools (the guild halls' map checks and generator) copied to notes/cc-P708-tools/p281sos with its
client folder pointed at D:/UO/golems/Iron/p708-work/sosclient: the stock client files with the server's SoS overlay
(the SoS base plus our trammel.mapops) as Trammel's map files and as Felucca's, which share them on the server (P675).
So check.py's walk checks run on the land the server reads. Only the .py files and README are copied (no PNGs)."""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'cc-P281-tools')
DST = os.path.join(HERE, 'p281sos')
os.makedirs(DST, exist_ok=True)
for f in os.listdir(SRC):
    if f.endswith('.py'):
        shutil.copy(os.path.join(SRC, f), os.path.join(DST, f))
p = os.path.join(DST, 'hallbase.py')
s = open(p, encoding='utf-8').read()
a = "CLIENT = uofiles.CLIENT = 'D:/UO/tool-trials/client-data-copy'"
assert s.count(a) == 1
s = s.replace(a, "CLIENT = uofiles.CLIENT = 'D:/UO/golems/Iron/p708-work/sosclient'  # cc-P708: the SoS land with today's patch (make_p281sos.py, make_sosclient.py)")
a = """        self.mf = uofiles.MapFile(CLIENT, fi)
        self.idx, self.sta = uofiles.load_statics_index(CLIENT, fi)"""
assert s.count(a) == 1
s = s.replace(a, """        # cc-P677: the server reads Felucca from Trammel's (SoS) files (P675), so facet 0 opens facet 1's
        files = 1 if fi == 0 else fi
        self.mf = uofiles.MapFile(CLIENT, files)
        self.idx, self.sta = uofiles.load_statics_index(CLIENT, files)""")
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('copied', len([f for f in os.listdir(DST) if f.endswith('.py')]), 'files')

# cc-P708: on the SoS land the server reads our decoration (server/data/Decoration, cc-P680, in place of pinned's
# Britannia/Trammel/Felucca folders) and adds our spawners (server/data/Spawns/sos, cc-P682) to pinned's, so the
# picks and checks keep clear of the new towns' shops and garrisons too.
p = os.path.join(DST, 'hallbase.py')
s = open(p, encoding='utf-8').read()
a = "        for f in glob.glob(PINNED + '/Distribution/Data/Decoration/%s/*.cfg' % folder):"
assert s.count(a) == 1
s = s.replace(a, "        root = SL_DATA if fi in (0, 1) else PINNED + '/Distribution/Data'  # cc-P708: the SoS land's decoration\n"
                 "        for f in glob.glob(root + '/Decoration/%s/*.cfg' % folder):")
a = "        for sub in ('shared', 'post-uoml'):   # Core.SA: AdminGump.cs:4031 picks post-uoml, and shared always\n            for f in glob.glob(PINNED + '/Distribution/Data/Spawns/%s/**/*.json' % sub, recursive=True):"
assert s.count(a) == 1
s = s.replace(a, "        for sub in ('shared', 'post-uoml', 'sos'):   # Core.SA: AdminGump.cs:4031 picks post-uoml, and shared always; cc-P708: and ours, sos\n"
                 "            for f in glob.glob((SL_DATA + '/Spawns/%s/**/*.json' if sub == 'sos' else PINNED + '/Distribution/Data/Spawns/%s/**/*.json') % sub, recursive=True):")
a = "PINNED = 'D:/UO/ModernUO-pinned'"
assert s.count(a) == 1
s = s.replace(a, a + "\nSL_DATA = 'D:/UO/golems/Iron/ShatteredLegacy/server/data'  # cc-P708: our Data overlay (decoration, the SoS spawns)")
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('hallbase: SoS decoration and spawns')

# cc-P708: the walk climbs sloped land as pinned Movement.Check does: a step between two land heights is allowed when
# the higher tile's lowest land corner is within StepHeight (2) of the lower one's top (its highest corner, on land) (a road down a hillside drops
# 5 a tile; P281's step of 3 between average heights cut it, e.g. Fort Whitestone's road, notes in cc-P708).
p = os.path.join(DST, 'walk.py')
s = open(p, encoding='utf-8').read()
a = "                            if abs(nz - z) <= step and (nx, ny, nz) not in seen:"
assert s.count(a) == 1
s = s.replace(a, "                            if (abs(nz - z) <= step or self.land_step(x, y, z, nx, ny, nz)) and (nx, ny, nz) not in seen:")
a = "    def flood(self, start):"
assert s.count(a) == 1
s = s.replace(a, '''    def land_step(self, x, y, z, nx, ny, nz):
        """cc-P708: pinned Movement.Check onto land: up onto a land tile whose lowest corner is within StepHeight 2 of the start's top."""
        lo, hi = ((x, y, z), (nx, ny, nz)) if z <= nz else ((nx, ny, nz), (x, y, z))
        hx, hy, hz = hi
        lid, _ = self.F.land(hx, hy)
        if self.F.ignored_land(lid) or H.LAND[lid][0] & (H.IMP | H.WET) or hz != self.F.avgz(hx, hy):
            return False
        low = min(self.F.landz(hx, hy), self.F.landz(hx + 1, hy), self.F.landz(hx, hy + 1), self.F.landz(hx + 1, hy + 1))
        # pinned GetStartZ: standing on land, the start's top is that tile's highest corner
        lx, ly, lz = lo
        lid2, _ = self.F.land(lx, ly)
        top = lz
        if not (self.F.ignored_land(lid2) or H.LAND[lid2][0] & (H.IMP | H.WET)) and lz == self.F.avgz(lx, ly):
            top = max(self.F.landz(lx, ly), self.F.landz(lx + 1, ly), self.F.landz(lx, ly + 1), self.F.landz(lx + 1, ly + 1))
        return low <= top + 2

    def flood(self, start):''')
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('walk: land slopes as pinned climbs them')
