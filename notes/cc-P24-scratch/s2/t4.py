import numpy as np
from PIL import Image
from uomap import load_radar
L=np.load('land_117.npy'); O=np.load('occ_117.npy'); E=np.load('empty_both.npy')
L4=np.load('land_114.npy'); O4=np.load('occ_114.npy')
rad=load_radar('D:/UO/UltimaOnlineVanilla/radarcol.mul')
img=rad[L]  # land color
# overlay statics: mark statics tiles grey-ish blending using top static? simple: darken
img=img.copy()
st=O>0
img[st]=(img[st]*0.5+np.array([200,200,200])*0.5).astype(np.uint8)
img[E]=[0,0,90]
diff=(L!=L4)|(O!=O4)
ys,xs=np.nonzero(diff)
print('diff bbox overall', xs.min(),xs.max(),ys.min(),ys.max())
m=(xs>=5120); print('diff bbox x>=5120', xs[m].min(),xs[m].max(),ys[m].min(),ys[m].max(), m.sum())
m2=xs<5120; print('diff west', xs[m2].min(),xs[m2].max(),ys[m2].min(),ys[m2].max(), m2.sum())
img[diff]=[255,0,255]
sub=img[:,5120:]
im=Image.fromarray(sub).resize((2048//2,4096//2),Image.NEAREST)
im.save('overview_strip_x5120.png')
Image.fromarray(img).resize((7168//4,4096//4),Image.BOX).save('overview_trammel_q.png')
