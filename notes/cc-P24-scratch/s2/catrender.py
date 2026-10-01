from render import *
import json, numpy as np
from PIL import Image, ImageDraw
land_n, items = load_tiledata_names(D+'/tiledata.mul')
pts=json.load(open('island_points.json'))
def cat(t):
    n=items[t][1].lower(); fl=items[t][0]
    if 'ruined' in n or n in ('debris','stone ruins') or n.startswith('broken'): return 'ruin'
    if 'door' in n: return 'door'
    if 'roof' in n or 'shingle' in n: return 'roof'
    if fl & 0x10: return 'wall'   # Wall flag
    if fl & 0x200 and ('floor' in n or 'board' in n or 'plank' in n or 'tile' in n or 'flagstone' in n or 'marble' in n or 'carpet' in n or 'cobble' in n): return 'floor'
    if 'tree' in n or 'leaves' in n or 'needles' in n: return 'tree'
    if fl & 0x40: return 'block'
    return 'other'
COL={'ruin':(220,40,40),'door':(40,220,40),'wall':(150,150,150),'floor':(200,170,110),'roof':(110,60,30),'tree':(20,90,20),'block':(90,90,160),'other':(160,140,80)}
PRI=['ruin','door','wall','block','tree','floor','other']
def crender(x0,y0,x1,y1,out,sc=10,show_pts=True,boxes=()):
    w,h=x1-x0,y1-y0
    rad=load_radar(D+'/radarcol.mul')
    img=(rad[L[y0:y1,x0:x1]]*0.6).astype(np.uint8)
    best=np.full((h,w),99); roof=np.zeros((h,w),bool)
    for (x,y,t,z,hu) in area_statics(idx,mul,x0,y0,x1,y1):
        c=cat(t)
        if c=='roof': roof[y-y0,x-x0]=True; continue
        p=PRI.index(c)
        if p<best[y-y0,x-x0]: best[y-y0,x-x0]=p
    for i,c in enumerate(PRI):
        img[best==i]=COL[c]
    im=Image.fromarray(img).resize((w*sc,h*sc),Image.NEAREST); dr=ImageDraw.Draw(im)
    for yy,xx in zip(*np.nonzero(roof)):
        dr.line([(xx*sc,yy*sc),(xx*sc+sc-1,yy*sc+sc-1)],fill=(110,60,30))
    for gx in range(x0 - x0%5 + 5, x1, 5):
        dr.line([((gx-x0)*sc,0),((gx-x0)*sc,h*sc)],fill=(60,60,60)); dr.text(((gx-x0)*sc+1,1),str(gx),fill=(255,255,255))
    for gy in range(y0 - y0%5 + 5, y1, 5):
        dr.line([(0,(gy-y0)*sc),(w*sc,(gy-y0)*sc)],fill=(60,60,60)); dr.text((1,(gy-y0)*sc+1),str(gy),fill=(255,255,255))
    if show_pts:
        for k,x,y in pts:
            if x0<=x<x1 and y0<=y<y1:
                cc=(0,255,255) if k.startswith('deco') else (255,60,255) if not k.startswith('spawn') and k!='tele' else (255,255,0)
                dr.rectangle([(x-x0)*sc+2,(y-y0)*sc+2,(x-x0)*sc+sc-3,(y-y0)*sc+sc-3],outline=cc,width=2)
    for (a,b,c,d,colr,lab) in boxes:
        dr.rectangle([(a-x0)*sc,(b-y0)*sc,(c-x0+1)*sc-1,(d-y0+1)*sc-1],outline=colr,width=3)
        dr.text(((a-x0)*sc+3,(b-y0)*sc+3),lab,fill=colr)
    # legend
    for i,c in enumerate(PRI+['roof']):
        dr.rectangle([4,h*sc-14*(i+1),14,h*sc-14*(i+1)+10],fill=COL[c]); dr.text((18,h*sc-14*(i+1)),c,fill=(255,255,255))
    im.save(out)
