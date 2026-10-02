"""cc-P30: type-name delta between pinned and upstream, intersected with our customizations.

Usage: python type_delta.py <pinned Projects> <upstream Projects> <our customizations> <outdir>
Writes types-*.txt to outdir and prints:
  - type names upstream ADDED that we also declare (duplicate-type risk; same namespace = build failure)
  - type names upstream REMOVED that our code mentions as a whole word (candidates, not results)
A name is a hypothesis: namespace and partial-ness decide whether a collision is real. The compile is the proof.
"""
import os, re, sys
from collections import defaultdict

DECL = re.compile(r'^\s*(?:\[[^\]]*\]\s*)*(?:(?:public|internal|private|protected|sealed|abstract|static|partial|readonly|unsafe|file|new)\s+)*'
                  r'(class|struct|interface|enum|record)\s+([A-Za-z_]\w*)', re.M)
NS = re.compile(r'^\s*namespace\s+([\w.]+)', re.M)

def scan(root):
    out = defaultdict(set)  # name -> {(namespace, relpath, partial)}
    for d, _, fs in os.walk(root):
        for f in fs:
            if not f.endswith('.cs'):
                continue
            p = os.path.join(d, f)
            try:
                s = open(p, encoding='utf-8', errors='replace').read()
            except OSError:
                continue
            m = NS.search(s)
            ns = m.group(1) if m else ''
            for m in DECL.finditer(s):
                line = s[m.start():m.end()]
                out[m.group(2)].add((ns, os.path.relpath(p, root).replace('\\', '/'), 'partial' in line))
    return out

pin, up, ours, outdir = sys.argv[1:5]
P, U, O = scan(pin), scan(up), scan(ours)
added = sorted(set(U) - set(P))
removed = sorted(set(P) - set(U))
for name, data in (('pinned', P), ('upstream', U), ('ours', O)):
    open(os.path.join(outdir, f'types-{name}.txt'), 'w').write('\n'.join(sorted(data)) + '\n')
open(os.path.join(outdir, 'types-upstream-added.txt'), 'w').write('\n'.join(added) + '\n')
open(os.path.join(outdir, 'types-upstream-removed.txt'), 'w').write('\n'.join(removed) + '\n')
print(f'pinned {len(P)} names, upstream {len(U)}, ours {len(O)}; upstream added {len(added)}, removed {len(removed)}')

print('\n== upstream ADDED, we also declare (name, upstream ns/file, our ns/file):')
for n in added:
    if n in O:
        for u in sorted(U[n]):
            for o in sorted(O[n]):
                same = 'SAME-NS' if u[0] == o[0] else 'diff-ns'
                print(f'  {n:40s} {same}  up={u[0]}:{u[1]}  ours={o[0]}:{o[1]}{" partial" if o[2] else ""}')

print('\n== upstream REMOVED, our code mentions the word (files):')
texts = {}
for d, _, fs in os.walk(ours):
    for f in fs:
        if f.endswith('.cs'):
            p = os.path.join(d, f)
            texts[p] = open(p, encoding='utf-8', errors='replace').read()
tests = os.path.join(os.path.dirname(ours.rstrip('/\\')), 'tests')
for d, _, fs in os.walk(tests):
    for f in fs:
        if f.endswith('.cs'):
            p = os.path.join(d, f)
            texts[p] = open(p, encoding='utf-8', errors='replace').read()
for n in removed:
    if n in O:
        continue  # we declare it ourselves
    rx = re.compile(r'\b' + re.escape(n) + r'\b')
    hits = [os.path.basename(p) for p, s in texts.items() if rx.search(s)]
    if hits:
        print(f'  {n:40s} {len(hits):3d}  {", ".join(sorted(hits)[:6])}{" ..." if len(hits) > 6 else ""}')
