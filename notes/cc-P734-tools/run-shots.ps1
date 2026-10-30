# cc-P734: the TazUO shots, then the walks, on the private shard (2596), detached; console output to <Out>\console-<spec>.txt.
param([string]$Spec = 'shots.json', [string]$Out = 'D:\UO\golems\Iron\p734-proof\shots')
$t = $PSScriptRoot
New-Item -ItemType Directory -Path $Out -Force | Out-Null
$console = Join-Path $Out ('console-' + [IO.Path]::GetFileNameWithoutExtension($Spec) + '.txt')
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $t 'isle-shots.ps1') -Spec (Join-Path $t $Spec) -Out $Out -Port 2596 -Bot 'D:\UO\golems\Iron\ShatteredLegacy\tools\playtest-bot' -Work 'D:\UO\golems\Iron\p734-proof\shots-work' *> $console
"EXIT=$LASTEXITCODE" | Out-File -Append -FilePath $console
