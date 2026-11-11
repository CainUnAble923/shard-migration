# cc-P861: the gated build, then, if it is green, the TazUO proof run (run861.ps1). Writes chain-done.txt.
param([string]$Name = 'main')
$t = 'D:\UO\golems\Iron\shard-migration\notes\cc-P861-tools'
Remove-Item -LiteralPath "$t\chain-done.txt" -ErrorAction SilentlyContinue
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\gated-build.ps1"
$log = [IO.File]::ReadAllText("$t\gated-build.log") -replace "`0", ''
if ($log -match 'EXIT=0') {
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\run861.ps1" -Name $Name
    'built and ran' | Out-File -FilePath "$t\chain-done.txt" -Encoding ascii
} else {
    'build failed' | Out-File -FilePath "$t\chain-done.txt" -Encoding ascii
}
