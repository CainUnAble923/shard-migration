#Requires -Version 5.1
<#
  classic-pkg.ps1 (cc-P690, from P740's classic-wake.ps1): the SECOND client, ClassicUO (the player launcher's
  D:\UO\CUO-Player, 1.1.0.317), on the private proof shard (127.0.0.1:2596 only; the caller holds the test-shard lock).
  A fresh copy of the client with no settings; a NEW account (made by the shard at the first login; its password only
  in p690-proof\client-accounts.json); the character made by the client at the character list with -City (P731's
  creation plugin, P740's .NET Framework build); the map from the PACKAGE's own override list (app\uo-overrides, built
  by the package's launcher in tazuo-pkg.ps1); then a frame every -EverySeconds, and -Keys arrow presses posted to the
  window (WM_KEYDOWN/UP; the real keyboard is never touched) from -KeyAt seconds.

      classic-pkg.ps1 -App <package>\app -Account <new> -Character <name> -City 1 -Out <folder>
#>
param(
    [Parameter(Mandatory)][string]$App,
    [Parameter(Mandatory)][string]$Account,
    [Parameter(Mandatory)][string]$Character,
    [Parameter(Mandatory)][int]$City,
    [Parameter(Mandatory)][string]$Out,
    [int]$Seconds = 50,
    [int]$KeyAt = 20,
    [int]$Keys = 6,
    [int]$KeyCode = 0x26,   # Up arrow: north-west in UO's screen directions
    [double]$EverySeconds = 2,
    [int]$Port = 2596
)
$ErrorActionPreference = 'Continue'
. 'D:\UO\golem\LegionTest.ps1'
Add-Type -Namespace P690 -Name K -MemberDefinition @'
[DllImport("user32.dll")] public static extern bool PostMessage(System.IntPtr h, uint m, System.IntPtr w, System.IntPtr l);
'@
$proof = 'D:\UO\golems\Iron\p690-proof'
$work = Join-Path $proof 'classic'
$client = Join-Path $work 'client'
$plugin = Join-Path $work 'plugin'
New-Item -ItemType Directory -Path $Out, $work, $plugin -Force | Out-Null
function Say([string]$t) { $l = '[' + (Get-Date).ToString('HH:mm:ss.fff') + '] ' + $t; Write-Host $l; Add-Content -LiteralPath (Join-Path $Out 'classic-log.txt') -Value $l -Encoding ASCII }
$guard = Test-LegionTarget '127.0.0.1' $Port
if (-not $guard.Ok -or $Port -lt 2595) { Say ('refused: ' + $guard.Why); exit 2 }
Say $guard.Why

if (Test-Path $client) { Remove-Item -Recurse -Force $client }
[void](& robocopy 'D:\UO\CUO-Player' $client /MIR /XD Data Logs Screenshots /XF settings.json /NFL /NDL /NJH /NJS /NP /R:1 /W:1)
Copy-Item -LiteralPath 'D:\UO\golems\Iron\p740-proof\classic\plugin\P731Create.dll' -Destination $plugin -Force
& python -P (Join-Path $PSScriptRoot 'make_create_bin.py') $Character $City (Join-Path $plugin 'create.bin') | ForEach-Object { Say ([string]$_) }
Remove-Item -LiteralPath (Join-Path $plugin 'P731Create.log') -ErrorAction SilentlyContinue
# P740 runs 4-5: a new ClassicUO profile opens the paperdoll over the scene; the game view goes right of it
$gdir = Join-Path $client ('Data\Profiles\' + $Account + '\_\' + $Character)
New-Item -ItemType Directory -Path $gdir -Force | Out-Null
Copy-Item -LiteralPath 'D:\UO\golems\Iron\p740-proof\classic-profile-template.json' -Destination (Join-Path $gdir 'profile.json') -Force
[IO.File]::WriteAllText((Join-Path $gdir 'gumps.xml'), '<?xml version="1.0" encoding="utf-8" standalone="yes"?>' + "`r`n<gumps>`r`n</gumps>`r`n", (New-Object Text.UTF8Encoding($true)))
$override = Join-Path $App 'uo-overrides\files-override.txt'
if (-not (Test-Path $override)) { Say 'no override list in the package (run tazuo-pkg.ps1 first)'; exit 1 }

if ($Account -eq 'iron-player') {
    # an account that has finished the isle (the bot's Iron Islander graduated on it): New Haven is unlocked there
    $ga = (& powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'D:\UO\golem\Get-GolemTestAccount.ps1' -Golem Iron -Role player -Json 2>$null | Select-Object -Last 1) | ConvertFrom-Json
    $accs = @{ $Account = [string]$ga.Password }
    $Account = [string]$ga.Username
    $ga = $null
} else {
    $accFile = Join-Path $proof 'client-accounts.json'
    $accs = @{}
    if (Test-Path $accFile) { (Get-Content -Raw $accFile | ConvertFrom-Json).psobject.Properties | ForEach-Object { $accs[$_.Name] = $_.Value } }
    if (-not $accs.ContainsKey($Account)) { $accs[$Account] = [guid]::NewGuid().ToString('N').Substring(0, 16) }
    [IO.File]::WriteAllText($accFile, ($accs | ConvertTo-Json), (New-Object Text.UTF8Encoding($false)))
}
$pw = if ($accs.ContainsKey($Account)) { [string]$accs[$Account] } else { [string]@($accs.Values)[0] }
$set = New-LegionSettings '127.0.0.1' $Port $Account (ConvertTo-CuoPassword $pw) 'D:\UO\UltimaOnlineVanilla'
$pw = $null
$accs = $null
$set.autologin = $false
$set.plugins = @((Join-Path $plugin 'P731Create.dll'))
$settings = Join-Path $client 'settings.p690.json'
[IO.File]::WriteAllText($settings, ($set | ConvertTo-Json -Depth 6), (New-Object Text.UTF8Encoding($false)))
$argv = @('-settings', ('"' + $settings + '"'), '-skiploginscreen', '-lastcharactername', ('"' + $Character + '"'), '-uofilesoverride', ('"' + $override + '"'))
$proc = Start-Process -FilePath (Join-Path $client 'ClassicUO.exe') -ArgumentList $argv -WorkingDirectory $client -PassThru
Say ('ClassicUO started, pid ' + $proc.Id)

$t0 = $null
for ($i = 0; $i -lt 120 -and -not $t0; $i++) {
    Start-Sleep -Milliseconds 500
    $proc.Refresh()
    if ($proc.HasExited) { Say 'ClassicUO exited'; break }
    if ($proc.MainWindowHandle -ne [IntPtr]::Zero -and (Get-Content -Raw (Join-Path $plugin 'P731Create.log') -ErrorAction SilentlyContinue) -match 'sent 0xF8') { $t0 = Get-Date }
    if ($i % 20 -eq 19) { [void](Save-LegionShot $proc.MainWindowHandle (Join-Path $Out ('waiting-{0:D3}.jpg' -f $i))) }
}
if (-not $t0) { Say 'no window or no creation'; try { $proc.Kill() } catch {}; exit 1 }
Say 'character sent; frames from now'
$n = 0; $pressed = 0
try {
    while (((Get-Date) - $t0).TotalSeconds -lt $Seconds -and -not $proc.HasExited) {
        $s = ((Get-Date) - $t0).TotalSeconds
        $n++
        [void](Save-LegionShot $proc.MainWindowHandle (Join-Path $Out ('classic-{0:D3}-{1:N0}s.jpg' -f $n, $s)))
        if ($s -ge $KeyAt -and $pressed -lt $Keys) {
            $h = $proc.MainWindowHandle
            [void][P690.K]::PostMessage($h, 0x0100, [IntPtr]$KeyCode, [IntPtr]0x01480001); Start-Sleep -Milliseconds 300
            [void][P690.K]::PostMessage($h, 0x0101, [IntPtr]$KeyCode, [IntPtr]([int64]0xC1480001))
            $pressed++
            Say ('posted arrow key ' + $pressed + ' at ' + [math]::Round($s, 1) + ' s')
        }
        $due = $t0.AddSeconds($n * $EverySeconds)
        $w = ($due - (Get-Date)).TotalMilliseconds
        if ($w -gt 0) { Start-Sleep -Milliseconds ([int]$w) }
    }
} finally {
    Say ('frames: ' + $n)
    try { $proc.CloseMainWindow() | Out-Null; Start-Sleep -Seconds 4; if (-not $proc.HasExited) { $proc.Kill() } } catch {}
    try { $j = Get-Content -LiteralPath $settings -Raw | ConvertFrom-Json; $j.password = ''; [IO.File]::WriteAllText($settings, ($j | ConvertTo-Json -Depth 6), (New-Object Text.UTF8Encoding($false))) } catch {}
    Copy-Item -LiteralPath (Join-Path $plugin 'P731Create.log') -Destination $Out -Force -ErrorAction SilentlyContinue
}
Say 'done'
