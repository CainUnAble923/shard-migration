# cc-P769: our TazUO build of the code copy's client\patches (with 0010, the skirt colour) to a private folder.
# The log ends with EXIT=<code>.
#   client-build.ps1 [-Repo <code copy>] [-Out <folder>] [-Log <log file>]
param(
    [string]$Repo = 'D:\UO\golems\Iron\ShatteredLegacy',
    [string]$Out = 'D:\UO\golems\Iron\p769-client',
    [string]$Log = 'D:\UO\golems\Iron\shard-migration\notes\cc-P769-tools\client-build.log'
)
$ErrorActionPreference = 'Continue'
& (Join-Path $Repo 'client\Build-Client.ps1') -Out $Out *> $Log
"EXIT=$LASTEXITCODE" | Out-File -Append -FilePath $Log
