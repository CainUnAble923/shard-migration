import move,hallbase as H
W=move.World(); W.bfs(); F=W.F
ML=[(220,231),(236,247),(268,279),(286,297),(321,324),(467,474),(476,487),(492,495),(543,579),(581,621),(1741,1757),(1771,1790),(1801,1824),(1831,1854),(1861,1884),(1981,2004),(2028,2033),(2100,2105)]
def mineland(i): return any(a<=i<=b for a,b in ML)
print('stand tiles with mineable land within 1, in ravine')
out=[]
for (x,y,z),d in sorted(W.dist.items()):
    if 3508<=x<=3532 and 2744<=y<=2760:
        n=[(x+a,y+b) for a in(-1,0,1) for b in(-1,0,1) if (a or b) and mineland(F.land(x+a,y+b)[0])]
        if n and H.lname(F.land(x,y)[0])=='dirt': out.append((x,y,z,d,len(n)))
print(out)
for x in range(3509,3520): pass
print(move.landmap(W,3508,2744,3532,2760))
print(W.gridmap(3508,2744,3532,2760))
# stable sign, housing
print(move.landmap(W,3514,2568,3526,2580))
print([(t,W.zs(*t),H.lname(F.land(*t)[0]),F.describe(*t)) for t in [(3521,2573),(3520,2573),(3521,2572),(3522,2572),(3463,2597),(3465,2597),(3464,2596),(3477,2617),(3478,2617),(3478,2616)]])
print(hex(F.land(3521,2573)[0]))
print(move.gridz(W,3440,2612,3462,2630,0,40))
print(move.landmap(W,3440,2612,3462,2630))
print(H.iname(0xFFA),H.flagstr(H.iflags(0xFFA)),H.iname(0xB2C),H.flagstr(H.iflags(0xB2C)),H.iheight(0xB2C))
