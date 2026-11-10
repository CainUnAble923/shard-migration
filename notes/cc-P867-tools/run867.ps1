# cc-P867: P855's run855.ps1 for the house rounds. (P849's after849.ps1): the TazUO proof run of the decor addons on main, under the test-shard lock, on a fresh copy
# of the bot world. Writes run-done.txt.
param([string]$Image = 'sl-modernuo:cc-P867')
$t = 'D:\UO\golems\Iron\shard-migration\notes\cc-P867-tools'
$lock = 'D:\UO\golem\Use-GolemLock.ps1'
$proof = 'D:\UO\golems\Iron\p740-proof'
$out = 'D:\UO\golems\Iron\shard-migration\notes\cc-P867-review\shots'
Remove-Item -LiteralPath "$t\run-done.txt" -ErrorAction SilentlyContinue
powershell -NoProfile -ExecutionPolicy Bypass -File $lock -Take test-shard -Minutes 45 -Wait
Remove-Item -LiteralPath "$proof\walk.log" -ErrorAction SilentlyContinue
Start-Process python -ArgumentList "-P $t\kit\stage867.py --name `"Iron Hearth`"" -WindowStyle Hidden -RedirectStandardOutput "$proof\stage-out.txt" -RedirectStandardError "$proof\stage-err.txt"
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\kit\run-tazuo.ps1" -Image $Image -Character "Iron Hearth" -Script 'Walk867Town.py' -Out $out -MaxMinutes 20
Copy-Item "$proof\walk.log" "$out\walk.txt" -Force
Copy-Item "$proof\stage-out.txt" "$out\stage-out.txt" -Force
Copy-Item "$proof\stage-err.txt" "$out\stage-err.txt" -Force
powershell -NoProfile -ExecutionPolicy Bypass -File $lock -Release test-shard
'done' | Out-File -FilePath "$t\run-done.txt" -Encoding ascii
