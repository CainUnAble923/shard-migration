# Read-only: index Body assignments in a source tree. Prints JSON {body: [[file, line, class, text]]}.
import os, re, sys, json
root = sys.argv[1]
num = r'(0x[0-9A-Fa-f]+|\d+)'
pat_assign = re.compile(r'\bBody\s*=\s*([^;]+);')
pat_base = re.compile(r':\s*base\s*\(([^)]*)\)')
out = {}
for dp, dn, fn in os.walk(root):
    if any(s in dp for s in ('\bin', '\obj', '/bin', '/obj', '.git')): continue
    for f in fn:
        if not f.endswith('.cs'): continue
        p = os.path.join(dp, f)
        try: lines = open(p, encoding='utf-8', errors='replace').read().split('\n')
        except Exception: continue
        cls = None
        for i, ln in enumerate(lines, 1):
            m = re.search(r'\bclass\s+(\w+)', ln)
            if m: cls = m.group(1)
            hits = []
            for m in pat_assign.finditer(ln):
                hits += re.findall(num, m.group(1))
            if 'base(' in ln and re.search(r'Mount|Ethereal|BaseWarHorse|BaseFamiliar', ln + ' '.join(lines[max(0,i-6):i])):
                m = pat_base.search(ln)
                if m:
                    args = [a.strip() for a in m.group(1).split(',')]
                    # BaseMount(name, bodyID, itemID, ...) / BaseMount(bodyID, itemID, ...)
                    for a in args[:3]:
                        if re.fullmatch(num, a): hits.append(a); break
            for h in hits:
                b = int(h, 0)
                out.setdefault(b, []).append([os.path.relpath(p, root), i, cls, ln.strip()[:120]])
json.dump(out, open(sys.argv[2], 'w'), indent=0)
print(len(out), 'bodies')
