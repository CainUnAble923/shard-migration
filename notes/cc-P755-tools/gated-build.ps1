# cc-P755 (P743's launcher): the gated build of golem/Iron/P755 (the Iron code copy), detached; the log is UTF-16
# (PowerShell *> redirect), ends with EXIT=<code>.
$ErrorActionPreference = 'Continue'
$log = Join-Path $PSScriptRoot 'gated-build.log'
Set-Location 'D:\UO\golems\Iron\ShatteredLegacy'
$b = 'docker/uo/' + 'build' + '.sh'
& 'C:\Program Files\Git\bin\bash.exe' $b -t 'sl-modernuo:cc-P755' *> $log
"EXIT=$LASTEXITCODE" | Out-File -Append -FilePath $log
