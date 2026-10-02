# cc-P27: can a player walk to a tile within LuckyCoin's target range (3, square: pinned Mobile.cs:3031,
# Target.cs Invoke) of a FountainOfFortune component at Ter Mur 1121,957,-42? Read only.
# Approximate walk model, NOT pinned's Movement code: 8-way steps between standable surfaces (fit.py's
# surfaces(), a port of Map.CanFit with height 16), stepping up at most 2 (pinned MovementImpl StepHeight)
# and down at most 20. No diagonal corner rule, no doors, no teleporters. Bounded to the Underworld region
# (regions.json: 898,808 - 1280,1231). Start: the region's GoLocation 1128,1207,-2.
import collections
exec(open('fit.py').read())
M=ns['Map'](5); DECO={}
_bc={}
_st=M.statics
def st_cached(bx,by):
    k=(bx,by)
    if k not in _bc: _bc[k]=_st(bx,by)
    return _bc[k]
M.statics=st_cached
_lc={}
_bl=M.block
def bl_cached(bx,by):
    k=(bx,by)
    if k not in _lc: _lc[k]=_bl(bx,by)
    return _lc[k]
M.block=bl_cached
X0,Y0,X1,Y1=898,808,1280,1231
SC={}
def surf(x,y):
    if (x,y) not in SC: SC[(x,y)]=surfaces(x,y) if X0<=x<X1 and Y0<=y<Y1 else []
    return SC[(x,y)]
FOOT=[(x,y) for x in range(1119,1123) for y in range(955,959)]
def inrange(x,y): return any(abs(x-fx)<=3 and abs(y-fy)<=3 for fx,fy in FOOT)
start=(1128,1207,-2)
print('start surfaces',surf(1128,1207))
seen={start}; q=collections.deque([start]); hits=set()
while q:
    x,y,z=q.popleft()
    if inrange(x,y): hits.add((x,y,z))
    for dx in (-1,0,1):
        for dy in (-1,0,1):
            if dx==dy==0: continue
            nx,ny=x+dx,y+dy
            for nz in surf(nx,ny):
                if -20<=nz-z<=2 and (nx,ny,nz) not in seen:
                    seen.add((nx,ny,nz)); q.append((nx,ny,nz))
print('reachable tiles:',len(seen))
print('reachable tiles within coin range of a component:',sorted(hits))

# Part 2: the pocket the in-range tiles belong to, and how a player gets into it (pinned teleporters.json).
import json
def flood(starts):
    seen=set(starts); q=collections.deque(starts)
    while q:
        x,y,z=q.popleft()
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                if dx==dy==0: continue
                nx,ny=x+dx,y+dy
                for nz in surf(nx,ny):
                    if -20<=nz-z<=2 and (nx,ny,nz) not in seen:
                        seen.add((nx,ny,nz)); q.append((nx,ny,nz))
    return seen
near=[(x,y,z) for x in range(1116,1126) for y in range(952,962) for z in surf(x,y) if inrange(x,y)]
print('standable tiles within coin range:',near)
pocket=flood(near)
xy={(x,y) for x,y,z in pocket}
print('pocket size:',len(pocket),'bbox',min(x for x,y in xy),min(y for x,y in xy),max(x for x,y in xy),max(y for x,y in xy))
tel=json.load(open(r'D:/UO/ModernUO-pinned/Distribution/Data/teleporters.json'))
for t in tel:
    for a,b in (('src','dst'),('dst','src')):
        if t[a]['map']=='TerMur' and (t[a]['loc'][0],t[a]['loc'][1]) in xy and (a=='dst' or t.get('back')):
            print(f'  into pocket: {t[b]["map"]} {t[b]["loc"]} -> {t[a]["loc"]} (back={t.get("back")})')
for t in tel:
    if t['src']['map']=='TerMur' and (t['src']['loc'][0],t['src']['loc'][1]) in xy:
        print(f'  out of pocket: {t["src"]["loc"]} -> {t["dst"]["map"]} {t["dst"]["loc"]}')
print('entrance pocket and fountain pocket the same:', start in pocket)

# Part 3: walk plus teleporters from the entrance, inside the Underworld box, until nothing new.
src_at={}
for t in tel:
    if t['src']['map']=='TerMur' and t['dst']['map']=='TerMur':
        src_at.setdefault(tuple(t['src']['loc'][:2]),[]).append(tuple(t['dst']['loc']))
        if t.get('back'): src_at.setdefault(tuple(t['dst']['loc'][:2]),[]).append(tuple(t['src']['loc']))
reached=set(); frontier=[start]; hops=[]
while frontier:
    new=flood([p for p in frontier if p not in reached]); reached|=new; frontier=[]
    for (x,y,z) in new:
        for d in src_at.get((x,y),[]):
            if X0<=d[0]<X1 and Y0<=d[1]<Y1:
                ds=surf(d[0],d[1]); dz=min(ds,key=lambda s:abs(s-d[2])) if ds else d[2]
                p=(d[0],d[1],dz)
                if p not in reached: frontier.append(p); hops.append(((x,y,z),p))
print('walk+teleport from entrance:',len(reached),'tiles;',len(hops),'teleporter hops')
print('fountain-side tiles reached:',[p for p in near if p in reached])

# Part 4: backwards from the fountain's pocket through teleporters until a source lies outside the box.
def pocket_of(p):
    x,y,z=p; ds=surf(x,y)
    if not ds: return None
    z=min(ds,key=lambda s:abs(s-z)); return flood([(x,y,z)])
seen_p=[]; todo=[(near[0],0,'fountain shore')]; done_xy=set()
while todo:
    p,depth,why=todo.pop(0)
    if depth>6: continue
    P=pocket_of(p)
    if P is None: print('  '*depth+f'{p}: no standable surface'); continue
    pxy={(x,y) for x,y,z in P}
    if pxy & done_xy: continue
    done_xy|=pxy
    print('  '*depth+f'pocket of {p} ({why}): {len(P)} tiles')
    for t in tel:
        for a,b,ok in (('dst','src',True),('src','dst',bool(t.get('back')))):
            if ok and t[a]['map']=='TerMur' and tuple(t[a]['loc'][:2]) in pxy:
                s=t[b]; sl=tuple(s['loc'])
                inside = s['map']=='TerMur' and X0<=sl[0]<X1 and Y0<=sl[1]<Y1
                print('  '*depth+f'  <- {s["map"]} {list(sl)} {"(inside Underworld)" if inside else "(OUTSIDE: an entry)"}')
                if inside: todo.append((sl,depth+1,f'teleporter to {t[a]["loc"]}'))

# Part 5: every pinned teleporter entering the Underworld box from outside it, and whether the walk+teleport
# closure from those entries reaches the fountain's shore.
def inbox(m,l): return m=='TerMur' and X0<=l[0]<X1 and Y0<=l[1]<Y1
entries=[]
for t in tel:
    for a,b,ok in (('src','dst',True),('dst','src',bool(t.get('back')))):
        if ok and inbox(t[b]['map'],t[b]['loc']) and not inbox(t[a]['map'],t[a]['loc']):
            entries.append((t[a]['map'],tuple(t[a]['loc']),tuple(t[b]['loc'])))
print('entries into the Underworld box:',entries)
reached=set(); frontier=[]
for _,_,d in entries:
    ds=surf(d[0],d[1])
    if ds: frontier.append((d[0],d[1],min(ds,key=lambda s:abs(s-d[2]))))
while frontier:
    new=flood([p for p in frontier if p not in reached]); reached|=new; frontier=[]
    for (x,y,z) in new:
        for d in src_at.get((x,y),[]):
            if X0<=d[0]<X1 and Y0<=d[1]<Y1:
                ds=surf(d[0],d[1])
                if ds:
                    p=(d[0],d[1],min(ds,key=lambda s:abs(s-d[2])))
                    if p not in reached: frontier.append(p)
print('closure from entries:',len(reached),'tiles; fountain shore tiles reached:',[p for p in near if p in reached])
