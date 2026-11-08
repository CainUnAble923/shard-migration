#Requires -Version 5.1
<#
  Test-GameRunning.ps1 (cc-P819): the one game check every bot uses on the game PC (GamePause.ps1 beside it).

      powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Test-GameRunning.ps1
          [-Wait] [-Until HH:mm] [-IntervalSeconds 600] [-Who <golem or bot>] [-What "<what waits>"] [-Root D:\UO\golem]

  Without -Wait: one line and an exit code.
      0  go on: no game running, or the pause does not apply here (off in settings.json, or not the game PC)
      1  a game is running: "waiting: Chase is playing <game>"
  With -Wait: waits while a game runs (GamePause.ps1 Wait-GolemNoGame), one log line at the start, per game change and
  at the end; keeps game-wait-<Who>.json in the kit root meanwhile (the consoles' status line).
      0  the game closed (or the pause was turned off): go on
      1  still playing at -Until: skip
  -Until HH:mm is today's, or tomorrow's when that time has passed today (a night bot started at 23:00 with -Until
  06:30 waits to the next morning). Exit 2 on a bad argument. A Golem in a Claude Code session runs -Wait in the
  background (a foreground command is cut off at 10 minutes) and goes on when it exits. ASCII only.
#>
param(
    [switch]$Wait,
    [string]$Until = '',
    [int]$IntervalSeconds = 600,
    [string]$Who = '',
    [string]$What = 'play testing',
    [string]$Root = ''
)
if (-not $Root) { $Root = $(if ($PSScriptRoot) { $PSScriptRoot } else { 'D:\UO\golem' }) }
. (Join-Path $PSScriptRoot 'GamePause.ps1')
if (-not $Who) { $Who = $(if ($env:GOLEM_NAME) { $env:GOLEM_NAME } else { 'bot' }) }

$untilAt = $null
if ($Until) {
    if ($Until -notmatch '^\s*(\d{1,2}):(\d{2})\s*$') { Write-Output ("not a time (HH:mm): '" + $Until + "'"); exit 2 }
    $untilAt = (Get-Date).Date.AddHours([int]$Matches[1]).AddMinutes([int]$Matches[2])
    if ($untilAt -le (Get-Date)) { $untilAt = $untilAt.AddDays(1) }
}

if (-not $Wait) {
    $st = Get-GamePauseState -Root $Root
    Write-Output $st.Why
    exit $(if ($st.Applies -and $st.Running) { 1 } else { 0 })
}

$r = Wait-GolemNoGame -Root $Root -Who $Who -What $What -Until $untilAt -IntervalSeconds $IntervalSeconds `
    -Log { param($t) [Console]::Out.WriteLine((Get-Date).ToString('yyyy-MM-dd HH:mm:ss') + ' ' + $t) }   # not the pipeline: that would join the result
if ($r.Outcome -in @('clear', 'off', 'elsewhere')) {
    if ($r.Waited -eq [TimeSpan]::Zero) { Write-Output $r.Why }
    exit 0
}
exit 1
