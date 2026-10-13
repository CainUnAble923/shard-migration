exec(open('nhmap.py').read().split("if __name__")[0])
import sys
X0,Y0,X1,Y1=map(int,sys.argv[1:5])
for bx in range(X0>>3,(X1>>3)+1):
    for by in range(Y0>>3,(Y1>>3)+1):
        for (sid,sx,sy,sz,hue) in M.statics(bx,by):
            x,y=bx*8+sx,by*8+sy
            if X0<=x<=X1 and Y0<=y<=Y1 and 'sign' in T.sname[sid].lower():
                print(x,y,sz,hex(sid),T.sname[sid])
