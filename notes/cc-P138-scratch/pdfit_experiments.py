# scratch: paperdoll refit experiments
from PIL import Image
import sys
R=r'D:\ShatteredLegacy\player-package\vendor'
K=R+r'\paperdoll-sos\ExternalImages\gumps'
B=R+r'\paperdoll-sos\bodies-sfw'
G=Image.open(R+r'\shattered-legacy-art\gumps\64783.png').convert('RGBA')
def comps(im):
    a=im.split()[3]; w,h=im.size; px={(x,y) for y in range(h) for x in range(w) if a.getpixel((x,y))}; seen=set(); out=[]
    for p in sorted(px):
        if p in seen: continue
        st=[p]; seen.add(p); c=[]
        while st:
            x,y=st.pop(); c.append((x,y))
            for n in ((x+1,y),(x-1,y),(x,y+1),(x,y-1),(x+1,y+1),(x-1,y-1),(x+1,y-1),(x-1,y+1)):
                if n in px and n not in seen: seen.add(n); st.append(n)
        out.append(c)
    return sorted(out,key=len,reverse=True)
cs=comps(G)
tail=cs[0]; ears=cs[1]; stray=cs[2:]
print('stray',stray)
def crop(pts):
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]; bb=(min(xs),min(ys),max(xs)+1,max(ys)+1)
    im=Image.new('RGBA',(bb[2]-bb[0],bb[3]-bb[1]),(0,0,0,0))
    for x,y in pts: im.putpixel((x-bb[0],y-bb[1]),G.getpixel((x,y)))
    return im,bb
EARS,EBB=crop(ears); TAIL,TBB=crop(tail)
print('ears bbox',EBB,'tail bbox',TBB)
# tail root: rightmost columns
for x in range(TBB[2]-6,TBB[2]):
    ys=[y for (px,y) in tail if px==x]; print(' tail col',x,'rows',min(ys),max(ys),len(ys))
def make(ears_d, tail_d, out):
    im=Image.new('RGBA',(260,237),(0,0,0,0))
    im.alpha_composite(EARS,(EBB[0]+ears_d[0],EBB[1]+ears_d[1]))
    im.alpha_composite(TAIL,(TBB[0]+tail_d[0],TBB[1]+tail_d[1]))
    im.save(out); return im
def composite(body, gump, hair=None, robe=None, bg=(0,0,0,255)):
    im=Image.new('RGBA',(260,237),bg)
    im.alpha_composite(Image.open(B+'\%s.png'%body).convert('RGBA'))
    if robe: im.alpha_composite(Image.open(K+'\%d.png'%robe).convert('RGBA'))
    elif hair: im.alpha_composite(Image.open(K+'\%d.png'%hair).convert('RGBA'))
    im.alpha_composite(gump)
    return im
def sheet(panels, out, scale=2):
    w=sum(p.width for p in panels)+10*(len(panels)-1); h=max(p.height for p in panels)
    s=Image.new('RGBA',(w,h),(60,60,60,255)); x=0
    for p in panels: s.paste(p,(x,0)); x+=p.width+10
    s=s.resize((s.width*scale,s.height*scale),Image.NEAREST); s.save(out)
if __name__=='__main__':
    S=r'C:/Users/ckfle/AppData/Local/Temp/claude/D--UO-shard-migration/976284ec-7e8e-4683-b039-62f2e1f12c26/scratchpad/p138'
    ed=(int(sys.argv[1]),int(sys.argv[2])); td=(int(sys.argv[3]),int(sys.argv[4])); tag=sys.argv[5]
    g=make(ed,td,S+'/cand_%s.png'%tag)
    if tag.startswith('F'):
        sheet([composite('13',g,hair=60701),composite('13',g,robe=60987),composite('15',g,hair=60701),composite('13',G,hair=60701)],S+'/sheet_%s.png'%tag)
    else:
        sheet([composite('12',g,hair=50701),composite('12',g,robe=50987),composite('14',g,hair=50701),composite('12',G,hair=50701)],S+'/sheet_%s.png'%tag)
