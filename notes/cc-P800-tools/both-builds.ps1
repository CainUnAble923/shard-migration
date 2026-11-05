# cc-P800: under the docker-build lock, the gated build of main then of the isle copy, one after the other, detached. Writes done.txt.
$t = 'D:\UO\golems\Iron\shard-migration\notes\cc-P800-tools'
Remove-Item -LiteralPath "$t\done.txt" -ErrorAction SilentlyContinue
powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Use-GolemLock.ps1 -Take docker-build -Minutes 40 -Wait
docker run --rm --privileged alpine:3.20 sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches'
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\gated-build.ps1" -Repo 'D:\UO\golems\Iron\ShatteredLegacy' -Tag 'sl-modernuo:cc-p800' -Log "$t\gated-build.log"
docker run --rm --privileged alpine:3.20 sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches'
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\gated-build.ps1" -Repo 'D:\UO\golems\Iron\p800-isle' -Tag 'sl-modernuo:cc-p800-isle' -Log "$t\gated-build-isle.log"
powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Use-GolemLock.ps1 -Release docker-build
'done' | Out-File -FilePath "$t\done.txt"
