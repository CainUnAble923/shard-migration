#Requires -Version 5.1
<#
  shots.ps1 (cc-P675, from P661 proof2.ps1, from P265's proof.ps1): per scene, the Golem's Admin types the scene's commands (P219's
  uobot.legionsetup), the shard is optionally restarted, then BOTH of the Golem's characters log in at once in two
  TazUO windows (the Player "<Golem> the Tester" and the Admin "<Golem>") and each window is captured.
  The caller holds the test-shard lock and runs a PRIVATE shard (proof-shard.ps1) on -Port. ASCII only.
#>
param(
    [Parameter(Mandatory)][string]$Spec,
    [Parameter(Mandatory)][string]$Out,
    [string]$CodeRepo = 'D:\UO\golems\Iron\ShatteredLegacy',
    [string]$Work = (Join-Path $env:TEMP 'p675-proof'),
    [string]$TargetHost = '127.0.0.1',
    [int]$Port = 2596,
    [string]$Golem = 'Iron',
    [string]$Container = 'sl-p675-proof',
    [int]$SettleSeconds = 30,
    [string]$ClientSource = 'D:\UO\golems\Iron\tazuo-p670\client'   # cc-P675: P674's client build (patch 0008); the shared one is stale
)
$ErrorActionPreference = 'Continue'
. 'D:\UO\golem\LegionTest.ps1'
function Say([string]$t) { $l = '[' + (Get-Date).ToString('HH:mm:ss') + '] ' + $t; Write-Host $l; Add-Content -LiteralPath (Join-Path $Out 'proof-log.txt') -Value $l -Encoding ASCII }
New-Item -ItemType Directory -Path $Out, $Work -Force | Out-Null
if ($Port -lt 2595 -or $Port -gt 2599) { Say "port $Port refused: private shards only (2595-2599)"; exit 2 }
$guard = Test-LegionTarget $TargetHost $Port
if (-not $guard.Ok) { Say $guard.Why; exit 2 }
Say $guard.Why
$Bot = Join-Path $CodeRepo 'tools\playtest-bot'

# Two client copies, so the two windows never share a log or settings file.
$roles = @(
    @{ Role = 'player'; Char = ($Golem + ' the Tester'); Dir = (Join-Path $Work 'client-player') },
    @{ Role = 'admin'; Char = $Golem; Dir = (Join-Path $Work 'client-admin') }
)
$profSrc = 'D:\UO\golem\legion-test\Iron\client\Data\Profiles'
foreach ($r in $roles) {
    [void](& robocopy $ClientSource $r.Dir /MIR /XD Data LegionScripts Logs Screenshots /NFL /NDL /NJH /NJS /NP /R:1 /W:1)
    $artOut = Join-Path $r.Dir 'ExternalImages\art'
    New-Item -ItemType Directory -Path $artOut -Force | Out-Null
    Copy-Item -Path (Join-Path $CodeRepo 'player-package\vendor\shattered-legacy-art\art\*.png') -Destination $artOut -Force
    $profDst = Join-Path $r.Dir 'Data\Profiles'
    [void](& robocopy $profSrc $profDst /E /NFL /NDL /NJH /NJS /NP /R:1 /W:1)
    foreach ($pf in @(Get-ChildItem -LiteralPath $profDst -Recurse -Filter 'profile.json')) {
        $j = Get-Content -LiteralPath $pf.FullName -Raw | ConvertFrom-Json
        $j.game_window_full_size = $true
        $j.game_window_position = [pscustomobject]@{ X = 0; Y = 0 }
        [IO.File]::WriteAllText($pf.FullName, ($j | ConvertTo-Json -Depth 20), (New-Object Text.UTF8Encoding($false)))
    }
}
$ovDir = Join-Path $Work 'uo-override'
$override = & (Join-Path $CodeRepo 'player-package\payload\app\Build-UoOverrides.ps1') -UoDir 'D:\UO\UltimaOnlineVanilla' `
    -Records (Join-Path $CodeRepo 'player-package\vendor\shattered-legacy-art\records.json') -OutDir $ovDir `
    -MapOps (Join-Path $CodeRepo 'player-package\vendor\shattered-legacy-map\trammel.mapops') `
    -MapBase (Join-Path $CodeRepo 'player-package\vendor\sos-trammel-map\files')   # cc-P675: S1's client on the SoS land, Trammel and Felucca
Say ('override: ' + $override)

$scenes = Get-Content -LiteralPath $Spec -Raw | ConvertFrom-Json
foreach ($s in $scenes) {
    Say ('--- ' + $s.name)
    $cf = Join-Path $Work ($s.name + '-commands.json')
    [IO.File]::WriteAllText($cf, (ConvertTo-Json @(@($s.commands) | ForEach-Object { [string]$_ })), (New-Object Text.UTF8Encoding($false)))
    Push-Location $Bot
    try { $sj = (& python -B -m uobot.legionsetup --host $TargetHost --port $Port --golem $Golem --commands $cf --out $Work 2>&1 | Out-String).Trim() } finally { Pop-Location }
    $line = @($sj -split "`r?`n" | Where-Object { $_ -match '^\{' }) | Select-Object -Last 1
    $sr = $null; try { $sr = $line | ConvertFrom-Json } catch {}
    if (-not $sr) { Say ('setup gave no result: ' + $sj); continue }
    foreach ($c in @($sr.commands)) { Say ('  ' + $c.command); foreach ($rp in @($c.replies)) { Say ('      ' + $rp) } }
    if (-not $sr.ok) { Say ('  setup not ok: ' + $sr.why) }

    if ($s.restart) {
        Start-Sleep -Seconds 5
        $since = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
        Say ('  restarting ' + $Container)
        docker restart $Container | Out-Null
        $up = $false
        for ($i = 0; $i -lt 120; $i++) {
            Start-Sleep -Seconds 2
            $l = docker logs --since $since $Container 2>&1 | Out-String
            if ($l -match 'Listening') { $up = $true; break }
        }
        $fold = @(docker logs --since $since $Container 2>&1 | Select-String -Pattern 'Fold|Saved map check|World: Loaded|Loading world')
        foreach ($f in $fold) { Say ('      log: ' + $f.Line.Trim()) }
        Say ('  restarted, up: ' + $up)
        Start-Sleep -Seconds 5
    }

    $procs = @()
    foreach ($r in $roles) {
        $acc = (& powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'D:\UO\golem\Get-GolemTestAccount.ps1' -Golem $Golem -Role $r.Role -Json 2>$null | Select-Object -Last 1) | ConvertFrom-Json
        $settings = Join-Path $r.Dir 'settings.p675.json'
        $set = New-LegionSettings $TargetHost $Port ([string]$acc.Username) (ConvertTo-CuoPassword ([string]$acc.Password)) 'D:\UO\UltimaOnlineVanilla'
        $acc = $null
        [IO.File]::WriteAllText($settings, ($set | ConvertTo-Json -Depth 6), (New-Object Text.UTF8Encoding($false)))
        $argv = @('-settings', ('"' + $settings + '"'), '-skiploginscreen', '-skipserverselect', '-lastcharactername', ('"' + $r.Char + '"'), '-uofilesoverride', ('"' + $override + '"'))
        $procs += , @{ R = $r; Settings = $settings; P = (Start-Process -FilePath (Join-Path $r.Dir 'TazUO.exe') -ArgumentList $argv -WorkingDirectory $r.Dir -PassThru) }
        Start-Sleep -Seconds 4
    }
    try {
        Start-Sleep -Seconds $SettleSeconds
        foreach ($x in $procs) {
            $x.P.Refresh()
            $p = Join-Path $Out ($s.name + '-' + $x.R.Role + '.jpg')
            if (Save-LegionShot $x.P.MainWindowHandle $p) { Say ('  shot: ' + $p) } else { Say ('  no window to capture for ' + $x.R.Role) }
        }
    } finally {
        foreach ($x in $procs) {
            try { $x.P.CloseMainWindow() | Out-Null; Start-Sleep -Seconds 3; if (-not $x.P.HasExited) { $x.P.Kill() } } catch {}
            try { $j = Get-Content -LiteralPath $x.Settings -Raw | ConvertFrom-Json; $j.password = ''; $j.autologin = $false; [IO.File]::WriteAllText($x.Settings, ($j | ConvertTo-Json -Depth 6), (New-Object Text.UTF8Encoding($false))) } catch {}
        }
    }
    Start-Sleep -Seconds 3
}
Say 'done'
