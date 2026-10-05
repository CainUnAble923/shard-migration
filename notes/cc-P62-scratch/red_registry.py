# P62 red run for find-free-art.py --check-registry: break each registered kind in a doctored client-data copy
# (D:\UO\cc-p62-work\red-data: hard links, except tiledata.mul and Bodyconv.def, which are copies).
#   art 15420     EA gives the slot a tiledata flag
#   anim 4783     an EA item (0x1087) names it as its animId, and Bodyconv.def names it
#   gump 64783    a shipped ExternalImages\gumps PNG (planted by the caller in Fiddle-Me-This's folder)
import struct
p = r'D:\UO\cc-p62-work\red-data\tiledata.mul'
d = bytearray(open(p, 'rb').read())
L = 512 * (4 + 32 * 30)
off = lambda i: L + (i // 32) * (4 + 32 * 41) + 4 + (i % 32) * 41
d[off(0x3C3C)] = 0x02
struct.pack_into('<H', d, off(0x1087) + 14, 4783)
open(p, 'wb').write(d)
with open(r'D:\UO\cc-p62-work\red-data\Bodyconv.def', 'a') as f:
    f.write('\n4783\t-1\t-1\t-1\t-1\t9\n')
print('doctored')
