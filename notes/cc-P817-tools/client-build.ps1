# cc-P817 (P769's): our TazUO build of the code copy's client\patches (with 0012, humans only) to a private folder.
# The log ends with EXIT=<code>.
param(
    [string]$Repo = 'D:\UO\golems\Iron\ShatteredLegacy',
    [string]$Out = 'D:\UO\golems\Iron\p817-client',
    [string]$Log = 'D:\UO\golems\Iron\shard-migration\notes\cc-P817-tools\client-build.log'
)
$ErrorActionPreference = 'Continue'
& (Join-Path $Repo 'client\Build-Client.ps1') -Out $Out *> $Log
"EXIT=$LASTEXITCODE" | Out-File -Append -FilePath $Log
