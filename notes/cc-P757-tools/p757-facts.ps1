# ---- cc-P757: the night check falls back to plan-usage.json, one batch on the last known week, a Golem's own pick ------
# Spliced into tests\Golem.Tests.ps1 before its summary lines. Uses P156's night world (New-Night156, $p156Night,
# $p156WeekReset: at 22:30 on 10-17, 47.1% of the week is allowed tonight) and P158's lane world (New-LaneWorld).
# Every usage file here is a copy in the test world's root, in the shapes the live files had on 11-01: usage.json with
# sevenDay only (no fiveHour), plan-usage.json with "session": null.
if ($Kind -eq 'golem') {
    # usage.json as the status line wrote it on 11-01 05:17: the week only.
    function Set-UsageWeekOnly757($w, [double]$SevenDay, [datetime]$At) {
        @{ updatedUtc = $At.ToUniversalTime().ToString('s'); sessionId = 's'; model = 'claude-opus-5-5'
           sevenDay = @{ pct = $SevenDay; resetsAt = [DateTimeOffset]::new($p156WeekReset).ToUnixTimeSeconds() } } | ConvertTo-Json -Depth 4 |
            Set-Content -LiteralPath (Join-Path $w.Root 'usage.json') -Encoding ASCII
    }
    # plan-usage.json as the overseer's reader writes it; -Session -1 writes "session": null (as on 11-01).
    function Set-Plan757($w, [double]$Week, [datetime]$ReadAt, [double]$Session = -1) {
        $fmt = { param($t) [DateTimeOffset]::new($t).ToString('yyyy-MM-ddTHH:mm:sszzz') }
        $j = [ordered]@{ schema = 1; readAt = (& $fmt $ReadAt); readBy = 'test'; plan = 'Ultra'
            session = $(if ($Session -ge 0) { @{ pct = $Session; resets = (& $fmt $ReadAt.AddHours(3)) } } else { $null })
            week = @{ pct = $Week; resets = (& $fmt $p156WeekReset); note = 'all models' }; fableWeek = $null; paceWarning = ''
            limitResets = @{ full = @{ available = $false; expires = '' }; fiveHour = @{ available = $false } } }
        $j | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $w.Root 'plan-usage.json') -Encoding ASCII
    }

    Fact 'P757_1_TheNightCheckTakesTheWindowUsageJsonLacksFromThePlanPage' {
        # 11-01: usage.json has the week only; the plan page (read 40 minutes ago, within planUsageMaxAgeHours) has both.
        $w = New-Night156
        Set-UsageWeekOnly757 $w 30 $p156Night.AddMinutes(-15)
        Set-Plan757 $w 30 $p156Night.AddMinutes(-40) -Session 12
        [void](Invoke-At156 $w 'NightShift' $p156Night)
        Assert-True ((Wait-CliCalls156 $w 1) -eq 1) ('a batch starts: ' + (Get-WLog $w))
        $l = Get-WLog $w
        Assert-True ($l -match 'night batch 1 started \(the night shift task\): budget the week to 47\.1% \(17\.1 points from 30%\), the 5-hour window to 50% \(from 12%\)') ('the 5-hour figure is the plan page''s: ' + $l)
        Assert-True ($l -match 'usage: the week from the status line, the 5-hour window from the plan usage page') ('the log says which source: ' + $l)
        Assert-True ($l -notmatch 'usage unknown') ('never "usage unknown": ' + $l)
        # The plan page too old (over planUsageMaxAgeHours 4): not used for the 5-hour window.
        $w2 = New-Night156
        Set-UsageWeekOnly757 $w2 30 $p156Night.AddMinutes(-15)
        Set-Plan757 $w2 30 $p156Night.AddHours(-6) -Session 12
        [void](Invoke-At156 $w2 'NightShift' $p156Night)
        Assert-True ((Get-WLog $w2) -match 'usage: the week from the status line, the 5-hour window not reported by the status line or the plan usage page') ('a stale plan page is not used: ' + (Get-WLog $w2))
        # usage.json gone, the plan page fresh: the plan page alone.
        $w3 = New-Night156
        Remove-Item -LiteralPath (Join-Path $w3.Root 'usage.json')
        Set-Plan757 $w3 30 $p156Night.AddMinutes(-20) -Session 12
        [void](Invoke-At156 $w3 'NightShift' $p156Night)
        Assert-True ((Wait-CliCalls156 $w3 1) -eq 1 -and (Get-WLog $w3) -match 'usage: the week from the plan usage page, the 5-hour window from the plan usage page') ('from the plan page alone: ' + (Get-WLog $w3))
    }

    Fact 'P757_2_AFiveHourWindowNeitherSourceReportsIsNotHeldFor' {
        # The live shapes of 11-01: usage.json week only, the plan page "session": null. The week decides.
        $w = New-Night156
        Set-UsageWeekOnly757 $w 30 $p156Night.AddMinutes(-15)
        Set-Plan757 $w 30 $p156Night.AddMinutes(-5)
        [void](Invoke-At156 $w 'NightShift' $p156Night)
        Assert-True ((Wait-CliCalls156 $w 1) -eq 1) ('a batch starts on the week alone: ' + (Get-WLog $w))
        $l = Get-WLog $w
        Assert-True ($l -match 'the 5-hour window to 50% \(its figure not known\)' -and $l -match 'the 5-hour window not reported by the status line or the plan usage page \(not held for\)') ('said: ' + $l)
        $b = @((Get-Night156 $w).batches)[0]
        Assert-True ([double]$b.weekLimit -eq 47.1 -and -not [bool]$b.usageFallback) ('an ordinary batch, the week''s budget: ' + ($b | ConvertTo-Json -Compress))
        # The pace gate still holds: the week at 60% starts nothing, and the log names the source.
        $w2 = New-Night156
        Set-UsageWeekOnly757 $w2 60 $p156Night.AddMinutes(-15)
        Set-Plan757 $w2 60 $p156Night.AddMinutes(-5)
        [void](Invoke-At156 $w2 'NightShift' $p156Night)
        Assert-True (@(Get-CliCalls $w2).Count -eq 0) 'over pace: no batch'
        Assert-True ((Get-WLog $w2) -match 'no batch: the week is at 60%, ahead of its pace \(47\.1% allowed tonight.*\(usage: the week from the plan usage page') ('why, and the source: ' + (Get-WLog $w2))
    }

    Fact 'P757_3_NeitherSourceUsableStartsOneBatchWhenTheLastKnownWeekIsUnderPace' {
        # usage.json 30 hours old (over nightUsageMaxAgeHours 24), the plan page 6 hours old (over planUsageMaxAgeHours 4).
        $w = New-Night156
        Set-UsageWeekOnly757 $w 30 $p156Night.AddHours(-30)
        Set-Plan757 $w 31 $p156Night.AddHours(-6)
        [void](Invoke-At156 $w 'NightShift' $p156Night)
        Assert-True ((Wait-CliCalls156 $w 1) -eq 1) ('one batch starts: ' + (Get-WLog $w))
        $l = Get-WLog $w
        Assert-True ($l -match 'night batch 1 started.*usage fallback: .*the week is the last known figure, 31% from the plan usage page at 16:30') ('the newest figure (the plan page''s), said: ' + $l)
        $b = @((Get-Night156 $w).batches)[0]
        Assert-True ([bool]$b.usageFallback -and [double]$b.weekLimit -eq 47.1 -and [double]$b.weekAtStart -eq 31) ('the batch is marked: ' + ($b | ConvertTo-Json -Compress))
        # The batch ends; the files are still stale at the 23:30 check: no second batch on old figures.
        $s = Get-WState $w
        $s.nightShift.batch = 0
        $s.nightShift | Add-Member -NotePropertyName nextCheck -NotePropertyValue '2026-10-17T23:30:00' -Force   # as Close-NightBatch sets it
        foreach ($k in @('longRun', 'wakePending')) { if ($s.PSObject.Properties.Name -contains $k) { $s.PSObject.Properties.Remove($k) } }
        $s | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $w.Root 'state.json') -Encoding ASCII
        [void](Invoke-At156 $w 'Watch' $p156Night.AddMinutes(60))
        Assert-True (@(Get-CliCalls $w).Count -eq 1) ('one batch a night on old figures: ' + (Get-WLog $w))
        Assert-True ((Get-WStatus $w).nightShift.whyNot -match 'the one batch a night on the last known week figure has run \(batch 1\)') ('why: ' + (Get-WStatus $w).nightShift.whyNot)
        # The last known week over pace: nothing.
        $w2 = New-Night156
        Set-UsageWeekOnly757 $w2 60 $p156Night.AddHours(-30)
        Remove-Item -LiteralPath (Join-Path $w2.Root 'plan-usage.json') -ErrorAction SilentlyContinue
        [void](Invoke-At156 $w2 'NightShift' $p156Night)
        Assert-True (@(Get-CliCalls $w2).Count -eq 0 -and (Get-WStatus $w2).nightShift.whyNot -match 'the week is at 60%, ahead of its pace') ('over pace: ' + (Get-WStatus $w2).nightShift.whyNot)
        # No figure at all: still unknown, nothing started.
        $w3 = New-Night156
        Remove-Item -LiteralPath (Join-Path $w3.Root 'usage.json')
        [void](Invoke-At156 $w3 'NightShift' $p156Night)
        Assert-True (@(Get-CliCalls $w3).Count -eq 0 -and (Get-WStatus $w3).nightShift.whyNot -match 'usage unknown \(no usage\.json.*no week figure') ('no figure: ' + (Get-WStatus $w3).nightShift.whyNot)
        # Away mode's rule (the same Test-NightUsage) does not take the fallback.
        $ast = [System.Management.Automation.Language.Parser]::ParseFile($Hook, [ref]$null, [ref]$null)
        $calls = @($ast.FindAll({ param($a) $a -is [System.Management.Automation.Language.CommandAst] -and $a.GetCommandName() -eq 'Test-NightUsage' }, $true))
        Assert-True ($calls.Count -eq 2 -and @($calls | Where-Object { $_.Extent.Text -match '-AllowFallback' }).Count -eq 1) ('only the night budget allows the fallback: ' + (@($calls | ForEach-Object { $_.Extent.Text }) -join ' | '))
    }

    Fact 'P757_4_AGolemsOwnRunNextPickIsTakenEvenWhenMarkedCodexOk' {
        $w = New-LaneWorld
        Add-PromptText $w 'cc-P105-forcodex.md' ("# CC task P105: for codex`n`n**Touches:** docs-only`n" + $laneOk)
        Add-PromptText $w 'cc-P106-plain.md' "# CC task P106: plain`n`n**Touches:** docs-only`n"
        Set-Content -LiteralPath (Join-Path $w.Root 'RUN-NEXT-Bronze') -Value 'cc-P105-forcodex.md' -Encoding ASCII
        [void](Invoke-Team $w 'Bronze' 'Stop' @{ last_assistant_message = 'go'; session_id = 'sess-b' })
        Assert-True ((Get-TeamState $w 'Bronze').current -eq 'P105') ('Bronze takes its own pick: ' + (Get-TeamState $w 'Bronze').current + ' / ' + (Get-TeamLog $w 'Bronze'))
        Assert-True ((Get-TeamLog $w 'Bronze') -match "claim: P105 is marked Codex OK, but it is Bronze's own run next pick: taken") ('said: ' + (Get-TeamLog $w 'Bronze'))
        # Another Golem's pick, or no pick: still left for the lane.
        $w2 = New-LaneWorld
        Add-PromptText $w2 'cc-P105-forcodex.md' ("# CC task P105: for codex`n`n**Touches:** docs-only`n" + $laneOk)
        Add-PromptText $w2 'cc-P106-plain.md' "# CC task P106: plain`n`n**Touches:** docs-only`n"
        [void](Invoke-Team $w2 'Bronze' 'Stop' @{ last_assistant_message = 'go'; session_id = 'sess-b' })
        Assert-True ((Get-TeamState $w2 'Bronze').current -eq 'P106' -and (Get-TeamLog $w2 'Bronze') -match 'claim: P105 is marked Codex OK and a Codex lane is on: left for it') ('no pick: left for the lane: ' + (Get-TeamState $w2 'Bronze').current)
    }
}
