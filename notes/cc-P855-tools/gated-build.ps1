# cc-P855: the gated build of the code copy; the log is UTF-16 (PowerShell *> redirect), ends with EXIT=<code>. Writes build-done.txt.
param(
    [string]$Repo = 'D:\UO\golems\Iron\ShatteredLegacy',
    [string]$Tag = 'sl-modernuo:cc-p855',
    [string]$Log = 'D:\UO\golems\Iron\shard-migration\notes\cc-P855-tools\gated-build.log'
)
$ErrorActionPreference = 'Continue'
$t = 'D:\UO\golems\Iron\shard-migration\notes\cc-P855-tools'
Remove-Item -LiteralPath "$t\build-done.txt" -ErrorAction SilentlyContinue
docker run --rm --privileged alpine:3.20 sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches'
Set-Location $Repo
$b = 'docker/uo/' + 'build' + '.sh'
& 'C:\Program Files\Git\bin\bash.exe' $b -t $Tag *> $Log
"EXIT=$LASTEXITCODE" | Out-File -Append -FilePath $Log
'done' | Out-File -FilePath "$t\build-done.txt"
