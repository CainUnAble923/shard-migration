# cc-P872 (P857's): under the docker-build lock, the gated build of main (golem/Iron/P872) as sl-modernuo:cc-p872,
# page cache dropped first. The log is UTF-16 (PowerShell *> redirect) and ends with EXIT=<code>. Writes build-done.txt.
param(
    [string]$Repo = 'D:\UO\golems\Iron\ShatteredLegacy',
    [string]$Tag = 'sl-modernuo:cc-p872',
    [string]$Log = 'D:\UO\golems\Iron\shard-migration\notes\cc-P872-tools\gated-build.log'
)
$ErrorActionPreference = 'Continue'
$t = 'D:\UO\golems\Iron\shard-migration\notes\cc-P872-tools'
Remove-Item -LiteralPath "$t\build-done.txt" -ErrorAction SilentlyContinue
powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Use-GolemLock.ps1 -Take docker-build -Minutes 40 -Wait
docker run --rm --privileged alpine:3.20 sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches'
Set-Location $Repo
$b = 'docker/uo/' + 'build' + '.sh'
& 'C:\Program Files\Git\bin\bash.exe' $b -t $Tag *> $Log
"EXIT=$LASTEXITCODE" | Out-File -Append -FilePath $Log
powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Use-GolemLock.ps1 -Release docker-build
'done' | Out-File -FilePath "$t\build-done.txt"
