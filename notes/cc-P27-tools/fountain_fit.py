# cc-P27: does every component of FountainOfFortune fit at Ter Mur 1121,957,-42? Read only.
# Run from notes/cc-P15-tools. Reuses P15's port of pinned Map.CanFit (fit.py), switched to map 5 (Ter Mur,
# 1280x4096, files map5LegacyMUL.uop / staidx5.mul / statics5.mul per pinned TileMatrix.cs:102,121,133 and
# map-definitions.json index 5). Pinned ships no Ter Mur decoration, so DECO is emptied.
# The check is pinned BaseAddon.CouldFit (UOContent/Items/Addons/BaseAddon.cs:148-180): per component,
# map.CanFit(x, y, z, ItemData.Height, checkBlocksFit=false, checkMobiles=true, requireSurface=c.Z==0).
import sys
exec(open('fit.py').read())
M=ns['Map'](5); DECO={}
def canfit_h(x,y,z,h,req):
    # fit.py's canfit with an explicit height and requireSurface flag (pinned Map.cs:925-1010)
    has=False; lid,_=M.land(x,y); low,avg=avgz(x,y); lf=T.lflags.get(lid&0x3FFF,0)
    if lf&IMP and avg>z and z+h>low: return False,'impassable land'
    if not lf&IMP and z==avg and not ignored(lid): has=True
    for (sid,sx,sy,sz,hue) in M.statics(x>>3,y>>3):
        if (x&7,y&7)!=(sx,sy): continue
        f=T.sflags[sid]; s=bool(f&SURF); i=bool(f&IMP)
        if (s or i) and sz+calch(sid)>z and z+h>sz: return False,f'static 0x{sid:X} {T.sname[sid]} z{sz}'
        if s and not i and z==sz+calch(sid): has=True
    if req and not has: return False,'no surface'
    return True,'ok'+('' if has else ' (no surface)')
# FountainOfFortune() component list, in constructor order (FountainOfFortune.cs:33-60)
ids=list(range(0x1731,0x1740))+[0x1741]
offs=[(-2,1),(-1,1),(0,1),(1,1),(1,0),(1,-1),(1,-2),(0,-2),(0,-1),(0,0),(-1,0),(-2,0),(-2,-1),(-1,-1),(-1,-2),(-2,-2)]
assert len(ids)==len(offs)==16
def check(X,Y,Z,verbose=True):
    ok=True
    for sid,(dx,dy) in zip(ids,offs):
        x,y=X+dx,Y+dy
        r_req=canfit_h(x,y,Z,T.sheight[sid],True); r_no=canfit_h(x,y,Z,T.sheight[sid],False)
        ok=ok and r_req[0]
        if verbose:
            land=M.land(x,y); low,avg=avgz(x,y)
            st=[(f'0x{s:X}',T.sname[s],z,T.sheight[s],hex(T.sflags[s])) for (s,sx,sy,z,h) in M.statics(x>>3,y>>3) if (x&7,y&7)==(sx,sy)]
            print(f'  0x{sid:X} {T.sname[sid]!r:22} h{T.sheight[sid]:<2} at {x},{y},{Z}: requireSurface={r_req} noSurface={r_no} land=0x{land[0]:X} z{land[1]} avg{avg} statics={st}')
    return ok
if __name__=='__main__':
    X,Y,Z=(int(a) for a in sys.argv[1:4]) if len(sys.argv)>3 else (1121,957,-42)
    print(f'Ter Mur {X},{Y},{Z}')
    print('ALL FIT' if check(X,Y,Z) else 'DOES NOT FIT')
    print('surfaces 5x5 around (x,y: standable z):')
    for y in range(Y-3,Y+3):
        print(y,' '.join(f"{x}:{'/'.join(str(z) for z in surfaces(x,y)) or '-':>4}" for x in range(X-3,X+3)))
