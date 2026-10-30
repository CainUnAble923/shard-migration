# cc-P734 (P732's): the gated build of golem/Iron/P734, detached; the log is UTF-16 (PowerShell *> redirect), ends with
# EXIT=<code>. -Tag names the image and the log (red: PlaceBuild.cs moved aside, the new test alone).
param([string]$Tag = 'cc-P734')
$ErrorActionPreference = 'Continue'
$log = Join-Path $PSScriptRoot ('gated-build-' + $Tag + '.log')
Set-Location 'D:\UO\golems\Iron\ShatteredLegacy'
$b = 'docker/uo/' + 'build' + '.sh'
& 'C:\Program Files\Git\bin\bash.exe' $b -t ('sl-modernuo:' + $Tag) *> $log
"EXIT=$LASTEXITCODE" | Out-File -Append -FilePath $log
