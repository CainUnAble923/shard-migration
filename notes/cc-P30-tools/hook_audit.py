"""cc-P30: for every Shattered Legacy hook line in a replacement file, report the method (and overload number)
that encloses it, so a three-way merge that attached a hook to the wrong overload shows up as a mismatch.

Usage: python hook_audit.py <ours-before.cs> <merged.cs> [regex]
"""
import re, sys, collections

HOOK = re.compile(sys.argv[3] if len(sys.argv) > 3 else
                  r'ClusterF|HammerOfHephaestus|RecordFamiliarity|DevTestingCrystal|HammerBODAutoFill|GetBestGroupAmount|cc-P18|Shattered Legacy')
SIG = re.compile(r'^\s{8}(?:public|private|protected|internal)[^=;(]*?\s(\w+)\s*\(', re.M)

def hooks(path):
    lines = open(path, encoding='utf-8-sig').read().split('\n')
    seen = collections.Counter()
    current = '<class>'
    out = []
    for i, l in enumerate(lines, 1):
        m = SIG.match(l)
        if m:
            seen[m.group(1)] += 1
            current = f'{m.group(1)}#{seen[m.group(1)]}'
        if HOOK.search(l):
            out.append((current, l.strip()[:90], i))
    return out

a, b = hooks(sys.argv[1]), hooks(sys.argv[2])
ca = collections.Counter((m, t) for m, t, _ in a)
cb = collections.Counter((m, t) for m, t, _ in b)
bad = 0
for key in sorted(set(ca) | set(cb)):
    if ca[key] != cb[key]:
        bad += 1
        print(f'MISMATCH before={ca[key]} after={cb[key]}  {key[0]}: {key[1]}')
print(f'{len(a)} hook lines before, {len(b)} after, {bad} mismatches')
