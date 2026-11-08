# cc-P818 (P817's, P749's): the private proof shard's map overlay: this code copy's trammel.mapops on the STOCK client
# data copy (the package ships stock land: vendor\sos-trammel-map\switch.txt), with the very script the test shard uses.
param([string]$Repo = 'D:\UO\golems\Iron\ShatteredLegacy', [string]$Out = 'D:\UO\golems\Iron\p818-proof\overlay')
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $Repo 'docker\uo\Build-MapOverlay.ps1') -Stock `
    -UoData 'D:\UO\tool-trials\client-data-copy' -Out $Out `
    -Ops (Join-Path $Repo 'player-package\vendor\shattered-legacy-map\trammel.mapops')
"EXIT=$LASTEXITCODE"
