#Requires -Version 5.1
<#
  tazuo-pkg.ps1 (cc-P690, from P740's tazuo-walk.ps1 and ui.ps1): TazUO FROM THE BUILT PLAYER PACKAGE, on the private
  proof shard (127.0.0.1:2596 only; the caller holds the test-shard lock). What a new player does, as far as a script can:

      tazuo-pkg.ps1 -App <unzipped package>\app -Account <new name> -Character <name> -City 0|1 -Script <walk.py> -Out <folder>

  1. The package's own launcher steps: Overrides-Launch.ps1's Invoke-UoOverrides builds the art and the SoS map from
     the player's UO folder (D:\UO\UltimaOnlineVanilla) into app\uo-overrides (timed: the first start), and
     Launch-Settings.ps1's Initialize-NewProfileDefaults writes the new-profile defaults, as Play.ps1 does.
  2. A NEW account: the shard creates it at the first login (accountHandler.enableAutoAccountCreation, as on the test
     shard). Its password is made here and kept only in p690-proof\client-accounts.json, outside the repos.
  3. The character is made by the client itself at the character list (P731's test-only creation plugin sends
     create.bin, made by make_create_bin.py with -City), then the Legion script runs (lscript.json autostart).
  4. Each "SHOT <name>" / "BURST <name> <n> <ms>" line the script writes to <Out>\shots.sig becomes <Out>\<name>.jpg;
     one more frame every -EverySeconds. "END" stops the run.
#>
param(
    [Parameter(Mandatory)][string]$App,
    [Parameter(Mandatory)][string]$Account,
    [Parameter(Mandatory)][string]$Character,
    [Parameter(Mandatory)][int]$City,
    [Parameter(Mandatory)][string]$Script,
    [Parameter(Mandatory)][string]$Out,
    [int]$Port = 2596,
    [int]$MaxMinutes = 20,
    [int]$EverySeconds = 30,
    [string]$UoDir = 'D:\UO\UltimaOnlineVanilla',
    [string]$Plugin = 'D:\UO\golems\Iron\p690-proof\plugin-tazuo'
)
$ErrorActionPreference = 'Continue'
. 'D:\UO\golem\LegionTest.ps1'
New-Item -ItemType Directory -Path $Out -Force | Out-Null
function Say([string]$t) { $l = '[' + (Get-Date).ToString('HH:mm:ss') + '] ' + $t; Write-Host $l; Add-Content -LiteralPath (Join-Path $Out 'runner-log.txt') -Value $l -Encoding ASCII }
$guard = Test-LegionTarget '127.0.0.1' $Port
if (-not $guard.Ok -or $Port -lt 2595) { Say ('refused: ' + $guard.Why); exit 2 }
Say $guard.Why
$tools = $PSScriptRoot
$client = Join-Path $App 'tazuo'
$profiles = Join-Path $client 'Data\Profiles'
$sig = Join-Path $Out 'shots.sig'

# 1. the launcher's steps
$sw = [Diagnostics.Stopwatch]::StartNew()
. (Join-Path $App 'Overrides-Launch.ps1')
$override = Invoke-UoOverrides -App $App -UoDir $UoDir -LimitSeconds 900
Say ('overrides (the first start): ' + [int]$sw.Elapsed.TotalSeconds + ' s; list ' + $override)
if (-not $override) { Say 'no override list: the map was not built'; exit 1 }
Say ('override list: ' + ((Get-Content -LiteralPath $override) -join ' | '))
. (Join-Path $App 'Launch-Settings.ps1')
$wrote = Initialize-NewProfileDefaults -ProfilesDir $profiles -ClientDir $client
Say ('new-profile defaults written by the launcher: ' + $wrote)

# 2. the account, 3. the plugin and the script
$accFile = 'D:\UO\golems\Iron\p690-proof\client-accounts.json'
$accs = @{}
if (Test-Path $accFile) { (Get-Content -Raw $accFile | ConvertFrom-Json).psobject.Properties | ForEach-Object { $accs[$_.Name] = $_.Value } }
if (-not $accs.ContainsKey($Account)) { $accs[$Account] = [guid]::NewGuid().ToString('N').Substring(0, 16) }
[IO.File]::WriteAllText($accFile, ($accs | ConvertTo-Json), (New-Object Text.UTF8Encoding($false)))
& python -P (Join-Path $tools 'make_create_bin.py') $Character $City (Join-Path $Plugin 'create.bin') *>&1 | ForEach-Object { Say ([string]$_) }
Remove-Item -LiteralPath (Join-Path $Plugin 'P731Create.log') -ErrorAction SilentlyContinue
$ls = Join-Path $client 'LegionScripts'
New-Item -ItemType Directory -Path $ls -Force | Out-Null
$text = (Get-Content -Raw -LiteralPath $Script) -replace '__CHARACTER__', $Character -replace '__OUT__', $Out
[IO.File]::WriteAllText((Join-Path $ls (Split-Path $Script -Leaf)), $text, (New-Object Text.UTF8Encoding($false)))
[IO.File]::WriteAllText((Join-Path $client 'Data\lscript.json'), (@{ GlobalAutoStartScripts = @((Split-Path $Script -Leaf)); CharAutoStartScripts = @{}; GroupCollapsed = @{}; DisableModuleCache = $false } | ConvertTo-Json -Depth 4), (New-Object Text.UTF8Encoding($false)))
Set-Content -LiteralPath $sig -Value '' -Encoding ASCII
$settings = Join-Path $client 'settings.p690.json'
$set = New-LegionSettings '127.0.0.1' $Port $Account (ConvertTo-CuoPassword ([string]$accs[$Account])) $UoDir
$set.autologin = $false   # stop at the character list: the new character is made there
$set.plugins = @((Join-Path $Plugin 'P731Create.dll'))
[IO.File]::WriteAllText($settings, ($set | ConvertTo-Json -Depth 6), (New-Object Text.UTF8Encoding($false)))
$accs = $null
$argv = @('-settings', ('"' + $settings + '"'), '-skiploginscreen', '-skipserverselect', '-lastcharactername', ('"' + $Character + '"'), '-uofilesoverride', ('"' + $override + '"'))
$proc = Start-Process -FilePath (Join-Path $client 'TazUO.exe') -ArgumentList $argv -WorkingDirectory $client -PassThru
Say ('TazUO (the package''s) started, pid ' + $proc.Id)

# 4. the shots
$seen = 0; $n = 0; $t0 = Get-Date; $next = $t0.AddSeconds(10)
try {
    while (((Get-Date) - $t0).TotalMinutes -lt $MaxMinutes -and -not $proc.HasExited) {
        Start-Sleep -Milliseconds 500
        $proc.Refresh()
        $lines = @(Get-Content -LiteralPath $sig -ErrorAction SilentlyContinue | Where-Object { $_ })
        for ($i = $seen; $i -lt $lines.Count; $i++) {
            if ($lines[$i] -eq 'END') { Say 'the script ended'; $t0 = [datetime]::MinValue; break }
            if ($lines[$i] -match '^BURST (\S+) (\d+) (\d+)$') {
                $bn = $Matches[1]; $bc = [int]$Matches[2]; $bms = [int]$Matches[3]; $bt = Get-Date
                for ($k = 1; $k -le $bc; $k++) {
                    [void](Save-LegionShot $proc.MainWindowHandle (Join-Path $Out ('{0}-{1:D2}.jpg' -f $bn, $k)))
                    $w = ($bt.AddMilliseconds($k * $bms) - (Get-Date)).TotalMilliseconds
                    if ($w -gt 0) { Start-Sleep -Milliseconds ([int]$w) }
                }
                Say ('burst: ' + $bn + ' x' + $bc)
                continue
            }
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
    Copy-Item -LiteralPath (Join-Path $Plugin 'P731Create.log') -Destination $Out -Force -ErrorAction SilentlyContinue
}
Say 'done'
