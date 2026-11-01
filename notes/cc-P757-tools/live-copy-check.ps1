#Requires -Version 5.1
<#
  cc-P757: the night usage rule on COPIES of the live usage files (never the live ones).
      powershell -NoProfile -ExecutionPolicy Bypass -File live-copy-check.ps1 -Hook <golem.ps1> -Copies <folder with usage.json and plan-usage.json> -Now 2026-11-01T00:16:53
  Pulls the usage functions out of the given golem.ps1 by name (as Golem.Tests.ps1 does), points $UsageFile and
  $PlanFile at the copies, and prints what Test-NightUsage (the night check's rule, with -AllowFallback when the hook
  has it) says at -Now. Settings are the hook's defaults for the night (nightUsageMaxAgeHours 24, planUsageMaxAgeHours 4,
  nightSessionMaxPct 50, nightWeekReservePct 10), marathon off.
#>
param([Parameter(Mandatory)][string]$Hook, [Parameter(Mandatory)][string]$Copies, [string]$Now = '')
$ErrorActionPreference = 'Stop'
$ast = [System.Management.Automation.Language.Parser]::ParseFile($Hook, [ref]$null, [ref]$null)
$want = 'Get-Prop', 'Get-PlanUsage', 'Get-Usage', 'Get-LastKnownWeek', 'Test-NightUsage', 'Get-WeekAllowance', 'Get-ModelFamily'
$text = ''
$defs = @($ast.FindAll({ param($x) $x -is [System.Management.Automation.Language.FunctionDefinitionAst] }, $true))
foreach ($n in $want) {
    $fn = $defs | Where-Object { $_.Name -eq $n } | Select-Object -First 1
    if ($fn) { $text += $fn.Extent.Text + "`n" } else { Write-Host ('(not in this golem.ps1: ' + $n + ')') }
}
. ([scriptblock]::Create($text))
$script:NowTime = $(if ($Now) { [datetime]$Now } else { Get-Date })
$UsageFile = Join-Path $Copies 'usage.json'
$PlanFile = Join-Path $Copies 'plan-usage.json'
function Get-Settings { [pscustomobject]@{ nightUsageMaxAgeHours = 24; planUsageMaxAgeHours = 4; nightSessionMaxPct = 50; nightWeekReservePct = 10; nightFableReservePct = 10; usageLimitPct = 95 } }
function Test-MarathonOn($s) { $false }
function Get-State { [pscustomobject]@{} }
$set = Get-Settings
$hasFallback = [bool]((Get-Command Test-NightUsage).Parameters.ContainsKey('AllowFallback'))
$r = $(if ($hasFallback) { Test-NightUsage $set 'Opus' -AllowFallback } else { Test-NightUsage $set 'Opus' })
'at ' + $NowTime.ToString('s') + ' (' + $Hook + ')'
'  Ok: ' + $r.Ok
'  Why: ' + $r.Why
'  Week: ' + $r.Week + '%  allowed: ' + $r.Allowed + '  5-hour: ' + $(if ($null -eq $r.Session) { 'not known' } else { [string]$r.Session + '%' })
if ($hasFallback) { '  Source: ' + $r.Source; '  Fallback: ' + $r.Fallback }
