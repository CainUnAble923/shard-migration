# cc-P806: a world as P799's image seeds it (crosswise bench, Rook facing north), saved, for the upgrade check.
$tools = 'D:\UO\golems\Iron\shard-migration\notes\cc-P806-tools'
$work = 'D:\UO\golems\Iron\p740-proof\shard'
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $tools 'proof-shard.ps1') -Work $work -Image sl-modernuo:cc-p799-isle -Overlay 'D:\UO\golems\Iron\p749-proof\overlay'
Start-Sleep -Seconds 20
& python -P (Join-Path $tools 'save806.py')
Start-Sleep -Seconds 5
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $tools 'proof-shard.ps1') -Work $work -Down
"EXIT=done"
