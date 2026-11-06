"""python -P r.py x0 y0 x1 y1 out.jpg [hide_above|-] [scale] [label:x:y:z ...]  (P799_CLIENT picks the client)"""
import sys,os
from PIL import Image
import hallbase as H
a=sys.argv
x0,y0,x1,y1=map(int,a[1:5]); out=a[5]
hide=None if len(a)<7 or a[6]=='-' else int(a[6])
sc=float(a[7]) if len(a)>7 else 1
marks=[]
for m in a[8:]:
    l,x,y,z=m.split(':'); marks.append((l,int(x),int(y),int(z),(255,60,60,255)))
F=H.Facet(1)
tmp=out+'.png'
H.render(F,x0,y0,x1,y1,marks=marks,out=tmp,scale=sc,hide_roofs_above=hide,label='%s %d,%d-%d,%d'%(os.path.basename(H.CLIENT),x0,y0,x1,y1))
im=Image.open(tmp).convert('RGB')
q=85
while True:
    im.save(out,quality=q)
    if os.path.getsize(out)<1000000 or q<40: break
    q-=10
os.remove(tmp)
print(out,im.size,os.path.getsize(out))
