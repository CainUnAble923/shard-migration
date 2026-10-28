"""cc-P677: notes/cc-P281-tools (the guild halls' map checks and generator) copied to notes/cc-P677-tools/p281sos with its
client folder pointed at D:/UO/golems/Iron/p677-work/sosclient: the stock client files with the server's SoS overlay
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
s = s.replace(a, "CLIENT = uofiles.CLIENT = 'D:/UO/golems/Iron/p677-work/sosclient'  # cc-P677: the SoS land (make_p281sos.py)")
a = """        self.mf = uofiles.MapFile(CLIENT, fi)
        self.idx, self.sta = uofiles.load_statics_index(CLIENT, fi)"""
assert s.count(a) == 1
s = s.replace(a, """        # cc-P677: the server reads Felucca from Trammel's (SoS) files (P675), so facet 0 opens facet 1's
        files = 1 if fi == 0 else fi
        self.mf = uofiles.MapFile(CLIENT, files)
        self.idx, self.sta = uofiles.load_statics_index(CLIENT, files)""")
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('copied', len([f for f in os.listdir(DST) if f.endswith('.py')]), 'files')
