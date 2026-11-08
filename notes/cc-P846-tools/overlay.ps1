# cc-P846 (P818's, on the isle release copy; cc-P818: P817's, P749's): the private proof shard's map overlay: the
# release copy's trammel.mapops on the STOCK client data copy (the package ships stock land), built by the code copy's
# Build-MapOverlay.ps1 (the release copy's has no -Stock switch).
param([string]$Repo = 'D:\UO\golems\Iron\p846-isle', [string]$Out = 'D:\UO\golems\Iron\p846-proof\overlay',
      [string]$Builder = 'D:\UO\golems\Iron\ShatteredLegacy\docker\uo\Build-MapOverlay.ps1')
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Builder -Stock `
    -UoData 'D:\UO\tool-trials\client-data-copy' -Out $Out `
    -Ops (Join-Path $Repo 'player-package\vendor\shattered-legacy-map\trammel.mapops')
"EXIT=$LASTEXITCODE"
