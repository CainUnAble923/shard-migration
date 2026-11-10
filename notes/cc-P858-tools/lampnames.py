# cc-P858: the client's tiledata name, flags and light number of every lamp art ID the downloads name.
import os, sys
sys.path.insert(0, r"D:\UO\golems\Iron\shard-migration\scripts")
os.environ.setdefault("MAPBUILD_CLIENT", r"D:\UO\tool-trials\client-data-copy")
from mapbuild import uofiles as U
_, items = U.read_tiledata(os.environ["MAPBUILD_CLIENT"])
ids = list(range(0x4C40, 0x4C5A)) + [0x4CDE, 0x4CDF, 0x4CE0, 0x4CE1, 0x4CE2, 0x4CE3, 0x04C1, 0x194D, 0x194E, 0x49C1, 0x49C2] \
    + list(range(0x983A, 0x9840)) + list(range(0x4691, 0x4699)) + list(range(0x9931, 0x9953))
for i in ids:
    t = items[i]
    print("0x%04X %-22s h=%-3d q(light)=%-3d %s" % (i, t["name"], t["height"], t["quality"], U.flagstr(t["flags"])))
