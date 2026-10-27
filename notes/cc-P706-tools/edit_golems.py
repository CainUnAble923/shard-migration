"""cc-P706: the integrator's reason for a refused merge commit names the blocking paths (Commit-ShardWork.ps1's
"BLOCKED <repo>: ..." lines), not a bare "exit 2".

    python -P edit_golems.py <in Golems.ps1> <out file>
"""
import sys

src, dst = sys.argv[1], sys.argv[2]
s = open(src, 'rb').read().decode('ascii')
nl = '\r\n' if '\r\n' in s else '\n'


def sub(old, new):
    global s
    old = old.replace('\n', nl)
    new = new.replace('\n', nl)
    n = s.count(old)
    if n != 1:
        raise SystemExit('expected one match, found %d: %r' % (n, old[:80]))
    s = s.replace(old, new)


sub(r"""function Get-ClipText([string]$s, [int]$n) {""", r"""# cc-P706: what Commit-ShardWork.ps1 refused, from its output: its closing "BLOCKED <repo>: <path> ..." lines, the first
# three joined with "; " (and how many more), or '' when there are none (an older script, or a failure that is not a
# refusal).
function Get-CommitRefusal([string]$out) {
    $b = @(([string]$out -split "`r?`n") | ForEach-Object { $_.Trim() } | Where-Object { $_ -match '^BLOCKED ' } | Select-Object -Unique)
    if (-not $b.Count) { return '' }
    $t = (@($b | Select-Object -First 3) -join '; ')
    if ($b.Count -gt 3) { $t += ('; and ' + ($b.Count - 3) + ' more') }
    return $t
}
function Get-ClipText([string]$s, [int]$n) {""")
sub(r"""                if ($cc -ne 0) { $why = 'the commit after the merge failed (Commit-ShardWork.ps1 exit ' + $cc + ')'; $detail""",
    r"""                if ($cc -ne 0) { $why = 'the commit after the merge failed (Commit-ShardWork.ps1 exit ' + $cc + ')'; $rf = Get-CommitRefusal $co; if ($rf) { $why += ': ' + $rf }; $detail""")

open(dst, 'wb').write(s.encode('ascii'))
print('wrote', dst)
