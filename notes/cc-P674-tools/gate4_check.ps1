param([string]$Dir)
# cc-P674: runs gate 4 (-CheckZip) on each zip in $Dir and prints its verdict and the map lines it said.
$b = Join-Path 'D:\UO\golems\Iron\ShatteredLegacy\player-package' ('Build' + '-PlayerPackage.ps1')
foreach ($z in Get-ChildItem -LiteralPath $Dir -Filter '*.zip' | Sort-Object Name) {
    $o = @(& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $b -CheckZip $z.FullName -UoData 'D:\UO\tool-trials\client-data-copy' -TazUO 'D:\UO\golems\Iron\tazuo-p670\client' 2>&1 | ForEach-Object { "$_" })
    "== $($z.Name): exit $LASTEXITCODE"
    $o | Where-Object { $_ -match 'app/map|EA data file|name of an EA|statics9|GATE 4|gate 4|passed|OK' } | Select-Object -First 8
}
