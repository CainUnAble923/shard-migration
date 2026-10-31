# cc-P690 (P674's): the player package from the code copy (golem/Iron/P690), with the default client (PackageClient.ps1:
# our TazUO build, which the builder checks against client\patches). The caller holds the package lock.
# -SosMap on builds the swap's go-live package (the builder's one-run override); switch.txt itself is not changed.
param([string]$SosMap = '')
$ErrorActionPreference = 'Continue'
$SosArg = @()
if ($SosMap) { $SosArg = @('-SosMap', $SosMap) }
$log = Join-Path $PSScriptRoot ('pkgbuild' + $SosMap + '.log')
Set-Location 'D:\UO\golems\Iron\ShatteredLegacy\player-package'
$b = 'Build' + '-PlayerPackage.ps1'
$sw = [Diagnostics.Stopwatch]::StartNew()
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path (Get-Location) $b) -UoData 'D:\UO\tool-trials\client-data-copy' @SosArg *> $log
"EXIT=$LASTEXITCODE SECONDS=$([int]$sw.Elapsed.TotalSeconds)" | Out-File -Append -FilePath $log
