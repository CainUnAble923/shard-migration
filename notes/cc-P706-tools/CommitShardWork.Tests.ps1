#Requires -Version 5.1
<#
  Facts for D:\UO\Commit-ShardWork.ps1's size cap (cc-P706): a 20 MB stray file in the overnight bot's run folder no
  longer blocks a merge, and a refusal names its path, its size and the cap in the last lines of the output.

      powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\tests\CommitShardWork.Tests.ps1 [-Script <copy>]

  Every repo is a throwaway under %TEMP% (a bare origin and a clone per repo); nothing touches the real ones. Exit code
  is the number of failed facts.
#>
param(
    [string]$Script = 'D:\UO\Commit-ShardWork.ps1',
    [string]$DocsIgnore = 'D:\UO\shard-migration\.gitignore',   # the real docs repo's rules, for the ignore fact
    [string]$GolemsLib = 'D:\UO\golem\Golems.ps1'                # the integrator's library, for the reason it gives
)
$ErrorActionPreference = 'Stop'
$work = Join-Path $env:TEMP ('csw-tests-' + [guid]::NewGuid().ToString('N').Substring(0, 8))
New-Item -ItemType Directory -Path $work -Force | Out-Null
$results = New-Object 'System.Collections.Generic.List[object]'

function Fact([string]$name, [scriptblock]$body) {
    try { & $body; $results.Add([pscustomobject]@{ Name = $name; Passed = $true }); Write-Host "  PASS  $name" -ForegroundColor Green }
    catch { $results.Add([pscustomobject]@{ Name = $name; Passed = $false }); Write-Host "  FAIL  $name" -ForegroundColor Red; Write-Host "        $($_.Exception.Message)" -ForegroundColor Red }
}
function Assert-True($c, [string]$why) { if (-not $c) { throw "not true: $why" } }
function Invoke-G([string]$repo, [string[]]$a) {
    $eap = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
    $o = & git -C $repo @a 2>&1 | Out-String
    $ErrorActionPreference = $eap
    return $o.Trim()
}

# A bare origin and a clone on main with one commit, for the code and the docs repo; then a branch with one change in
# each, merged into main with --no-commit, as the integrator leaves it for Commit-ShardWork.ps1 -Merge.
function New-World([string]$name, [string]$gitignore = '') {
    $w = @{ Dir = (Join-Path $work $name) }
    foreach ($r in 'code', 'docs') {
        $origin = Join-Path $w.Dir "$r-origin.git"; $repo = Join-Path $w.Dir $r
        [void](& git init -q --bare -b main $origin 2>&1)
        [void](& git init -q -b main $repo 2>&1)
        [void](Invoke-G $repo @('config', 'user.email', 'test@example.invalid')); [void](Invoke-G $repo @('config', 'user.name', 'test'))
        [void](Invoke-G $repo @('config', 'core.autocrlf', 'false'))
        Set-Content -LiteralPath (Join-Path $repo 'README.md') -Value "$r" -Encoding ASCII
        if ($r -eq 'docs' -and $gitignore) { Copy-Item -LiteralPath $gitignore -Destination (Join-Path $repo '.gitignore') }
        [void](Invoke-G $repo @('add', '-A')); [void](Invoke-G $repo @('commit', '-q', '-m', 'base'))
        [void](Invoke-G $repo @('remote', 'add', 'origin', $origin)); [void](Invoke-G $repo @('push', '-q', '-u', 'origin', 'main'))
        [void](Invoke-G $repo @('checkout', '-q', '-b', 'golem/Test/P1'))
        Set-Content -LiteralPath (Join-Path $repo "$r-change.txt") -Value 'the branch' -Encoding ASCII
        [void](Invoke-G $repo @('add', '-A')); [void](Invoke-G $repo @('commit', '-q', '-m', 'P1'))
        [void](Invoke-G $repo @('checkout', '-q', 'main'))
        [void](Invoke-G $repo @('merge', '--no-commit', '--no-ff', 'golem/Test/P1'))
        $w[$r] = $repo
    }
    return $w
}
# A file of n MB of zeros (a run transcript's size, not its content).
function New-BigFile([string]$path, [int]$mb) {
    New-Item -ItemType Directory -Path (Split-Path -Parent $path) -Force | Out-Null
    $fs = [IO.File]::Create($path); try { $fs.SetLength([int64]$mb * 1MB) } finally { $fs.Dispose() }
}
function Invoke-Commit($w, [string[]]$extra) {
    $a = @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', $Script, '-CodeRepo', $w.code, '-DocsRepo', $w.docs, '-Message', 'Merge golem/Test/P1: test', '-NoArchive') + $extra   # never the real prompt queue
    $eap = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
    $o = & powershell.exe @a 2>&1 | Out-String
    $script:LastCode = $LASTEXITCODE
    $ErrorActionPreference = $eap
    return $o
}
$stray = 'testing\bot-runs\2026-10-27-0130\transcripts\soak.txt'

Write-Host "Commit-ShardWork.ps1 size cap facts (cc-P706): $Script" -ForegroundColor Cyan

Fact 'P706_A20MbStrayInTheBotRunFolderIsLeftOutAndTheMergeCommitsAndPushes' {
    $w = New-World 'leftout'
    New-BigFile (Join-Path $w.docs $stray) 20
    Set-Content -LiteralPath (Join-Path $w.docs 'testing\bot-runs\2026-10-27-0130\report.md') -Value '# report' -Encoding ASCII
    $o = Invoke-Commit $w @('-Merge')
    Assert-True ($script:LastCode -eq 0) "exit 0, got $($script:LastCode): $o"
    Assert-True ($o -match 'left out of this commit \(1\)' -and $o -match 'testing/bot-runs/2026-10-27-0130/transcripts/soak\.txt  \(20\.0 MB, over the 5 MB cap') "the file is named as left out: $o"
    foreach ($r in 'code', 'docs') {
        Assert-True ((Invoke-G $w[$r] @('log', '-1', '--format=%P')).Split(' ').Count -eq 2) "$r`: a merge commit"
        Assert-True ((Invoke-G $w[$r] @('rev-parse', 'main')) -eq (Invoke-G $w[$r] @('rev-parse', 'origin/main'))) "$r`: pushed"
    }
    $tracked = Invoke-G $w.docs @('ls-files', 'testing')
    Assert-True ($tracked -match 'report\.md' -and $tracked -notmatch 'soak\.txt') "the small report went in, the transcript did not: $tracked"
    Assert-True ((Invoke-G $w.docs @('status', '--porcelain', '--untracked-files=all')) -match '\?\? testing/bot-runs/2026-10-27-0130/transcripts/soak\.txt') 'the transcript is still on disk, untracked'
    Assert-True ((Get-Item -LiteralPath (Join-Path $w.docs $stray)).Length -eq 20MB) 'and whole'
}

Fact 'P706_A20MbStrayElsewhereIsRefusedAndTheLastLineNamesItsPathSizeAndTheCap' {
    $w = New-World 'refused'
    New-BigFile (Join-Path $w.docs 'notes\big.bin') 20
    $headBefore = Invoke-G $w.docs @('rev-parse', 'main')
    $o = Invoke-Commit $w @('-Merge')
    Assert-True ($script:LastCode -eq 2) "exit 2, got $($script:LastCode): $o"
    $last = @($o.Trim() -split "`r?`n" | Where-Object { $_.Trim() })[-1]
    Assert-True ($last -match '^BLOCKED docs: size notes/big\.bin \(20\.0 MB, over the 5 MB cap, -MaxFileMB\)$') "the last line names it: [$last]"
    Assert-True ((Invoke-G $w.docs @('rev-parse', 'main')) -eq $headBefore) 'nothing was committed in docs'
    # The integrator's one-line reason (the fix-up prompt, the email, the handled- marker) carries the same line.
    . $GolemsLib
    $rf = Get-CommitRefusal $o
    Assert-True ($rf -eq 'BLOCKED docs: size notes/big.bin (20.0 MB, over the 5 MB cap, -MaxFileMB)') "the integrator's reason: [$rf]"
}

Fact 'P706_ABlockedPatternIsNamedInTheSummaryToo' {
    $w = New-World 'pattern'
    New-Item -ItemType Directory -Path (Join-Path $w.code 'dist') -Force | Out-Null
    Set-Content -LiteralPath (Join-Path $w.code 'dist\pkg.txt') -Value 'x' -Encoding ASCII
    $o = Invoke-Commit $w @('-Merge')
    Assert-True ($script:LastCode -eq 2) "exit 2: $o"
    Assert-True ($o -match '(?m)^BLOCKED code: pattern dist/pkg\.txt \(matched') "named: $o"
}

Fact 'P706_OnlyAnOversizedBotFilePendingIsNothingToCommit' {
    $w = New-World 'onlystray'
    foreach ($r in 'code', 'docs') { [void](Invoke-G $w[$r] @('commit', '-q', '-m', 'merged')); [void](Invoke-G $w[$r] @('push', '-q')) }
    New-BigFile (Join-Path $w.docs $stray) 20
    $headBefore = Invoke-G $w.docs @('rev-parse', 'main')
    $o = Invoke-Commit $w @()
    Assert-True ($script:LastCode -eq 0) "exit 0, got $($script:LastCode): $o"
    Assert-True ($o -match 'nothing else to commit') "said: $o"
    Assert-True ((Invoke-G $w.docs @('rev-parse', 'main')) -eq $headBefore) 'no empty commit'
}

Fact 'P706_TheDocsRepoIgnoresRunTranscriptsSoTheyAreNotEvenPending' {
    Assert-True (Test-Path -LiteralPath $DocsIgnore) "no $DocsIgnore"
    $w = New-World 'ignored' $DocsIgnore
    New-BigFile (Join-Path $w.docs $stray) 20
    Set-Content -LiteralPath (Join-Path $w.docs 'testing\bot-runs\2026-10-27-0130\transcripts\P64-6-run1.txt') -Value 'a check' -Encoding ASCII
    Set-Content -LiteralPath (Join-Path $w.docs 'testing\bot-runs\2026-10-27-0130\results.json') -Value '{}' -Encoding ASCII
    $o = Invoke-Commit $w @('-Merge')
    Assert-True ($script:LastCode -eq 0) "exit 0, got $($script:LastCode): $o"
    Assert-True ($o -notmatch 'left out of this commit') "nothing to leave out, the rule ignores it: $o"
    $tracked = Invoke-G $w.docs @('ls-files', 'testing')
    Assert-True ($tracked -match 'results\.json' -and $tracked -notmatch 'transcripts/') "results.json committed, no transcript: $tracked"
}

Remove-Item -LiteralPath $work -Recurse -Force -ErrorAction SilentlyContinue
$failed = @($results | Where-Object { -not $_.Passed }).Count
Write-Host ''
Write-Host ("{0} facts, {1} passed, {2} failed" -f $results.Count, ($results.Count - $failed), $failed) -ForegroundColor $(if ($failed) { 'Red' } else { 'Green' })
exit $failed
