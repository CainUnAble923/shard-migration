# cc-P806: m4 again, then the final gated builds of the release copy and main, one after the other, detached.
$bash = 'C:\Program Files\Git\bin\bash.exe'
$env:M_NAME = 'm4b-rook-faces-north'; $env:M_FILE = 'HavenSpots.cs'; $env:M_SED = 's/RookFacing = Direction\.South/RookFacing = Direction.North/'
& $bash 'D:/UO/golems/Iron/shard-migration/notes/cc-P806-tools/mutant.sh' 'FullyQualifiedName~NewHaven' *> 'D:\UO\golems\Iron\shard-migration\notes\cc-P806-tools\mutant-logs\m4b-rook-faces-north.txt'
Remove-Item Env:M_NAME, Env:M_FILE, Env:M_SED
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'D:\UO\golems\Iron\shard-migration\notes\cc-P806-tools\gated-build-isle.ps1'
& docker run --rm --privileged alpine:3.20 sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches'
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'D:\UO\golems\Iron\shard-migration\notes\cc-P806-tools\gated-build-main.ps1'
'ALL DONE' | Out-File -FilePath 'D:\UO\golems\Iron\shard-migration\notes\cc-P806-tools\final-done.txt' -Encoding ascii
