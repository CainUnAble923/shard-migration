import re, glob, json, os
pts=[]
srcs=glob.glob('D:/ShatteredLegacy/server/customizations/**/*.cs',recursive=True)+[
 'D:/UO/shard-migration/notes/cc-P16-mine-camp-tents.md','D:/UO/shard-migration/notes/cc-P17-playtest-bugs-1.md',
 'D:/UO/shard-migration/notes/cc-P19-registrar-office-decor.md','D:/UO/shard-migration/notes/new-haven-quest-board.md',
 'D:/UO/cc-prompts/cc-P22-small-features-1.md']
pat=re.compile(r'\b(3[3-7]\d\d)\s*,\s*(2[3-9]\d\d)\b')
pat2=re.compile(r'x:\s*(3[3-7]\d\d),\s*y:\s*(2[3-9]\d\d)')
for f in srcs:
    for i,line in enumerate(open(f,encoding='utf-8',errors='ignore'),1):
        for m in list(pat.finditer(line))+list(pat2.finditer(line)):
            pts.append((os.path.basename(f)+':'+str(i), int(m.group(1)), int(m.group(2))))
tp=json.load(open('tram_points.json'))
pts+= [(k,x,y) for k,x,y in tp if 3300<=x<=3820 and 2340<=y<=3100]
json.dump(pts,open('island_points.json','w'))
print('island points', len(pts))
ruins=json.load(open('ruins.json'))
for i,(a,b,c,d,n) in enumerate(ruins[:8]):
    near=[p for p in pts if a-10<=p[1]<=c+10 and b-10<=p[2]<=d+10]
    print('ruin',i,(a,b,c,d), 'nearby refs', len(near))
    for p in near[:25]: print('   ',p)
