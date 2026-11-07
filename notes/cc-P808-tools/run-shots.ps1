# cc-P808: one detached shot run; writes run-shots.done when finished.
$t = 'D:\UO\golems\Iron\shard-migration\notes\cc-P808-tools'
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $t 'run-tazuo.ps1') -Image 'sl-modernuo:cc-p808' -Character 'Iron Cogs' -Script 'Shots808.py' -Out 'D:\UO\golems\Iron\shard-migration\notes\cc-P808-shots' -MaxMinutes 15 *> (Join-Path $t 'run-shots.log')
'done' | Out-File (Join-Path $t 'run-shots.done')
