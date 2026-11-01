# cc-P758 (after P722, P731, P733 and P749): the gated build of release/isle-20261028, detached; the log is UTF-16 (PowerShell *> redirect),
# ends with EXIT=<code>.
$ErrorActionPreference = 'Continue'
$log = Join-Path $PSScriptRoot 'gated-build.log'
Set-Location 'D:\UO\golems\Iron\release-isle-20261028'
$b = 'docker/uo/' + 'build' + '.sh'
& 'C:\Program Files\Git\bin\bash.exe' $b -t 'sl-modernuo:cc-P758' *> $log
"EXIT=$LASTEXITCODE" | Out-File -Append -FilePath $log
