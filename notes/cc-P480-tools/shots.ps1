#Requires -Version 5.1
<#
  shots.ps1 (cc-P480): client screenshots of the tutorial on the PRIVATE scratch shard, in our TazUO, for Chase.

      powershell -NoProfile -ExecutionPolicy Bypass -File shots.ps1 -Mode companion|core -Out <folder> -Work <scratch>
          [-Character "Iron Arrival"] [-Port 2596]

  A copy of D:\UO\tazuo-sl-build\client (as cc-P265's proof.ps1 and P219's Test-LegionScript.ps1 make one) with this
  branch's art and the package's uo overrides, P219's Iron profile with the game window filling the client, and
  P480Shots.py started by itself in the world (Data\lscript.json). The script plays (walk to Rook, double-click, press)
  and asks for each picture; this harness captures the window (P219's Save-LegionShot) into <Out>\<mode>-<name>.jpg.
  Test ports only (Test-LegionTarget). The password is cleared from the client's settings file afterwards. ASCII only.
#>
param(
    [Parameter(Mandatory)][ValidateSet('companion', 'core')][string]$Mode,
    [Parameter(Mandatory)][string]$Out,
    [Parameter(Mandatory)][string]$Work,
    [string]$Character = 'Iron Arrival',
    [string]$CodeRepo = 'D:\UO\golems\Iron\ShatteredLegacy',
    [string]$TargetHost = '127.0.0.1',
    [int]$Port = 2596,
    [string]$Golem = 'Iron'
)
$ErrorActionPreference = 'Continue'
. 'D:\UO\golem\LegionTest.ps1'
New-Item -ItemType Directory -Path $Out, $Work -Force | Out-Null
$logFile = Join-Path $Out 'shots-log.txt'
function Say([string]$t) { $l = '[' + (Get-Date).ToString('HH:mm:ss') + '] ' + $t; Write-Host $l; Add-Content -LiteralPath $logFile -Value $l -Encoding ASCII }

$guard = Test-LegionTarget $TargetHost $Port
if (-not $guard.Ok) { Say $guard.Why; exit 2 }
Say ($Mode + ': ' + $guard.Why)

$client = Join-Path $Work 'client'
[void](& robocopy 'D:\UO\tazuo-sl-build\client' $client /MIR /XD Data LegionScripts Logs Screenshots /NFL /NDL /NJH /NJS /NP /R:1 /W:1)
$artOut = Join-Path $client 'ExternalImages\art'
New-Item -ItemType Directory -Path $artOut -Force | Out-Null
Copy-Item -Path (Join-Path $CodeRepo 'player-package\vendor\shattered-legacy-art\art\*.png') -Destination $artOut -Force
$profDst = Join-Path $client 'Data\Profiles'
[void](& robocopy 'D:\UO\golem\legion-test\Iron\client\Data\Profiles' $profDst /E /NFL /NDL /NJH /NJS /NP /R:1 /W:1)
foreach ($pf in @(Get-ChildItem -LiteralPath $profDst -Recurse -Filter 'profile.json')) {
    $j = Get-Content -LiteralPath $pf.FullName -Raw | ConvertFrom-Json
    $j.game_window_full_size = $true
    $j.game_window_position = [pscustomobject]@{ X = 0; Y = 0 }
    [IO.File]::WriteAllText($pf.FullName, ($j | ConvertTo-Json -Depth 20), (New-Object Text.UTF8Encoding($false)))
}
$ovDir = Join-Path $Work 'uo-override'
$override = & (Join-Path $CodeRepo 'player-package\payload\app\Build-UoOverrides.ps1') -UoDir 'D:\UO\UltimaOnlineVanilla' `
    -Records (Join-Path $CodeRepo 'player-package\vendor\shattered-legacy-art\records.json') -OutDir $ovDir

# the Legion script, started by itself
$run = Join-Path $Work ('run-' + $Mode)
if (Test-Path $run) { Remove-Item -Recurse -Force $run }
New-Item -ItemType Directory -Path $run -Force | Out-Null
Set-Content -LiteralPath (Join-Path $run 'mode.txt') -Value $Mode -Encoding ASCII
$ls = Join-Path $client 'LegionScripts'
New-Item -ItemType Directory -Path $ls -Force | Out-Null
$src = [IO.File]::ReadAllText((Join-Path $PSScriptRoot 'P480Shots.py')).Replace('@RUN_DIR@', $run)
[IO.File]::WriteAllText((Join-Path $ls 'P480Shots.py'), $src, (New-Object Text.UTF8Encoding($false)))
[IO.File]::WriteAllText((Join-Path $client 'Data\lscript.json'), (@{ GlobalAutoStartScripts = @('P480Shots.py'); CharAutoStartScripts = @{}; GroupCollapsed = @{}; DisableModuleCache = $false } | ConvertTo-Json -Depth 4), (New-Object Text.UTF8Encoding($false)))

$acc = (& powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'D:\UO\golem\Get-GolemTestAccount.ps1' -Golem $Golem -Role player -Json 2>$null | Select-Object -Last 1) | ConvertFrom-Json
$settings = Join-Path $client 'settings.p480.json'
$set = New-LegionSettings $TargetHost $Port ([string]$acc.Username) (ConvertTo-CuoPassword ([string]$acc.Password)) 'D:\UO\UltimaOnlineVanilla'
$acc = $null
[IO.File]::WriteAllText($settings, ($set | ConvertTo-Json -Depth 6), (New-Object Text.UTF8Encoding($false)))
$argv = @('-settings', ('"' + $settings + '"'), '-skiploginscreen', '-skipserverselect', '-lastcharactername', ('"' + $Character + '"'), '-uofilesoverride', ('"' + $override + '"'))
$proc = Start-Process -FilePath (Join-Path $client 'TazUO.exe') -ArgumentList $argv -WorkingDirectory $client -PassThru
Say ('TazUO started (process ' + $proc.Id + '), logging in ' + $Character)
$statusFile = Join-Path $run 'status.json'
$t0 = Get-Date
$taken = @{}
try {
    while (((Get-Date) - $t0).TotalMinutes -lt 6) {
        if ($proc.HasExited) { Say ('TazUO exited (' + $proc.ExitCode + ')'); break }
        $st = $null
        if (Test-Path -LiteralPath $statusFile) { try { $st = Get-Content -LiteralPath $statusFile -Raw | ConvertFrom-Json } catch {} }
        if ($st -and $st.state -eq 'shot' -and -not $taken.ContainsKey($st.name)) {
            $proc.Refresh()
            $p = Join-Path $Out ($Mode + '-' + $st.name + '.jpg')
            if (Save-LegionShot $proc.MainWindowHandle $p) { Say ('  shot: ' + $p) } else { Say ('  no window for ' + $st.name) }
            $taken[$st.name] = $true
            Set-Content -LiteralPath (Join-Path $run ('ack-' + $st.name)) -Value 'ok' -Encoding ASCII
        }
        if ($st -and $st.state -eq 'done') { Say ('script done ' + [string]$st.why); break }
        Start-Sleep -Milliseconds 400
    }
} finally {
    if (Test-Path (Join-Path $run 'runner.log')) { Get-Content (Join-Path $run 'runner.log') | ForEach-Object { Say ('  legion: ' + $_) } }
    try { $proc.CloseMainWindow() | Out-Null; Start-Sleep -Seconds 4; if (-not $proc.HasExited) { $proc.Kill() } } catch {}
    try { $j = Get-Content -LiteralPath $settings -Raw | ConvertFrom-Json; $j.password = ''; $j.autologin = $false; [IO.File]::WriteAllText($settings, ($j | ConvertTo-Json -Depth 6), (New-Object Text.UTF8Encoding($false))) } catch {}
}
Say 'done'
