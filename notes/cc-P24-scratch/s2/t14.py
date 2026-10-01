from render import *
import json
pts=json.load(open('island_points.json'))
def col(k):
    if k.startswith('deco'): return (0,255,255)
    if k.startswith('spawn'): return (255,60,60)
    if k=='tele': return (255,255,255)
    return (255,0,255)
def rr(x0,y0,x1,y1,name,sc=8,lab=False):
    marks=[(x,y,col(k),(k.split(':')[0][:14] if lab else '')) for k,x,y in pts if x0<=x<x1 and y0<=y<y1]
    render(x0,y0,x1,y1,name,scale=sc,marks=marks,grid=5)
rr(3600,2590,3660,2650,'ruin_secondbank_mapmaker.png',sc=10)
rr(3650,2580,3690,2660,'ruin_eastblock.png',sc=10)
rr(3400,2470,3560,2660,'newhaven_points.png',sc=5)
