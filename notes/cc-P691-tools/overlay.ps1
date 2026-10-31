# cc-P725 (P720's): the private proof shard's map overlay, made by the very script the test shard uses, on the SoS base
# (the script's default -Base, this code copy's package files). -Ops: the patch (this branch's, or main's for "before").
param([Parameter(Mandatory)][string]$Ops, [Parameter(Mandatory)][string]$Out)
$repo = 'D:\UO\golems\Iron\ShatteredLegacy'
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $repo 'docker\uo\Build-MapOverlay.ps1') `
    -UoData 'D:\UO\tool-trials\client-data-copy' -Out $Out -Ops $Ops
"EXIT=$LASTEXITCODE"
