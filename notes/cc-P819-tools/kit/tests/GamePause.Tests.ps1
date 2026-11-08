#Requires -Version 5.1
<#
  GamePause.Tests.ps1 (cc-P819). Facts for GamePause.ps1, Test-GameRunning.ps1, Set-GamePause.ps1 and the game check in
  LegionTest.ps1's Test-LegionTarget. Some facts use a fake list of processes; the real ones start a fake game: a copy
  of ping.exe renamed FakeGame.exe in a temp steamapps\common\FakeGame folder (harmless: it pings loopback), and stop
  it after. A temp kit root (its own settings.json, gamePausePc set to this PC) is used throughout, never the real one.

      powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\tests\GamePause.Tests.ps1 [-Kit D:\UO\golem] [-Only <name part>]

  Prints PASS/FAIL per fact; the exit code is the number of failed checks. ASCII only.
#>
param([string]$Kit = 'D:\UO\golem', [string]$Only)
$ErrorActionPreference = 'Stop'
$script:fails = 0; $script:passes = 0
function Assert-True($cond, [string]$what) { if ($cond) { $script:passes++ } else { $script:fails++; Write-Host ('    FAIL: ' + $what) -ForegroundColor Red } }
function Fact([string]$name, [scriptblock]$body) {
    if ($Only -and $name -notlike "*$Only*") { return }
    $before = $script:fails
    try { & $body } catch { $script:fails++; Write-Host ('    FAIL (threw): ' + $_.Exception.Message + ' | ' + $_.InvocationInfo.PositionMessage) -ForegroundColor Red }
    if ($script:fails -eq $before) { Write-Host "PASS $name" -ForegroundColor Green } else { Write-Host "FAIL $name" -ForegroundColor Red }
}

$lib = Join-Path $Kit 'GamePause.ps1'
if (Test-Path -LiteralPath $lib) { . $lib } else { Write-Host ('no ' + $lib) -ForegroundColor Red }
$cli = Join-Path $Kit 'Test-GameRunning.ps1'
$setter = Join-Path $Kit 'Set-GamePause.ps1'

$tmp = Join-Path ([IO.Path]::GetTempPath()) ('gamepause-' + [guid]::NewGuid().ToString('N').Substring(0, 8))
$root = Join-Path $tmp 'kit'
New-Item -ItemType Directory -Force -Path $root | Out-Null
function Set-Root([bool]$On = $true, [string]$Pc = $env:COMPUTERNAME) {
    $j = [ordered]@{ maxPerRun = 6; gamePause = $On; gamePausePc = $Pc }
    [IO.File]::WriteAllText((Join-Path $root 'settings.json'), ($j | ConvertTo-Json), (New-Object Text.UTF8Encoding $false))
}
Set-Root
$gameDir = Join-Path $tmp 'Steam\steamapps\common\FakeGame'
New-Item -ItemType Directory -Force -Path $gameDir | Out-Null
$fakeExe = Join-Path $gameDir 'FakeGame.exe'
Copy-Item -LiteralPath (Join-Path $env:SystemRoot 'System32\PING.EXE') -Destination $fakeExe
function Start-FakeGame { Start-Process -FilePath $fakeExe -ArgumentList @('-n', '600', '127.0.0.1') -WindowStyle Hidden -PassThru }
function Stop-FakeGame($p) { if ($p -and -not $p.HasExited) { Stop-Process -Id $p.Id -Force; $p.WaitForExit(10000) | Out-Null } }
function Run-Cli([string[]]$a) {
    $out = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $cli @a 2>&1 | ForEach-Object { [string]$_ }
    [pscustomobject]@{ Exit = $LASTEXITCODE; Text = ($out -join "`n") }
}

try {
    Fact 'OurOwnUoClientsAndWallpaperEngineAreNeverAnotherGame' {
        $procs = @(
            @{ Name = 'TazUO'; Path = 'D:\UO\tazuo-sl-build\client\TazUO.exe' },
            @{ Name = 'ClassicUO'; Path = 'C:\Games\ClassicUO\ClassicUO.exe' },
            @{ Name = 'UOSA'; Path = 'C:\Program Files (x86)\Electronic Arts\Ultima Online Enhanced\UOSA.exe' },
            @{ Name = 'client'; Path = 'C:\Program Files (x86)\Electronic Arts\Ultima Online Classic\client.exe' },
            @{ Name = 'steam'; Path = 'C:\Program Files (x86)\Steam\steam.exe' },
            @{ Name = 'wallpaperui'; Path = 'D:\SteamLibrary\steamapps\common\wallpaper_enginein\wallpaperui.exe' },
            @{ Name = 'wallpaper64'; Path = 'D:\SteamLibrary\steamapps\common\wallpaper_engine\wallpaper64.exe' })
        $g = Test-GolemGameRunning -Root $root -Fake @{ Processes = $procs }
        Assert-True (-not $g.Running) ('our clients and a launcher counted as a game: ' + ($g.Games -join ', '))
    }

    Fact 'AGameUnderSteamappsCountsAndIsNamed' {
        $procs = @(@{ Name = 'TazUO'; Path = 'D:\UO\tazuo-sl-build\client\TazUO.exe' }, @{ Name = 'eldenring'; Path = 'C:\Steam\steamapps\common\ELDEN RING\Game\eldenring.exe' })
        $g = Test-GolemGameRunning -Root $root -Fake @{ Processes = $procs }
        Assert-True $g.Running 'eldenring under steamapps\common is not seen'
        Assert-True ($g.Game -eq 'eldenring') ('the game is named ' + $g.Game)
        $s = Get-GamePauseState -Root $root -Fake @{ Processes = $procs }
        Assert-True ($s.Applies -and $s.Why -eq 'waiting: Chase is playing eldenring') ('the state line: ' + $s.Why)
    }

    Fact 'TheSwitchOffAndAnotherPcMeanNoPause' {
        $procs = @(@{ Name = 'eldenring'; Path = 'C:\Steam\steamapps\common\ELDEN RING\Game\eldenring.exe' })
        Set-Root -On $false
        $s = Get-GamePauseState -Root $root -Fake @{ Processes = $procs }
        Assert-True (-not $s.Applies -and -not $s.On) ('the pause applies while switched off: ' + $s.Why)
        Set-Root -Pc 'SOME-OTHER-PC'
        $s = Get-GamePauseState -Root $root -Fake @{ Processes = $procs }
        Assert-True (-not $s.Applies -and $s.On) ('the pause applies on another PC: ' + $s.Why)
        Remove-Item -LiteralPath (Join-Path $root 'settings.json')
        $c = Get-GamePauseConfig $root
        Assert-True ($c.On -and $c.Pc -eq 'CHASES-TOWER') 'with no settings the pause is on, for the game PC'
        Set-Root
    }

    Fact 'SetGamePauseWritesTheKeyAndKeepsTheRest' {
        $null = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $setter -Off -Root $root
        $j = Get-Content -LiteralPath (Join-Path $root 'settings.json') -Raw | ConvertFrom-Json
        Assert-True ($j.gamePause -eq $false) 'gamePause is not false after -Off'
        Assert-True ($j.maxPerRun -eq 6 -and $j.gamePausePc -eq $env:COMPUTERNAME) 'another key was lost'
        $null = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $setter -On -Root $root
        $j = Get-Content -LiteralPath (Join-Path $root 'settings.json') -Raw | ConvertFrom-Json
        Assert-True ($j.gamePause -eq $true) 'gamePause is not true after -On'
    }

    Fact 'WaitGoesOnWhenTheGameClosesAndShowsItMeanwhile' {
        $script:n = 0
        $probe = { $script:n++; [pscustomobject]@{ Applies = $true; On = $true; Running = ($script:n -lt 3); Game = 'eldenring'; Why = 'x' } }
        $script:t = Get-Date '2026-11-08T01:00:00'
        $script:lines = New-Object System.Collections.Generic.List[string]
        $script:seen = $null
        $file = Join-Path $root 'game-wait-Night.json'
        $r = Wait-GolemNoGame -Root $root -Who 'Night' -What 'the overnight play tests' -Until ([datetime]'2026-11-08T06:30:00') -IntervalSeconds 600 `
            -Probe $probe -Clock { $script:t } -Sleep { param($s) if (Test-Path -LiteralPath $file) { $script:seen = Get-Content -LiteralPath $file -Raw | ConvertFrom-Json }; $script:t = $script:t.AddSeconds($s) } `
            -Log { param($l) $script:lines.Add($l) }
        Assert-True ($r.Outcome -eq 'clear') ('outcome ' + $r.Outcome)
        Assert-True ([int]$r.Waited.TotalMinutes -eq 20) ('waited ' + $r.Waited)
        Assert-True ($script:seen -and $script:seen.line -eq 'waiting: Chase is playing eldenring' -and $script:seen.who -eq 'Night') 'no status file while waiting'
        Assert-True (-not (Test-Path -LiteralPath $file)) 'the status file is left behind'
        Assert-True ($script:lines[0] -like 'waiting: Chase is playing eldenring*every 10 min until 06:30') ('first line: ' + $script:lines[0])
        Assert-True ($script:lines[-1] -like 'the game closed: the overnight play tests goes on (waited 20 min)') ('last line: ' + $script:lines[-1])
    }

    Fact 'WaitGivesUpAtTheEndOfTheNight' {
        $probe = { [pscustomobject]@{ Applies = $true; On = $true; Running = $true; Game = 'eldenring'; Why = 'x' } }
        $script:t = Get-Date '2026-11-08T05:55:00'
        $script:lines = New-Object System.Collections.Generic.List[string]
        $r = Wait-GolemNoGame -Root $root -Who 'Night' -What 'the overnight play tests' -Until ([datetime]'2026-11-08T06:30:00') -IntervalSeconds 600 `
            -Probe $probe -Clock { $script:t } -Sleep { param($s) $script:t = $script:t.AddSeconds($s) } -Log { param($l) $script:lines.Add($l) }
        Assert-True ($r.Outcome -eq 'timeout') ('outcome ' + $r.Outcome)
        Assert-True ($script:t -eq [datetime]'2026-11-08T06:30:00') ('stopped at ' + $script:t)
        Assert-True ($script:lines[-1] -like 'still playing eldenring at 06:30: the overnight play tests is skipped*') ('last line: ' + $script:lines[-1])
    }

    Fact 'TheCliSeesARealFakeGameAndNotAfterItCloses' {
        $p = Start-FakeGame
        try {
            Start-Sleep -Milliseconds 800
            $r = Run-Cli @('-Root', $root)
            Assert-True ($r.Exit -eq 1) ('exit ' + $r.Exit + ' with a game running: ' + $r.Text)
            Assert-True ($r.Text -eq 'waiting: Chase is playing FakeGame') ('line: ' + $r.Text)
        } finally { Stop-FakeGame $p }
        $r = Run-Cli @('-Root', $root)
        Assert-True ($r.Exit -eq 0 -and $r.Text -eq 'no game running') ('after: exit ' + $r.Exit + ': ' + $r.Text)
        Set-Root -On $false
        $p = Start-FakeGame
        try { Start-Sleep -Milliseconds 800; $r = Run-Cli @('-Root', $root); Assert-True ($r.Exit -eq 0) ('pause off but exit ' + $r.Exit) } finally { Stop-FakeGame $p; Set-Root }
    }

    Fact 'TheCliWaitsWhileTheFakeGameRunsAndGoesOnWhenItCloses' {
        $p = Start-FakeGame
        $out = Join-Path $tmp 'wait-out.txt'
        $w = $null
        try {
            Start-Sleep -Milliseconds 800
            $w = Start-Process -FilePath 'powershell.exe' -ArgumentList @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', ('"' + $cli + '"'), '-Wait', '-IntervalSeconds', '2', '-Who', 'FactBot', '-What', '"the fact"', '-Root', ('"' + $root + '"')) -WindowStyle Hidden -RedirectStandardOutput $out -PassThru
            $null = $w.Handle   # PowerShell 5.1 keeps ExitCode only when the handle is read while it runs
            $file = Join-Path $root 'game-wait-FactBot.json'
            $deadline = (Get-Date).AddSeconds(20)
            while (-not (Test-Path -LiteralPath $file) -and (Get-Date) -lt $deadline) { Start-Sleep -Milliseconds 300 }
            Assert-True (Test-Path -LiteralPath $file) 'no game-wait file while it waits'
            Start-Sleep -Seconds 3
            Assert-True (-not $w.HasExited) 'it did not wait while the game ran'
        } finally { Stop-FakeGame $p }
        $w.WaitForExit(30000) | Out-Null
        Assert-True $w.HasExited 'it still waits after the game closed'
        Assert-True ($w.ExitCode -eq 0) ('exit ' + $w.ExitCode)
        $text = Get-Content -LiteralPath $out -Raw
        Assert-True ($text -match 'waiting: Chase is playing FakeGame' -and $text -match 'the game closed: the fact goes on') ('output: ' + $text)
        Assert-True (-not (Test-Path -LiteralPath (Join-Path $root 'game-wait-FactBot.json'))) 'the game-wait file is left behind'
    }

    Fact 'TheLegionGuardRefusesWhileAGameRuns' {
        . (Join-Path $Kit 'LegionTest.ps1')
        $script:LegionGameCheck = $false
        $own = @('127.0.0.1')
        $playing = [pscustomobject]@{ Applies = $true; On = $true; Running = $true; Game = 'eldenring'; Why = 'waiting: Chase is playing eldenring' }
        $r = Test-LegionTarget '127.0.0.1' 2596 $own $playing
        Assert-True (-not $r.Ok) 'a client may open while a game runs'
        Assert-True ($r.Why -like 'waiting: Chase is playing eldenring*Test-GameRunning.ps1 -Wait*') ('why: ' + $r.Why)
        $clear = [pscustomobject]@{ Applies = $true; On = $true; Running = $false; Game = ''; Why = 'no game running' }
        Assert-True ((Test-LegionTarget '127.0.0.1' 2596 $own $clear).Ok) 'refused with no game'
        $off = [pscustomobject]@{ Applies = $false; On = $false; Running = $true; Game = 'eldenring'; Why = 'game pause off' }
        Assert-True ((Test-LegionTarget '127.0.0.1' 2596 $own $off).Ok) 'refused with the pause off'
        Assert-True (-not (Test-LegionTarget '127.0.0.1' 2593 $own $clear).Ok) 'the live port is no longer refused'
    }
} finally {
    Remove-Item -LiteralPath $tmp -Recurse -Force -ErrorAction SilentlyContinue
}
Write-Host ("{0} passed, {1} failed" -f $script:passes, $script:fails)
exit $script:fails
