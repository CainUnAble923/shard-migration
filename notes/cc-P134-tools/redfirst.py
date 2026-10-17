"""cc-P134 red-first runner: break validate-art.py one way at a time, run the tests, restore. Prints which tests
went red for each break, and proves the file is restored byte for byte."""
import hashlib, os, shutil, subprocess, sys

REPO = r'D:\ShatteredLegacy'
SCRIPT = os.path.join(REPO, 'scripts', 'validate-art.py')
BACKUP = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'validate-art.py.orig')

MUTATIONS = [
    ('bodyconv: first column wins (vseUOAware)', "                out[body] = (i, toks[i], where)",
     "                out.setdefault(body, (i, toks[i], where))"),
    ('bodyconv: columns for missing files applied', "if toks[i] >= 0 and i in files_present:", "if toks[i] >= 0:"),
    ('layout: mobtypes type ignored', "t = type_idx if type_idx is not None else type_by_graphic(slot, fi)",
     "t = type_by_graphic(slot, fi)"),
    ('layout: slot range ignored', "    return 0 if slot < 200 else (2 if slot < 400 else 3)", "    return 0"),
    ('uop: wrong flag bit', "UOP_FLAG, PEOPLE_FLAG, LOW_FLAG, LOW_EXT_FLAG, IDLE8_FLAG, FLY_FLAG = 0x10000,",
     "UOP_FLAG, PEOPLE_FLAG, LOW_FLAG, LOW_EXT_FLAG, IDLE8_FLAG, FLY_FLAG = 0x20000,"),
    ('layout: animal 0x20 ignored', "        if flags & LOW_EXT_FLAG:\n            g = 'people'",
     "        if False:\n            g = 'people'"),
    ('overrides: equipAnims not applied', "        self.bodyconv = read_bodyconv(self.bodyconv_path, set(self.files), extra)",
     "        self.bodyconv = read_bodyconv(self.bodyconv_path, set(self.files), ())"),
    ('check-vd: planned slot frames not checked', "                problems.append('frames: %s records %d-%d already hold actions %s'",
     "                out.append('frames: %s records %d-%d already hold actions %s'"),
    ('check-vd: layout mismatch not reported',
     "            problems.append('layout: the .vd is a %s block but the client reads a %s block here' % (vd.group, r['group']))",
     "            out.append('layout: the .vd is a %s block but the client reads a %s block here' % (vd.group, r['group']))"),
    ('check-vd: existing bodyconv line not a problem',
     "        problems.append('bodyconv: already has a line (%s, %s slot %d)' % (b[2], file_name(b[0]), b[1]))",
     "        out.append('bodyconv: already has a line (%s, %s slot %d)' % (b[2], file_name(b[0]), b[1]))"),
    ('check-vd: Body.def applied to every body', "            if tgt['format'] == 'classic' and tgt['file'] == 0:",
     "            if True:"),
    ('check-vd: server body table not read', "    if body in c.body_table:\n        out.append('server:",
     "    if False:\n        out.append('server:"),
    ('check-vd: hover hint missing', "    if 8 in acts and vd.group == 'high':", "    if 99 in acts and vd.group == 'high':"),
    ('vd: header not checked', "        if magic != 6 or lay not in VD_LAYOUTS:", "        if lay not in VD_LAYOUTS:"),
    ('propose: bodyTable bodies offered', " or b in c.bodyconv or b in c.body_table:", " or b in c.bodyconv:"),
    ('check-registry: duplicates missed', "            if (k, i) in seen:", "            if False:"),
    ('check-registry: missing mobtypes missed', "                    if i not in c.mobtypes:\n                        prob.append('missing: no mobtypes.txt entry')",
     "                    if False:\n                        prob.append('missing: no mobtypes.txt entry')"),
    ('hues: alpha bit compared', "if (x[1][i] & 0x7FFF) != (y[1][i] & 0x7FFF))", "if x[1][i] != y[1][i])"),
    ('hues: names counted as colours', "    col = [h for h, w in diff if any('colours' in x for x in w)]",
     "    col = [h for h, w in diff]"),
    ('render: header XOR (double bias)', "            x = (hd >> 22) & 0x3FF\n",
     "            hd ^= (0x200 << 22) | (0x200 << 12)\n            x = (hd >> 22) & 0x3FF\n"),
    ('render: mirror wrong', "    return (direction, False) if direction <= 4 else (8 - direction, True)",
     "    return (direction, False) if direction <= 4 else (direction - 4, True)"),
]


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def run_tests():
    # A mutation of the same size written in the same second leaves a stale .pyc that Python trusts: clear it.
    cache = os.path.join(REPO, 'scripts', '__pycache__')
    for f in os.listdir(cache) if os.path.isdir(cache) else []:
        if f.startswith('validate-art.'):
            os.remove(os.path.join(cache, f))
    r = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'scripts/tests', '-p', 'test_validate_art.py'],
                       cwd=REPO, capture_output=True, text=True,
                       env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
    failed = sorted({l.split('(')[0].split(':', 1)[1].strip() for l in r.stderr.splitlines()
                     if l.startswith(('FAIL:', 'ERROR:'))})
    last = [l for l in r.stderr.splitlines() if l.startswith(('OK', 'FAILED'))]
    return r.returncode, failed, last[-1] if last else '?'


def main():
    shutil.copyfile(SCRIPT, BACKUP)
    orig = sha(SCRIPT)
    rc, failed, last = run_tests()
    print('baseline: rc %d %s' % (rc, last))
    src = open(BACKUP, encoding='ascii').read()
    bad = 0
    try:
        for name, old, new in MUTATIONS:
            if src.count(old) != 1:
                print('SKIP %s: pattern found %d times' % (name, src.count(old)))
                bad += 1
                continue
            with open(SCRIPT, 'w', encoding='ascii', newline='\n') as f:
                f.write(src.replace(old, new))
            rc, failed, last = run_tests()
            print('%s %s: rc %d %s; red: %s' % ('RED ' if rc else 'GREEN?', name, rc, last, ', '.join(failed) or '-'))
            bad += rc == 0
    finally:
        shutil.copyfile(BACKUP, SCRIPT)
    rc, failed, last = run_tests()
    print('restored: sha256 %s; rc %d %s' % ('identical' if sha(SCRIPT) == orig else 'DIFFERENT', rc, last))
    return 1 if bad or sha(SCRIPT) != orig or rc else 0


if __name__ == '__main__':
    sys.exit(main())
