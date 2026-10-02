"""cc-P30: rewrite generator-v2 save-flag attributes to the v4 form, in place.

  [SerializableFieldSaveFlag(N)] on a ShouldSerialize method  +  [SerializableFieldDefault(N)] on a default method
    ->  [SaveFlag(nameof(ShouldSerializeX)[, nameof(XDefaultValue)])] on the [SerializableField(N...)] field itself.

Generator 4.2.0's own obsolete message says "The wire format does not change." Run only on a COPY.
Usage: python v4_saveflag.py <file.cs>...   (prints a per-file summary; fails loudly on anything it cannot place)
"""
import re, sys

SAVE = re.compile(r'^[ \t]*\[SerializableFieldSaveFlag\((\d+)\)\][ \t]*\r?\n(?=[ \t]*[\w<>\[\], ]+?\s(\w+)\s*\()', re.M)
DEF = re.compile(r'^[ \t]*\[SerializableFieldDefault\((\d+)\)\][ \t]*\r?\n(?=[ \t]*[\w<>\[\], ?]+?\s(\w+)\s*\()', re.M)
FIELD = r'^([ \t]*)\[SerializableField\({n}(?:\s*,[^)]*)?\)\][ \t]*(\r?\n)'

for path in sys.argv[1:]:
    s = open(path, encoding='utf-8-sig', newline='').read()
    had_bom = open(path, 'rb').read(3) == b'\xef\xbb\xbf'
    flags, defaults = {}, {}
    for m in SAVE.finditer(s):
        flags[int(m.group(1))] = m.group(2)
    for m in DEF.finditer(s):
        defaults[int(m.group(1))] = m.group(2)
    if not flags and not defaults:
        continue
    s = SAVE.sub('', s)
    s = DEF.sub('', s)
    for n in sorted(set(flags) | set(defaults)):
        if n not in flags:
            sys.exit(f'{path}: default for field {n} with no save flag; v4 needs both on [SaveFlag]')
        args = f'nameof({flags[n]})' + (f', nameof({defaults[n]})' if n in defaults else '')
        rx = re.compile(FIELD.format(n=n), re.M)
        hits = list(rx.finditer(s))
        if len(hits) != 1:
            sys.exit(f'{path}: field {n}: expected one [SerializableField({n})], found {len(hits)}')
        m = hits[0]
        s = s[:m.end()] + f'{m.group(1)}[SaveFlag({args})]{m.group(2)}' + s[m.end():]
    with open(path, 'w', encoding='utf-8-sig' if had_bom else 'utf-8', newline='') as f:
        f.write(s)
    print(f'{path}: {len(flags)} save flags, {len(defaults)} defaults moved onto fields')
