# cc-P813: gate 4 (and 6) alone against the package this prompt built; the log ends with EXIT=<code>.
param(
    [string]$Repo = 'D:\UO\golems\Iron\ShatteredLegacy',
    [string]$Zip = 'D:\UO\golems\Iron\p813-pkg\ShatteredLegacy-2026.11.07.1347.zip',
    [string]$Log = 'D:\UO\golems\Iron\shard-migration\notes\cc-P813-tools\checkzip.log'
)
$ErrorActionPreference = 'Continue'
Set-Location $Repo
$b = Join-Path $Repo ('player-package\' + 'Build-Player' + 'Package.ps1')
& $b -CheckZip $Zip -UoData 'D:\UO\tool-trials\client-data-copy' *> $Log
"EXIT=$LASTEXITCODE" | Out-File -Append -FilePath $Log
