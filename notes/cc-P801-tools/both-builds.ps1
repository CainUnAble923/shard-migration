# cc-P801: the gated build of main, then of the isle copy, one lock each, then the last mutants on main's fresh builder image.
$t = 'D:\UO\golems\Iron\shard-migration\notes\cc-P801-tools'
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\main-build.ps1"
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\isle-build.ps1"
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\mutants-run.ps1"
'all done' | Out-File -FilePath "$t\both-done.txt"
