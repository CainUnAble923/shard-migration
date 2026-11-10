# cc-P862 (P867's run867.ps1): the TazUO proof run of Battle Chess on main, under the test-shard lock, on a fresh copy of
# the bot world: chessbot862.py (the admin through uobot) is the opponent; Chess862.py is the trainee's script. Shots go to
# notes\cc-P862-shots. Writes run-done.txt.
param([string]$Image = 'sl-modernuo:cc-P862')
$t = 'D:\UO\golems\Iron\shard-migration\notes\cc-P862-tools'
$lock = 'D:\UO\golem\Use-GolemLock.ps1'
$proof = 'D:\UO\golems\Iron\p740-proof'
$out = 'D:\UO\golems\Iron\shard-migration\notes\cc-P862-shots'
Remove-Item -LiteralPath "$t\run-done.txt" -ErrorAction SilentlyContinue
powershell -NoProfile -ExecutionPolicy Bypass -File $lock -Take test-shard -Minutes 45 -Wait
Remove-Item -LiteralPath "$proof\walk.log" -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path "$proof\stage" -Force | Out-Null
Start-Process python -ArgumentList "-P $t\kit\chessbot862.py --name `"Iron Chess`"" -WindowStyle Hidden -RedirectStandardOutput "$proof\chessbot-out.txt" -RedirectStandardError "$proof\chessbot-err.txt"
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\kit\run-tazuo.ps1" -Image $Image -Character "Iron Chess" -Script 'Chess862.py' -Out $out -MaxMinutes 20
Copy-Item "$proof\walk.log" "$out\walk.txt" -Force
Copy-Item "$proof\chessbot-out.txt" "$out\chessbot-out.txt" -Force
Copy-Item "$proof\chessbot-err.txt" "$out\chessbot-err.txt" -Force
Copy-Item "$proof\stage\chessbot-transcript.txt" "$out\chessbot-transcript.txt" -Force -ErrorAction SilentlyContinue
powershell -NoProfile -ExecutionPolicy Bypass -File $lock -Release test-shard
'done' | Out-File -FilePath "$t\run-done.txt" -Encoding ascii
