"""ServUO type names that pinned ModernUO has only as a [TypeAlias] string, never as a declaration.

A name-only index (S3, S9) calls every one of these missing. Two consequences:
  A. a ServUO file whose PRIMARY type is alias-only survives the step-1 filter and looks like a candidate
     although porting it would put a second type under one name;
  B. a ServUO class DERIVING from an alias-only type is bucketed as blocked on a missing base.
"""
import os, re
from secondary import S, M, C, DECL, ALIAS, STR, PARENT, read, walk

decl, al = set(), {}
for p in walk(M):
    t = read(p)
    for a in ALIAS.findall(t):
        for s in re.findall(r'"([^"]+)"', a):
            al.setdefault(s.split('.')[-1], os.path.relpath(p, M))
    decl.update(DECL.findall(STR.sub('""', t)))
ours = set()
for p in walk(C):
    ours.update(DECL.findall(STR.sub('""', read(p))))

alias_only = {k: v for k, v in al.items() if k not in decl}
sv_decl, prim_files, parents = {}, [], []
for p in walk(S):
    t = STR.sub('""', read(p))
    ts = DECL.findall(t)
    rel = os.path.relpath(p, S)
    for x in ts:
        sv_decl.setdefault(x, rel)
    if ts:
        stem = os.path.basename(p)[:-3]
        prim = stem if stem in ts else ts[0]
        if prim in alias_only:
            prim_files.append((rel, prim))
    for c, b in PARENT.findall(t):
        b = b.split('.')[-1]
        if b in alias_only:
            parents.append((rel, c, b))

hit = sorted(k for k in alias_only if k in sv_decl)
print('pinned alias-only names:', len(alias_only), '; of which ServUO declares a type by that name:', len(hit))
for k in hit:
    print('   ', k, '->', alias_only[k], '| ServUO', sv_decl[k])
print('\nA. ServUO files whose primary type is alias-only in pinned:', len(prim_files))
for r, p in sorted(prim_files):
    print('   ', r, '|', p)
print('\nB. ServUO classes deriving directly from an alias-only type:', len(parents))
for r, c, b in sorted(parents):
    print('   ', r, '|', c, ':', b, '|', 'OURS' if c in ours else ('PINNED' if c in decl else 'ABSENT'))
