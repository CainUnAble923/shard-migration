#Requires -Version 5.1
<#
  shots.ps1 (cc-P670, from P661's proof2.ps1): per scene, the Golem's Admin moves "<Golem> the Tester" (P219's
  uobot.legionsetup), then the Tester logs in twice in OUR client build (patches 0001-0008) with the redrawn art
  installed: once with Options > Interface > Appearance > "Redrawn world art (Zigholtul)" off (the profile's
  SlRedrawnArt false, the default) and once on, and each window is captured. Both shots of a scene use the same client
  folder and the same spot, so the only difference is the setting.
  The caller holds the test-shard lock and runs a PRIVATE shard (P661's proof-shard.ps1) on -Port. ASCII only.
#>
param(
    [Parameter(Mandatory)][string]$Spec,
    [Parameter(Mandatory)][string]$Out,
    [string]$CodeRepo = 'D:\UO\golems\Iron\ShatteredLegacy',
    [string]$Work = (Join-Path $env:TEMP 'p670-shots'),
    [string]$TargetHost = '127.0.0.1',
    [int]$Port = 2596,
    [string]$Golem = 'Iron',
    [int]$SettleSeconds = 30,
    [string]$ClientSource = 'D:\UO\golems\Iron\tazuo-p670\client'
)
$ErrorActionPreference = 'Continue'
. 'D:\UO\golem\LegionTest.ps1'
function Say([string]$t) { $l = '[' + (Get-Date).ToString('HH:mm:ss') + '] ' + $t; Write-Host $l; Add-Content -LiteralPath (Join-Path $Out 'shots-log.txt') -Value $l -Encoding ASCII }
New-Item -ItemType Directory -Path $Out, $Work -Force | Out-Null
if ($Port -lt 2595 -or $Port -gt 2599) { Say "port $Port refused: private shards only (2595-2599)"; exit 2 }
$guard = Test-LegionTarget $TargetHost $Port
if (-not $guard.Ok) { Say $guard.Why; exit 2 }
Say $guard.Why
$Bot = Join-Path $CodeRepo 'tools\playtest-bot'
$char = $Golem + ' the Tester'
$dir = Join-Path $Work 'client'

[void](& robocopy $ClientSource $dir /MIR /XD Data LegionScripts Logs Screenshots /NFL /NDL /NJH /NJS /NP /R:1 /W:1)
$artOut = Join-Path $dir 'ExternalImages\art'
New-Item -ItemType Directory -Path $artOut -Force | Out-Null
Copy-Item -Path (Join-Path $CodeRepo 'player-package\vendor\shattered-legacy-art\art\*.png') -Destination $artOut -Force
$rdOut = Join-Path $dir 'ExternalImages\sl-redrawn-art'
New-Item -ItemType Directory -Path $rdOut -Force | Out-Null
Copy-Item -Path (Join-Path $CodeRepo 'player-package\vendor\zigholtul-redrawn-statics\art\*.png') -Destination $rdOut -Force
Say ('redrawn PNGs installed: ' + @(Get-ChildItem -LiteralPath $rdOut -File).Count)
$profDst = Join-Path $dir 'Data\Profiles'
[void](& robocopy 'D:\UO\golem\legion-test\Iron\client\Data\Profiles' $profDst /E /NFL /NDL /NJH /NJS /NP /R:1 /W:1)
function Set-Redrawn([bool]$on) {
    foreach ($pf in @(Get-ChildItem -LiteralPath $profDst -Recurse -Filter 'profile.json')) {
        $j = Get-Content -LiteralPath $pf.FullName -Raw | ConvertFrom-Json
        $j.game_window_full_size = $true
        $j.game_window_position = [pscustomobject]@{ X = 0; Y = 0 }
        # The profile's own key for Profile.SlRedrawnArt is snake case (as sl_skins is); a first run with
        # "SlRedrawnArt" changed nothing, and the client wrote sl_redrawn_art false back beside it.
        if ($j.PSObject.Properties.Name -contains 'SlRedrawnArt') { $j.PSObject.Properties.Remove('SlRedrawnArt') }
        if ($j.PSObject.Properties.Name -contains 'sl_redrawn_art') { $j.sl_redrawn_art = $on } else { $j | Add-Member -NotePropertyName sl_redrawn_art -NotePropertyValue $on }
        [IO.File]::WriteAllText($pf.FullName, ($j | ConvertTo-Json -Depth 20), (New-Object Text.UTF8Encoding($false)))
    }
}
$ovDir = Join-Path $Work 'uo-override'
$override = & (Join-Path $CodeRepo 'player-package\payload\app\Build-UoOverrides.ps1') -UoDir 'D:\UO\UltimaOnlineVanilla' `
    -Records (Join-Path $CodeRepo 'player-package\vendor\shattered-legacy-art\records.json') -OutDir $ovDir
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
    Start-Sleep -Seconds 3

    foreach ($v in @(@{ Name = 'off'; On = $false }, @{ Name = 'on'; On = $true })) {
        Set-Redrawn $v.On
        $acc = (& powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'D:\UO\golem\Get-GolemTestAccount.ps1' -Golem $Golem -Role 'player' -Json 2>$null | Select-Object -Last 1) | ConvertFrom-Json
        $settings = Join-Path $dir 'settings.p670.json'
        $set = New-LegionSettings $TargetHost $Port ([string]$acc.Username) (ConvertTo-CuoPassword ([string]$acc.Password)) 'D:\UO\UltimaOnlineVanilla'
        $acc = $null
        [IO.File]::WriteAllText($settings, ($set | ConvertTo-Json -Depth 6), (New-Object Text.UTF8Encoding($false)))
        $argv = @('-settings', ('"' + $settings + '"'), '-skiploginscreen', '-skipserverselect', '-lastcharactername', ('"' + $char + '"'), '-uofilesoverride', ('"' + $override + '"'))
        $p = Start-Process -FilePath (Join-Path $dir 'TazUO.exe') -ArgumentList $argv -WorkingDirectory $dir -PassThru
        try {
            Start-Sleep -Seconds $SettleSeconds
            $p.Refresh()
            $shot = Join-Path $Out ($s.name + '-' + $v.Name + '.jpg')
            if (Save-LegionShot $p.MainWindowHandle $shot) { Say ('  shot: ' + $shot) } else { Say ('  no window to capture (' + $v.Name + ')') }
        } finally {
            try { $p.CloseMainWindow() | Out-Null; Start-Sleep -Seconds 3; if (-not $p.HasExited) { $p.Kill() } } catch {}
            try { $j = Get-Content -LiteralPath $settings -Raw | ConvertFrom-Json; $j.password = ''; $j.autologin = $false; [IO.File]::WriteAllText($settings, ($j | ConvertTo-Json -Depth 6), (New-Object Text.UTF8Encoding($false))) } catch {}
        }
        Start-Sleep -Seconds 4
    }
}
Set-Redrawn $false
Say 'done'
