# cc-P813: the gated build of the isle release copy of a code copy, detached; the log is UTF-16 (PowerShell *> redirect), ends with EXIT=<code>.
param(
    [string]$Repo = 'D:\UO\golems\Iron\p813-isle',
    [string]$Tag = 'sl-modernuo:cc-p813-isle',
    [string]$Log = 'D:\UO\golems\Iron\shard-migration\notes\cc-P813-tools\gated-build-isle.log'
)
$ErrorActionPreference = 'Continue'
Set-Location $Repo
$b = 'docker/uo/' + 'build' + '.sh'
& 'C:\Program Files\Git\bin\bash.exe' $b -t $Tag *> $Log
"EXIT=$LASTEXITCODE" | Out-File -Append -FilePath $Log
