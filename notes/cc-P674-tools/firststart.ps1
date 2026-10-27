$ErrorActionPreference = 'Stop'
. 'D:\UO\golems\Iron\ShatteredLegacy\player-package\payload\app\Apply-MapOps.ps1'
$out = 'C:/Users/ckfle/AppData/Local/Temp/claude/D--UO-golems-Iron-shard-migration/8a22c23c-dc07-4563-a080-b92e53c9b16f/scratchpad/p674\ff-out'
if (Test-Path $out) { Remove-Item $out -Recurse -Force }
$base = 'D:\UO\golems\Iron\ShatteredLegacy\player-package\vendor\sos-trammel-map\files'
$ops = 'D:\UO\golems\Iron\ShatteredLegacy\player-package\vendor\shattered-legacy-map\trammel.mapops'
$sw = [Diagnostics.Stopwatch]::StartNew()
$lines = @(Build-MapOverride -UoDir 'D:\UO\tool-trials\client-data-copy' -Ops $ops -OutDir $out -BaseDir $base -AlsoAs 0)
"first start: {0:n1} s" -f ($sw.ElapsedMilliseconds / 1000)
$lines
$sw.Restart()
$lines2 = @(Build-MapOverride -UoDir 'D:\UO\tool-trials\client-data-copy' -Ops $ops -OutDir $out -BaseDir $base -AlsoAs 0)
"second start: {0:n2} s, {1} lines, same: {2}" -f ($sw.ElapsedMilliseconds / 1000), $lines2.Count, (($lines -join '|') -eq ($lines2 -join '|'))
Get-ChildItem $out | ForEach-Object { "{0} {1}" -f $_.Name, $_.Length }
"total MB: {0:n1}" -f ((Get-ChildItem $out | Measure-Object Length -Sum).Sum / 1MB)
