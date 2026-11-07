# cc-P812: one proof-shot run on the private shard (2596), log to run-shots.log. Keeps the shard up so the capture file can be
# copied out of its world folder, then takes it down.
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'D:\UO\golems\Iron\shard-migration\notes\cc-P812-tools\run-tazuo.ps1' -Image 'sl-modernuo:cc-p812' -Character 'Iron Tools' -Script 'Shots812.py' -Out 'D:\UO\golems\Iron\shard-migration\notes\cc-P812-shots' -MaxMinutes 12 *> 'D:\UO\golems\Iron\shard-migration\notes\cc-P812-tools\run-shots.log'
"EXIT=$LASTEXITCODE" | Out-File -Append -FilePath 'D:\UO\golems\Iron\shard-migration\notes\cc-P812-tools\run-shots.log'
