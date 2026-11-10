# cc-P859 (P855's run855.ps1): the TazUO proof run of the Horn of Plenty on main, under the test-shard lock, on a fresh
# copy of the bot world. Run 1 wrote cc-P859-shots; the pig runs 2-11 wrote cc-P859-shots/runN-pig (run 11 kept).
# Writes run-done.txt.
param([string]$Image = 'sl-modernuo:cc-p859')
$t = 'D:\UO\golems\Iron\shard-migration\notes\cc-P859-tools'
$lock = 'D:\UO\golem\Use-GolemLock.ps1'
$proof = 'D:\UO\golems\Iron\p740-proof'
$out = 'D:\UO\golems\Iron\shard-migration\notes\cc-P859-shots\run11-pig'
Remove-Item -LiteralPath "$t\run-done.txt" -ErrorAction SilentlyContinue
powershell -NoProfile -ExecutionPolicy Bypass -File $lock -Take test-shard -Minutes 45 -Wait
Remove-Item -LiteralPath "$proof\walk.log" -ErrorAction SilentlyContinue
Start-Process python -ArgumentList "-P $t\kit\stage859.py --name `"Iron Harvest`"" -WindowStyle Hidden -RedirectStandardOutput "$proof\stage-out.txt" -RedirectStandardError "$proof\stage-err.txt"
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\kit\run-tazuo.ps1" -Image $Image -Character "Iron Harvest" -Script 'Walk859.py' -Out $out -MaxMinutes 14
Copy-Item "$proof\walk.log" "$out\walk.txt" -Force
Copy-Item "$proof\stage-out.txt" "$out\stage-out.txt" -Force
Copy-Item "$proof\stage-err.txt" "$out\stage-err.txt" -Force
powershell -NoProfile -ExecutionPolicy Bypass -File $lock -Release test-shard
'done' | Out-File -FilePath "$t\run-done.txt" -Encoding ascii
