# cc-P801: the final chain: both gated builds, the mutants, both client walks.
$t = 'D:\UO\golems\Iron\shard-migration\notes\cc-P801-tools'
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\both-builds.ps1"
$a = (Get-Content -Raw "$t\gated-build.log") -replace "`0",''
$b = (Get-Content -Raw "$t\gated-build-isle.log") -replace "`0",''
if ($a -match 'EXIT=0' -and $b -match 'EXIT=0') {
  Remove-Item -Recurse -Force -LiteralPath 'D:\UO\golems\Iron\shard-migration\notes\cc-P801-review\shots-main' -ErrorAction SilentlyContinue
  Remove-Item -Recurse -Force -LiteralPath 'D:\UO\golems\Iron\shard-migration\notes\cc-P801-review\shots-isle' -ErrorAction SilentlyContinue
  & powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\run801main.ps1"
  Copy-Item 'D:\UO\golems\Iron\p740-proof\walk.log' "$t\walk-main.log" -Force
  & powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\run801isle.ps1"
  Copy-Item 'D:\UO\golems\Iron\p740-proof\walk.log' "$t\walk-isle.log" -Force
}
'final done' | Out-File -FilePath "$t\final-done.txt"
