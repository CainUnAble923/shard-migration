# cc-P863 (P872's): the gated build (sl-modernuo:cc-p863), then, if it is green, the TazUO proof run into
# cc-P863-shots\<Name>. Writes chain-done.txt.
param([string]$Name = 'main')
$t = 'D:\UO\golems\Iron\shard-migration\notes\cc-P863-tools'
Remove-Item -LiteralPath "$t\chain-done.txt" -ErrorAction SilentlyContinue
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\gated-build.ps1"
$log = [IO.File]::ReadAllText("$t\gated-build.log") -replace "`0", ''
if ($log -match 'EXIT=0') {
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\run863.ps1" -Name $Name
    'built and ran' | Out-File -FilePath "$t\chain-done.txt" -Encoding ascii
} else {
    'build failed' | Out-File -FilePath "$t\chain-done.txt" -Encoding ascii
}
