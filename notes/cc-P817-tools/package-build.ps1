# cc-P817 (P769's): the player package's own build of a code copy (no publish), to a private folder; the log ends with
# EXIT=<code>. The client is the private build with client patch 0012 (client-build.ps1): the client gate checks every patch.
#   package-build.ps1 [-Repo <code copy>] [-Out <folder>] [-Log <log file>]
param(
    [string]$Repo = 'D:\UO\golems\Iron\ShatteredLegacy',
    [string]$TazUO = 'D:\UO\golems\Iron\p817-client\client',
    [string]$UoData = 'D:\UO\tool-trials\client-data-copy',
    [string]$Out = 'D:\UO\golems\Iron\p817-pkg',
    [string]$Log = (Join-Path 'D:\UO\golems\Iron\shard-migration\notes\cc-P817-tools' 'package-build.log')
)
$ErrorActionPreference = 'Continue'
Set-Location $Repo
$b = Join-Path $Repo ('player-package\' + 'Build-Player' + 'Package.ps1')
& $b -TazUO $TazUO -UoData $UoData -Out $Out *> $Log
"EXIT=$LASTEXITCODE" | Out-File -Append -FilePath $Log
