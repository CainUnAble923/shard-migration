#Requires -Version 5.1
<#
  tasks-shots.ps1 (cc-P789): a TazUO screenshot of the [tasks window on a private proof shard, for the before and after
  shots in notes\cc-P789-review\. Never the shared Test Shard: P281's proof-shard.ps1 refuses 2593 and 2594.

      powershell -NoProfile -ExecutionPolicy Bypass -File tasks-shots.ps1 -Image sl-modernuo:cc-p786 -Name before
          [-Out <folder>] [-Work <scratch>] [-Card isle-01-new-character] [-Port 2596]

  The caller holds the test-shard lock. In order:
    1. a private shard of -Image on 127.0.0.1:<Port> (a copy of the overnight bot world);
    2. its playtest folder gets testers.json (the Golem's Player account) and tasks.json (one task, G-0001, from the
       card in scripts\playtest-task-bank.json, with P773's test id P762-0, as the Goblin hands it out);
    3. TazUO (a copy of D:\UO\tazuo-sl-build\client, the Golem's Player profile, window 1280 x 800 as New-LegionSettings
       sets it) logs the Player in; after -SettleSeconds the script posts Enter, [tasks and Enter to the window (posted
       keys reach the game, cc-P740), waits, and captures the window (Save-LegionShot);
    4. the client closes, the password is cleared from its settings, and the shard is removed (its log kept in -Work).
  Writes <Out>\<Name>.jpg and <Out>\<Name>-log.txt. ASCII only.
#>
param(
    [Parameter(Mandatory)][string]$Image,
    [Parameter(Mandatory)][string]$Name,
    [string]$Out = 'D:\UO\golems\Iron\shard-migration\notes\cc-P789-review',
    [string]$Work = (Join-Path $env:TEMP 'p789-shots'),
    [string]$Card = 'isle-01-new-character',
    [string]$CodeRepo = 'D:\UO\golems\Iron\ShatteredLegacy',
    [int]$Port = 2596,
    [string]$Golem = 'Iron',
    [int]$SettleSeconds = 30,
    [string]$ClientSource = 'D:\UO\tazuo-sl-build\client'
)
$ErrorActionPreference = 'Continue'
. 'D:\UO\golem\LegionTest.ps1'
New-Item -ItemType Directory -Path $Out, $Work -Force | Out-Null
$logFile = Join-Path $Out ($Name + '-log.txt')
Set-Content -LiteralPath $logFile -Value '' -Encoding ASCII
function Say([string]$t) { $l = '[' + (Get-Date).ToString('HH:mm:ss') + '] ' + $t; Write-Host $l; Add-Content -LiteralPath $logFile -Value $l -Encoding ASCII }

$guard = Test-LegionTarget '127.0.0.1' $Port
if (-not $guard.Ok) { Say $guard.Why; exit 2 }

# 1. the private shard
$shardWork = Join-Path $Work 'shard'
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'D:\UO\golems\Iron\shard-migration\notes\cc-P281-tools\proof-shard.ps1' -Work $shardWork -Image $Image -Port $Port
if ($LASTEXITCODE -ne 0) { Say "the private shard did not come up ($Image)"; exit 1 }
Say "private shard up: $Image on 127.0.0.1:$Port"

try {
    # 2. the play test files
    $acc = (& powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'D:\UO\golem\Get-GolemTestAccount.ps1' -Golem $Golem -Role player -Json 2>$null | Select-Object -Last 1) | ConvertFrom-Json
    $user = [string]$acc.Username
    $bank = Get-Content -LiteralPath (Join-Path $CodeRepo 'scripts\playtest-task-bank.json') -Raw | ConvertFrom-Json
    $c = @($bank.cards | Where-Object { $_.key -eq $Card })[0]
    $pt = Join-Path $shardWork 'world\playtest'
    New-Item -ItemType Directory -Path $pt -Force | Out-Null
    $testers = [ordered]@{ version = 1; testers = @([ordered]@{ account = $user; name = "$Golem the Tester"; paused = $false; addedAt = '2026-11-03T05:00:00Z' }) }
    $task = [ordered]@{ id = 'G-0001'; account = $user; card = $c.key; testId = $c.testId; title = $c.title; why = $c.why; where = $c.where
        coords = $c.coords; steps = @($c.steps); lookFor = $c.lookFor; intro = 'The Goblin sniffed this one out of a sand dune. It smells suspicious.'
        needsPlayer = $true; status = 'open'; assignedAt = '2026-11-03T05:00:01Z' }
    $tasks = [ordered]@{ version = 1; tasks = @($task) }
    $enc = New-Object Text.UTF8Encoding($false)
    [IO.File]::WriteAllText((Join-Path $pt 'testers.json'), ($testers | ConvertTo-Json -Depth 6), $enc)
    [IO.File]::WriteAllText((Join-Path $pt 'tasks.json'), ($tasks | ConvertTo-Json -Depth 6), $enc)
    Say "playtest files: tester $Golem the Tester, task G-0001 from card $Card"

    # 3. the client
    $client = Join-Path $Work 'client'
    [void](& robocopy $ClientSource $client /MIR /XD Data LegionScripts Logs Screenshots /NFL /NDL /NJH /NJS /NP /R:1 /W:1)
    [void](& robocopy 'D:\UO\golem\legion-test\Iron\client\Data\Profiles' (Join-Path $client 'Data\Profiles') /E /NFL /NDL /NJH /NJS /NP /R:1 /W:1)
    foreach ($pf in @(Get-ChildItem -LiteralPath (Join-Path $client 'Data\Profiles') -Recurse -Filter 'profile.json')) {
        $j = Get-Content -LiteralPath $pf.FullName -Raw | ConvertFrom-Json
        $j.game_window_full_size = $true
        $j.game_window_position = [pscustomobject]@{ X = 0; Y = 0 }
        [IO.File]::WriteAllText($pf.FullName, ($j | ConvertTo-Json -Depth 20), $enc)
    }
    $settings = Join-Path $client 'settings.p789.json'
    $set = New-LegionSettings '127.0.0.1' $Port $user (ConvertTo-CuoPassword ([string]$acc.Password)) 'D:\UO\UltimaOnlineVanilla'
    [IO.File]::WriteAllText($settings, ($set | ConvertTo-Json -Depth 6), $enc)
    $acc = $null
    if (-not ('P789Keys' -as [type])) {
        Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public static class P789Keys {
    [DllImport("user32.dll")] public static extern bool PostMessage(IntPtr h, uint msg, IntPtr w, IntPtr l);
    public static void Enter(IntPtr h) { PostMessage(h, 0x100, (IntPtr)0x0D, (IntPtr)0x001C0001); PostMessage(h, 0x102, (IntPtr)0x0D, (IntPtr)0x001C0001); PostMessage(h, 0x101, (IntPtr)0x0D, (IntPtr)unchecked((int)0xC01C0001)); }
    public static void Type(IntPtr h, string s) { foreach (var c in s) { PostMessage(h, 0x102, (IntPtr)c, (IntPtr)1); System.Threading.Thread.Sleep(40); } }
}
'@
    }
    $argv = @('-settings', ('"' + $settings + '"'), '-skiploginscreen', '-skipserverselect', '-lastcharactername', ('"' + $Golem + ' the Tester"'))
    $proc = Start-Process -FilePath (Join-Path $client 'TazUO.exe') -ArgumentList $argv -WorkingDirectory $client -PassThru
    try {
        Start-Sleep -Seconds $SettleSeconds
        $proc.Refresh()
        $h = $proc.MainWindowHandle
        Save-LegionShot $h (Join-Path $Out ($Name + '-login.jpg')) | Out-Null
        [P789Keys]::Enter($h); Start-Sleep -Milliseconds 400
        [P789Keys]::Type($h, '[tasks'); Start-Sleep -Milliseconds 400
        [P789Keys]::Enter($h)
        Start-Sleep -Seconds 6
        $p = Join-Path $Out ($Name + '.jpg')
        if (Save-LegionShot $h $p) { Say ('shot: ' + $p) } else { Say 'no window to capture' }
    } finally {
        try { $proc.CloseMainWindow() | Out-Null; Start-Sleep -Seconds 4; if (-not $proc.HasExited) { $proc.Kill() } } catch {}
        try { $j = Get-Content -LiteralPath $settings -Raw | ConvertFrom-Json; $j.password = ''; $j.autologin = $false; [IO.File]::WriteAllText($settings, ($j | ConvertTo-Json -Depth 6), $enc) } catch {}
    }
} finally {
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'D:\UO\golems\Iron\shard-migration\notes\cc-P281-tools\proof-shard.ps1' -Work $shardWork -Down | Out-Null
    $l = Get-Content -LiteralPath (Join-Path $shardWork 'shard.log') -ErrorAction SilentlyContinue | Select-String -Pattern 'PlayTest|tasks' | Select-Object -Last 5
    foreach ($x in $l) { Say ('shard: ' + $x.Line.Trim()) }
    Say 'done'
}
