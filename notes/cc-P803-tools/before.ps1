# cc-P803: the before shots of the League field office, release (the image testers play) then main, under the test-shard lock.
param([string]$RelImage = 'sl-modernuo:isle12-20261107', [string]$MainImage = 'sl-modernuo:cc-p817', [string]$Phase = 'before')
$t = 'D:\UO\golems\Iron\shard-migration\notes\cc-P803-tools'
$lock = 'D:\UO\golem\Use-GolemLock.ps1'
$proof = 'D:\UO\golems\Iron\p740-proof'
$review = 'D:\UO\golems\Iron\shard-migration\notes\cc-P803-review'
powershell -NoProfile -ExecutionPolicy Bypass -File $lock -Take test-shard -Minutes 30 -Wait
$rs = 'WalkRel' + (Get-Culture).TextInfo.ToTitleCase($Phase) + '.py'
$ms = 'WalkMain' + (Get-Culture).TextInfo.ToTitleCase($Phase) + '.py'
Start-Process python -ArgumentList "-P $t\stage803.py --name `"Iron Stock`"" -WindowStyle Hidden -RedirectStandardOutput "$proof\stage-out.txt" -RedirectStandardError "$proof\stage-err.txt"
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\run-tazuo.ps1" -Image $RelImage -Character "Iron Stock" -Script $rs -Out "$review\shots-release-$Phase" -MaxMinutes 6
Copy-Item "$proof\walk.log" "$review\shots-release-$Phase\walk.txt" -Force
Copy-Item "$proof\stage-out.txt" "$review\shots-release-$Phase\stage-out.txt" -Force
Start-Process python -ArgumentList "-P $t\stage803.py --name `"Iron Main`"" -WindowStyle Hidden -RedirectStandardOutput "$proof\stage-out.txt" -RedirectStandardError "$proof\stage-err.txt"
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\main\run-tazuo.ps1" -Image $MainImage -Character "Iron Main" -Script $ms -Out "$review\shots-main-$Phase" -MaxMinutes 6
Copy-Item "$proof\walk.log" "$review\shots-main-$Phase\walk.txt" -Force
Copy-Item "$proof\stage-out.txt" "$review\shots-main-$Phase\stage-out.txt" -Force
powershell -NoProfile -ExecutionPolicy Bypass -File $lock -Release test-shard
"done $Phase" | Out-File -FilePath "$t\$Phase-done.txt" -Encoding ascii
