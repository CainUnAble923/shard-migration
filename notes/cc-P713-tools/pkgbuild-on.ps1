$ErrorActionPreference = 'Continue'
$log = Join-Path $PSScriptRoot 'pkgbuild-on.log'
Set-Location 'D:\UO\golems\Iron\ShatteredLegacy\player-package'
$b = 'Build' + '-PlayerPackage.ps1'
$sw = [Diagnostics.Stopwatch]::StartNew()
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path (Get-Location) $b) -UoData 'D:\UO\tool-trials\client-data-copy' -SosMap on -TazUO 'D:\UO\golems\Iron\tazuo-p670\client' *> $log
"EXIT=$LASTEXITCODE SECONDS=$([int]$sw.Elapsed.TotalSeconds)" | Out-File -Append -FilePath $log
