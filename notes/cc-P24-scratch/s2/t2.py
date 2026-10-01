from uomap import *
import numpy as np, struct
land_n, items = load_tiledata_names('D:/UO/UltimaOnlineVanilla/tiledata.mul')
for t in (0x2,0x244,0x1af,0x1db,0x3,0x64,0x1ae,0x22c,0x0): print(hex(t), land_n[t][1], hex(land_n[t][0]))
for name, d in [('117','D:/UO/UltimaOnlineVanilla'),('114','D:/ShatteredLegacy/client-data/classic-client')]:
    idx, mul = load_statics(d+'/staidx1.mul', d+'/statics1.mul')
    occ = np.zeros((H, W), np.uint16)
    lk = idx[:,0]; ln = idx[:,1]
    n=0
    for b in np.nonzero((lk>=0)&(ln>0))[0]:
        bx, by = divmod(int(b), BH)
        o=int(lk[b])
        for k in range(int(ln[b])//7):
            t,x,y,zz,hue = struct.unpack_from('<HBBbH', mul, o+k*7)
            occ[by*8+y, bx*8+x] += 1; n+=1
    np.save('occ_%s.npy'%name, occ)
    print(name, 'statics total', n)
