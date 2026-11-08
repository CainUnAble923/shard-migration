#Requires -Version 5.1
<#
  creation817.ps1 (cc-P817: the client from -ClientSource as given, its ExternalImages from -App's package, the
  overrides from -App's own Build-UoOverrides.ps1; a "burst" step: { "do": "burst", "name": "x", "n": 6, "ms": 2000 }.
  From creation762.ps1, cc-P762; the client set-up is P761's isle-shots742.ps1): TazUO's character creation screens as a new
  player sees them, on the PRIVATE proof shard (127.0.0.1:2596; 2593 and 2594 refused).

      powershell -NoProfile -ExecutionPolicy Bypass -File creation762.ps1 -Steps steps.json -Out <folder>
          [-Account p762newbie] [-Work <scratch>] [-Port 2596]

  A fresh account (made by the shard at its first login, as a player's is) with no character: TazUO logs in by itself
  and opens character creation at once (LoginScene: no character, StartCharCreation). Then -Steps, in order:
    { "do": "shot", "name": "x" }             window capture to <Out>\x.jpg (Save-LegionShot)
    { "do": "click", "x": 100, "y": 200 }     a left click posted to the window at that client-area point
    { "do": "text", "value": "Name" }         characters posted to the window (WM_CHAR)
    { "do": "key", "vk": 13 }                 a key posted (WM_KEYDOWN/UP)
    { "do": "wait", "s": 2 }
  The password is random, lives only in the client's settings (TazUO's own encoding) and is cleared when the run ends.
  The caller holds the test-shard lock and runs the proof shard. ASCII only.
#>
param(
    [Parameter(Mandatory)][string]$Steps,
    [Parameter(Mandatory)][string]$Out,
    [string]$Account = ('p817n' + (Get-Random -Minimum 10000 -Maximum 99999)),
    [Parameter(Mandatory)][string]$App,
    [string]$Plugin = '',
    [string]$Character = '',   # the plugin's character's name (make_create_bin.py's)   # cc-P817: P731's creation plugin dll (create.bin beside it): the character is made without the screens
    [string]$CodeRepo = 'D:\UO\golems\Iron\ShatteredLegacy',
    [string]$Work = 'D:\UO\golems\Iron\p817-proof\tazuo',
    [string]$TargetHost = '127.0.0.1',
    [int]$Port = 2596,
    [int]$FirstSettle = 25,
    [string]$ClientSource = ''
)
$ErrorActionPreference = 'Continue'
. 'D:\UO\golem\LegionTest.ps1'

# cc-P817: restore a minimized client window without activating it (it never takes focus), then capture.
if (-not ('P817.Win' -as [type])) {
    Add-Type -Namespace P817 -Name Win -MemberDefinition '[DllImport("user32.dll")] public static extern bool IsIconic(IntPtr h); [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int c);'
}
function Save-LegionShot817([IntPtr]$Window, [string]$Path) {
    if ($Window -ne [IntPtr]::Zero -and [P817.Win]::IsIconic($Window)) { [void][P817.Win]::ShowWindow($Window, 4); Start-Sleep -Milliseconds 900 }
    Save-LegionShot $Window $Path
}
New-Item -ItemType Directory -Path $Out, $Work -Force | Out-Null
function Say([string]$t) { $l = '[' + (Get-Date).ToString('HH:mm:ss') + '] ' + $t; Write-Host $l; Add-Content -LiteralPath (Join-Path $Out 'creation-log.txt') -Value $l -Encoding ASCII }
if ($Port -lt 2595 -or $Port -gt 2599) { Say "port $Port refused: 2595-2599 only"; exit 2 }
$guard = Test-LegionTarget $TargetHost $Port
if (-not $guard.Ok) { Say $guard.Why; exit 2 }

Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public static class P817Post {
    [DllImport("user32.dll")] public static extern bool PostMessage(IntPtr h, uint msg, IntPtr w, IntPtr l);
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
    public static IntPtr XY(int x, int y) { return (IntPtr)((y << 16) | (x & 0xFFFF)); }
}
'@

if (-not $ClientSource) { $ClientSource = Join-Path $App 'tazuo' }
$client = Join-Path $Work 'client'
[void](& robocopy $ClientSource $client /MIR /XD Data LegionScripts Logs Screenshots /NFL /NDL /NJH /NJS /NP /R:1 /W:1)
# The package's own pictures, whatever client runs (a private build has none).
[void](& robocopy (Join-Path (Join-Path $App 'tazuo') 'ExternalImages') (Join-Path $client 'ExternalImages') /E /NFL /NDL /NJH /NJS /NP /R:1 /W:1)
# cc-P817: fresh profiles with the launcher's new-profile defaults, as Play.ps1 writes them for a player (no paperdoll at login).
$profiles = Join-Path $client 'Data\Profiles'
if (Test-Path -LiteralPath $profiles) { Remove-Item -LiteralPath $profiles -Recurse -Force }
. (Join-Path $App 'Launch-Settings.ps1')
[void](Initialize-NewProfileDefaults -ProfilesDir $profiles -ClientDir $client)
$ovDir = Join-Path $Work 'uo-override'
$override = & (Join-Path $App 'Build-UoOverrides.ps1') -UoDir 'D:\UO\UltimaOnlineVanilla' -OutDir $ovDir -ListDir $ovDir
Say ('override (with our clilocs: the city list descriptions): ' + $override)
Say ('account: ' + $Account + ' (new; the shard makes it at this login)')

$pw = -join ((48..57) + (97..122) | Get-Random -Count 16 | ForEach-Object { [char]$_ })
$settings = Join-Path $client 'settings.p817.json'
$set = New-LegionSettings $TargetHost $Port $Account (ConvertTo-CuoPassword $pw) 'D:\UO\UltimaOnlineVanilla'
if ($Plugin) { $set.plugins = @($Plugin); Say ('plugin: ' + $Plugin) }
[IO.File]::WriteAllText($settings, ($set | ConvertTo-Json -Depth 6), (New-Object Text.UTF8Encoding($false)))
$pw = $null
$argv = @('-settings', ('"' + $settings + '"'), '-skiploginscreen', '-skipserverselect', '-uofilesoverride', ('"' + $override + '"'))
# cc-P817: with the plugin the screens never record a name, and TazUO refuses to enter the world without one.
if ($Character) { $argv += @('-lastcharactername', ('"' + $Character + '"')) }
$proc = Start-Process -FilePath (Join-Path $client 'TazUO.exe') -ArgumentList $argv -WorkingDirectory $client -PassThru
try {
    Start-Sleep -Seconds $FirstSettle
    $proc.Refresh()
    $h = $proc.MainWindowHandle
    Say ('window ' + $h)
    $stepList = Get-Content -LiteralPath $Steps -Raw | ConvertFrom-Json   # PS 5.1: assigned first, so foreach unrolls it
    foreach ($s in $stepList) {
        switch ([string]$s.do) {
            'shot' {
                $proc.Refresh(); $h = $proc.MainWindowHandle
                $p = Join-Path $Out ([string]$s.name + '.jpg')
                if (Save-LegionShot817 $h $p) { Say ('shot: ' + $p) } else { Say 'no window to capture' }
            }
            'click' {
                $xy = [P817Post]::XY([int]$s.x, [int]$s.y)
                [void][P817Post]::PostMessage($h, 0x200, [IntPtr]::Zero, $xy); Start-Sleep -Milliseconds 120
                [void][P817Post]::PostMessage($h, 0x201, [IntPtr]1, $xy); Start-Sleep -Milliseconds 90
                [void][P817Post]::PostMessage($h, 0x202, [IntPtr]::Zero, $xy)
                Say ('click ' + $s.x + ',' + $s.y); Start-Sleep -Milliseconds 700
            }
            'text' {
                foreach ($ch in ([string]$s.value).ToCharArray()) { [void][P817Post]::PostMessage($h, 0x102, [IntPtr][int]$ch, [IntPtr]1); Start-Sleep -Milliseconds 60 }
                Say ('typed ' + $s.value)
            }
            'key' {
                [void][P817Post]::PostMessage($h, 0x100, [IntPtr][int]$s.vk, [IntPtr]1); Start-Sleep -Milliseconds 80
                [void][P817Post]::PostMessage($h, 0x101, [IntPtr][int]$s.vk, [IntPtr]1)
                Say ('key ' + $s.vk)
            }
            'activate' {
                [void][P817Post]::PostMessage($h, 0x0006, [IntPtr]1, [IntPtr]::Zero)   # WM_ACTIVATE, active
                [void][P817Post]::PostMessage($h, 0x0007, [IntPtr]::Zero, [IntPtr]::Zero) # WM_SETFOCUS
                [void][P817Post]::SetForegroundWindow($h)
                Say 'activate'; Start-Sleep -Milliseconds 500
            }
            'wait' { Start-Sleep -Milliseconds ([int]([double]$s.s * 1000)) }
            'burst' {
                for ($k = 1; $k -le [int]$s.n; $k++) {
                    $proc.Refresh(); $h = $proc.MainWindowHandle
                    $p = Join-Path $Out ([string]$s.name + '-' + $k + '.jpg')
                    if (Save-LegionShot817 $h $p) { Say ('shot: ' + $p) } else { Say ('no shot (window ' + $h + ', exited ' + $proc.HasExited + ')') }
                    Start-Sleep -Milliseconds ([int]$s.ms)
                }
            }
        }
    }
} finally {
    try { $proc.CloseMainWindow() | Out-Null; Start-Sleep -Seconds 3; if (-not $proc.HasExited) { $proc.Kill() } } catch {}
    try { $j = Get-Content -LiteralPath $settings -Raw | ConvertFrom-Json; $j.password = ''; $j.autologin = $false; [IO.File]::WriteAllText($settings, ($j | ConvertTo-Json -Depth 6), (New-Object Text.UTF8Encoding($false))) } catch {}
}
Say 'done'
