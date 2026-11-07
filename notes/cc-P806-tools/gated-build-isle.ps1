# cc-P799: the gated build of the isle release copy, detached; the log is UTF-16, ends with EXIT=<code>.
param(
    [string]$Repo = 'D:\UO\golems\Iron\p799-isle',
    [string]$Tag = 'sl-modernuo:cc-p806-isle',
    [string]$Log = 'D:\UO\golems\Iron\shard-migration\notes\cc-P806-tools\gated-build-isle.txt'
)
$ErrorActionPreference = 'Continue'
Set-Location $Repo
$b = 'docker/uo/' + 'build' + '.sh'
& 'C:\Program Files\Git\bin\bash.exe' $b -t $Tag *> $Log
"EXIT=$LASTEXITCODE" | Out-File -Append -FilePath $Log
