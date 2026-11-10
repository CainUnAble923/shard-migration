# cc-P855 (P849's after849.ps1): the TazUO proof run of the decor addons on main, under the test-shard lock, on a fresh copy
# of the bot world. Writes run-done.txt.
param([string]$Image = 'sl-modernuo:cc-p855')
$t = 'D:\UO\golems\Iron\shard-migration\notes\cc-P855-tools'
$lock = 'D:\UO\golem\Use-GolemLock.ps1'
$proof = 'D:\UO\golems\Iron\p740-proof'
$out = 'D:\UO\golems\Iron\shard-migration\notes\cc-P855-shots\player'
Remove-Item -LiteralPath "$t\run-done.txt" -ErrorAction SilentlyContinue
powershell -NoProfile -ExecutionPolicy Bypass -File $lock -Take test-shard -Minutes 40 -Wait
Remove-Item -LiteralPath "$proof\walk.log" -ErrorAction SilentlyContinue
Start-Process python -ArgumentList "-P $t\kit\stage855.py --name `"Iron Decor`"" -WindowStyle Hidden -RedirectStandardOutput "$proof\stage-out.txt" -RedirectStandardError "$proof\stage-err.txt"
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\kit\run-tazuo.ps1" -Image $Image -Character "Iron Decor" -Script 'Walk855.py' -Out $out -MaxMinutes 12
Copy-Item "$proof\walk.log" "$out\walk.txt" -Force
Copy-Item "$proof\stage-out.txt" "$out\stage-out.txt" -Force
Copy-Item "$proof\stage-err.txt" "$out\stage-err.txt" -Force
powershell -NoProfile -ExecutionPolicy Bypass -File $lock -Release test-shard
'done' | Out-File -FilePath "$t\run-done.txt" -Encoding ascii
