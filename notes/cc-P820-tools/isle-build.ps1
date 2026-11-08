# cc-P820: under the docker-build lock, the gated build of the release copy only (run 2, after dropping P801's duplicates).
$t = 'D:\UO\golems\Iron\shard-migration\notes\cc-P820-tools'
Remove-Item -LiteralPath "$t\isle-done.txt" -ErrorAction SilentlyContinue
powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Use-GolemLock.ps1 -Take docker-build -Minutes 25 -Wait
docker run --rm --privileged alpine:3.20 sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches'
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\gated-build.ps1" -Repo 'D:\UO\golems\Iron\p820-isle' -Tag 'sl-modernuo:cc-p820-isle' -Log "$t\gated-build-isle.log"
powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Use-GolemLock.ps1 -Release docker-build
'done' | Out-File -FilePath "$t\isle-done.txt"
