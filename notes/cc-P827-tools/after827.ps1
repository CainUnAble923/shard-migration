# cc-P827: the after shots and walks of the League field office, release (the image testers play) then main, under the
# test-shard lock (a copy of notes/cc-P803-tools/before.ps1 with P827's images, walk scripts and review folder).
param([string]$RelImage = 'sl-modernuo:cc-P827-isle', [string]$MainImage = 'sl-modernuo:cc-P827')
$t = 'D:\UO\golems\Iron\shard-migration\notes\cc-P827-tools'
$lock = 'D:\UO\golem\Use-GolemLock.ps1'
$proof = 'D:\UO\golems\Iron\p740-proof'
$review = 'D:\UO\golems\Iron\shard-migration\notes\cc-P827-review'
powershell -NoProfile -ExecutionPolicy Bypass -File $lock -Take test-shard -Minutes 40 -Wait
Start-Process python -ArgumentList "-P $t\stage827.py --name `"Iron Stock`"" -WindowStyle Hidden -RedirectStandardOutput "$proof\stage-out.txt" -RedirectStandardError "$proof\stage-err.txt"
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\run-tazuo.ps1" -Image $RelImage -Character "Iron Stock" -Script 'Walk827Rel.py' -Out "$review\shots-release-after" -MaxMinutes 7
Copy-Item "$proof\walk.log" "$review\shots-release-after\walk.txt" -Force
Copy-Item "$proof\stage-out.txt" "$review\shots-release-after\stage-out.txt" -Force
Start-Process python -ArgumentList "-P $t\stage827.py --name `"Iron Main`"" -WindowStyle Hidden -RedirectStandardOutput "$proof\stage-out.txt" -RedirectStandardError "$proof\stage-err.txt"
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\main\run-tazuo.ps1" -Image $MainImage -Character "Iron Main" -Script 'Walk827Main.py' -Out "$review\shots-main-after" -MaxMinutes 7
Copy-Item "$proof\walk.log" "$review\shots-main-after\walk.txt" -Force
Copy-Item "$proof\stage-out.txt" "$review\shots-main-after\stage-out.txt" -Force
powershell -NoProfile -ExecutionPolicy Bypass -File $lock -Release test-shard
'done after' | Out-File -FilePath "$t\after-done.txt" -Encoding ascii
