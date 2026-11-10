# cc-P871: the gated build (gated-build.ps1 takes and releases the docker-build lock itself, page cache dropped first),
# then the TazUO proof run (run871.ps1 takes the test-shard lock). Writes chain-done.txt.
$t = 'D:\UO\golems\Iron\shard-migration\notes\cc-P871-tools'
Remove-Item -LiteralPath "$t\chain-done.txt" -ErrorAction SilentlyContinue
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\gated-build.ps1"
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\run871.ps1"
'done' | Out-File -FilePath "$t\chain-done.txt" -Encoding ascii
