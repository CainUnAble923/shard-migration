import struct, sys
from PIL import Image
NACT={0:22,1:13,2:35}
def load(path):
    d=open(path,'rb').read()
    ft,at=struct.unpack_from('<hh',d,0)
    n=NACT[at]*5
    idx=[struct.unpack_from('<iii',d,4+i*12) for i in range(n)]
    return d,at,idx
def frames(d,entry):
    look,length,extra=entry
    if look<0 or length<=0 or look+length>len(d): return []
    p=look
    pal=struct.unpack_from('<256H',d,p); p+=512
    start=p
    cnt=struct.unpack_from('<i',d,p)[0]
    if cnt<=0 or cnt>200: return []
    offs=struct.unpack_from('<%di'%cnt,d,p+4)
    out=[]
    for o in offs:
        q=start+o
        cx,cy,w,h=struct.unpack_from('<hhHH',d,q); q+=8
        if w==0 or h==0 or w>1024 or h>1024: continue
        img=Image.new('RGBA',(w,h),(0,0,0,0)); px=img.load()
        xb=cx-0x200; yb=cy+h-0x200
        while True:
            hd=struct.unpack_from('<I',d,q)[0]; q+=4
            if hd==0x7FFF7FFF: break
            hd^=(0x200<<22)|(0x200<<12)
            x=((hd>>22)&0x3FF)+xb; y=((hd>>12)&0x3FF)+yb; ln=hd&0xFFF
            for k in range(ln):
                c=pal[d[q+k]]
                r=((c>>10)&31)*255//31; g=((c>>5)&31)*255//31; b=(c&31)*255//31
                if 0<=x+k<w and 0<=y<h: px[x+k,y]=(r,g,b,255)
            q+=ln
        out.append((cx,cy,img))
    return out
