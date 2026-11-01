
# ---- cc-P747: a build review nobody takes goes to Iron; a timeout never merges; reviews in a fresh session; answers win --
if ($Kind -eq 'golem') {
    # P734's world with Gold in the registry, so the review is Gold's first (not Iron's).
    function New-P747World([hashtable]$settings = @{}) {
        $w = New-P734World
        $rf = Join-Path $w.Root 'golems.json'
        $r = Get-Content -LiteralPath $rf -Raw | ConvertFrom-Json
        $r.golems = @(@($r.golems) + [pscustomobject]@{ name = 'Gold'; machine = 'STEPHS-DESKTOP'; engine = 'claude'; lane = 'any'; account = ''; areas = @('map', 'docs-only'); work = [pscustomobject]@{ code = 'D:\x'; docs = 'D:\y' }; enabled = $true; integrator = $false; hours = '' })
        $r | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $rf -Encoding ASCII
        if ($settings.Count) {
            $s = Get-Content -LiteralPath (Join-Path $w.Root 'settings.json') -Raw | ConvertFrom-Json
            foreach ($k in $settings.Keys) { $s | Add-Member -NotePropertyName $k -NotePropertyValue $settings[$k] -Force }
            $s | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $w.Root 'settings.json') -Encoding ASCII
        }
        $w
    }
    function Set-P747Age($w, [int]$minutes, [string]$verdict = '') {
        $mf = Join-Path $w.Root 'merge-queue\review-P105.json'
        $rec = Get-Content -LiteralPath $mf -Raw | ConvertFrom-Json
        $rec.queuedAt = (Get-Date).AddMinutes(-$minutes).ToString('s')
        if ($verdict) { $rec.verdict = $verdict }
        $rec | ConvertTo-Json | Set-Content -LiteralPath $mf -Encoding ASCII
    }
    function Get-P747RunNext($w) { $f = Join-Path $w.Root 'RUN-NEXT'; if (Test-Path -LiteralPath $f) { (Get-Content -LiteralPath $f -Raw).Trim() } else { '' } }

    Fact 'P747_1_AnUnclaimedReviewGoesToIronAfterTwoHoursAsItsNextHandOff' {
        $w = New-P747World
        [void](Invoke-Shadow $w)
        $rq = @(Get-ChildItem -LiteralPath $w.Queue -Filter 'cc-P*-review-build-*.md')[0]
        Assert-True ($rq -and (Get-Content -LiteralPath $rq.FullName -Raw) -match '(?m)^\*\*Golem:\*\* Gold\s*$') 'Gold first'
        Set-P747Age $w 70
        [void](Invoke-Shadow $w)
        Assert-True (-not (Get-P747RunNext $w) -and (Get-ShadowLog $w) -notmatch 'assigned to Iron') ('70 minutes: only opened wider, not yet Iron''s: ' + (Get-P747RunNext $w))
        Set-P747Age $w 125
        $o = Invoke-Shadow $w
        $l = Get-ShadowLog $w
        $rt = Get-Content -LiteralPath $rq.FullName -Raw
        Assert-True ($o -match 'P105 from Bronze: review' -and -not (Test-Path -LiteralPath (Join-Path $w.Code 'server\data\Decoration\Britannia\dock.cfg'))) ('P105 still waits: ' + $o)
        Assert-True ($rt -match '(?m)^\*\*Golem:\*\* Iron\s*$') ('the review is Iron''s now: ' + $rt)
        Assert-True ((Get-P747RunNext $w) -eq $rq.Name) ('and Iron''s run next pick (RUN-NEXT): ' + (Get-P747RunNext $w))
        Assert-True ($l -match ('build review: ' + [regex]::Escape($rq.Name) + ' unclaimed for \d+ minutes: assigned to Iron with Assign-Prompt\.ps1 -RunNext')) ('logged: ' + $l)
        $rec = Get-Content -LiteralPath (Join-Path $w.Root 'merge-queue\review-P105.json') -Raw | ConvertFrom-Json
        Assert-True ([string]$rec.fallback -eq 'Iron') ('the record says so: ' + ($rec | ConvertTo-Json -Compress))
        [void](Invoke-Shadow $w)
        Assert-True (@([regex]::Matches((Get-ShadowLog $w), 'assigned to Iron')).Count -eq 1) 'done once, not every round'
        # A review a Golem has claimed is left alone.
        $w2 = New-P747World
        [void](Invoke-Shadow $w2)
        $rq2 = @(Get-ChildItem -LiteralPath $w2.Queue -Filter 'cc-P*-review-build-*.md')[0]
        $cg = Join-Path $w2.Prompts 'claimed\Gold'; New-Item -ItemType Directory -Path $cg -Force | Out-Null
        Move-Item -LiteralPath $rq2.FullName -Destination (Join-Path $cg $rq2.Name)
        Set-P747Age $w2 125
        [void](Invoke-Shadow $w2)
        Assert-True (-not (Get-P747RunNext $w2) -and (Get-ShadowLog $w2) -notmatch 'assigned to Iron') 'a claimed review is not taken away'
        # buildReviewFallbackMinutes sets the wait.
        $w3 = New-P747World @{ buildReviewFallbackMinutes = 30 }
        [void](Invoke-Shadow $w3)
        Set-P747Age $w3 40
        [void](Invoke-Shadow $w3)
        Assert-True ((Get-P747RunNext $w3) -match '^cc-P\d+-review-build-isle-dock\.md$') ('buildReviewFallbackMinutes 30: Iron''s after 40 minutes: ' + (Get-P747RunNext $w3))
    }

    Fact 'P747_3_ALateReviewNeverMergesOnItsOwnOnlyAVerdictOrASkip' {
        $w = New-P747World
        [void](Invoke-Shadow $w)
        Set-P747Age $w 540
        $o = Invoke-Shadow $w
        $l = Get-ShadowLog $w
        Assert-True ($o -match 'P105 from Bronze: review' -and -not (Test-Path -LiteralPath (Join-Path $w.Code 'server\data\Decoration\Britannia\dock.cfg'))) ('nine hours, no verdict: still held, nothing merged: ' + $o)
        Assert-True ($l -match 'build review: P105 has waited \d+ minutes with no verdict .*still held' -and $l -notmatch 'merged without one') ('logged as held: ' + $l)
        [void](Invoke-Shadow $w)
        Assert-True (@([regex]::Matches((Get-ShadowLog $w), 'with no verdict')).Count -eq 1) 'said once'
        # A record an older kit marked timeout is held too.
        Set-P747Age $w 600 'timeout'
        Assert-True ((Invoke-Shadow $w) -match 'P105 from Bronze: review') 'an old timeout record does not let it through'
        # Skip-BuildReview.ps1 does.
        $eap = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
        [void](& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path (Split-Path -Parent $Hook) 'Skip-BuildReview.ps1') -Prompt 105 -Root $w.Root -Reason 'overseer looked' 2>&1 | Out-String)
        $ErrorActionPreference = $eap
        Assert-True ((Invoke-Shadow $w) -match 'P105 from Bronze: merged' -and (Test-Path -LiteralPath (Join-Path $w.Code 'server\data\Decoration\Britannia\dock.cfg'))) 'Skip-BuildReview.ps1 lets it through'
        # The review prompt no longer promises a merge after the time-out.
        $w2 = New-P747World
        [void](Invoke-Shadow $w2)
        $rt = Get-Content -LiteralPath (@(Get-ChildItem -LiteralPath $w2.Queue -Filter 'cc-P*-review-build-*.md')[0].FullName) -Raw
        Assert-True ($rt -notmatch 'merges anyway' -and $rt -match 'Skip-BuildReview\.ps1') ('the review prompt: ' + $rt)
    }

    Fact 'P747_2_AReviewIsNeverHandedIntoTheSessionThatBuiltTheWork' {
        $w = New-WakeWorld
        Remove-Item -LiteralPath (Join-Path $w.Queue 'cc-P101-b.md') -Force
        Add-PromptText $w 'cc-P101-review-build-a.md' "# CC task P101: build review of P100 (a)`n`n**Model:** Opus`n**Touches:** docs-only`n**Golem:** Iron`n"
        Set-Session $w 'sess-a' @{ contextPct = 10; contextSize = 200000; model = 'claude-opus-5-5'; source = 'statusline' }
        [void](Invoke-HookX $w 'Stop' @{ last_assistant_message = 'P100 DONE'; session_id = 'sess-a' } $w.CliArgs)
        Assert-True (Test-Path -LiteralPath $w.Marker) 'P100 committed'
        Assert-True ((Get-WState $w).current -eq '') ('the review is not handed into the session that just finished P100: ' + (Get-WState $w).current)
        Assert-True ((Get-WStatus $w).restReason -eq 'review') ('a review rest: ' + (Get-WStatus $w).restReason)
        $calls = @(Get-CliCalls $w)
        Assert-True ($calls.Count -eq 1 -and $calls[0] -match 'Golem P101' -and $calls[0] -match '--model opus') ('a fresh Opus session woken for it: ' + ($calls -join ' | '))
        Assert-True ((Get-WLog $w) -match 'P101 is a build review: not handed into this session') ('logged: ' + (Get-WLog $w))
        $o = Invoke-HookX $w 'Prompt' @{ prompt = 'Golem, please work on the shard tasks.'; session_id = 'sess-n' } $w.CliArgs
        Assert-True (($o | ConvertFrom-Json).hookSpecificOutput.additionalContext -match 'cc-P101-review-build-a\.md in full') ('the fresh session gets it: ' + $o)
    }

    Fact 'P747_4_AnAnsweredPromptKeepsItsPlaceAheadOfALaterRunNext' {
        $w = New-AskWorld
        [void](Invoke-HookX $w 'Stop' @{ last_assistant_message = 'P100 STOPPED: which world?'; session_id = 'sess-a' } $w.CliArgs)
        $id = (@(Get-WQuestions $w 'open'))[0].id
        $r = Invoke-Answer $w $id 0 'the Tokuno one'
        Assert-True ($r.Code -eq 0 -and (Get-RunNext182 $w) -eq 'cc-P100-a.md') ('answered: P100 goes next: ' + $r.Out)
        $rn = Invoke-Event182 $w 'RunNext' @('-Prompt', 'P101')
        Assert-True ($rn.Code -eq 0 -and $rn.Text -match 'P101 goes next after P100') ('a later pick waits behind the answered prompt: ' + $rn.Text)
        Assert-True ((Get-RunNext182 $w) -eq 'cc-P100-a.md') ('RUN-NEXT still names P100: ' + (Get-RunNext182 $w))
        $sj = Get-WStatus $w
        Assert-True ((@($sj.queued)[0] -eq 'cc-P100-a.md') -and (@($sj.queued)[1] -eq 'cc-P101-b.md')) ('the queue shows P100 then P101: ' + (@($sj.queued) -join ', '))
        $o = Invoke-HookX $w 'Prompt' @{ prompt = 'Golem, please work on the shard tasks.'; session_id = 'sess-n' } $w.CliArgs
        Assert-True (($o | ConvertFrom-Json).hookSpecificOutput.additionalContext -match 'cc-P100-a\.md in full') ('the woken session takes P100: ' + $o.Substring(0, [Math]::Min(300, $o.Length)))
        Assert-True ((Get-RunNext182 $w) -eq 'cc-P101-b.md' -and (Get-WLog $w) -match 'run next: P101 goes next now') ('then P101 is the pick: ' + (Get-RunNext182 $w))
        # Cancel while an answered prompt is held clears only the waiting pick.
        $w2 = New-AskWorld
        [void](Invoke-HookX $w2 'Stop' @{ last_assistant_message = 'P100 STOPPED: which world?'; session_id = 'sess-a' } $w2.CliArgs)
        [void](Invoke-Answer $w2 (@(Get-WQuestions $w2 'open'))[0].id 0 'x')
        [void](Invoke-Event182 $w2 'RunNext' @('-Prompt', 'P101'))
        [void](Invoke-Event182 $w2 'RunNext' @('-Cancel'))
        Assert-True ((Get-RunNext182 $w2) -eq 'cc-P100-a.md' -and -not (Test-Path -LiteralPath (Join-Path $w2.Root 'RUN-NEXT.after'))) ('cancel leaves the answered prompt first: ' + (Get-RunNext182 $w2))
    }
}
