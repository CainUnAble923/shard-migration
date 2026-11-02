# cc-P769: the player package's own build of the code copy (no publish), to a private folder; the log ends with EXIT=<code>.
# The client is the private build with client patch 0010 (client-build.ps1), since the client gate checks every patch.
#   package-build.ps1 [-Repo <code copy>] [-TazUO <client folder>] [-Out <folder>] [-Log <log file>]
param(
    [string]$Repo = 'D:\UO\golems\Iron\ShatteredLegacy',
    [string]$TazUO = 'D:\UO\golems\Iron\p769-client\client',
    [string]$UoData = 'D:\UO\tool-trials\client-data-copy',
    [string]$Out = 'D:\UO\golems\Iron\p769-pkg',
    [string]$Log = (Join-Path 'D:\UO\golems\Iron\shard-migration\notes\cc-P769-tools' 'package-build.log')
)
$ErrorActionPreference = 'Continue'
Set-Location $Repo
$b = Join-Path $Repo ('player-package\' + 'Build-Player' + 'Package.ps1')
& $b -TazUO $TazUO -UoData $UoData -Out $Out *> $Log
"EXIT=$LASTEXITCODE" | Out-File -Append -FilePath $Log
