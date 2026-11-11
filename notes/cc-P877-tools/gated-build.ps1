# cc-P877: under the docker-build lock, the gated build of the code copy (golem/Iron/P877) as sl-modernuo:cc-P877, page
# cache dropped first; `latest` is not moved. The log is UTF-16 (PowerShell *> redirect), ends with EXIT=<code>.
# Writes build-done.txt.
param(
    [string]$Repo = 'D:\UO\golems\Iron\ShatteredLegacy',
    [string]$Tag = 'sl-modernuo:cc-P877',
    [string]$Log = 'D:\UO\golems\Iron\shard-migration\notes\cc-P877-tools\gated-build.log'
)
$ErrorActionPreference = 'Continue'
$t = 'D:\UO\golems\Iron\shard-migration\notes\cc-P877-tools'
Remove-Item -LiteralPath "$t\build-done.txt" -ErrorAction SilentlyContinue
powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Use-GolemLock.ps1 -Take docker-build -Minutes 40 -Wait
docker run --rm --privileged alpine:3.20 sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches'
Set-Location $Repo
$b = 'docker/uo/' + 'build' + '.sh'
& 'C:\Program Files\Git\bin\bash.exe' $b -t $Tag *> $Log
"EXIT=$LASTEXITCODE" | Out-File -Append -FilePath $Log
powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Use-GolemLock.ps1 -Release docker-build
'done' | Out-File -FilePath "$t\build-done.txt"
