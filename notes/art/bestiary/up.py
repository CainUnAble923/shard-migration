import numpy as np
from PIL import Image
def scale2x(im):
    a=np.array(im.convert('RGBA')).astype(np.int32)
    h,w,_=a.shape
    P=np.pad(a,((1,1),(1,1),(0,0)),mode='edge')
    E=P[1:-1,1:-1];B=P[:-2,1:-1];H=P[2:,1:-1];D=P[1:-1,:-2];F=P[1:-1,2:]
    eq=lambda x,y:(x==y).all(-1)
    c=~eq(B,H)&~eq(D,F)
    e0=np.where((c&eq(D,B))[...,None],D,E); e1=np.where((c&eq(B,F))[...,None],F,E)
    e2=np.where((c&eq(D,H))[...,None],D,E); e3=np.where((c&eq(H,F))[...,None],F,E)
    o=np.zeros((h*2,w*2,4),np.int32); o[0::2,0::2]=e0;o[0::2,1::2]=e1;o[1::2,0::2]=e2;o[1::2,1::2]=e3
    return Image.fromarray(o.astype(np.uint8),'RGBA')
def up(im,f):
    if f==1: return im
    big=scale2x(im)
    if f>2: big=scale2x(big)
    W,H=int(round(im.width*f)),int(round(im.height*f))
    return big.resize((W,H),Image.BOX)
