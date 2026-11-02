import os, sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kit770'))


def edit(path, pairs):
    raw = open(path, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in raw else '\n'
    s = raw.replace('\r\n', '\n')
    for old, new in pairs:
        n = s.count(old)
        if n != 1:
            sys.exit('%s: %d matches for %r' % (path, n, old[:90]))
        s = s.replace(old, new)
    open(path, 'w', encoding='utf-8', newline='').write(s.replace('\n', nl))
    print('edited', path, repr(nl))


# ---------------------------------------------------------------- golem.ps1
edit('golem.ps1', [
# A: an idle Golem with a run-next pick in its queue wakes for it at the watch.
(r"""    if (-not $cur) { Write-Status; exit 0 }
    $p = Get-Progress""",
r"""    # cc-P770: a Run next pick for an idle Golem is honored at the next watch: the Golem wakes for it. Before this only a
    # hand-off read RUN-NEXT, so a pick set while the Golem rested waited until someone woke it (Gold, 11-01: P766 at 11:21
    # and P768 at 17:20 sat unclaimed for hours). Not while rested by hand, winding down, waiting for Chase, a wake already
    # on its way, or within 10 minutes of the last self-wake; Test-SelfWake's own rules (usage, pace, spacing) still hold.
    if (-not $cur -and (Get-RunNextName) -and -not (Get-Prop $st 'wakePending' $null) -and -not [bool](Get-Prop $st 'stoppedByHand' $false) -and
        -not [string](Get-Prop $st 'stoppedPrompt' '') -and [string](Get-Prop $st 'restReason' '') -notin @('wrap up', 'stopping point') -and -not [string](Get-Prop $st 'winding' '')) {
        $rnPick = Get-RunNextName
        $lwR = Get-Prop $st 'lastSelfWake' $null
        $recentR = $false; if ($lwR) { try { $recentR = (($NowTime - [datetime]::Parse([string]$lwR.at)).TotalMinutes -lt 10) } catch {} }
        if (-not $recentR) {
            $tgP = Get-WakeTarget $st   # syncs a git queue first; the pick sorts first when it is still queued and this Golem may take it
            $rnN = [regex]::Match($rnPick, '^cc-P(\d+)-').Groups[1].Value
            if ($tgP -and $rnN -and $tgP.For -eq ('P' + $rnN)) {
                Log ("run next: P$rnN is picked and the Golem is idle: waking for it")
                $r = Invoke-SelfWake $st 'run next' $tgP.For $tgP.Model
                if ($r.Ok) { Write-Status ''; exit 0 }
            } elseif ([string](Get-Prop $st 'runNextSkipNoted' '') -ne $rnPick) {
                $why = $(if (-not (Test-Path -LiteralPath (Join-Path $QueueDir $rnPick))) { 'it is no longer in the queue' } elseif ($tgP) { 'this Golem may not take it now; ' + $tgP.For + ' would go first' } else { 'this Golem may not take it now (see the claim lines)' })
                Log ("run next: $rnPick is picked but not woken for: $why")
                $st | Add-Member -NotePropertyName runNextSkipNoted -NotePropertyValue $rnPick -Force
                Save-State $st
            }
        }
    }
    if (-not $cur) { Write-Status; exit 0 }
    $p = Get-Progress"""),
# RunNext: the queue as origin has it before looking the prompt up (a family PC's clone only pulls at a claim).
(r"""    $pf = $(if ($Prompt) { Find-PromptFile $QueueDir $Prompt } else { $null })
    if (-not $pf) { [Console]::Out.Write(("Not changed: '{0}' is not in the queue ({1}). Only a queued prompt can go next; the running one and finished ones cannot." -f $Prompt, $QueueDir)); exit 1 }""",
r"""    if ($script:QueueMode -eq 'git' -and -not $DryRun) { Sync-PromptsGit $PromptDir }   # cc-P770: an idle Golem's clone only pulls at a claim
    $pf = $(if ($Prompt) { Find-PromptFile $QueueDir $Prompt } else { $null })
    if (-not $pf) { [Console]::Out.Write(("Not changed: '{0}' is not in the queue ({1}). Only a queued prompt can go next; the running one and finished ones cannot." -f $Prompt, $QueueDir)); exit 1 }"""),
# C: a retry's move back to the queue reaches origin in git mode.
(r"""        Move-Item -LiteralPath $pf.FullName -Destination (Join-Path $QueueDir $pf.Name)
        Remove-Item -LiteralPath ($pf.FullName + '.claim.json') -Force -ErrorAction SilentlyContinue
        if ($Multi) { Remove-ClaimToken $PromptDir $pf.Name }
    }""",
r"""        Move-Item -LiteralPath $pf.FullName -Destination (Join-Path $QueueDir $pf.Name)
        Remove-Item -LiteralPath ($pf.FullName + '.claim.json') -Force -ErrorAction SilentlyContinue
        if ($Multi) { Remove-ClaimToken $PromptDir $pf.Name }
        # cc-P770: in git mode the move is committed and pushed like every other queue change. Left uncommitted (Gold, 11-01
        # 14:39), it made every later pull fail, and the clone's queue stayed as it was for the rest of the day.
        if ($script:QueueMode -eq 'git' -and $HandedDir -like ($PromptDir.TrimEnd('\') + '\*')) {
            if (-not (Invoke-PromptsGit $PromptDir "$sp back in the queue: retried by $(if ($script:Me) { [string]$script:Me.name } else { 'the Golem' })")) { Log "retry: the push of $sp's move was rejected; the next sync takes origin's queue" }
        }
    }"""),
])

# ---------------------------------------------------------------- Golems.ps1 (B)
edit('Golems.ps1', [
(r"""    $p = Invoke-Git $PromptDir @('pull', '-q', '--rebase')
    # cc-P370: a pull whose rebase stopped (an unpushed claim that conflicts) used to stay stopped: the clone sat detached
    # mid-rebase and its queue went stale ("nothing for Copper", 10-21). Put it back on origin/main at once.
    if ($p.Code -ne 0) { [void](Repair-PromptsClone $PromptDir) }
}""",
r"""    $p = Invoke-Git $PromptDir @('pull', '-q', '--rebase')
    # cc-P370: a pull whose rebase stopped (an unpushed claim that conflicts) used to stay stopped: the clone sat detached
    # mid-rebase and its queue went stale ("nothing for Copper", 10-21). Put it back on origin/main at once.
    if ($p.Code -ne 0 -and -not (Repair-PromptsClone $PromptDir)) { [void](Reset-DirtyPromptsClone $PromptDir) }
}
# cc-P770: a clone on main whose pull fails because of changes never committed (Gold, 11-01: a retry's move of P765, made
# without a commit, failed every pull after 14:39 and froze its queue). In git mode every queue change is committed and
# pushed at once, so an uncommitted one is a change that never landed: as with an unpushed claim (cc-P370), origin's queue
# wins. The dropped paths are logged. Returns them ('' when the clone was clean).
function Reset-DirtyPromptsClone([string]$PromptDir) {
    if (-not (Test-Path -LiteralPath (Join-Path $PromptDir '.git'))) { return '' }
    $dirty = @(((Invoke-Git $PromptDir @('status', '--porcelain')).Text -split "`r?`n") | Where-Object { $_.Trim() })
    if (-not $dirty.Count) { return '' }
    $f = Invoke-Git $PromptDir @('fetch', '-q', 'origin')
    $r = Invoke-Git $PromptDir @('reset', '-q', '--hard', 'origin/main')
    $c = Invoke-Git $PromptDir @('clean', '-q', '-f', '-d', '--', 'queue', 'claimed', 'merging')
    $what = (@($dirty | ForEach-Object { $_.Trim() }) -join '; ')
    Write-GolemLog ('prompts clone: a pull failed on uncommitted changes; reset to origin/main and dropped ' + $what + $(if ($r.Code -ne 0) { ' (the reset failed: ' + $r.Text.Trim() + ')' } else { '' }))
    $what
}"""),
])

# ---------------------------------------------------------------- Set-RunNext.ps1 (D)
edit('Set-RunNext.ps1', [
(r"""$a = @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', (Join-Path $Root 'golem.ps1'), '-Event', 'RunNext', '-Root', $Root)""",
r"""# cc-P770: a Golem on another PC reads its own RUN-NEXT there. Writing one here did nothing for it (Gold, 11-01): the pick
# goes to that PC's agent as the web console's Run next does, and it honors it at once (Remote-Agent.ps1 runs its watch).
if ($Golem) {
    . (Join-Path $Root 'Golems.ps1')
    $reg = $null; try { $reg = Read-GolemRegistry (Join-Path $Root 'golems.json') } catch {}
    $g = $(if ($reg) { Get-GolemByName $reg $Golem } else { $null })
    if ($g -and -not (Test-GolemLocal $g)) {
        if (-not $Cancel -and $Prompt -notmatch '^(?i)P?\d{1,4}$') { Write-Host ("Not changed: '" + $Prompt + "' is not a prompt number (P<nn>).") -ForegroundColor Yellow; exit 1 }
        $pn = $(if ($Cancel) { '' } else { 'P' + ($Prompt -replace '^(?i)P', '') })
        $f = Add-RemoteCommand $Root ([string]$g.name) $(if ($Cancel) { 'runnext-cancel' } else { 'runnext' }) $(if ($Cancel) { 'Cancel Run next' } else { 'Run next ' + $pn }) ('Set-RunNext on ' + $env:COMPUTERNAME) (Get-Date) 30 $(if ($Cancel) { @{} } else { @{ prompt = $pn } })
        Write-Host ($(if ($Cancel) { 'Run next cancel' } else { $pn + ' as Run next' }) + ' sent to ' + [string]$g.name + "'s agent on " + [string]$g.machine + ' (' + $f + '). It is set there at the agent''s next poll, and the Golem wakes for it if it is idle.') -ForegroundColor Green
        exit 0
    }
}
$a = @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', (Join-Path $Root 'golem.ps1'), '-Event', 'RunNext', '-Root', $Root)"""),
])

# ---------------------------------------------------------------- Assign-Prompt.ps1 (D)
edit('Assign-Prompt.ps1', [
(r"""if ($RunNext) {
    $a = @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', (Join-Path $Kit 'golem.ps1'), '-Event', 'RunNext', '-Root', $Root, '-Prompt', ('P' + $num), '-PromptDir', $PromptDir)""",
r"""if ($RunNext) {
    # cc-P770: a Golem on another PC gets the pick through its agent (Set-RunNext.ps1 sends it there).
    $gR = $(if (-not $isInt) { $g } else { $null })
    if ($gR -and -not (Test-GolemLocal $gR)) {
        $r = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $Kit 'Set-RunNext.ps1') -Prompt ('P' + $num) -Golem $name -Root $Root
        $code = $LASTEXITCODE
        Write-Host ([string]($r -join "`r`n")) -ForegroundColor $(if ($code -eq 0) { 'Green' } else { 'Yellow' })
        exit $(if ($code -eq 0) { 0 } else { 1 })
    }
    $a = @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', (Join-Path $Kit 'golem.ps1'), '-Event', 'RunNext', '-Root', $Root, '-Prompt', ('P' + $num), '-PromptDir', $PromptDir)"""),
])
