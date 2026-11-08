# cc-P827: both gated builds under the docker-build lock, one after the other, detached.
$t = 'D:\UO\golems\Iron\shard-migration\notes\cc-P827-tools'
$lock = 'D:\UO\golem\Use-GolemLock.ps1'
powershell -NoProfile -ExecutionPolicy Bypass -File $lock -Take docker-build -Minutes 70 -Wait
docker run --rm --privileged alpine:3.20 sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches'
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\gated-build.ps1" -Repo 'D:\UO\golems\Iron\p803-isle' -Tag 'sl-modernuo:cc-P827-isle' -Log "$t\gated-build-isle.log"
docker run --rm --privileged alpine:3.20 sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches'
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\gated-build.ps1" -Repo 'D:\UO\golems\Iron\ShatteredLegacy' -Tag 'sl-modernuo:cc-P827' -Log "$t\gated-build.log"
powershell -NoProfile -ExecutionPolicy Bypass -File $lock -Release docker-build
'done' | Out-File -FilePath "$t\builds-done.txt" -Encoding ascii
