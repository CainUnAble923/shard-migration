# cc-P707: the server's map overlay for the private proof shard: this branch's trammel.mapops on the stock client data
# copy (D:\UO\tool-trials\client-data-copy, SHA-256 equal to the shard's), with the very script the test shard uses.
$repo = 'D:\UO\golems\Iron\ShatteredLegacy'
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $repo 'docker\uo\Build-MapOverlay.ps1') `
    -UoData 'D:\UO\tool-trials\client-data-copy' -Out 'D:\UO\golems\Iron\p707-proof\overlay'
"EXIT=$LASTEXITCODE"
