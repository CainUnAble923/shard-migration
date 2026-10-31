# cc-P690 (P740's): the private proof shard's map overlay: this branch's trammel.mapops (main with P691's Blackthorn)
# on the SoS base, with the very script the test shard uses.
$repo = 'D:\UO\golems\Iron\ShatteredLegacy'
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $repo 'docker\uo\Build-MapOverlay.ps1') `
    -UoData 'D:\UO\tool-trials\client-data-copy' -Out 'D:\UO\golems\Iron\p690-proof\overlay' `
    -Ops (Join-Path $repo 'player-package\vendor\shattered-legacy-map\trammel.mapops') `
    -Base (Join-Path $repo 'player-package\vendor\sos-trammel-map\files')
"EXIT=$LASTEXITCODE"
