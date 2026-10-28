# cc-P675: build the server's map overlay on the SoS map into a scratch folder, then three refusals:
#   a map1.mul in the client data, a base file that is not the manifest's, and a missing base file.
#   powershell -NoProfile -ExecutionPolicy Bypass -File overlay-run.ps1 -Scratch <folder> [-Code <code copy>]
param([Parameter(Mandatory = $true)][string]$Scratch, [string]$Code = 'D:\UO\golems\Iron\ShatteredLegacy')
$ErrorActionPreference = 'Continue'   # the refusals write to stderr
$script = Join-Path $Code ('docker\uo\Build-Map' + 'Overlay.ps1')
$ea = 'D:\UO\UltimaOnlineVanilla'
$out = Join-Path $Scratch 'overlay'

function Run([string]$name, [string[]]$extra) {
    $sw = [Diagnostics.Stopwatch]::StartNew()
    $o = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $script @extra 2>&1 | Out-String
    "== $name (exit $LASTEXITCODE, $([math]::Round($sw.Elapsed.TotalSeconds, 1)) s)"
    $o.Trim()
}

Run 'build on SoS' @('-UoData', $ea, '-Out', $out)
Run 'again (the stamp skips)' @('-UoData', $ea, '-Out', $out)
Get-ChildItem -LiteralPath $out | ForEach-Object { '  {0,-22} {1,12:n0}' -f $_.Name, $_.Length }

# 1. a map1.mul in the client data would beat the overlay's UOP
$fakeEa = Join-Path $Scratch 'ea-with-mul'
New-Item -ItemType Directory -Path $fakeEa -Force | Out-Null
[IO.File]::WriteAllBytes((Join-Path $fakeEa 'map1.mul'), [byte[]](1, 2, 3))
Run 'refuse: map1.mul in the client data' @('-UoData', $fakeEa, '-Out', (Join-Path $Scratch 'overlay-x'))

# 2. a base file with one byte changed
$bad = Join-Path $Scratch 'base-bad'
New-Item -ItemType Directory -Path $bad -Force | Out-Null
$files = Join-Path $Code 'player-package\vendor\sos-trammel-map\files'
foreach ($f in 'base-map1legacymul.uop', 'base-statics1.mul', 'base-staidx1.mul') { Copy-Item -LiteralPath (Join-Path $files $f) -Destination $bad -Force }
$b = [IO.File]::ReadAllBytes((Join-Path $bad 'base-staidx1.mul')); $b[100] = $b[100] -bxor 1; [IO.File]::WriteAllBytes((Join-Path $bad 'base-staidx1.mul'), $b)
Run 'refuse: a base file changed' @('-UoData', $ea, '-Base', $bad, '-Out', (Join-Path $Scratch 'overlay-x'))

# 3. a base file missing
Remove-Item -LiteralPath (Join-Path $bad 'base-staidx1.mul') -Force
Run 'refuse: a base file missing' @('-UoData', $ea, '-Base', $bad, '-Out', (Join-Path $Scratch 'overlay-x'))
Remove-Item -LiteralPath $bad, $fakeEa -Recurse -Force
