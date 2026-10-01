from uomap import *
import numpy as np, collections
for name, d in [('117','D:/UO/UltimaOnlineVanilla'),('114','D:/ShatteredLegacy/client-data/classic-client')]:
    tid, z = load_land(d+'/map1LegacyMUL.uop')
    np.save('land_%s.npy'%name, tid); np.save('z_%s.npy'%name, z)
    print(name, tid.shape)
    c = collections.Counter(tid[:, 5120:].ravel().tolist())
    print(' dungeon strip top land ids', [(hex(k),v) for k,v in c.most_common(8)])
    print(' newhaven sample', hex(tid[2600,3500]))
