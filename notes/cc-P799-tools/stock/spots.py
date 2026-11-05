"""cc-P799: checks every chosen stock spot. Standable = reached by the BFS over the Movement.cs port at that exact Z, before and
after the pieces we would add (signs, release plaza and camp pieces). Also prints the route through the south gate."""
import json, os, re
import move, hallbase as H
A = dict(
 theater_player=(3414,2602,55), theater_echoA=(3410,2603,60), theater_echoB=(3411,2604,60),
 stables_arrival=(3534,2577,7), sick_stall=(3534,2575,7), stable_bucket=(3535,2575,7),
 mine_arm=(3512,2747,-1),
 yard_player=(3529,2544,20), yard_echo=(3531,2541,20),
 mage_player=(3486,2501,52), mage_target=(3484,2497,52), mage_demo=(3488,2500,52),
 rook=(3502,2530,22), bench2=(3503,2530,22), gate_exit=(3502,2532,22),
 house_stop1=(3465,2596,13), house_stop2=(3474,2603,10),
)
MINE = [(3512,2746,-1),(3513,2746,-1),(3513,2747,0),(3514,2747,0),(3515,2747,1),(3516,2747,1),(3517,2747,1),(3512,2748,1),(3513,2748,1),(3514,2748,2),(3515,2748,2),(3517,2748,2)]
SIGNS = dict(stable_sign=(3521,2573), mine_sign=(3477,2617), house_sign1=(3464,2596), house_sign2=(3474,2601))
SIGNZ = {}
W = move.World(); W.bfs(); F = W.F
ML=[(220,231),(236,247),(268,279),(286,297),(321,324),(467,474),(476,487),(492,495),(543,579),(581,621),(1741,1757),(1771,1790),(1801,1824),(1831,1854),(1861,1884),(1981,2004),(2028,2033),(2100,2105)]
ml = lambda i: any(a<=i<=b for a,b in ML)
def row(n,x,y,z,steps2):
    lid=F.land(x,y)
    return '%-16s %d,%d,%d steps %s after-pieces %s land 0x%04X %s z%d avg%d roof %s | %s' % (n,x,y,z,W.steps(x,y,z),steps2,lid[0],H.lname(lid[0]),lid[1],F.avgz(x,y),F.roof_over(x,y,z),F.describe(x,y)[:70])
# second BFS, with the pieces in
W2 = move.World(); 
for n,(x,y) in SIGNS.items():
    z = F.avgz(x,y); SIGNZ[n]=z; W2.add_item(x,y,z,0xA854)
BLOCK=0x0B24
for x in range(3495,3499):
    for y in range(2581,2585): W2.add_item(x,y,14,BLOCK)    # fountain 3497,2583 -2..+1
for t in [(3512,2574,14),(3506,2581,14),(3501,2575,14),(3502,2573,14),(3508,2746,0),(3510,2746,0)]:
    W2.add_item(t[0],t[1],t[2],BLOCK)
W2.bfs(tag='stock-pieces')
print('== spots')
for n,(x,y,z) in A.items(): print(row(n,x,y,z,W2.steps(x,y,z)))
print('== mining tiles (all in ore bank', {(x//8,y//8) for x,y,z in MINE}, ')')
for (x,y,z) in MINE:
    rock=[(x+a,y+b,hex(F.land(x+a,y+b)[0])) for a in(-1,0,1) for b in(-1,0,1) if (a or b) and ml(F.land(x+a,y+b)[0])]
    print(row('mine',x,y,z,W2.steps(x,y,z)),'rock',rock[:4])
print('== signs (tile must be walkable ground before; blocked after)')
for n,(x,y) in SIGNS.items():
    z=SIGNZ[n]; doors=sorted(W.doors,key=lambda d:max(abs(d[0]-x),abs(d[1]-y)))[0]
    print('%-14s %d,%d,%d reach-before %s land %s statics %s nearest door %s dist %d' % (n,x,y,z,W.steps(x,y,z),H.lname(F.land(x,y)[0]),F.describe(x,y)[:60],doors,max(abs(doors[0]-x),abs(doors[1]-y))))
def los(a,b):
    """Rough line of sight: no impassable or wall static crossing eye height (z+10) on the tiles between."""
    n=max(abs(a[0]-b[0]),abs(a[1]-b[1])); hit=[]
    for i in range(1,n):
        x=round(a[0]+(b[0]-a[0])*i/n); y=round(a[1]+(b[1]-a[1])*i/n); ez=a[2]+10+(b[2]-a[2])*i/n
        for s,z in F.statics(x,y):
            f=H.iflags(s)
            if f&(move.IMP|H.WALL) and z<=ez<z+max(H.iheight(s),1): hit.append((x,y,hex(s)))
    return hit
print('== line of sight (rough)')
for p,q in [('theater_player','theater_echoA'),('theater_player','theater_echoB'),('theater_echoA','theater_echoB'),('yard_player','yard_echo'),('mage_player','mage_target'),('mage_demo','mage_target'),('mage_player','mage_demo')]:
    print(p,q,'dist',max(abs(A[p][0]-A[q][0]),abs(A[p][1]-A[q][1])),los(A[p],A[q]) or 'clear')
print('== mine route by the south gate')
W3=move.World()
_c=W3.check
def chk(x,y,sz,st,mz):
    if 3483<=x<=3500 and 2593<=y<=2632: return False,0   # closes the shoreline strip, so the BFS takes the gate
    return _c(x,y,sz,st,mz)
W3.check=chk
W3.bfs(tag='stock-gate')
print('mine_arm via gate',W3.steps(3512,2747,-1), 'gate tile', W3.steps(3472,2614,10))
print(W3.path(3512,2747,-1)[::12])
print('shore route',W.path(3512,2747,-1)[::12])
