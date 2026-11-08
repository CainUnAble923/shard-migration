# cc-P818 isle release (P817's, P811's): the gated build of the release copy, detached; the log is UTF-16 (PowerShell *>
# redirect), ends with EXIT=<code>.
param(
    [string]$Repo = 'D:\UO\golems\Iron\p818-isle',
    [string]$Tag = 'sl-modernuo:cc-p818-isle',
    [string]$Log = 'D:\UO\golems\Iron\shard-migration\notes\cc-P818-tools\gated-build-isle.log'
)
$ErrorActionPreference = 'Continue'
Set-Location $Repo
$b = 'docker/uo/' + 'build' + '.sh'
& 'C:\Program Files\Git\bin\bash.exe' $b -t $Tag *> $Log
"EXIT=$LASTEXITCODE" | Out-File -Append -FilePath $Log
