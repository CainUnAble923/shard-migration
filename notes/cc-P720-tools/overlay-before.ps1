# cc-P720: the "before" overlay: main's trammel.mapops (HEAD, P718) on the same SoS base, for the before shots.
$repo = 'D:\UO\golems\Iron\ShatteredLegacy'
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $repo 'docker\uo\Build-MapOverlay.ps1') `
    -UoData 'D:\UO\tool-trials\client-data-copy' -Out 'D:\UO\golems\Iron\p720-proof\overlay-before' `
    -Ops 'D:\UO\golems\Iron\p720-proof\before-repo\player-package\vendor\shattered-legacy-map\trammel.mapops'
"EXIT=$LASTEXITCODE"
