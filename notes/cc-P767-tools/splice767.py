import sys
p='kit767/Codex.ps1'; raw=open(p,encoding='utf-8',newline='').read()
nl='\r\n' if '\r\n' in raw else '\n'; s=raw.replace('\r\n','\n')
funcs=open('p767-codex-funcs.ps1',encoding='utf-8').read().replace('\r\n','\n')
blocks=open('splice767-blocks.txt',encoding='utf-8').read().replace('\r\n','\n').split('\n@@@@\n')
assert len(blocks)%2==0, len(blocks)
for i in range(0,len(blocks),2):
    old,new=blocks[i],blocks[i+1].replace('<<FUNCS>>',funcs.strip('\n'))
    assert s.count(old)==1,(old[:80],s.count(old)); s=s.replace(old,new)
open(p,'w',encoding='utf-8',newline='').write(s.replace('\n',nl))
print('ok',repr(nl))
