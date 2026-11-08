# cc-P820: under the docker-build lock, the gated build of main, then of the release copy (update 12 + the diff). Writes builds-done.txt.
$t = 'D:\UO\golems\Iron\shard-migration\notes\cc-P820-tools'
Remove-Item -LiteralPath "$t\builds-done.txt" -ErrorAction SilentlyContinue
foreach ($b in @(@('D:\UO\golems\Iron\ShatteredLegacy', 'sl-modernuo:cc-p820', 'gated-build.log'), @('D:\UO\golems\Iron\p820-isle', 'sl-modernuo:cc-p820-isle', 'gated-build-isle.log'))) {
    powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Use-GolemLock.ps1 -Take docker-build -Minutes 25 -Wait
    docker run --rm --privileged alpine:3.20 sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches'
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\gated-build.ps1" -Repo $b[0] -Tag $b[1] -Log (Join-Path $t $b[2])
    powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Use-GolemLock.ps1 -Release docker-build
}
'done' | Out-File -FilePath "$t\builds-done.txt"
