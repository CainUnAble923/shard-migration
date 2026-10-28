# cc-P720 (P707's): the private proof shard's map overlay: this branch's trammel.mapops on the SoS base (the script's
# default -Base, this code copy's package files), with the very script the test shard uses.
$repo = 'D:\UO\golems\Iron\ShatteredLegacy'
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $repo 'docker\uo\Build-MapOverlay.ps1') `
    -UoData 'D:\UO\tool-trials\client-data-copy' -Out 'D:\UO\golems\Iron\p720-proof\overlay' `
    -Ops (Join-Path $repo 'player-package\vendor\shattered-legacy-map\trammel.mapops')
"EXIT=$LASTEXITCODE"
