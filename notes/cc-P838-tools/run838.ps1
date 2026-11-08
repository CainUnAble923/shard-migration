# cc-P838 (P820's run820.ps1): the jail lesson walked by a fresh Player character in TazUO on both images, private proof
# shard 127.0.0.1:2596, one test-shard lock each. Shots into notes\cc-P838-review\shots-main and shots-isle. Writes walks-done.txt.
$t = 'D:\UO\golems\Iron\shard-migration\notes\cc-P838-tools'
$r = 'D:\UO\golems\Iron\shard-migration\notes\cc-P838-review'
$p = 'D:\UO\golems\Iron\p740-proof'
Remove-Item -LiteralPath "$t\walks-done.txt" -ErrorAction SilentlyContinue
$runs = @(
    @{ Name = 'Iron Main';  Image = 'sl-modernuo:cc-P838';      Kit = "$t\main"; Script = 'Walk838Main.py'; Out = "$r\shots-main"; Log = 'walk-main.log' },
    @{ Name = 'Iron Stock'; Image = 'sl-modernuo:cc-P838-isle'; Kit = $t;        Script = 'Walk838Isle.py'; Out = "$r\shots-isle"; Log = 'walk-isle.log' }
)
foreach ($run in $runs) {
    powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Use-GolemLock.ps1 -Take test-shard -Minutes 20 -Wait
    Remove-Item -Recurse -Force -LiteralPath $run.Out -ErrorAction SilentlyContinue
    $stageArgs = '-P "' + "$t\stage801.py" + '" --name "' + $run.Name + '"'
    Start-Process python -ArgumentList $stageArgs -WindowStyle Hidden -RedirectStandardOutput "$p\stage-out.txt" -RedirectStandardError "$p\stage-err.txt"
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $run.Kit 'run-tazuo.ps1') -Image $run.Image -Character $run.Name -Script $run.Script -Out $run.Out -MaxMinutes 7
    Copy-Item "$p\walk.log" (Join-Path $t $run.Log) -Force -ErrorAction SilentlyContinue
    Copy-Item "$p\stage-out.txt" $run.Out -Force -ErrorAction SilentlyContinue
    powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Use-GolemLock.ps1 -Release test-shard
}
'done' | Out-File -FilePath "$t\walks-done.txt"
