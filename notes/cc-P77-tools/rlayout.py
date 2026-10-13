import sys
exec(open('rend.py').read())
exec(open('layout.py').read())
zmax=int(sys.argv[1]) if len(sys.argv)>1 else 60
ZMAX[0]=zmax
x0,y0,x1,y1=3454,2560,3467,2573
deco=[(sid,x,y,z) for (x,y),v in DECO.items() for (sid,z) in v if x0<=x<=x1 and y0<=y<=y1 and z<zmax]
deco+=[(i,x,y,z) for (i,n,x,y,z) in LAYOUT]
marks=[(GM[0],GM[1],GM[2],GM[3],(80,255,80,255)),('Sadrah',3462,2567,35,(255,80,80,255)),('spawn',3461,2566,35,(255,80,80,255))]
print(RNS['render'](1,x0,y0,x1,y1,extra=deco,marks=marks,grid=100,out=f'layout_z{zmax}.png',scale=2))
