# cc-P26: red runs for player-package/tests/Build-UoOverrides.Tests.ps1. Each mutation breaks one behaviour,
# the facts run, then every file is restored from memory and checked by SHA-256.
import hashlib, subprocess, sys

B = r'D:\ShatteredLegacy\player-package\payload\app\Build-UoOverrides.ps1'
P = r'D:\ShatteredLegacy\player-package\payload\app\Play.ps1'
T = r'D:\ShatteredLegacy\player-package\tests\Build-UoOverrides.Tests.ps1'

MUTATIONS = [
    ('m1 tiledata record one byte late', B,
     "function Write-TileRecord([byte[]]$d, $r) {\n    $o = Get-TileOffset $r.id",
     "function Write-TileRecord([byte[]]$d, $r) {\n    $o = (Get-TileOffset $r.id) + 1"),
    ('m2 a named slot counts as free', B,
     "    if ($name -and $name -ne 'UNUSED') { return \"is named '$name' in tiledata\" }",
     "    if ($false) { return \"is named '$name' in tiledata\" }"),
    ('m3 frames of other animations not seen', B,
     "            if ($v -ne 0) { [void]$t.Add($i + $v) }",
     "            if ($false) { [void]$t.Add($i + $v) }"),
    ('m4 the stamp never matches', B,
     "[IO.File]::ReadAllText($stampOut) -ceq $stamp -and",
     "[IO.File]::ReadAllText($stampOut) -ceq 'never' -and"),
    ('m5 a failure is thrown, not swallowed', B,
     "    Say-Skip \"Shattered Legacy art could not be prepared ($($_.Exception.Message)). Starting without it.\"\n    return $null",
     "    throw"),
    ('m6 Play.ps1 passes an override path even with none', P,
     "if ($uoOverride) { $tazArgs += @('-uofilesoverride', \"`\"$uoOverride`\"\") }",
     "$tazArgs += @('-uofilesoverride', \"`\"$uoOverride`\"\")"),
]


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def main():
    which = sys.argv[1:] or [m[0].split()[0] for m in MUTATIONS]
    for name, path, old, new in MUTATIONS:
        if name.split()[0] not in which:
            continue
        orig = open(path, 'rb').read()
        h = sha(path)
        s = orig.decode('ascii')
        assert s.count(old) == 1, (name, s.count(old))
        open(path, 'wb').write(s.replace(old, new).encode('ascii'))
        try:
            r = subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', T],
                               capture_output=True, text=True)
            fails = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith('FAIL')]
            print('%s: exit %d; %s' % (name, r.returncode, '; '.join(fails) or 'NO FACT FAILED'))
        finally:
            open(path, 'wb').write(orig)
            assert sha(path) == h, 'restore failed: ' + path
    print('restored, byte-identical: %s %s' % (sha(B)[:12], sha(P)[:12]))


if __name__ == '__main__':
    main()
