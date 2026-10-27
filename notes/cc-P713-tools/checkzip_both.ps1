# cc-P713: gate 4 (-CheckZip) on real zips, both ways of the switch: P674's SoS package (built with the land) and this
# task's switched-off package. Each should pass with its own setting and fail with the other.
$ErrorActionPreference = 'Continue'
$pp = 'D:\UO\golems\Iron\ShatteredLegacy\player-package'
$b = Join-Path $pp ('Build' + '-PlayerPackage.ps1')
$log = Join-Path $PSScriptRoot 'checkzip-both.txt'
'' | Out-File -FilePath $log -Encoding ascii
foreach ($c in @(
    @('ShatteredLegacy-2026.10.27.1515.zip', 'on'), @('ShatteredLegacy-2026.10.27.1515.zip', ''),
    @('ShatteredLegacy-2026.10.27.1704.zip', ''), @('ShatteredLegacy-2026.10.27.1704.zip', 'on'))) {
    $a = @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', $b, '-CheckZip', (Join-Path $pp "dist\$($c[0])"), '-UoData', 'D:\UO\tool-trials\client-data-copy')
    if ($c[1]) { $a += @('-SosMap', $c[1]) }
    "=== $($c[0]) -SosMap $(if ($c[1]) { $c[1] } else { '(switch.txt: off)' })" | Out-File -Append -FilePath $log -Encoding ascii
    & powershell.exe @a 2>&1 | ForEach-Object { "$_" } | Where-Object { $_ -match 'GATE|app/map|README|land' } | Out-File -Append -FilePath $log -Encoding ascii
    "EXIT=$LASTEXITCODE" | Out-File -Append -FilePath $log -Encoding ascii
}
