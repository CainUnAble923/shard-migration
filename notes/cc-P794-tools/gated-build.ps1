# cc-P794 (P769's): the gated build of a code copy, detached; the log is UTF-16 (PowerShell *> redirect), ends with EXIT=<code>.
param(
    [string]$Repo = 'D:\UO\golems\Iron\ShatteredLegacy',
    [string]$Tag = 'sl-modernuo:cc-p794',
    [string]$Log = 'D:\UO\golems\Iron\shard-migration\notes\cc-P794-tools\gated-build.log'
)
$ErrorActionPreference = 'Continue'
Set-Location $Repo
$b = 'docker/uo/' + 'build' + '.sh'
& 'C:\Program Files\Git\bin\bash.exe' $b -t $Tag *> $Log
"EXIT=$LASTEXITCODE" | Out-File -Append -FilePath $Log
