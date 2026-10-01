import numpy as np, struct, json
from PIL import Image, ImageDraw
from uomap import *
D='D:/UO/UltimaOnlineVanilla'
L=np.load('land_117.npy'); Zl=np.load('z_117.npy')
rad=load_radar(D+'/radarcol.mul')
idx,mul=load_statics(D+'/staidx1.mul',D+'/statics1.mul')
tram=json.load(open('tram_regions.json'))
def top_statics(x0,y0,x1,y1):
    top=-np.ones((y1-y0,x1-x0),np.int32); tz=np.full((y1-y0,x1-x0),-200)
    for (x,y,t,z,h) in area_statics(idx,mul,x0,y0,x1,y1):
        if z>=tz[y-y0,x-x0]: tz[y-y0,x-x0]=z; top[y-y0,x-x0]=t
    return top
def render(x0,y0,x1,y1,out,scale=2,boxes=(),marks=(),grid=None, regions=True):
    x0=max(0,x0);y0=max(0,y0);x1=min(7168,x1);y1=min(4096,y1)
    img=rad[L[y0:y1,x0:x1]].copy()
    top=top_statics(x0,y0,x1,y1)
    m=top>=0
    img[m]=rad[0x4000+top[m]]
    im=Image.fromarray(img).resize(((x1-x0)*scale,(y1-y0)*scale),Image.NEAREST)
    dr=ImageDraw.Draw(im)
    if regions:
        for n,t,a,b,c,d in tram:
            if c<x0 or a>x1 or d<y0 or b>y1: continue
            dr.rectangle([(a-x0)*scale,(b-y0)*scale,(c-x0+1)*scale-1,(d-y0+1)*scale-1],outline=(255,255,0))
            dr.text(((max(a,x0)-x0)*scale+2,(max(b,y0)-y0)*scale+2),n[:24],fill=(255,255,0))
    for (a,b,c,d,col,lab) in boxes:
        dr.rectangle([(a-x0)*scale,(b-y0)*scale,(c-x0+1)*scale-1,(d-y0+1)*scale-1],outline=col,width=2)
        if lab: dr.text(((a-x0)*scale+3,(b-y0)*scale+12),lab,fill=col)
    for (x,y,col,lab) in marks:
        cx,cy=(x-x0)*scale,(y-y0)*scale
        dr.ellipse([cx-4,cy-4,cx+4,cy+4],outline=col,width=2)
        if lab: dr.text((cx+6,cy-6),lab,fill=col)
    if grid:
        for gx in range((x0//grid+1)*grid,x1,grid):
            dr.line([((gx-x0)*scale,0),((gx-x0)*scale,6)],fill=(255,255,255)); dr.text(((gx-x0)*scale+1,7),str(gx),fill=(255,255,255))
        for gy in range((y0//grid+1)*grid,y1,grid):
            dr.line([(0,(gy-y0)*scale),(6,(gy-y0)*scale)],fill=(255,255,255)); dr.text((8,(gy-y0)*scale-5),str(gy),fill=(255,255,255))
    im.save(out)
