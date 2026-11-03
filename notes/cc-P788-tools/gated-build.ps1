# cc-P788 (P763's): the gated build of a code copy, detached; the log is UTF-16 (PowerShell *> redirect), ends with EXIT=<code>.
#   gated-build.ps1 -Repo <code copy> -Tag <image tag> -Log <log file>
param(
    [string]$Repo = 'D:\UO\golems\Iron\p788-isle',
    [string]$Tag = 'sl-modernuo:cc-p788-isle',
    [string]$Log = 'D:\UO\golems\Iron\shard-migration\notes\cc-P788-tools\gated-build-isle.log'
)
$ErrorActionPreference = 'Continue'
Set-Location $Repo
$b = 'docker/uo/' + 'build' + '.sh'
& 'C:\Program Files\Git\bin\bash.exe' $b -t $Tag *> $Log
"EXIT=$LASTEXITCODE" | Out-File -Append -FilePath $Log
