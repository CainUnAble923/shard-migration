"""cc-P706: the refused-merge fact also checks the integrator's reason (Golems.ps1 Get-CommitRefusal)."""
import sys

p = sys.argv[1]
s = open(p, 'rb').read().decode('ascii')
old = r"""    [string]$DocsIgnore = 'D:\UO\shard-migration\.gitignore'   # the real docs repo's rules, for the ignore fact
)"""
new = r"""    [string]$DocsIgnore = 'D:\UO\shard-migration\.gitignore',   # the real docs repo's rules, for the ignore fact
    [string]$GolemsLib = 'D:\UO\golem\Golems.ps1'                # the integrator's library, for the reason it gives
)"""
old2 = r"""    Assert-True ((Invoke-G $w.docs @('rev-parse', 'main')) -eq $headBefore) 'nothing was committed in docs'
}"""
new2 = r"""    Assert-True ((Invoke-G $w.docs @('rev-parse', 'main')) -eq $headBefore) 'nothing was committed in docs'
    # The integrator's one-line reason (the fix-up prompt, the email, the handled- marker) carries the same line.
    . $GolemsLib
    $rf = Get-CommitRefusal $o
    Assert-True ($rf -eq 'BLOCKED docs: size notes/big.bin (20.0 MB, over the 5 MB cap, -MaxFileMB)') "the integrator's reason: [$rf]"
}"""
for a, b in ((old, new), (old2, new2)):
    a2 = a.replace('\n', '\r\n') if '\r\n' in s else a
    b2 = b.replace('\n', '\r\n') if '\r\n' in s else b
    assert s.count(a2) == 1, a[:60]
    s = s.replace(a2, b2)
open(p, 'wb').write(s.encode('ascii'))
print('ok')
