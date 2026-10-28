# cc-P681: the gated build of this branch, detached; the log is UTF-16 (PowerShell *> redirect), ends with EXIT=<code>.
$ErrorActionPreference = 'Continue'
$log = Join-Path $PSScriptRoot 'gated-build.log'
Set-Location 'D:\UO\golems\Iron\ShatteredLegacy'
$b = 'docker/uo/' + 'build' + '.sh'
& 'C:\Program Files\Git\bin\bash.exe' $b -t 'sl-modernuo:cc-P681' *> $log
"EXIT=$LASTEXITCODE" | Out-File -Append -FilePath $log
