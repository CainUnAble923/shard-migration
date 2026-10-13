# Walkability of the Alembic hall with the cc-P77 decor: the pinned CanFit port (fit.py) with the layout added as
# decoration, then a breadth-first walk at z35 from both doors. A step needs the target to fit at the floor z.
exec(open('fit.py').read())
exec(open('layout.py').read())
for (i,n,x,y,z) in LAYOUT: DECO.setdefault((x,y),[]).append((i,z))
X0,Y0,X1,Y1=3455,2561,3467,2572
fits={(x,y) for x in range(X0,X1+1) for y in range(Y0,Y1+1) if 35 in surfaces(x,y)}
gx,gy=GM[1],GM[2]
print('GM tile fits at z35:', canfit(gx,gy,35,why=True))
doors=[(3465,2567),(3457,2567)]
seen=set(); q=[d for d in doors if d in fits]; seen.update(q)
while q:
    x,y=q.pop()
    for dx in (-1,0,1):
        for dy in (-1,0,1):
            n=(x+dx,y+dy)
            if n in fits and n not in seen: seen.add(n); q.append(n)
print('doors in fit set:', [d for d in doors if d in fits])
for dx in (-1,0,1):
    for dy in (-1,0,1):
        n=(gx+dx,gy+dy); print(n, 'reachable' if n in seen else ('fits, cut off' if n in fits else 'blocked: '+str(canfit(n[0],n[1],35,why=True)[1])))
for y in range(Y0,Y1+1):
    print(y,''.join('G' if (x,y)==(gx,gy) else ('o' if (x,y) in seen else ('x' if (x,y) in fits else '.')) for x in range(X0,X1+1)))
print('   x',X0,'..',X1)
for (i,n,x,y,z) in LAYOUT: print(f'{n:18} {x},{y},{z} 0x{i:04X} under it fits at 35: {(x,y) in fits}')
