# cc-P734: the shots, then the walks, one after the other (one TazUO at a time on a short-of-memory PC).
$t = $PSScriptRoot
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $t 'run-shots.ps1') -Spec 'shots.json' -Out 'D:\UO\golems\Iron\p734-proof\shots'
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $t 'run-shots.ps1') -Spec 'walks.json' -Out 'D:\UO\golems\Iron\p734-proof\walks'
'ALLDONE' | Out-File -FilePath 'D:\UO\golems\Iron\p734-proof\all-done.txt' -Encoding ascii
