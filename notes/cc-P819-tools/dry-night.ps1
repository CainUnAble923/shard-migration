# cc-P819: one night's dry run of the overnight runner's game pause, on the game PC with the installed kit's check.
# A fake game (ping.exe copied as FakeGame.exe under a temp ...\steamapps\common\FakeGame) runs from 23:50-ish for about
# 70 seconds; the runner, started with one open play-test item (T-047) so the night has work, waits for it (checking
# every 20 s instead of 600), resumes when it closes, then stops at Rule 1 because its bot root's path names a repo
# (shard-migration): nothing is built, no worktree, no container, the shared test shard never touched, no email
# (-NoEmail). Its overnight.log, the evidence, is copied beside this script as dry-night-overnight.log.
#     powershell -NoProfile -ExecutionPolicy Bypass -File dry-night.ps1 -Work <scratch folder>
param([Parameter(Mandatory)][string]$Work, [string]$Code = 'D:\UO\golems\Iron\ShatteredLegacy', [int]$GameSeconds = 70)
$ErrorActionPreference = 'Stop'
$gameDir = Join-Path $Work 'Steam\steamapps\common\FakeGame'
New-Item -ItemType Directory -Force -Path $gameDir | Out-Null
$exe = Join-Path $gameDir 'FakeGame.exe'
Copy-Item -LiteralPath (Join-Path $env:SystemRoot 'System32\PING.EXE') -Destination $exe -Force
$plays = Join-Path $Work 'play-tests.json'
[IO.File]::WriteAllText($plays, '{"schema": 1, "items": [{"id": "T-047", "status": "open", "resultAt": "", "reopenedAt": ""}]}')
$bot = Join-Path $Work 'shard-migration-dryrun\bot'
if (Test-Path -LiteralPath $bot) { Remove-Item -LiteralPath $bot -Recurse -Force }
$game = Start-Process -FilePath $exe -ArgumentList @('-n', '900', '127.0.0.1') -WindowStyle Hidden -PassThru
Start-Sleep -Seconds 1
$stopper = Start-Job -ScriptBlock { param($id, $s) Start-Sleep -Seconds $s; Stop-Process -Id $id -Force } -ArgumentList $game.Id, $GameSeconds
$ErrorActionPreference = 'Continue'
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $Code 'tools\playtest-bot\Run-OvernightPlaytests.ps1') `
    -PlayTests $plays -RunsRoot (Join-Path $Work 'runs') -BotRoot $bot -NoEmail -ArchiveDrive (Join-Path $Work 'nocloud') `
    -GameIntervalSeconds 20 2>&1 | ForEach-Object { [string]$_ }
"runner exit: $LASTEXITCODE"
Wait-Job $stopper | Out-Null; Remove-Job $stopper
if (-not $game.HasExited) { Stop-Process -Id $game.Id -Force }
$log = Join-Path $bot 'overnight.log'
Copy-Item -LiteralPath $log -Destination (Join-Path $PSScriptRoot 'dry-night-overnight.log') -Force
'--- overnight.log'
Get-Content -LiteralPath $log
