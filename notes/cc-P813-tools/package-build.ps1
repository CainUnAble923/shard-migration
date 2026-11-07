# cc-P813: the player package's own build of a code copy (no publish), to a private folder; the log ends with EXIT=<code>.
# No client patch in this prompt, so the builder's own client (D:\UO\tazuo-sl-build) is used.
#   package-build.ps1 [-Repo <code copy>] [-Out <folder>] [-Log <log file>]
param(
    [string]$Repo = 'D:\UO\golems\Iron\ShatteredLegacy',
    [string]$UoData = 'D:\UO\tool-trials\client-data-copy',
    [string]$Out = 'D:\UO\golems\Iron\p813-pkg',
    [string]$Log = (Join-Path 'D:\UO\golems\Iron\shard-migration\notes\cc-P813-tools' 'package-build.log')
)
$ErrorActionPreference = 'Continue'
Set-Location $Repo
$b = Join-Path $Repo ('player-package\' + 'Build-Player' + 'Package.ps1')
& $b -UoData $UoData -Out $Out *> $Log
"EXIT=$LASTEXITCODE" | Out-File -Append -FilePath $Log
