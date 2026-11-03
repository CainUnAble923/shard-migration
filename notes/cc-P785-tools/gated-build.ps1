# cc-P785 (P781 and P763): the gated build of a code copy, detached; the log is UTF-16 (PowerShell *> redirect), ends with EXIT=<code>.
#   gated-build.ps1 -Repo <code copy> -Tag <image tag> -Log <log file>
param(
    [string]$Repo = 'D:\UO\golems\Iron\ShatteredLegacy',
    [string]$Tag = 'sl-modernuo:cc-p785',
    [string]$Log = 'D:\UO\golems\Iron\shard-migration\notes\cc-P785-tools\gated-build.log'
)
$ErrorActionPreference = 'Continue'
Set-Location $Repo
$b = 'docker/uo/' + 'build' + '.sh'
& 'C:\Program Files\Git\bin\bash.exe' $b -t $Tag *> $Log
"EXIT=$LASTEXITCODE" | Out-File -Append -FilePath $Log
