# cc-P809: one proof-shot run on the private shard (2596), log to run-shots.log.
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'D:\UO\golems\Iron\shard-migration\notes\cc-P809-tools\run-tazuo.ps1' -Image 'sl-modernuo:cc-p809' -Character 'Iron Perch' -Script 'Shots809.py' -Out 'D:\UO\golems\Iron\shard-migration\notes\cc-P809-shots' -MaxMinutes 15 *> 'D:\UO\golems\Iron\shard-migration\notes\cc-P809-tools\run-shots.log'
"EXIT=$LASTEXITCODE" | Out-File -Append -FilePath 'D:\UO\golems\Iron\shard-migration\notes\cc-P809-tools\run-shots.log'
