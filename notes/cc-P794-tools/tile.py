r"""cc-P794: the art each ethereal uses, from the client data the package launches and TazUO's mount table. Read only."""
import re
import struct

d = open("D:/UO/tool-trials/client-data-copy/tiledata.mul", "rb").read()
land = 512 * (4 + 32 * 30)


def item(i):
    o = land + (i // 32) * (4 + 32 * 41) + 4 + (i % 32) * 41
    r = d[o:o + 41]
    return hex(struct.unpack("<Q", r[:8])[0]), struct.unpack("<H", r[14:16])[0], r[21:41].split(b"\0")[0].decode("latin-1")


src = open("D:/UO/tazuo-sl-build/src/src/ClassicUO.Client/Game/Data/Mounts.cs", encoding="utf-8").read()
for name, st, mo in [("windrunner", 0x9ED5, 0x3ECC), ("lasher", 0x9E35, 0x3ECB), ("tiger", 0x9844, 0x3EC8), ("light tiger", 0x9844, 0x3EC7),
                     ("hellhound", 0x3FFD, 0x3EC9), ("boura", 0x46F8, 0x3EC6), ("peacock", 0xA0C0, 0x3ECF)]:
    m = re.search(r"_mounts\[0x%04X\] = new\(0x([0-9A-Fa-f]+), 0x%04X, (-?\d+)" % (mo, mo), src)
    print(name, "statuette", hex(st), item(st), "| mount", hex(mo), item(mo), "| TazUO body", m and (int(m.group(1), 16), "height", m.group(2)))
