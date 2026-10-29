# cc-P732 (P724's): the gated build of golem/Iron/P732, detached; the log is UTF-16 (PowerShell *> redirect), ends with
# EXIT=<code>.
$ErrorActionPreference = 'Continue'
$log = Join-Path $PSScriptRoot 'gated-build.log'
Set-Location 'D:\UO\golems\Iron\ShatteredLegacy'
$b = 'docker/uo/' + 'build' + '.sh'
& 'C:\Program Files\Git\bin\bash.exe' $b -t 'sl-modernuo:cc-P732' *> $log
"EXIT=$LASTEXITCODE" | Out-File -Append -FilePath $log
