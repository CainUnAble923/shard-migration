#Requires -Version 5.1
<#
  classic-wake.ps1 (cc-P740): the wake in the CLASSIC client (ClassicUO, the player launcher's D:\UO\CUO-Player), on the
  private proof shard (127.0.0.1:2596 only; the caller holds the test-shard lock and the shard is up on the image).
  ClassicUO has no Legion scripting, so: a fresh copy of the client, no profiles; P731's creation plugin rebuilt for
  ClassicUO's .NET Framework host (plugin472, test only) makes the character from the character list; TazUO's own
  override list (p740-proof\tazuo\uo-override, the branch's map on the SoS land) is passed as -uofilesoverride; then a
  frame every -EverySeconds. At -KeyAt seconds after the window is up, one Down-arrow key press is posted to the window
  (WM_KEYDOWN/UP; the real keyboard is never touched): a move, which gets the trainee up. If the client ignores posted
  keys, the 60 s safety gets them up instead, the same slow get-up.

      classic-wake.ps1 -Character "Iron Classic" -Out <folder> [-Seconds 80] [-KeyAt 20]
#>
param(
    [Parameter(Mandatory)][string]$Character,
    [Parameter(Mandatory)][string]$Out,
    [int]$Seconds = 80,
    [int]$KeyAt = 20,
    [double]$EverySeconds = 0.5,
    [int]$Port = 2596
)
$ErrorActionPreference = 'Continue'
. 'D:\UO\golem\LegionTest.ps1'
Add-Type -Namespace P740 -Name K -MemberDefinition @'
[DllImport("user32.dll")] public static extern bool PostMessage(System.IntPtr h, uint m, System.IntPtr w, System.IntPtr l);
'@
$proof = 'D:\UO\golems\Iron\p740-proof'
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
Copy-Item -Path 'C:\Users\ckfle\AppData\Local\Temp\claude\D--UO-golems-Iron-shard-migration\05eadec1-1186-4790-a3c9-46bbeb603ba6\scratchpad\plugin472\out\P731Create.dll' -Destination $plugin -Force
& python -P (Join-Path $PSScriptRoot 'make_create_bin.py') $Character (Join-Path $plugin 'create.bin') | ForEach-Object { Say ([string]$_) }
Remove-Item -LiteralPath (Join-Path $plugin 'P731Create.log') -ErrorAction SilentlyContinue
# run 4: a new ClassicUO profile opens the paperdoll over the scene when it has no saved windows; give it an empty list
$gdir = Join-Path $client ('Data\Profiles\iron-player\_\' + $Character)
New-Item -ItemType Directory -Path $gdir -Force | Out-Null
# run 5: it opens anyway; so the game view moves right of it: ClassicUO's own default profile (from run 4) with
# game_window_position 420,10 (p740-proof\classic-profile-template.json)
Copy-Item -LiteralPath (Join-Path $proof 'classic-profile-template.json') -Destination (Join-Path $gdir 'profile.json') -Force
[IO.File]::WriteAllText((Join-Path $gdir 'gumps.xml'), '<?xml version="1.0" encoding="utf-8" standalone="yes"?>' + "`r`n<gumps>`r`n</gumps>`r`n", (New-Object Text.UTF8Encoding($true)))
$override = Join-Path $proof 'tazuo\uo-override\files-override.txt'
if (-not (Test-Path $override)) { Say 'no override list (run the TazUO walk first)'; exit 1 }

$acc = (& powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'D:\UO\golem\Get-GolemTestAccount.ps1' -Golem Iron -Role player -Json 2>$null | Select-Object -Last 1) | ConvertFrom-Json
$set = New-LegionSettings '127.0.0.1' $Port ([string]$acc.Username) (ConvertTo-CuoPassword ([string]$acc.Password)) 'D:\UO\UltimaOnlineVanilla'
$acc = $null
$set.autologin = $false
$set.plugins = @((Join-Path $plugin 'P731Create.dll'))
$settings = Join-Path $client 'settings.p740.json'
[IO.File]::WriteAllText($settings, ($set | ConvertTo-Json -Depth 6), (New-Object Text.UTF8Encoding($false)))
$argv = @('-settings', ('"' + $settings + '"'), '-skiploginscreen', '-lastcharactername', ('"' + $Character + '"'), '-uofilesoverride', ('"' + $override + '"'))
$proc = Start-Process -FilePath (Join-Path $client 'ClassicUO.exe') -ArgumentList $argv -WorkingDirectory $client -PassThru
Say ('ClassicUO started, pid ' + $proc.Id)

# the window, then the frames
$t0 = $null
for ($i = 0; $i -lt 120 -and -not $t0; $i++) {
    Start-Sleep -Milliseconds 500
    $proc.Refresh()
    if ($proc.HasExited) { Say 'ClassicUO exited'; break }
    if ($proc.MainWindowHandle -ne [IntPtr]::Zero -and (Get-Content -Raw (Join-Path $plugin 'P731Create.log') -ErrorAction SilentlyContinue) -match 'sent 0xF8') { $t0 = Get-Date }
    if ($i % 20 -eq 19) { [void](Save-LegionShot $proc.MainWindowHandle (Join-Path $Out ('waiting-{0:D3}.jpg' -f $i))) }   # run 3: where it stops
}
if (-not $t0) { Say 'no window or no creation'; try { $proc.Kill() } catch {}; exit 1 }
Say 'character sent; frames from now'
$n = 0; $keyed = $false
try {
    while (((Get-Date) - $t0).TotalSeconds -lt $Seconds -and -not $proc.HasExited) {
        $s = ((Get-Date) - $t0).TotalSeconds
        $n++
        [void](Save-LegionShot $proc.MainWindowHandle (Join-Path $Out ('classic-{0:D3}-{1:N1}s.jpg' -f $n, $s)))
        if (-not $keyed -and $s -ge $KeyAt) {
            $keyed = $true
            $h = $proc.MainWindowHandle
            [void][P740.K]::PostMessage($h, 0x0100, [IntPtr]0x28, [IntPtr]0x01500001); Start-Sleep -Milliseconds 80
            [void][P740.K]::PostMessage($h, 0x0101, [IntPtr]0x28, [IntPtr]([int64]0xC1500001))
            Say ('posted a Down-arrow key at ' + [math]::Round($s, 1) + ' s')
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
