import sys,os,io,base64,json
sys.path.insert(0,os.path.dirname(__file__))
from vd import load,frames
from PIL import Image
HIGH={0:'walk',1:'idle',2:'die',3:'die 2',4:'attack',5:'attack 2',6:'attack 3',7:'bow',8:'crossbow',9:'throw',10:'hit',11:'pillage',12:'stomp',13:'cast',14:'cast 2',15:'block R',16:'block L',17:'fidget',18:'fidget 2',19:'fly',20:'land',21:'die in flight'}  # cc-P139: 12 stomp was missing, so 12-21 were one off
LOW={0:'walk',1:'run',2:'idle',3:'eat',4:'alert',5:'attack',6:'attack 2',7:'hit',8:'die',9:'idle 2',10:'fidget',11:'lie down',12:'die 2'}
def anim(fr,scale):
    if not fr: return None
    L=min(-cx for cx,cy,i in fr); T=min(-cy-i.height for cx,cy,i in fr)
    R=max(-cx+i.width for cx,cy,i in fr); B=max(-cy for cx,cy,i in fr)
    W,H=R-L,B-T; ims=[]
    for cx,cy,i in fr:
        c=Image.new('RGBA',(W,H),(0,0,0,0)); c.paste(i,(-cx-L,-cy-i.height-T),i)
        if scale!=1: c=c.resize((W*scale,H*scale),Image.NEAREST)
        ims.append(c)
    return ims
def gif(ims,dur):
    bg=(43,40,36)
    pal=[]
    for im in ims:
        b=Image.new('RGB',im.size,bg); b.paste(im,(0,0),im); pal.append(b)
    buf=io.BytesIO()
    pal[0].save(buf,'GIF',save_all=True,append_images=pal[1:],duration=dur,loop=0,optimize=True)
    return base64.b64encode(buf.getvalue()).decode()
def do(path):
    d,at,idx=load(path); names=HIGH if at==0 else LOW
    have=[]
    for a in range(len(idx)//5):
        if any(frames(d,idx[a*5+k]) for k in (0,)): have.append(names.get(a,str(a)))
    out={'type':'monster (H)' if at==0 else 'animal (L)','actions':have}
    for key,a in (('walk',0),('attack',4 if at==0 else 5),('die',2 if at==0 else 8)):
        fr=[]
        for dirn in (2,1,3,0,4):
            fr=frames(d,idx[a*5+dirn])
            if fr: break
        ims=anim(fr,1)
        if ims:
            sc=2 if max(ims[0].size)<90 else 1
            ims=anim(fr,sc); out[key]=gif(ims,110); out[key+'_n']=len(fr)
    return out
if __name__=='__main__':
    print(json.dumps({k:(v if not isinstance(v,str) or len(v)<80 else len(v)) for k,v in do(sys.argv[1]).items()}))
