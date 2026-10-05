import json,os,re,collections,sys
root=r"D:\UO\ModernUO-pinned\Distribution\Data\Spawns"
pat=re.compile(r'^(TreasureChestLevel[1-4]|treasurelevel1h)$',re.I)
tot=collections.Counter()
for dp,dn,fn in sorted(os.walk(root)):
    for f in sorted(fn):
        if not f.endswith('.json'): continue
        p=os.path.join(dp,f); rel=os.path.relpath(p,root)
        data=json.load(open(p,encoding='utf-8-sig'))
        sp=0; ent=collections.Counter(); mc=collections.Counter(); settings=collections.Counter(); mixed=0; maps=collections.Counter(); cap=0
        for s in data:
            ch=[e for e in s.get('entries',[]) if pat.match(e['name'])]
            if not ch: continue
            sp+=1; maps[s.get('map')]+=1
            other=[e for e in s['entries'] if not pat.match(e['name'])]
            if other: mixed+=1
            for e in ch:
                ent[e['name']]+=1; mc[e['name']]+=e.get('maxCount',1)
            capc=min(s.get('count',0), sum(e.get('maxCount',1) for e in ch))
            cap+=capc
            settings[(s.get('count'),s.get('minDelay'),s.get('maxDelay'),s.get('homeRange'),s.get('walkingRange'),s.get('$type'))]+=1
        if sp:
            print(f"== {rel} maps={dict(maps)} spawners={sp} mixed={mixed} chest-capacity(min(count,sum maxCount))={cap}")
            for k in sorted(ent): print(f"   {k}: entries={ent[k]} sumMaxCount={mc[k]}")
            for k,v in sorted(settings.items(),key=lambda x:-x[1]): print(f"   settings count/min/max/home/walk/type={k} x{v}")
            for k in ent: tot[(rel.split(os.sep)[0]+'/'+rel.split(os.sep)[1],k)]+=ent[k]
print(tot)
