#Requires -Version 5.1
<#
  proof.ps1 (cc-P265): seed each guild hall decor set on THIS PC's test shard and take a client screenshot of it.

      powershell -NoProfile -ExecutionPolicy Bypass -File proof.ps1 -Spec shots.json -Out <folder for the JPEGs>
          [-CodeRepo D:\UO\golems\Iron\ShatteredLegacy] [-Bot <scratch copy of tools\playtest-bot with P219's
          legionsetup.py>] [-Work <scratch folder>]

  The caller holds the test-shard lock and has the test shard running the image under test. In order:
    1. the never-live guard (P219's Test-LegionTarget: 127.0.0.1, ports 2594-2599; 2593 refused from any host);
    2. a TazUO of its own: a copy of D:\UO\tazuo-sl-build\client with this branch's art PNGs in ExternalImages\art (as
       the player package installs them) and P219's profile for Iron the Tester, its game window filling the client;
    3. this branch's records written into copies of the client data's tiledata.mul and animdata.mul by the package's
       own Build-UoOverrides.ps1, handed to TazUO with -uofilesoverride (as Play.ps1 does), so the art animates;
    4. per shot: the Golem's Admin types the shot's commands (P219's uobot.legionsetup: go to the spot, seed, put the
       Player's logout spot beside it); TazUO logs the Player in; after -SettleSeconds the window is captured (P219's
       Save-LegionShot); the client closes and the password is cleared from its settings file.
  Writes <Out>\<shot>.jpg and <Out>\proof-log.txt (each command and the server's answers). ASCII only.
  cc-P374: -ClientSource runs another TazUO build (default D:\UO\tazuo-sl-build\client). -Frames N also writes <shot>-f1.jpg .. -f(N-1).jpg, FrameMs apart, right after the shot (animation check).
#>
param(
    [Parameter(Mandatory)][string]$Spec,
    [Parameter(Mandatory)][string]$Out,
    [string]$CodeRepo = 'D:\UO\golems\Iron\ShatteredLegacy',
    [string]$Bot = '',
    [string]$Work = (Join-Path $env:TEMP 'p265-proof'),
    [string]$TargetHost = '127.0.0.1',
    [int]$Port = 2594,
    [string]$Golem = 'Iron',
    [int]$SettleSeconds = 25,
    [string]$ClientSource = 'D:\UO\tazuo-sl-build\client',
    [int]$Frames = 1,
    [int]$FrameMs = 250
)
$ErrorActionPreference = 'Continue'
. 'D:\UO\golem\LegionTest.ps1'
function Say([string]$t) { $l = '[' + (Get-Date).ToString('HH:mm:ss') + '] ' + $t; Write-Host $l; Add-Content -LiteralPath (Join-Path $Out 'proof-log.txt') -Value $l -Encoding ASCII }
New-Item -ItemType Directory -Path $Out, $Work -Force | Out-Null

$guard = Test-LegionTarget $TargetHost $Port
if (-not $guard.Ok) { Say $guard.Why; exit 2 }
Say $guard.Why

# 2. the client
$client = Join-Path $Work 'client'
[void](& robocopy $ClientSource $client /MIR /XD Data LegionScripts Logs Screenshots /NFL /NDL /NJH /NJS /NP /R:1 /W:1)
$artOut = Join-Path $client 'ExternalImages\art'
New-Item -ItemType Directory -Path $artOut -Force | Out-Null
Copy-Item -Path (Join-Path $CodeRepo 'player-package\vendor\shattered-legacy-art\art\*.png') -Destination $artOut -Force
Say ('client: ' + $client + ', ' + @(Get-ChildItem -LiteralPath $artOut -Filter '*.png').Count + ' art PNGs')
$profSrc = 'D:\UO\golem\legion-test\Iron\client\Data\Profiles'
$profDst = Join-Path $client 'Data\Profiles'
[void](& robocopy $profSrc $profDst /E /NFL /NDL /NJH /NJS /NP /R:1 /W:1)
foreach ($pf in @(Get-ChildItem -LiteralPath $profDst -Recurse -Filter 'profile.json')) {
    $j = Get-Content -LiteralPath $pf.FullName -Raw | ConvertFrom-Json
    $j.game_window_full_size = $true
    $j.game_window_position = [pscustomobject]@{ X = 0; Y = 0 }
    [IO.File]::WriteAllText($pf.FullName, ($j | ConvertTo-Json -Depth 20), (New-Object Text.UTF8Encoding($false)))
}

# 3. the records, as the package writes them
$ovDir = Join-Path $Work 'uo-override'
$override = & (Join-Path $CodeRepo 'player-package\payload\app\Build-UoOverrides.ps1') -UoDir 'D:\UO\UltimaOnlineVanilla' `
    -Records (Join-Path $CodeRepo 'player-package\vendor\shattered-legacy-art\records.json') -OutDir $ovDir
Say ('override: ' + $override)

# 4. the shots
$shots = Get-Content -LiteralPath $Spec -Raw | ConvertFrom-Json
$acc = (& powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'D:\UO\golem\Get-GolemTestAccount.ps1' -Golem $Golem -Role player -Json 2>$null | Select-Object -Last 1) | ConvertFrom-Json
foreach ($s in $shots) {
    Say ('--- ' + $s.name)
    $cf = Join-Path $Work ($s.name + '-commands.json')
    [IO.File]::WriteAllText($cf, (ConvertTo-Json @(@($s.commands) | ForEach-Object { [string]$_ })), (New-Object Text.UTF8Encoding($false)))
    Push-Location $Bot
    try { $sj = (& python -B -m uobot.legionsetup --host $TargetHost --port $Port --golem $Golem --commands $cf --out $Work 2>&1 | Out-String).Trim() } finally { Pop-Location }
    $line = @($sj -split "`r?`n" | Where-Object { $_ -match '^\{' }) | Select-Object -Last 1
    $sr = $null; try { $sr = $line | ConvertFrom-Json } catch {}
    if (-not $sr) { Say ('setup gave no result: ' + $sj); continue }
    foreach ($c in @($sr.commands)) { Say ('  ' + $c.command); foreach ($r in @($c.replies)) { Say ('      ' + $r) } }
    if (-not $sr.ok) { Say ('  setup not ok: ' + $sr.why) }
    $settings = Join-Path $client 'settings.p265.json'
    $set = New-LegionSettings $TargetHost $Port ([string]$acc.Username) (ConvertTo-CuoPassword ([string]$acc.Password)) 'D:\UO\UltimaOnlineVanilla'
    [IO.File]::WriteAllText($settings, ($set | ConvertTo-Json -Depth 6), (New-Object Text.UTF8Encoding($false)))
    $argv = @('-settings', ('"' + $settings + '"'), '-skiploginscreen', '-skipserverselect', '-lastcharactername', ('"' + $Golem + ' the Tester"'), '-uofilesoverride', ('"' + $override + '"'))
    $proc = Start-Process -FilePath (Join-Path $client 'TazUO.exe') -ArgumentList $argv -WorkingDirectory $client -PassThru
    try {
        Start-Sleep -Seconds $SettleSeconds
        $proc.Refresh()
        $p = Join-Path $Out ($s.name + '.jpg')
        if (Save-LegionShot $proc.MainWindowHandle $p) { Say ('  shot: ' + $p) } else { Say '  no window to capture' }
        for ($f = 1; $f -lt $Frames; $f++) {
            Start-Sleep -Milliseconds $FrameMs
            [void](Save-LegionShot $proc.MainWindowHandle (Join-Path $Out ($s.name + '-f' + $f + '.jpg')))
        }
    } finally {
        try { $proc.CloseMainWindow() | Out-Null; Start-Sleep -Seconds 4; if (-not $proc.HasExited) { $proc.Kill() } } catch {}
        try { $j = Get-Content -LiteralPath $settings -Raw | ConvertFrom-Json; $j.password = ''; $j.autologin = $false; [IO.File]::WriteAllText($settings, ($j | ConvertTo-Json -Depth 6), (New-Object Text.UTF8Encoding($false))) } catch {}
    }
    Start-Sleep -Seconds 3
}
$acc = $null
Say 'done'
