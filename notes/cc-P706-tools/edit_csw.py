"""cc-P706: Commit-ShardWork.ps1: oversized overnight-bot output is left out of the commit (named, not refused), and
every refusal names its path, its reason and the cap in a closing summary that a caller's last lines carry.

    python -P edit_csw.py <in Commit-ShardWork.ps1> <out file>

Each replacement must match exactly once, or nothing is written.
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


# 1. The header.
sub(r"""  client data, or any single file over -MaxFileMB (default 5). It prints what it
  found and stops, rather than asking. Both repos are public, so a wrong commit
  is public immediately and rewriting history afterwards does not unpublish it.
""", r"""  client data, or any single file over -MaxFileMB (default 5). It prints what it
  found and stops, rather than asking. Both repos are public, so a wrong commit
  is public immediately and rewriting history afterwards does not unpublish it.
  cc-P706: a refusal ends with one "BLOCKED <repo>: <path> ..." line per path (its size and the cap, or the pattern),
  the last lines a caller keeps. One exception to refusing: a file over the cap under testing/bot-runs/ (the overnight
  play-test bot's output, which every commit sweeps in) is LEFT OUT of the commit, named in a yellow "left out" line,
  and stays on disk; the rest commits. The bot's transcripts are git-ignored since cc-P706, so this is the backstop.
""")

# 2. The rule, beside the patterns.
sub(r"""function Get-PendingPaths {""", r"""# cc-P706: machine output that never blocks a commit for its size: left out instead (Test-Safe, then git reset after add).
$LeaveOutOversized = '^testing/bot-runs/'

function Get-PendingPaths {""")

# 3. Test-Safe: refusals and left-out files apart, each line naming the size and the cap.
sub(r"""function Test-Safe {
    param([string]$RepoPath, [string[]]$Paths)
    $bad = @()
    foreach ($p in $Paths) {
        foreach ($rx in $BlockPatterns) {
            if ($p -match $rx) { $bad += "pattern  $p  (matched $rx)"; break }
        }
        $full = Join-Path $RepoPath ($p -replace '/','\')
        if (Test-Path -LiteralPath $full -PathType Leaf) {
            $mb = (Get-Item -LiteralPath $full).Length / 1MB
            if ($mb -gt $MaxFileMB) { $bad += ("size     {0}  ({1:N1} MB)" -f $p, $mb) }
        }
    }
    return $bad
}""", r"""function Test-Safe {
    param([string]$RepoPath, [string[]]$Paths)
    # cc-P706: returns { Bad = refusals; LeaveOut = paths over the cap under $LeaveOutOversized, with their lines }.
    $bad = @(); $leave = @(); $leaveLines = @()
    foreach ($p in $Paths) {
        $hit = $false
        foreach ($rx in $BlockPatterns) {
            if ($p -match $rx) { $bad += "pattern  $p  (matched $rx)"; $hit = $true; break }
        }
        $full = Join-Path $RepoPath ($p -replace '/','\')
        if (-not $hit -and (Test-Path -LiteralPath $full -PathType Leaf)) {
            $mb = (Get-Item -LiteralPath $full).Length / 1MB
            if ($mb -gt $MaxFileMB) {
                $line = ("size     {0}  ({1:N1} MB, over the {2} MB cap, -MaxFileMB)" -f $p, $mb, $MaxFileMB)
                if ($p -match $LeaveOutOversized) { $leave += $p; $leaveLines += $line } else { $bad += $line }
            }
        }
    }
    return [pscustomobject]@{ Bad = @($bad); LeaveOut = @($leave); LeaveOutLines = @($leaveLines) }
}""")

# 4. The repo loop: refusal lines kept for the summary; left-out files named, then unstaged after add.
sub(r"""$anyBlocked = $false
$anyFailed  = $false   # add, commit or push failed (P60 section 7 item 2, 2026-10-05)
""", r"""$anyBlocked = $false
$anyFailed  = $false   # add, commit or push failed (P60 section 7 item 2, 2026-10-05)
$blockedLines = @()    # cc-P706: "BLOCKED <repo>: <what>", printed last so a caller's tail of the output names each path
""")
sub(r"""    $bad = Test-Safe -RepoPath $path -Paths $pending
    if ($bad.Count -gt 0) {
        $anyBlocked = $true
        Write-Host ''
        Write-Host "  REFUSING to commit this repo. The shard's two repos are public; the scripts repo gets the same checks." -ForegroundColor Red
        $bad | ForEach-Object { Write-Host "    $_" -ForegroundColor Red }
        Write-Host "  Add these to .gitignore, or move them out, then run again." -ForegroundColor Red
        $results += [pscustomobject]@{ Repo = $repo.Name; Result = 'BLOCKED' }
        continue
    }
""", r"""    $safe = Test-Safe -RepoPath $path -Paths $pending
    $bad = $safe.Bad
    if ($bad.Count -gt 0) {
        $anyBlocked = $true
        Write-Host ''
        Write-Host "  REFUSING to commit this repo. The shard's two repos are public; the scripts repo gets the same checks." -ForegroundColor Red
        $bad | ForEach-Object { Write-Host "    $_" -ForegroundColor Red }
        Write-Host "  Add these to .gitignore, or move them out, then run again." -ForegroundColor Red
        $results += [pscustomobject]@{ Repo = $repo.Name; Result = 'BLOCKED' }
        $bad | ForEach-Object { $blockedLines += ('BLOCKED {0}: {1}' -f $repo.Name, ($_ -replace '\s+', ' ')) }
        continue
    }
    # cc-P706: the overnight bot's oversized output stays on disk and out of the commit; everything else goes in.
    $leaveOut = $safe.LeaveOut
    if ($leaveOut.Count -gt 0) {
        Write-Host ''
        Write-Host ("  left out of this commit ({0}): the overnight bot's output over the cap stays on disk, uncommitted:" -f $leaveOut.Count) -ForegroundColor Yellow
        $safe.LeaveOutLines | ForEach-Object { Write-Host "    $_" -ForegroundColor Yellow }
        if ($leaveOut.Count -eq $pending.Count -and -not $Merge) {
            Write-Host "  nothing else to commit" -ForegroundColor Gray
            $results += [pscustomobject]@{ Repo = $repo.Name; Result = 'clean (left out)' }
            continue
        }
    }
""")
sub(r"""    & git -C $path add -A
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  git add failed ($LASTEXITCODE)" -ForegroundColor Red
        $results += [pscustomobject]@{ Repo = $repo.Name; Result = 'add failed' }; $anyFailed = $true
        continue
    }
""", r"""    & git -C $path add -A
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  git add failed ($LASTEXITCODE)" -ForegroundColor Red
        $results += [pscustomobject]@{ Repo = $repo.Name; Result = 'add failed' }; $anyFailed = $true
        continue
    }
    # cc-P706: unstage what is left out (a new file goes back to untracked, a changed one keeps its change on disk).
    $unstageFailed = $false
    foreach ($lp in $leaveOut) {
        & git -C $path reset -q -- $lp
        if ($LASTEXITCODE -ne 0) { $unstageFailed = $true }
    }
    if ($unstageFailed) {
        & git -C $path reset -q
        Write-Host "  git reset of a left-out file failed; nothing was committed here" -ForegroundColor Red
        $results += [pscustomobject]@{ Repo = $repo.Name; Result = 'add failed' }; $anyFailed = $true
        continue
    }
""")

# 4b. The other refusals name themselves in the summary too.
sub(r"""        Write-Host ("  REFUSING: this copy is on '{0}', not on {1}. Nothing was committed here." -f $head, $Branch) -ForegroundColor Red
""", r"""        Write-Host ("  REFUSING: this copy is on '{0}', not on {1}. Nothing was committed here." -f $head, $Branch) -ForegroundColor Red
        $blockedLines += ('BLOCKED {0}: {1} is on {2}, not on {3}' -f $repo.Name, $path, $head, $Branch)
""")
sub(r"""        Write-Host ("  REFUSING: -Merge needs main, this copy is on '{0}'. Nothing was committed here." -f $head) -ForegroundColor Red
""", r"""        Write-Host ("  REFUSING: -Merge needs main, this copy is on '{0}'. Nothing was committed here." -f $head) -ForegroundColor Red
        $blockedLines += ('BLOCKED {0}: {1} is on {2}; -Merge needs main' -f $repo.Name, $path, $head)
""")
sub(r"""        Write-Host "  Run this script as the repo owner (your own Windows login), not SYSTEM or another account." -ForegroundColor Red
""", r"""        Write-Host "  Run this script as the repo owner (your own Windows login), not SYSTEM or another account." -ForegroundColor Red
        $blockedLines += ('BLOCKED {0}: git status failed in {1}' -f $repo.Name, $path)
""")

# 5. The closing summary.
sub(r"""if ($anyBlocked) {
    Write-Host "One or more repos were refused. Nothing was committed there." -ForegroundColor Red
    exit 2
}""", r"""if ($anyBlocked) {
    Write-Host "One or more repos were refused. Nothing was committed there." -ForegroundColor Red
    # cc-P706: the paths, last, so the integrator's clipped tail and its one-line reason carry them.
    $blockedLines | ForEach-Object { Write-Host $_ -ForegroundColor Red }
    exit 2
}""")

open(dst, 'wb').write(s.encode('ascii'))
print('wrote', dst)
