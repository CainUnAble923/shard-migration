#Requires -Version 5.1
<#
  tazuo-walk.ps1 (cc-P732, from P722's isle-shots.ps1): a real character's first login and the isle's new steps in
  TazUO, on the private proof shard (127.0.0.1:2596 only; the caller holds the test-shard lock).

      powershell -NoProfile -ExecutionPolicy Bypass -File tazuo-walk.ps1 -Character "Iron Wakes" -Out <folder>

  1. A copy of the built client (D:\UO\tazuo-sl-build\client) with NO profiles: its Data\Profiles\default.json is
     written by the release branch's own launcher function (Launch-Settings.ps1, Initialize-NewProfileDefaults, P729),
     as Play.ps1 does before every start; the art PNGs and the map/records override as the package installs them.
  2. TazUO logs the character in (a fresh character: create_fresh.py made it and dropped the line at once) and runs
     Wake732.py by itself (Data\lscript.json GlobalAutoStartScripts).
  3. Each "SHOT <name>" the script writes to shots.sig becomes <Out>\<name>.jpg; one more frame every -EverySeconds.
  The character's new profile.json is copied to <Out> at the end (its last_version_history_shown).
#>
param(
    [Parameter(Mandatory)][string]$Character,
    [Parameter(Mandatory)][string]$Out,
    [string]$Repo = 'D:\UO\golems\Iron\ShatteredLegacy',   # cc-P732: the code copy (main: the SoS land)
    [string]$Work = 'D:\UO\golems\Iron\p732-proof\tazuo',
    [string]$ClientSource = 'D:\UO\tazuo-sl-build\client',
    [int]$Port = 2596,
    [int]$MaxMinutes = 20,
    [int]$EverySeconds = 30,
    [switch]$Prepare,   # only set up the client (fresh profiles, script, override), for ui.ps1 to start it
    [switch]$Attach     # no setup or start: watch the TazUO ui.ps1 started (p732-proof\ui.pid) for its shots
)
$ErrorActionPreference = 'Continue'
. 'D:\UO\golem\LegionTest.ps1'
New-Item -ItemType Directory -Path $Out, $Work -Force | Out-Null
function Say([string]$t) { $l = '[' + (Get-Date).ToString('HH:mm:ss') + '] ' + $t; Write-Host $l; Add-Content -LiteralPath (Join-Path $Out 'runner-log.txt') -Value $l -Encoding ASCII }

$guard = Test-LegionTarget '127.0.0.1' $Port
if (-not $guard.Ok -or $Port -lt 2595) { Say ('refused: ' + $guard.Why); exit 2 }
Say $guard.Why

# 1. the client, fresh
$client = Join-Path $Work 'client'
$profiles = Join-Path $client 'Data\Profiles'
$settings = Join-Path $client 'settings.p732.json'
$sig = 'D:\UO\golems\Iron\p732-proof\shots.sig'
if (-not $Attach) {
if (Test-Path $client) { Remove-Item -Recurse -Force $client }
[void](& robocopy $ClientSource $client /MIR /XD Data LegionScripts Logs Screenshots /NFL /NDL /NJH /NJS /NP /R:1 /W:1)
$artOut = Join-Path $client 'ExternalImages\art'
New-Item -ItemType Directory -Path $artOut -Force | Out-Null
Copy-Item -Path (Join-Path $Repo 'player-package\vendor\shattered-legacy-art\art\*.png') -Destination $artOut -Force
. (Join-Path $Repo 'player-package\payload\app\Launch-Settings.ps1')
$wrote = Initialize-NewProfileDefaults -ProfilesDir $profiles -ClientDir $client
Say ('default.json written by the launcher: ' + $wrote + ': ' + ((Get-Content -Raw (Join-Path $profiles 'default.json')) -replace '\s+', ' '))
Say ('profiles before login: ' + (@(Get-ChildItem -LiteralPath $profiles -Recurse -File | ForEach-Object { $_.FullName.Substring($profiles.Length) }) -join ', '))

$ovDir = Join-Path $Work 'uo-override'
$override = & (Join-Path $Repo 'player-package\payload\app\Build-UoOverrides.ps1') -UoDir 'D:\UO\UltimaOnlineVanilla' `
    -MapOps (Join-Path $Repo 'player-package\vendor\shattered-legacy-map\trammel.mapops') `
    -Records (Join-Path $Repo 'player-package\vendor\shattered-legacy-art\records.json') -OutDir $ovDir `
    -MapBase (Join-Path $Repo 'player-package\vendor\sos-trammel-map\files')   # cc-P732: main's land is the SoS map
Say ('override: ' + $override)

# 2. the script and the login
$ls = Join-Path $client 'LegionScripts'
New-Item -ItemType Directory -Path $ls -Force | Out-Null
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'Wake732.py') -Destination $ls -Force
[IO.File]::WriteAllText((Join-Path $client 'Data\lscript.json'), (@{ GlobalAutoStartScripts = @('Wake732.py'); CharAutoStartScripts = @{}; GroupCollapsed = @{}; DisableModuleCache = $false } | ConvertTo-Json -Depth 4), (New-Object Text.UTF8Encoding($false)))
Set-Content -LiteralPath $sig -Value '' -Encoding ASCII
if ($Prepare) { Say 'prepared'; exit 0 }
$acc = (& powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'D:\UO\golem\Get-GolemTestAccount.ps1' -Golem Iron -Role player -Json 2>$null | Select-Object -Last 1) | ConvertFrom-Json
$set = New-LegionSettings '127.0.0.1' $Port ([string]$acc.Username) (ConvertTo-CuoPassword ([string]$acc.Password)) 'D:\UO\UltimaOnlineVanilla'
[IO.File]::WriteAllText($settings, ($set | ConvertTo-Json -Depth 6), (New-Object Text.UTF8Encoding($false)))
$acc = $null
$argv = @('-settings', ('"' + $settings + '"'), '-skiploginscreen', '-skipserverselect', '-lastcharactername', ('"' + $Character + '"'), '-uofilesoverride', ('"' + $override + '"'))
$proc = Start-Process -FilePath (Join-Path $client 'TazUO.exe') -ArgumentList $argv -WorkingDirectory $client -PassThru
Say ('TazUO started, pid ' + $proc.Id)
} else {
    $proc = Get-Process -Id ([int](Get-Content 'D:\UO\golems\Iron\p732-proof\ui.pid'))
    Say ('watching TazUO pid ' + $proc.Id)
}

# 3. the shots
$seen = 0; $n = 0; $t0 = Get-Date; $next = $t0.AddSeconds(10)
try {
    while (((Get-Date) - $t0).TotalMinutes -lt $MaxMinutes -and -not $proc.HasExited) {
        Start-Sleep -Milliseconds 500
        $proc.Refresh()
        $lines = @(Get-Content -LiteralPath $sig -ErrorAction SilentlyContinue | Where-Object { $_ })
        for ($i = $seen; $i -lt $lines.Count; $i++) {
            if ($lines[$i] -eq 'END') { Say 'the script ended'; $t0 = [datetime]::MinValue; break }
            $name = ($lines[$i] -replace '^SHOT ', '')
            $p = Join-Path $Out ($name + '.jpg')
            if (Save-LegionShot $proc.MainWindowHandle $p) { Say ('shot: ' + $p) } else { Say ('no window for ' + $name) }
        }
        $seen = $lines.Count
        if ((Get-Date) -ge $next) {
            $n++
            [void](Save-LegionShot $proc.MainWindowHandle (Join-Path $Out ('frame-{0:D3}.jpg' -f $n)))
            $next = (Get-Date).AddSeconds($EverySeconds)
        }
    }
} finally {
    Start-Sleep -Seconds 2
    try { $proc.CloseMainWindow() | Out-Null; Start-Sleep -Seconds 5; if (-not $proc.HasExited) { $proc.Kill() } } catch {}
    try { $j = Get-Content -LiteralPath $settings -Raw | ConvertFrom-Json; $j.password = ''; $j.autologin = $false; [IO.File]::WriteAllText($settings, ($j | ConvertTo-Json -Depth 6), (New-Object Text.UTF8Encoding($false))) } catch {}
    foreach ($pf in @(Get-ChildItem -LiteralPath $profiles -Recurse -Filter 'profile.json' -ErrorAction SilentlyContinue)) {
        $v = (Get-Content -Raw $pf.FullName | ConvertFrom-Json).last_version_history_shown
        Say ('new profile ' + $pf.FullName.Substring($profiles.Length) + ': last_version_history_shown = ' + $v)
        Copy-Item -LiteralPath $pf.FullName -Destination (Join-Path $Out 'profile.json') -Force
    }
    Copy-Item -LiteralPath 'D:\UO\golems\Iron\p732-proof\walk.log' -Destination $Out -Force -ErrorAction SilentlyContinue
}
Say 'done'
