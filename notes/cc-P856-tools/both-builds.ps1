# cc-P856 (P849's): under the docker-build lock, the gated build of main (golem/Iron/P856), then of the release copy
# (p856-isle: release/isle-20261028 at 6459dd3 plus this change). Page cache dropped before each. Writes builds-done.txt.
$t = 'D:\UO\golems\Iron\shard-migration\notes\cc-P856-tools'
Remove-Item -LiteralPath "$t\builds-done.txt" -ErrorAction SilentlyContinue
foreach ($b in @(@('D:\UO\golems\Iron\ShatteredLegacy', 'sl-modernuo:cc-p856', 'gated-build.log'), @('D:\UO\golems\Iron\p856-isle', 'sl-modernuo:cc-p856-isle', 'gated-build-isle.log'))) {
    powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Use-GolemLock.ps1 -Take docker-build -Minutes 40 -Wait
    docker run --rm --privileged alpine:3.20 sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches'
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\gated-build.ps1" -Repo $b[0] -Tag $b[1] -Log (Join-Path $t $b[2])
    powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Use-GolemLock.ps1 -Release docker-build
}
'done' | Out-File -FilePath "$t\builds-done.txt"
