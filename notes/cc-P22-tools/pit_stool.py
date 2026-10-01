# cc-P22: read the client statics around the New Haven fighting pit (thief lookout's stool). Read only.
# Run from notes/cc-P15-tools (it execs fit.py, which execs nhmap.py).
exec(open('fit.py').read())
SID=0xA2A
print(f'0x{SID:X} name={T.sname[SID]!r} height={T.sheight[SID]} flags=0x{T.sflags[SID]:X} surface={bool(T.sflags[SID]&SURF)} impassable={bool(T.sflags[SID]&IMP)}')
for y in range(2552,2563):
    for x in range(3436,3451):
        st=[(sid,sz) for (sid,sx,sy,sz,hue) in M.statics(x>>3,y>>3) if (x&7,y&7)==(sx,sy)]
        if any(T.sname[s].lower().find(k)>=0 for s,_ in st for k in ('stool','bench','chair')):
            print(x,y,[(f'0x{s:X}',T.sname[s],z,T.sheight[s]) for s,z in st if T.sheight[s]<20 or 'stool' in T.sname[s].lower()])
for x,y in [(3440,2558),(3441,2558),(3439,2558)]:
    st=[(f'0x{sid:X}',T.sname[sid],sz,T.sheight[sid],hex(T.sflags[sid])) for (sid,sx,sy,sz,hue) in M.statics(x>>3,y>>3) if (x&7,y&7)==(sx,sy)]
    print('tile',x,y,st,'land',M.land(x,y),'surfaces',surfaces(x,y),'deco',DECO.get((x,y)))
    for z in (55,56,57,58,59,60,61,62,63,64,65,66,67): 
        r=canfit(x,y,z,why=True)
        if r[0] or z in (55,58,61): print('  canfit z',z,r)
print('surfaces grid (x 3438..3451, y 2551..2563):')
for y in range(2551,2564):
    print(y, ' '.join(f"{x%100:02d}:{'/'.join(str(z) for z in surfaces(x,y)) or '-':>6}" for x in range(3438,3452)))
