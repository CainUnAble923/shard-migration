"""cc-P675 (S2 part 1): the server's map overlay is built on the Siege of Sosaria map, and the test shard builds it
whenever the SoS files are on the PC. Edits the code copy in place; run once."""
import os

CODE = os.environ.get('SL_SHARD_REPO', r'D:\UO\golems\Iron\ShatteredLegacy')
OVERLAY = 'docker\\uo\\Build-Map' + 'Overlay.ps1'
STARTER = 'docker\\uo\\Start-Test' + 'Shard.ps1'


def edit(rel, pairs):
    p = os.path.join(CODE, rel)
    s = open(p, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in s else '\n'
    for old, new in pairs:
        old, new = old.replace('\n', nl), new.replace('\n', nl)
        assert s.count(old) == 1, (rel, old[:90])
        s = s.replace(old, new)
    assert all(ord(c) < 128 for c in s), rel
    open(p, 'w', encoding='utf-8', newline='').write(s)
    print('edited', rel)


edit(OVERLAY, [
    ('''      .\\docker\\uo\\Build-MapOverlay.ps1                  build client-data\\sl-map-overlay\\ from the shard's client data
      .\\docker\\uo\\Build-MapOverlay.ps1 -UoData <folder> [-Out <folder>] [-Ops <trammel.mapops>]
''', '''      .\\docker\\uo\\Build-MapOverlay.ps1                  build client-data\\sl-map-overlay\\ on the Siege of Sosaria map
      .\\docker\\uo\\Build-MapOverlay.ps1 [-Base <folder>] [-UoData <folder>] [-Out <folder>] [-Ops <trammel.mapops>]
      .\\docker\\uo\\Build-MapOverlay.ps1 -Stock -UoData <folder>   the old way: our patch on EA's own Trammel files
'''),
    ('''  Idempotent: the applier's stamp (map-stamp.txt in the overlay) skips the work when the EA files and the patch are
  unchanged. The shard's client data is only ever read. ASCII only, no Add-Type.
#>
''', '''  Idempotent: the applier's stamp (map-stamp.txt in the overlay) skips the work when the EA files and the patch are
  unchanged. The shard's client data is only ever read. ASCII only, no Add-Type.

  cc-P675 (the Siege of Sosaria swap, S2): the base is no longer EA's Trammel but the SoS map by Zigholtul, the same
  three files the player package ships (player-package\\vendor\\sos-trammel-map\\files\\, made by Add-SosMap.ps1 and
  checked here against its manifest.csv), and trammel.mapops is re-based onto it. The applier's -BaseDir (cc-P674)
  reads base-map1legacymul.uop, base-statics1.mul and base-staidx1.mul in place of the client's own; the overlay still
  holds map1LegacyMUL.uop, statics1.mul and staidx1.mul, first in dataDirectories. Felucca reads the same three
  (server/customizations/Maps/SosMaps.cs: file index 1), so no map0 file is made.
  The reader's order: pinned's TileMatrix asks for map1.mul FIRST, in every data folder, and only then for
  map1LegacyMUL.uop (TileMatrix.cs:105-113; FindDataFile walks dataDirectories in order, Main.cs:346-372). So the
  overlay's UOP wins over the client's own map1LegacyMUL.uop because it is in the first folder, and a map1.mul in ANY
  data folder would beat both. This script refuses when the client data (-UoData) or the overlay holds one.
  -Stock keeps the old build (our patch on EA's files) for a comparison; the patch's Burrows and isle sit on void that is
  the same in both maps, so it applies there too.
#>
'''),
    ('''    [string]$Ops = ''
)
$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path "$PSScriptRoot\\..\\..").Path
if (-not $Ops) { $Ops = Join-Path $repo 'player-package\\vendor\\shattered-legacy-map\\trammel.mapops' }
if (-not (Test-Path -LiteralPath (Join-Path $UoData 'map1LegacyMUL.uop'))) { throw "no map1LegacyMUL.uop in $UoData (-UoData)" }
if (-not (Test-Path -LiteralPath $Ops)) { throw "no map patch at $Ops" }
. (Join-Path $repo 'player-package\\payload\\app\\Apply-MapOps.ps1')
$lines = @(Build-MapOverride -UoDir $UoData -Ops $Ops -OutDir $Out)
''', '''    [string]$Ops = '',
    [string]$Base = '',     # cc-P675: the SoS map's base-* files (default: player-package\\vendor\\sos-trammel-map\\files)
    [switch]$Stock          # cc-P675: our patch on EA's own Trammel (-UoData), as before the swap
)
$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path "$PSScriptRoot\\..\\..").Path
if (-not $Ops) { $Ops = Join-Path $repo 'player-package\\vendor\\shattered-legacy-map\\trammel.mapops' }
if (-not (Test-Path -LiteralPath $Ops)) { throw "no map patch at $Ops" }
foreach ($d in @($UoData, $Out)) {
    if ($d -and (Test-Path -LiteralPath (Join-Path $d 'map1.mul'))) {
        throw "map1.mul in ${d}: pinned reads map1.mul before map1LegacyMUL.uop from every data folder (TileMatrix.cs:105-113), so it would beat the overlay. Remove it."
    }
}
$override = @{ UoDir = $UoData; Ops = $Ops; OutDir = $Out }
if ($Stock) {
    if (-not (Test-Path -LiteralPath (Join-Path $UoData 'map1LegacyMUL.uop'))) { throw "no map1LegacyMUL.uop in $UoData (-UoData)" }
} else {
    if (-not $Base) { $Base = Join-Path $repo 'player-package\\vendor\\sos-trammel-map\\files' }
    $manifest = Join-Path $repo 'player-package\\vendor\\sos-trammel-map\\manifest.csv'
    $ship = @(Get-Content -LiteralPath $manifest | Where-Object { $_ -notmatch '^#' } | ConvertFrom-Csv | Where-Object { $_.kind -eq 'ship' })
    if ($ship.Count -ne 3) { throw "$manifest lists $($ship.Count) ship rows, not 3" }
    foreach ($r in $ship) {
        $f = Join-Path $Base $r.file
        if (-not (Test-Path -LiteralPath $f)) { throw "the Siege of Sosaria map: $f is missing. Run player-package\\vendor\\sos-trammel-map\\Add-SosMap.ps1." }
        $i = Get-Item -LiteralPath $f
        if ($i.Length -ne [long]$r.bytes -or (Get-FileHash -LiteralPath $f -Algorithm SHA256).Hash -ne $r.sha256) {
            throw "the Siege of Sosaria map: $f is not the manifest's file. Run player-package\\vendor\\sos-trammel-map\\Add-SosMap.ps1."
        }
    }
    $override.BaseDir = $Base
}
. (Join-Path $repo 'player-package\\payload\\app\\Apply-MapOps.ps1')
$lines = @(Build-MapOverride @override)
'''),
    ('''Write-Host "map overlay: $Out" -ForegroundColor Cyan
''', '''Write-Host "map overlay: $Out ($(if ($Stock) { "EA's Trammel from $UoData" } else { "the Siege of Sosaria map from $Base" }))" -ForegroundColor Cyan
'''),
])

edit(STARTER, [
    ('''      .\\docker\\uo\\Start-TestShard.ps1 -NoMapOverlay
                                                 cc-P188: start on EA's Trammel, without our map changes (an empty
                                                 overlay is mounted), to see what the map patch adds or to prove
                                                 status.json's rootdeepMap reads false without it
''', '''      .\\docker\\uo\\Start-TestShard.ps1 -NoMapOverlay
                                                 cc-P188: start on EA's Trammel, without our map changes (an empty
                                                 overlay is mounted), to see what the map patch adds or to prove
                                                 status.json's rootdeepMap reads false without it. cc-P675: also
                                                 without the Siege of Sosaria map; Felucca then shows EA's Trammel too
                                                 (it reads Trammel's files since the swap)
'''),
    ('''# so the shard reads our map1LegacyMUL.uop, statics1.mul and staidx1.mul and EA's everything else. The overlay is
# (re)built here when the patch or the EA files changed (the applier's stamp decides); an empty overlay folder is
# harmless, the shard then reads EA's Trammel.
''', '''# so the shard reads our map1LegacyMUL.uop, statics1.mul and staidx1.mul and EA's everything else. The overlay is
# (re)built here when the patch or the EA files changed (the applier's stamp decides); an empty overlay folder is
# harmless, the shard then reads EA's Trammel.
# cc-P675 (SoS swap S2): the overlay is the Siege of Sosaria map plus our patch, built from the package's SoS files
# (player-package\\vendor\\sos-trammel-map\\files\\, Add-SosMap.ps1), and Trammel and Felucca both read it. Without those
# files the overlay is left as it is, with a warning, as it was without EA's client data.
'''),
    ('''} elseif (Test-Path -LiteralPath (Join-Path $eaData 'map1LegacyMUL.uop')) {
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot 'Build-MapOverlay.ps1') -UoData $eaData -Out $overlayDir
    if ($LASTEXITCODE -ne 0) { throw "Build-MapOverlay.ps1 failed ($LASTEXITCODE). Not starting." }
} else {
    Write-Host "no EA client data at ${eaData}: the map overlay is left as it is" -ForegroundColor Yellow
}
''', '''} elseif (Test-Path -LiteralPath "$repo\\player-package\\vendor\\sos-trammel-map\\files\\base-map1legacymul.uop") {
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot 'Build-MapOverlay.ps1') -UoData $eaData -Out $overlayDir
    if ($LASTEXITCODE -ne 0) { throw "Build-MapOverlay.ps1 failed ($LASTEXITCODE). Not starting." }
} else {
    Write-Host "no Siege of Sosaria map files in player-package\\vendor\\sos-trammel-map\\files (Add-SosMap.ps1): the map overlay is left as it is" -ForegroundColor Yellow
}
'''),
])
