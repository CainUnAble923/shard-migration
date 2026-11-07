# cc-P810: one proof-shot run on the private shard (2596), log to run-shots.log.
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'D:\UO\golems\Iron\shard-migration\notes\cc-P810-tools\run-tazuo.ps1' -Image 'sl-modernuo:cc-p810' -Character 'Iron Events' -Script 'Shots810.py' -Out 'D:\UO\golems\Iron\shard-migration\notes\cc-P810-shots' -MaxMinutes 15 *> 'D:\UO\golems\Iron\shard-migration\notes\cc-P810-tools\run-shots.log'
"EXIT=$LASTEXITCODE" | Out-File -Append -FilePath 'D:\UO\golems\Iron\shard-migration\notes\cc-P810-tools\run-shots.log'
