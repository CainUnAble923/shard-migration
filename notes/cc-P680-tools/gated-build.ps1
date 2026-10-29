# cc-P680: the gated build of this branch, detached; the log is UTF-16 (PowerShell *> redirect), ends with EXIT=<code>.
param([string]$Log = 'gated-build.log', [string]$Tag = 'sl-modernuo:cc-P680')
$ErrorActionPreference = 'Continue'
$log = Join-Path $PSScriptRoot $Log
Set-Location 'D:\UO\golems\Iron\ShatteredLegacy'
$b = 'docker/uo/' + 'build' + '.sh'
& 'C:\Program Files\Git\bin\bash.exe' $b -t $Tag *> $log
"EXIT=$LASTEXITCODE" | Out-File -Append -FilePath $log
