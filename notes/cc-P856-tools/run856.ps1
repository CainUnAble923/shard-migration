# cc-P856 (P849's after849.ps1): the TazUO proof runs of the winter set, release (the image testers play) then main,
# under the test-shard lock, each on a fresh copy of the bot world. Writes run-done.txt.
param([string]$RelImage = 'sl-modernuo:cc-p856-isle', [string]$MainImage = 'sl-modernuo:cc-p856')
$t = 'D:\UO\golems\Iron\shard-migration\notes\cc-P856-tools'
$lock = 'D:\UO\golem\Use-GolemLock.ps1'
$proof = 'D:\UO\golems\Iron\p740-proof'
$shots = 'D:\UO\golems\Iron\shard-migration\notes\cc-P856-shots'
Remove-Item -LiteralPath "$t\run-done.txt" -ErrorAction SilentlyContinue
powershell -NoProfile -ExecutionPolicy Bypass -File $lock -Take test-shard -Minutes 50 -Wait
foreach ($r in @(@('kit-isle', $RelImage, 'release'), @('kit', $MainImage, 'main'))) {
    $out = Join-Path $shots $r[2]
    Remove-Item -LiteralPath "$proof\walk.log" -ErrorAction SilentlyContinue
    Start-Process python -ArgumentList "-P $t\kit\stage856.py --name `"Iron Winter`"" -WindowStyle Hidden -RedirectStandardOutput "$proof\stage-out.txt" -RedirectStandardError "$proof\stage-err.txt"
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\$($r[0])\run-tazuo.ps1" -Image $r[1] -Character "Iron Winter" -Script 'Walk856.py' -Out $out -MaxMinutes 8
    Copy-Item "$proof\walk.log" "$out\walk.txt" -Force
    Copy-Item "$proof\stage-out.txt" "$out\stage-out.txt" -Force
    Copy-Item "$proof\stage-err.txt" "$out\stage-err.txt" -Force
}
powershell -NoProfile -ExecutionPolicy Bypass -File $lock -Release test-shard
'done' | Out-File -FilePath "$t\run-done.txt" -Encoding ascii
