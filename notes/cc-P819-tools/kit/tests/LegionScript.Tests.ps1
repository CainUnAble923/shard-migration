#Requires -Version 5.1
<#
  LegionScript.Tests.ps1 (cc-P219). Facts for Test-LegionScript.ps1 and LegionTest.ps1: the never-live guard (this
  PC's own test shard only; 2593 refused from any host) and the test-shard lock (taken before anything touches the
  shard, refused while another Golem holds it, released after a run and after a failure), plus the plan, the script
  overrides, the client's settings and the report. cc-P819: the guard's game check is off here. No client is started and no shard is touched: -DryRun, refusals
  and a fixture Golem folder (its own locks\).

      powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\tests\LegionScript.Tests.ps1 [-Harness <folder>]

  Prints PASS/FAIL per fact; the exit code is the number of failed checks. ASCII only.
#>
param([string]$Harness = 'D:\UO\golem', [string]$Only)
$ErrorActionPreference = 'Stop'
$script:fails = 0; $script:passes = 0
Remove-Item Env:GOLEM_NAME, Env:GOLEM_ROOT -ErrorAction SilentlyContinue
function Assert-True($cond, [string]$what) { if ($cond) { $script:passes++ } else { $script:fails++; Write-Host ('    FAIL: ' + $what) -ForegroundColor Red } }
function Fact([string]$name, [scriptblock]$body) {
    if ($Only -and $name -notlike "*$Only*") { return }
    $before = $script:fails
    try { & $body } catch { $script:fails++; Write-Host ('    FAIL (threw): ' + $_.Exception.Message + ' | ' + $_.InvocationInfo.PositionMessage) -ForegroundColor Red }
    if ($script:fails -eq $before) { Write-Host "PASS $name" -ForegroundColor Green } else { Write-Host "FAIL $name" -ForegroundColor Red }
}
$lib = Join-Path $Harness 'LegionTest.ps1'
$tls = Join-Path $Harness 'Test-LegionScript.ps1'
if (Test-Path -LiteralPath $lib) { . $lib }
$script:LegionGameCheck = $false   # cc-P819: the facts never wait on a game being played on this PC (GamePause.Tests.ps1 covers it)

# A fixture Golem folder (locks\ of its own) and a plan.
function New-LWorld {
    $d = Join-Path ([IO.Path]::GetTempPath()) ('legion-test-' + [guid]::NewGuid().ToString('N').Substring(0, 8))
    New-Item -ItemType Directory -Path (Join-Path $d 'root') -Force | Out-Null
    $plan = Join-Path $d 'SL_Mining.json'
    '{ "script": "SL_Mining.py", "timeLimitMinutes": 2, "overrides": { "GUI": "False" }, "setup": [ "[global set Skills.Mining.Base 100 where playermobile Name == \"{player}\"" ], "steps": [ { "name": "digs", "type": "journal", "pattern": "You dig some", "count": 1 } ] }' |
        Set-Content -LiteralPath $plan -Encoding ASCII
    [pscustomobject]@{ Dir = $d; Root = (Join-Path $d 'root'); Plan = $plan; Locks = (Join-Path $d 'root\locks') }
}
function Invoke-Tls($w, [string[]]$more) {
    $a = @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', $tls, '-Golem', 'Iron', '-Script', 'SL_Mining.py', '-Plan', $w.Plan, '-Root', $w.Root, '-LockWaitMinutes', '0') + @($more)
    $eap = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
    $o = & powershell.exe @a 2>&1
    $code = $LASTEXITCODE
    $ErrorActionPreference = $eap
    [pscustomobject]@{ Code = $code; Out = (($o | Out-String).Trim()) }
}
function Get-LockFiles($w) { @(Get-ChildItem -LiteralPath $w.Locks -Filter '*.json' -File -ErrorAction SilentlyContinue) }
$own = @('127.0.0.1', '::1', 'localhost', 'chases-tower', '192.168.1.58')

Fact 'P219_TheGuardTakesOnlyThisPcsOwnTestShard' {
    Assert-True (Test-Path -LiteralPath $lib) 'LegionTest.ps1 is beside the harness'
    foreach ($ok in @(@('127.0.0.1', 2594), @('localhost', 2595), @('CHASES-TOWER', 2594), @('192.168.1.58', 2599), @('::1', 2596))) {
        $r = Test-LegionTarget $ok[0] $ok[1] $own
        Assert-True ($r.Ok) ('allowed: ' + $ok[0] + ':' + $ok[1] + ' / ' + $r.Why)
    }
}

Fact 'P219_TheGuardRefusesTheLivePortFromAnyHostAndEveryOtherHost' {
    foreach ($bad in @(@('127.0.0.1', 2593, 'live shard'), @('localhost', 2593, 'live shard'), @('192.168.1.58', 2593, 'live shard'), @('shatteredlegacyuo.com', 2593, 'live shard'),
                       @('shatteredlegacyuo.com', 2594, 'live shard or Haven'), @('get.shatteredlegacyuo.com', 2594, 'live shard or Haven'), @('haven', 2594, 'live shard or Haven'),
                       @('192.168.1.61', 2594, 'not this PC'), @('192.0.2.10', 2594, 'not this PC'), @('chases-tower.tail81098d.ts.net', 2594, 'not this PC'),
                       @('127.0.0.1', 8080, 'not a test shard port'), @('127.0.0.1', 2600, 'not a test shard port'), @('', 2594, 'no host'))) {
        $r = Test-LegionTarget $bad[0] $bad[1] $own
        Assert-True (-not $r.Ok -and $r.Why -match [regex]::Escape($bad[2])) ('refused ' + $bad[0] + ':' + $bad[1] + ' (' + $bad[2] + '): ' + $r.Why)
    }
    # Without a list, this PC's own names and addresses are read; another machine's address is still refused.
    Assert-True (Test-LegionTarget '127.0.0.1' 2594).Ok 'loopback, from this PC''s own list'
    Assert-True (-not (Test-LegionTarget '203.0.113.7' 2594).Ok) 'a documentation address is not this PC'
}

Fact 'P219_TheHarnessRefusesALiveOrForeignTargetBeforeTheLock' {
    foreach ($t in @(@('-TargetHost', 'shatteredlegacyuo.com'), @('-Port', '2593'), @('-TargetHost', '192.0.2.10'))) {
        $w = New-LWorld
        $r = Invoke-Tls $w (@($t) + @('-DryRun'))
        Assert-True ($r.Code -eq 2 -and $r.Out -match 'refused') ('refused, exit 2: ' + ($t -join ' ') + ' / ' + $r.Code + ' ' + $r.Out)
        Assert-True ((Get-LockFiles $w).Count -eq 0 -and $r.Out -notmatch 'Took test-shard') ('no lock taken: ' + ($t -join ' '))
        Remove-Item -LiteralPath $w.Dir -Recurse -Force -ErrorAction SilentlyContinue
    }
}

Fact 'P219_TheHarnessTakesTheTestShardLockAndReleasesIt' {
    $w = New-LWorld
    $r = Invoke-Tls $w @('-DryRun')
    Assert-True ($r.Code -eq 0) ('the dry run passes: ' + $r.Code + ' ' + $r.Out)
    Assert-True ($r.Out -match 'Took test-shard' -and $r.Out -match 'Released test-shard') ('took the test-shard lock, then released it: ' + $r.Out)
    Assert-True ((Get-LockFiles $w).Count -eq 0) 'no lock left behind'
    Remove-Item -LiteralPath $w.Dir -Recurse -Force -ErrorAction SilentlyContinue
}

Fact 'P219_ALockHeldByAnotherGolemMeansNoRun' {
    $w = New-LWorld
    New-Item -ItemType Directory -Path $w.Locks -Force | Out-Null
    $held = [ordered]@{ resource = 'test-shard'; owner = 'Bronze'; session = 'sess-b'; since = (Get-Date).ToString('s'); ttlMinutes = 60; why = 'a Docker build'; machine = 'X' }
    $held | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $w.Locks 'test-shard.json') -Encoding ASCII
    $r = Invoke-Tls $w @('-DryRun')
    Assert-True ($r.Code -eq 3 -and $r.Out -match 'Not run' -and $r.Out -match 'held by Bronze') ('exit 3, Bronze holds it: ' + $r.Code + ' ' + $r.Out)
    $l = Get-Content -LiteralPath (Join-Path $w.Locks 'test-shard.json') -Raw | ConvertFrom-Json
    Assert-True ($l.owner -eq 'Bronze') ('Bronze''s lock is left as it was: ' + $l.owner)
    Assert-True ($r.Out -notmatch 'Dry run: the guard') 'nothing went on'
    Remove-Item -LiteralPath $w.Dir -Recurse -Force -ErrorAction SilentlyContinue
}

Fact 'P219_TheLockIsReleasedWhenARunStopsPartway' {
    # Past the lock, the PC check fails (a work copy with no play-test bot): refused, exit 2, and the lock comes back.
    $w = New-LWorld
    $r = Invoke-Tls $w @('-CodeRepo', (Join-Path $w.Dir 'no-such-repo'), '-DocsRepo', (Join-Path $w.Dir 'docs'))
    Assert-True ($r.Code -eq 2 -and $r.Out -match 'Took test-shard' -and $r.Out -match 'cannot run a Legion script test') ('stopped after the lock: ' + $r.Code + ' ' + $r.Out)
    Assert-True ($r.Out -match 'Released test-shard' -and (Get-LockFiles $w).Count -eq 0) ('the lock released: ' + $r.Out)
    Assert-True (-not (Test-Path -LiteralPath (Join-Path $w.Dir 'docs\testing'))) 'no report for a refused run'
    Remove-Item -LiteralPath $w.Dir -Recurse -Force -ErrorAction SilentlyContinue
}

Fact 'P219_ABadPlanIsRefusedBeforeTheLock' {
    $w = New-LWorld
    foreach ($bad in @(
        @('{ "timeLimitMinutes": 2, "steps": [] }', 'names no script'),
        @('{ "script": "SL_Mining.py", "timeLimitMinutes": 0, "steps": [] }', 'timeLimitMinutes must be 1 to 60'),
        @('{ "script": "SL_Mining.py", "setup": [ "say hello" ], "steps": [] }', 'not a staff command'),
        @('{ "script": "SL_Mining.py", "steps": [ { "name": "x", "type": "click" } ] }', 'journal, items or at'),
        @('{ "script": "SL_Lumberjack.py", "steps": [] }', 'the plan is for SL_Lumberjack.py'))) {
        Set-Content -LiteralPath $w.Plan -Value $bad[0] -Encoding ASCII
        $r = Invoke-Tls $w @('-DryRun')
        Assert-True ($r.Code -eq 2 -and $r.Out -match [regex]::Escape($bad[1]) -and (Get-LockFiles $w).Count -eq 0 -and $r.Out -notmatch 'Took test-shard') ('refused before the lock: ' + $bad[1] + ' / ' + $r.Out)
    }
    Remove-Item -LiteralPath $w.Dir -Recurse -Force -ErrorAction SilentlyContinue
}

Fact 'P219_TheClientCanNeverBeSentElsewhereAndKeepsNoPlainPassword' {
    $s = New-LegionSettings '127.0.0.1' 2594 'iron-player' (ConvertTo-CuoPassword 'abc' 'PC') 'D:\UO\UltimaOnlineVanilla'
    Assert-True ($s.ignore_relay_ip -eq $true -and $s.ip -eq '127.0.0.1' -and $s.port -eq 2594) 'relay redirects ignored, this PC''s test shard'
    Assert-True ($s.autologin -eq $true -and @($s.plugins).Count -eq 0) 'auto-login, no plugins'
    # ClassicUO.Utility.Crypter.Encrypt: "1-", each byte XOR the PC name, in hex: a^P b^C c^P = 31 21 33.
    Assert-True ((ConvertTo-CuoPassword 'abc' 'PC') -eq '1-312133') (ConvertTo-CuoPassword 'abc' 'PC')
    Assert-True ($s.password -ne 'abc') 'never the plain password'
    $src = Get-Content -LiteralPath $tls -Raw
    Assert-True ($src -match '\$j\.password = ''''' -and $src -match '\$j\.autologin = \$false') 'the harness clears the password from the settings when the run ends'
}

Fact 'P219_ThePlansOverridesRewriteOnlyTheScriptsConfigLines' {
    $text = "import API`nGUI             = True      # show the window`nWANDER = True`nx = 1`n"
    $o = $null
    $o = Set-LegionOverrides $text ([pscustomobject]@{ GUI = 'False'; WANDER = 'False'; NOPE = '1' })
    Assert-True ($o.Text -match '(?m)^GUI = False  # cc-P219 test override$' -and $o.Text -match '(?m)^WANDER = False' -and $o.Text -match '(?m)^x = 1$') $o.Text
    Assert-True (@($o.Applied).Count -eq 2 -and @($o.Missing) -contains 'NOPE') ('applied 2, NOPE missing: ' + ($o.Missing -join ','))
}

Fact 'P219_TheReportSaysPassOrFailPerStepWithTheJournalAndTheErrors' {
    $now = Get-Date
    $r = [pscustomobject]@{ Script = 'SL_Mining.py'; Golem = 'Iron'; Host = '127.0.0.1'; Port = 2594; Plan = [pscustomobject]@{ timeLimitMinutes = 6 }; PlanFile = 'plans\SL_Mining.json'; Result = 'fail'; Why = 'a step failed'
        Steps = @([pscustomobject]@{ name = 'digs'; result = 'pass'; detail = '5 of 5' }, [pscustomobject]@{ name = 'ore'; result = 'fail'; detail = '0 more | none' })
        Setup = @([pscustomobject]@{ command = '[global addtopack Pickaxe'; replies = @('1 object generated'); ok = $true }); Overrides = @('GUI = False')
        Journal = @('You dig some iron ore'); LegionLog = @(); RunnerLog = @('done'); ClientErrors = @(); ServerErrors = @('Exception: boom'); Shots = @([pscustomobject]@{ What = 'start'; Rel = 'x/1-start.jpg' })
        Started = $now.AddMinutes(-1); Ended = $now; Branch = ''; ScriptFile = 'D:\UO\sl-scripts\SL_Mining.py' }
    $t = Format-LegionReport $r
    Assert-True ($t -match '\*\*Result: FAIL\*\*: a step failed\.' -and $t -match '\| digs \| pass \| 5 of 5 \|' -and $t -match '\| ore \| \*\*fail\*\* \| 0 more / none \|') 'the result and each step'
    Assert-True ($t -match '## Journal' -and $t -match 'You dig some iron ore' -and $t -match '## Server errors' -and $t -match 'Exception: boom' -and $t -match '!\[start\]\(x/1-start\.jpg\)') 'the journal, the errors, the screenshots'
    Assert-True ($t -match '## Legion log[^\n]*\r?\n\r?\nNone\.') 'an empty section says None'
}

Write-Host ''
Write-Host ('{0} checks passed, {1} failed (Legion script tests, {2})' -f $script:passes, $script:fails, $Harness)
exit $script:fails
