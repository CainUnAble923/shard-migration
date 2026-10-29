# cc-P733 (P722's): the private proof shard's map overlay: release/isle-20261028's trammel.mapops on the STOCK client
# data (9ee74b6's Build-MapOverlay.ps1 has no SoS base), with the very script the test shard uses.
$repo = 'D:\UO\golems\Iron\release-isle-20261028'
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $repo 'docker\uo\Build-MapOverlay.ps1') `
    -UoData 'D:\UO\tool-trials\client-data-copy' -Out 'D:\UO\golems\Iron\p733-proof\overlay' `
    -Ops (Join-Path $repo 'player-package\vendor\shattered-legacy-map\trammel.mapops')
"EXIT=$LASTEXITCODE"
