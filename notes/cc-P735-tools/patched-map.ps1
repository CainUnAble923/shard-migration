# cc-P735: the patched SoS land for P688's bot-point proof: today's trammel.mapops (code copy) on the SoS base files,
# built by the test shard's own Build-MapOverlay.ps1, into D:\UO\golems\Iron\p735-work\patched.
$repo = 'D:\UO\golems\Iron\ShatteredLegacy'
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $repo 'docker\uo\Build-MapOverlay.ps1') `
    -UoData 'D:\UO\tool-trials\client-data-copy' -Out 'D:\UO\golems\Iron\p735-work\patched' `
    -Ops (Join-Path $repo 'player-package\vendor\shattered-legacy-map\trammel.mapops') `
    -Base (Join-Path $repo 'player-package\vendor\sos-trammel-map\files')
"EXIT=$LASTEXITCODE"
