#Requires -Version 5.1
<#
  run-tazuo.ps1 (cc-P740): one real-client run on the private proof shard (127.0.0.1:2596; the caller holds the
  test-shard lock): a fresh copy of the bot world on -Image, a fresh TazUO that makes the character itself (P731's
  test-only creation plugin), the walk script, the shots into -Out, then the shard down.

      run-tazuo.ps1 -Image sl-modernuo:cc-P740 -Character "Iron Sands" -Script IsleWalk740.py -Out <folder> [-KeepShard]
#>
param(
    [Parameter(Mandatory)][string]$Image,
    [Parameter(Mandatory)][string]$Character,
    [Parameter(Mandatory)][string]$Script,
    [Parameter(Mandatory)][string]$Out,
    [int]$MaxMinutes = 25,
    [switch]$KeepShard
)
$ErrorActionPreference = 'Continue'
$tools = 'D:\UO\golems\Iron\shard-migration\notes\cc-P740-tools'
$proof = 'D:\UO\golems\Iron\p740-proof'
New-Item -ItemType Directory -Path $Out -Force | Out-Null
function Say([string]$t) { $l = '[' + (Get-Date).ToString('HH:mm:ss') + '] ' + $t; Write-Host $l; Add-Content -LiteralPath (Join-Path $Out 'run-log.txt') -Value $l -Encoding ASCII }

Say ("shard: " + $Image)
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $tools 'proof-shard.ps1') -Work (Join-Path $proof 'shard') -Image $Image -Overlay (Join-Path $proof 'overlay') *>&1 | ForEach-Object { Say ([string]$_) }
if ($LASTEXITCODE -ne 0) { Say 'the shard did not come up'; exit 1 }

& python -P (Join-Path $tools 'make_create_bin.py') $Character (Join-Path $proof 'plugin\out\create.bin') *>&1 | ForEach-Object { Say ([string]$_) }
Remove-Item -LiteralPath (Join-Path $proof 'plugin\out\P731Create.log') -ErrorAction SilentlyContinue
Remove-Item -LiteralPath (Join-Path $proof 'walk.log') -ErrorAction SilentlyContinue

& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $tools 'tazuo-walk.ps1') -Character $Character -Out $Out -Script $Script -Prepare *>&1 | ForEach-Object { Say ([string]$_) }
# run 1 (before): ui.ps1 through a pipe kept the pipe open in TazUO, so this waited on TazUO and the shots were never
# taken; it starts in its own hidden window now.
$uiOut = Join-Path $Out 'ui-start.txt'
$uiArgs = '-NoProfile -ExecutionPolicy Bypass -File "' + (Join-Path $tools 'ui.ps1') + '" -Do start -Character "' + $Character + '"'
# (no -Wait: in Windows PowerShell 5.1 it also waits for TazUO, the child's child; wait for its line instead)
Remove-Item -LiteralPath $uiOut -ErrorAction SilentlyContinue
Start-Process powershell.exe -ArgumentList $uiArgs -WindowStyle Hidden -RedirectStandardOutput $uiOut
for ($i = 0; $i -lt 60 -and -not ((Get-Content -Raw $uiOut -ErrorAction SilentlyContinue) -match 'started'); $i++) { Start-Sleep -Seconds 1 }
Say ('ui: ' + ((Get-Content -Raw $uiOut -ErrorAction SilentlyContinue) -replace '\s+', ' '))
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $tools 'tazuo-walk.ps1') -Character $Character -Out $Out -Script $Script -Attach -MaxMinutes $MaxMinutes -EverySeconds 30 *>&1 | ForEach-Object { Say ([string]$_) }

Copy-Item -LiteralPath (Join-Path $proof 'plugin\out\P731Create.log') -Destination $Out -Force -ErrorAction SilentlyContinue
if (-not $KeepShard) {
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $tools 'proof-shard.ps1') -Work (Join-Path $proof 'shard') -Down *>&1 | ForEach-Object { Say ([string]$_) }
    Copy-Item -LiteralPath (Join-Path $proof 'shard\shard.log') -Destination $Out -Force -ErrorAction SilentlyContinue
}
Say 'run done'
