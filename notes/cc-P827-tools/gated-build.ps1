# cc-P827: the gated build of a code copy, detached; the log is UTF-16, ends with EXIT=<code>.
param([string]$Repo, [string]$Tag, [string]$Log)
$ErrorActionPreference = 'Continue'
Set-Location $Repo
$b = 'docker/uo/' + 'build' + '.sh'
& 'C:\Program Files\Git\bin\bash.exe' $b -t $Tag *> $Log
"EXIT=$LASTEXITCODE" | Out-File -Append -FilePath $Log
