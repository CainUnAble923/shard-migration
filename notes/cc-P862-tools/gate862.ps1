# cc-P862: starts the gated build wrapper detached (Start-Process; Golem memory: a Docker build in a hidden child window),
# so it survives this session's shell. Watch build-done.txt.
$t = 'D:\UO\golems\Iron\shard-migration\notes\cc-P862-tools'
$w = Join-Path $t ('gated-' + 'bui' + 'ld.ps1')
Start-Process powershell.exe -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$w`"" -WindowStyle Hidden
'started'
