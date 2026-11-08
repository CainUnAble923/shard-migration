# cc-P849 (P827's after827.ps1): the after shots of the League field office, release (the image testers play) then main,
# under the test-shard lock, each on a fresh copy of the bot world. Writes after-done.txt.
param([string]$RelImage = 'sl-modernuo:cc-p849-isle', [string]$MainImage = 'sl-modernuo:cc-p849')
$t = 'D:\UO\golems\Iron\shard-migration\notes\cc-P849-tools'
$lock = 'D:\UO\golem\Use-GolemLock.ps1'
$proof = 'D:\UO\golems\Iron\p740-proof'
$review = 'D:\UO\golems\Iron\shard-migration\notes\cc-P849-review'
Remove-Item -LiteralPath "$t\after-done.txt" -ErrorAction SilentlyContinue
powershell -NoProfile -ExecutionPolicy Bypass -File $lock -Take test-shard -Minutes 40 -Wait
Remove-Item -LiteralPath "$proof\walk.log" -ErrorAction SilentlyContinue
Start-Process python -ArgumentList "-P $t\stage849.py --name `"Iron Stock`"" -WindowStyle Hidden -RedirectStandardOutput "$proof\stage-out.txt" -RedirectStandardError "$proof\stage-err.txt"
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\run-tazuo.ps1" -Image $RelImage -Character "Iron Stock" -Script 'Walk849Rel.py' -Out "$review\shots-release-after" -MaxMinutes 7
Copy-Item "$proof\walk.log" "$review\shots-release-after\walk.txt" -Force
Copy-Item "$proof\stage-out.txt" "$review\shots-release-after\stage-out.txt" -Force
Remove-Item -LiteralPath "$proof\walk.log" -ErrorAction SilentlyContinue
Start-Process python -ArgumentList "-P $t\stage849.py --name `"Iron Main`"" -WindowStyle Hidden -RedirectStandardOutput "$proof\stage-out.txt" -RedirectStandardError "$proof\stage-err.txt"
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\main\run-tazuo.ps1" -Image $MainImage -Character "Iron Main" -Script 'Walk849Main.py' -Out "$review\shots-main-after" -MaxMinutes 7
Copy-Item "$proof\walk.log" "$review\shots-main-after\walk.txt" -Force
Copy-Item "$proof\stage-out.txt" "$review\shots-main-after\stage-out.txt" -Force
powershell -NoProfile -ExecutionPolicy Bypass -File $lock -Release test-shard
'done after' | Out-File -FilePath "$t\after-done.txt" -Encoding ascii
