# cc-P848 (P838's run838.ps1): two real-client runs on the private proof shard 127.0.0.1:2596 under one test-shard lock.
#  A: P838's release build (sl-modernuo:cc-P838-isle) on a fresh copy of the bot world: the hall with the stray stop 2 signpost
#     (the "before" shots), then [save.
#  B: this build (sl-modernuo:cc-p848-isle) on that same saved world (-KeepWorld): the old signpost is taken away on load, the
#     housing lesson walked on foot to the new stop 2, and the hall shot again. Writes walks-done.txt.
param([switch]$AfterOnly)  # cc-P848 run 2: only B, again on run A's saved world
$t = 'D:\UO\golems\Iron\shard-migration\notes\cc-P848-tools'
$r = 'D:\UO\golems\Iron\shard-migration\notes\cc-P848-review'
$p = 'D:\UO\golems\Iron\p740-proof'
Remove-Item -LiteralPath "$t\walks-done.txt" -ErrorAction SilentlyContinue
powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Use-GolemLock.ps1 -Take test-shard -Minutes 40 -Wait
$runs = @(
    @{ Name = 'Iron Stock'; Image = 'sl-modernuo:cc-P838-isle'; Script = 'Walk848Before.py'; Out = "$r\shots-before"; Log = 'walk-before.log'; Keep = $false },
    @{ Name = 'Iron Lawn';  Image = 'sl-modernuo:cc-p848-isle'; Script = 'Walk848Isle.py';   Out = "$r\shots-after";  Log = 'walk-after.log';  Keep = $true }
)
if ($AfterOnly) { $runs = @($runs[1]) }
foreach ($run in $runs) {
    Remove-Item -Recurse -Force -LiteralPath $run.Out -ErrorAction SilentlyContinue
    Remove-Item -LiteralPath "$p\walk.log" -ErrorAction SilentlyContinue  # run 1: a failed run copied P838's old walk.log
    $stageArgs = '-P "' + "$t\stage801.py" + '" --name "' + $run.Name + '"'
    Start-Process python -ArgumentList $stageArgs -WindowStyle Hidden -RedirectStandardOutput "$p\stage-out.txt" -RedirectStandardError "$p\stage-err.txt"
    $a = @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', "$t\run-tazuo.ps1", '-Image', $run.Image, '-Character', $run.Name, '-Script', $run.Script, '-Out', $run.Out, '-MaxMinutes', '7')
    if ($run.Keep) { $a += '-KeepWorld' }
    & powershell.exe @a
    Copy-Item "$p\walk.log" (Join-Path $t $run.Log) -Force -ErrorAction SilentlyContinue
    Copy-Item "$p\stage-out.txt" $run.Out -Force -ErrorAction SilentlyContinue
    Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object { $_.CommandLine -like '*cc-P848-tools*stage801.py*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
}
powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Use-GolemLock.ps1 -Release test-shard
'done' | Out-File -FilePath "$t\walks-done.txt"
