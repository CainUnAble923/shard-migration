# cc-P871 (P857's run857.ps1): the TazUO proof run of the six carpet styles laid non-square, under the test-shard lock,
# on a fresh copy of the bot world on -Image. Writes run-done.txt.
param([string]$Image = 'sl-modernuo:cc-p871', [string]$Name = 'main')
$t = 'D:\UO\golems\Iron\shard-migration\notes\cc-P871-tools'
$lock = 'D:\UO\golem\Use-GolemLock.ps1'
$proof = 'D:\UO\golems\Iron\p740-proof'
$out = Join-Path 'D:\UO\golems\Iron\shard-migration\notes\cc-P871-shots' $Name
Remove-Item -LiteralPath "$t\run-done.txt" -ErrorAction SilentlyContinue
powershell -NoProfile -ExecutionPolicy Bypass -File $lock -Take test-shard -Minutes 40 -Wait
Remove-Item -LiteralPath "$proof\walk.log" -ErrorAction SilentlyContinue
Start-Process python -ArgumentList "-P $t\kit\stage871.py --name `"Iron Carpet`"" -WindowStyle Hidden -RedirectStandardOutput "$proof\stage-out.txt" -RedirectStandardError "$proof\stage-err.txt"
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\kit\run-tazuo.ps1" -Image $Image -Character "Iron Carpet" -Script 'Walk871.py' -Out $out -MaxMinutes 12
Copy-Item "$proof\walk.log" "$out\walk.txt" -Force
Copy-Item "$proof\stage-out.txt" "$out\stage-out.txt" -Force
Copy-Item "$proof\stage-err.txt" "$out\stage-err.txt" -Force
powershell -NoProfile -ExecutionPolicy Bypass -File $lock -Release test-shard
'done' | Out-File -FilePath "$t\run-done.txt" -Encoding ascii
