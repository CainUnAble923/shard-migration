# cc-P741 (P733's): the gated build of golem/Iron/P741 (the Iron code copy), detached; the log is UTF-16 (PowerShell
# *> redirect), ends with EXIT=<code>.
$ErrorActionPreference = 'Continue'
$log = Join-Path $PSScriptRoot 'gated-build.log'
Set-Location 'D:\UO\golems\Iron\ShatteredLegacy'
$b = 'docker/uo/' + 'build' + '.sh'
& 'C:\Program Files\Git\bin\bash.exe' $b -t 'sl-modernuo:cc-P741' *> $log
"EXIT=$LASTEXITCODE" | Out-File -Append -FilePath $log
