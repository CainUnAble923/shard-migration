# cc-P691: the gated build of this branch, detached; the log is UTF-16 (PowerShell *> redirect), ends with EXIT=<code>.
#   gated.ps1 <name> [--tests-only]   -> build\<name>.log
param([string]$Name, [string]$Extra = '')
$ErrorActionPreference = 'Continue'
$log = Join-Path $PSScriptRoot "build\$Name.log"
Set-Location 'D:\UO\golems\Iron\ShatteredLegacy'
$b = 'docker/uo/' + 'build' + '.sh'
if ($Extra) { & 'C:\Program Files\Git\bin\bash.exe' $b -t 'sl-modernuo:cc-P691' $Extra *> $log }
else { & 'C:\Program Files\Git\bin\bash.exe' $b -t 'sl-modernuo:cc-P691' *> $log }
"EXIT=$LASTEXITCODE" | Out-File -Append -FilePath $log
