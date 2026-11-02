
# ---- cc-P767: each lane on its own account ----------------------------------------------------------------------------

# The login a CODEX_HOME belongs to when -Account is not given: a lane's home is <Root>\codex-home\<login> (Join-Golem.ps1).
# Before this, `-Action status -CodexHome ...\lane-steph` read this PC's codex-usage.json (Chase's own readings) and took
# its newer reading over lane-steph's own (11-01: both lanes showed the same session log).
function Resolve-CodexAccount([string]$Root, [string]$CodexHomeDir, [string]$Acct) {
    if ($Acct) { return $Acct }
    $lanes = ((Join-Path $Root 'codex-home') -replace '/', '\').TrimEnd('\')
    $h = (([string]$CodexHomeDir) -replace '/', '\').TrimEnd('\')
    if (-not $h) { return '' }
    $parent = (Split-Path -Parent $h).TrimEnd('\')
    if ($parent -ieq $lanes) { return (Split-Path -Leaf $h) }
    ''
}

# The CODEX_HOME for a login when -CodexHome was left at this account's own ~\.codex: the lane's own home when there is one,
# so `-Account lane-steph` alone never reads Chase's session logs.
function Resolve-CodexHomeFor([string]$Root, [string]$CodexHomeDir, [string]$Acct, [string]$DefaultHome) {
    $h = (([string]$CodexHomeDir) -replace '/', '\').TrimEnd('\')
    if (-not $Acct -or ($h -and $h -ine ([string]$DefaultHome).TrimEnd('\'))) { return $CodexHomeDir }
    $lane = Join-Path $Root ('codex-home\' + ($Acct -replace '[^A-Za-z0-9_-]', ''))
    if (Test-Path -LiteralPath $lane -PathType Container) { return $lane }
    $CodexHomeDir
}

# How old a reading is, and whether it is fresh: taken within codexLimitsFreshMinutes (default 300, the 5-hour window).
# Not fresh: the state is "unknown" and the reading kept is the lane's last good one, with its age.
function Get-LimitsFreshness($Limits, $Settings, [datetime]$Now) {
    $fm = [double](Get-CodexProp $Settings 'codexLimitsFreshMinutes' 300)
    if (-not $Limits) { return [pscustomobject]@{ state = 'unknown'; ageMinutes = $null; note = 'unknown: no reading for this account yet (no session log in its own Codex homes)' } }
    $t = Get-LimitsTime $Limits
    if ($t -eq [DateTimeOffset]::MinValue) { return [pscustomobject]@{ state = 'unknown'; ageMinutes = $null; note = 'unknown: the last reading has no time (' + [string]$Limits.source + ')' } }
    $age = [Math]::Max(0, [Math]::Round(([DateTimeOffset]::new($Now) - $t).TotalMinutes, 0))
    if ($age -le $fm) { return [pscustomobject]@{ state = 'fresh'; ageMinutes = $age; note = 'fresh: ' + (Format-CodexAge $age) + ' old (' + [string]$Limits.source + ')' } }
    [pscustomobject]@{ state = 'unknown'; ageMinutes = $age; note = 'unknown: no session log of this account in the last ' + (Format-CodexAge $fm) + '; the last good reading is ' + (Format-CodexAge $age) + ' old (' + [string]$Limits.source + ')' }
}

function Format-CodexAge([double]$Minutes) {
    if ($Minutes -lt 60) { return ([string][int]$Minutes + ' min') }
    if ($Minutes -lt 2880) { return ('{0}h {1:D2}m' -f [int][Math]::Floor($Minutes / 60), [int]($Minutes % 60)) }
    ([string][Math]::Round($Minutes / 1440, 1) + ' days')
}

# One window as the lanes view shows it: used percent (0 once its reset has passed: a new window) and the reset time.
function Get-CodexWindowView($Window, [datetime]$Now) {
    if (-not $Window) { return [pscustomobject]@{ usedPct = $null; resets = 'unknown'; text = 'unknown' } }
    $nowU = [DateTimeOffset]::new($Now).ToUnixTimeSeconds()
    $r = [long](Get-CodexProp $Window 'resetsAt' 0)
    $passed = ($r -gt 0 -and $r -le $nowU)
    $used = $(if ($passed) { 0.0 } else { [double](Get-CodexProp $Window 'usedPct' 0) })
    $resets = $(if ($r -le 0) { 'unknown' } elseif ($passed) { 'reset already' } else { [DateTimeOffset]::FromUnixTimeSeconds($r).LocalDateTime.ToString('ddd HH:mm', $script:Inv) })
    [pscustomobject]@{ usedPct = $used; resets = $resets; text = ([string]$used + '% (resets ' + $resets + ')') }
}

# A lane's idle time today from its log's idle lines (golem.ps1 Write-LaneIdle, one per watch): each line counts until the
# next one, at most one watch (10 minutes), the last until now. By reason: "nothing claimable" (the summary of skipped
# prompts), budget, error, hours, backs off, queue empty, held, needs you, off.
function Get-LaneIdleToday([string]$LogFile, [string]$Name, [datetime]$Now, [int]$WatchMinutes = 10) {
    $res = [ordered]@{ minutes = 0; byReason = [ordered]@{}; last = ''; lastAt = '' }
    if (-not (Test-Path -LiteralPath $LogFile -PathType Leaf)) { return [pscustomobject]$res }
    $day = $Now.ToString('yyyy-MM-dd', $script:Inv)
    $tag = ' ' + $Name + ' idle: '
    $hits = New-Object System.Collections.Generic.List[object]
    try {
        foreach ($l in [IO.File]::ReadLines($LogFile)) {
            if (-not $l.StartsWith($day)) { continue }
            $i = $l.IndexOf($tag); if ($i -lt 0) { continue }
            $at = [datetime]::MinValue
            if (-not [datetime]::TryParseExact($l.Substring(0, 19), 'yyyy-MM-dd HH:mm:ss', $script:Inv, [Globalization.DateTimeStyles]::None, [ref]$at)) { continue }
            $hits.Add([pscustomobject]@{ at = $at; text = $l.Substring($i + $tag.Length) })
        }
    } catch { }
    for ($k = 0; $k -lt $hits.Count; $k++) {
        $end = $(if ($k + 1 -lt $hits.Count) { $hits[$k + 1].at } else { $Now })
        $m = [Math]::Max(0, [Math]::Min([double]$WatchMinutes, ($end - $hits[$k].at).TotalMinutes))
        $t = [string]$hits[$k].text
        $why = $(if ($t -match '^\d+ prompts?, 0 claimable') { 'nothing claimable' } elseif ($t -match '^([a-z][a-z ]*?):') { $Matches[1] } else { $t })
        if (-not $res.byReason.Contains($why)) { $res.byReason[$why] = 0.0 }
        $res.byReason[$why] = [double]$res.byReason[$why] + $m
        $res.minutes += $m
    }
    if ($hits.Count) { $res.last = [string]$hits[$hits.Count - 1].text; $res.lastAt = $hits[$hits.Count - 1].at.ToString('HH:mm', $script:Inv) }
    $res.minutes = [Math]::Round($res.minutes, 0)
    foreach ($k in @($res.byReason.Keys)) { $res.byReason[$k] = [Math]::Round([double]$res.byReason[$k], 0) }
    [pscustomobject]$res
}

# Every Codex lane in golems.json (engine codex, with its login), side by side: its own account's 5-hour and week windows,
# whether the reading is fresh, today's runs, and its idle time today with the reasons.
function Get-CodexLanesView([string]$Root, $Settings, [datetime]$Now) {
    $reg = $null
    try { $reg = [IO.File]::ReadAllText((Join-Path $Root 'golems.json')) | ConvertFrom-Json } catch { }
    $out = @()
    foreach ($g in @(Get-CodexProp $reg 'golems' @())) {
        if ([string](Get-CodexProp $g 'engine' '') -ne 'codex') { continue }
        $name = [string](Get-CodexProp $g 'name' ''); $acct = [string](Get-CodexProp $g 'account' '')
        if (-not $acct) { continue }
        $home2 = Join-Path $Root ('codex-home\' + $acct)
        $doc = Read-CodexUsageFile (Get-CodexUsagePath $Root $acct)
        $lim = Read-AccountRateLimits $home2 $Settings $acct $doc
        $fr = Get-LimitsFreshness $lim $Settings $Now
        $p = Get-CodexWindowView $(if ($lim) { $lim.primary } else { $null }) $Now
        $s = Get-CodexWindowView $(if ($lim) { $lim.secondary } else { $null }) $Now
        $idle = Get-LaneIdleToday (Join-Path $Root ('golem-' + $name + '.log')) $name $Now
        $why = ''
        try { $st = [IO.File]::ReadAllText((Join-Path $Root ('status-' + $name + '.json'))) | ConvertFrom-Json; $why = [string](Get-CodexProp $st 'current' (Get-CodexProp $st 'state' '')) } catch { }
        $today = $(if ($doc) { $doc.today } else { $null })
        $runsToday = $(if ($today -and [string]$today.date -eq $Now.ToString('yyyy-MM-dd', $script:Inv)) { [int]$today.runs } else { 0 })
        $reasons = @(); foreach ($k in @($idle.byReason.Keys)) { $reasons += ($k + ' ' + (Format-CodexAge ([double]$idle.byReason[$k]))) }
        $text = ('{0} ({1}): 5-hour {2}, week {3}; {4}; runs today {5}; idle today {6}{7}' -f $name, $acct, $p.text, $s.text, $fr.note, $runsToday,
            (Format-CodexAge ([double]$idle.minutes)), $(if ($reasons.Count) { ': ' + ($reasons -join ', ') } else { '' }))
        $out += [pscustomobject]@{ golem = $name; account = $acct; codexHome = $home2; enabled = [bool](Get-CodexProp $g 'enabled' $false)
            limitsState = $fr.state; limitsAgeMinutes = $fr.ageMinutes; limitsNote = $fr.note; source = $(if ($lim) { [string]$lim.source } else { '' })
            fiveHour = $p; week = $s; runsToday = $runsToday; idleTodayMinutes = $idle.minutes; idleByReason = $idle.byReason
            lastIdle = $(if ($idle.last) { $idle.lastAt + ' ' + $idle.last } else { '' }); status = $why; text = $text }
    }
    $out
}
