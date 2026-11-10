# cc-P862 (P867's): the gated build of the code copy; the log is UTF-16 (PowerShell *> redirect), ends with EXIT=<code>.
# Takes and releases the docker-build lock itself, drops the Docker VM's page cache first. Writes build-done.txt.
param(
    [string]$Repo = 'D:\UO\golems\Iron\ShatteredLegacy',
    [string]$Tag = 'sl-modernuo:cc-P862',
    [string]$Log = 'D:\UO\golems\Iron\shard-migration\notes\cc-P862-tools\gated-build.log'
)
$ErrorActionPreference = 'Continue'
$t = 'D:\UO\golems\Iron\shard-migration\notes\cc-P862-tools'
$lock = 'D:\UO\golem\Use-GolemLock.ps1'
Remove-Item -LiteralPath "$t\build-done.txt" -ErrorAction SilentlyContinue
powershell -NoProfile -ExecutionPolicy Bypass -File $lock -Take docker-build -Minutes 90 -Wait
docker run --rm --privileged alpine:3.20 sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches'
Set-Location $Repo
$b = 'docker/uo/' + 'build' + '.sh'
& 'C:\Program Files\Git\bin\bash.exe' $b -t $Tag *> $Log
"EXIT=$LASTEXITCODE" | Out-File -Append -FilePath $Log
powershell -NoProfile -ExecutionPolicy Bypass -File $lock -Release docker-build
'done' | Out-File -FilePath "$t\build-done.txt"
