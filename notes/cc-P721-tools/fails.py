import re, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
lines = open(sys.argv[1], encoding='utf-8', errors='replace').read().split('\n')
out = []
i = 0
seen = set()
while i < len(lines):
    l = lines[i]
    if l.startswith('  Failed ShatteredLegacy'):
        name = re.sub(r'.*Tests\.', '', l).split('(')[0].split(' [')[0]
        msg = []
        stack = ''
        j = i + 1
        while j < len(lines) and not lines[j].startswith('  Failed ') and not lines[j].startswith('  Passed '):
            t = lines[j].strip()
            if t and not t.startswith('Error Message') and not t.startswith('Stack Trace') and not t.startswith('at ') and len(msg) < 4:
                msg.append(t[:220])
            if 'at ShatteredLegacy' in t and not stack:
                stack = re.sub(r'.*/Tests/', '', t)
            j += 1
        if name not in seen:
            seen.add(name)
            out.append('## %s\n  %s\n  @ %s' % (name, ' | '.join(msg), stack))
        i = j
    else:
        i += 1
print('\n'.join(out))
