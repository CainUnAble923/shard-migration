# P62 red runs for player-package\tests\Build-UoOverrides.Tests.ps1. One mutation at a time, in place, restored
# from a copy and checked by SHA-256 afterwards.
#   python mutate_player.py <name>     runs the facts with that mutation and restores
import hashlib, shutil, subprocess, sys

B = r'D:\ShatteredLegacy\player-package\payload\app\Build-UoOverrides.ps1'
K = r'D:\ShatteredLegacy\server\customizations\KitsuneEarsTail.cs'
M = {
    'p1-no-bodyconv-skip': (B, "elseif ($used.Contains($n)) { $why = 'Bodyconv.def already names it' }",
                            "elseif ($false) { $why = 'Bodyconv.def already names it' }"),
    'p2-no-line-break': (B, 'if ($src.Length -and $src[$src.Length - 1] -ne 10) { $tail = "`r`n" }', 'if ($false) { $tail = "`r`n" }'),
    'p3-anim7-not-checked': (B, 'if (Test-Path -LiteralPath (Join-Path $UoDir $n)) { throw "your Ultima Online folder now has its own $n" }',
                             'if ($false) { throw "your Ultima Online folder now has its own $n" }'),
    'p4-icon-record-not-written': (B, '        Write-TileRecord $tile $r\n    }\n\n    if (-not (Test-Path -LiteralPath $OutDir))',
                                   '        # Write-TileRecord $tile $r\n    }\n\n    if (-not (Test-Path -LiteralPath $OutDir))'),
    'p5-cs-animation-drifts': (K, 'AnimationId = 4783;', 'AnimationId = 4784;'),
    'p6-cs-flag-misnamed': (K, 'TileFlag.Wearable | TileFlag.Weapon;', 'TileFlag.Wearable | TileFlag.Background;'),
}
name = sys.argv[1]
path, old, new = M[name]
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
h0 = sha(path)
text = open(path, 'rb').read().decode('ascii')
assert text.count(old) == 1, 'mutation %s does not apply exactly once' % name
shutil.copyfile(path, path + '.p62bak')
try:
    open(path, 'wb').write(text.replace(old, new).encode('ascii'))
    r = subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File',
                        r'D:\ShatteredLegacy\player-package\tests\Build-UoOverrides.Tests.ps1'],
                       capture_output=True, text=True)
    out = r.stdout + r.stderr
    print('\n'.join(l for l in out.splitlines() if 'FAIL' in l or 'facts,' in l or l.startswith('        ')))
    print('exit', r.returncode)
finally:
    shutil.copyfile(path + '.p62bak', path)
    import os
    os.remove(path + '.p62bak')
    assert sha(path) == h0, 'NOT RESTORED'
    print('restored', h0[:12])
