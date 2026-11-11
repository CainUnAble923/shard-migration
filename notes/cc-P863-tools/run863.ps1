# cc-P863 (P872's run872.ps1): the TazUO proof run of Color Wars under the test-shard lock, on a fresh copy of the bot
# world on -Image, with the other team's player (foe863.py, the uobot client) alongside. Writes run-done.txt.
param([string]$Image = 'sl-modernuo:cc-p863', [string]$Name = 'main')
$t = 'D:\UO\golems\Iron\shard-migration\notes\cc-P863-tools'
$lock = 'D:\UO\golem\Use-GolemLock.ps1'
$proof = 'D:\UO\golems\Iron\p740-proof'
$out = Join-Path 'D:\UO\golems\Iron\shard-migration\notes\cc-P863-shots' $Name
Remove-Item -LiteralPath "$t\run-done.txt" -ErrorAction SilentlyContinue
powershell -NoProfile -ExecutionPolicy Bypass -File $lock -Take test-shard -Minutes 40 -Wait
Remove-Item -LiteralPath "$proof\walk.log" -ErrorAction SilentlyContinue
Start-Process python -ArgumentList "-P $t\kit\foe863.py" -WindowStyle Hidden -RedirectStandardOutput "$proof\foe-out.txt" -RedirectStandardError "$proof\foe-err.txt"
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\kit\run-tazuo.ps1" -Image $Image -Character "Iron Wars" -Script 'Walk863.py' -Out $out -MaxMinutes 12
Copy-Item "$proof\walk.log" "$out\walk.txt" -Force
Copy-Item "$proof\foe-out.txt" "$out\foe-out.txt" -Force
Copy-Item "$proof\foe-err.txt" "$out\foe-err.txt" -Force
powershell -NoProfile -ExecutionPolicy Bypass -File $lock -Release test-shard
'done' | Out-File -FilePath "$t\run-done.txt" -Encoding ascii
