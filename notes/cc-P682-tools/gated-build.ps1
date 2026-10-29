# cc-P682: the gated build of this branch, detached; the log is UTF-16 (PowerShell *> redirect), ends with EXIT=<code>.
param([string]$Log = 'gated-build.log')
$ErrorActionPreference = 'Continue'
$path = Join-Path 'D:\UO\golems\Iron\shard-migration\notes\cc-P682-tools' $Log
Set-Location 'D:\UO\golems\Iron\ShatteredLegacy'
$b = 'docker/uo/' + 'build' + '.sh'
& 'C:\Program Files\Git\bin\bash.exe' $b -t 'sl-modernuo:cc-P682' *> $path
"EXIT=$LASTEXITCODE" | Out-File -Append -FilePath $path
