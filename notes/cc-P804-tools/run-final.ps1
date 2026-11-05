#Requires -Version 5.1
# cc-P804: the shots on the final main image, a real restart of that world (patches seeded once, the picked one still hidden or regrown,
# the plant records read), then the isle image's first start. The caller holds the test-shard lock.
$ErrorActionPreference = 'Continue'
$t = 'D:\UO\golems\Iron\shard-migration\notes\cc-P804-tools'
$out = 'D:\UO\golems\Iron\shard-migration\notes\cc-P804-shots\final'
$name = 'sl-p804-proof'
$work = 'D:\UO\golems\Iron\p740-proof\shard'
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\run-tazuo.ps1" -Image 'sl-modernuo:cc-p804' -Character 'Iron Herb' -Script Shots804.py -Out $out -MaxMinutes 8 -KeepShard
Copy-Item -LiteralPath 'D:\UO\golems\Iron\p740-proof\walk.log' -Destination (Join-Path $out 'walk.log') -Force
docker restart $name | Out-Null
for ($i = 0; $i -lt 90; $i++) {
    Start-Sleep -Seconds 2
    $l = docker logs --since 1m $name 2>&1 | Out-String
    if ($l -match 'Listening') { break }
}
Start-Sleep -Seconds 8
docker logs $name > (Join-Path $out 'restart.log') 2>&1
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\proof-shard.ps1" -Work $work -Down
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\proof-shard.ps1" -Work $work -Image 'sl-modernuo:cc-p804-isle' -Overlay 'D:\UO\golems\Iron\p735-work\patched'
Start-Sleep -Seconds 10
docker logs $name > (Join-Path $out 'isle-start.log') 2>&1
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\proof-shard.ps1" -Work $work -Down
