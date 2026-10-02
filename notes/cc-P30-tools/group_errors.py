"""cc-P30: group dotnet build errors (deduplicated) by code+symbol and by file.

Usage: python group_errors.py <build.log>
"""
import re, sys, collections

LINE = re.compile(r'Projects[\\/](?P<file>[^(]+)\((?P<pos>\d+,\d+)\): error (?P<code>[A-Z]+\d+): (?P<msg>.*?) \[')
seen = set()
by_cause = collections.Counter()
by_file = collections.Counter()
examples = {}
for raw in open(sys.argv[1], encoding='utf-8', errors='replace'):
    m = LINE.search(raw)
    if not m:
        continue
    key = (m['file'], m['pos'], m['code'], m['msg'])
    if key in seen:
        continue
    seen.add(key)
    msg = m['msg']
    sym = re.findall(r"'([^']+)'", msg)
    cause = f"{m['code']} " + (re.sub(r'\d+', 'N', msg[:90]) if not sym else msg.split("'")[0] + "'" + sym[0] + "' " + msg.split("'")[-1][:50])
    by_cause[cause] += 1
    by_file[m['file']] += 1
    examples.setdefault(cause, f"{m['file']}({m['pos']})")
print(f'{len(seen)} distinct errors in {len(by_file)} files\n\n== by cause')
for k, v in by_cause.most_common():
    print(f'{v:4d}  {k}\n        e.g. {examples[k]}')
print('\n== by file')
for k, v in by_file.most_common():
    print(f'{v:4d}  {k}')
