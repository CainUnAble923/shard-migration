# cc-P838 (P820's): the gated build of a code copy; the log is UTF-16 (PowerShell *> redirect), ends with EXIT=<code>.
param(
    [string]$Repo = 'D:\UO\golems\Iron\ShatteredLegacy',
    [string]$Tag = 'sl-modernuo:cc-P838',
    [string]$Log = 'D:\UO\golems\Iron\shard-migration\notes\cc-P838-tools\gated-build.log'
)
$ErrorActionPreference = 'Continue'
Set-Location $Repo
$b = 'docker/uo/' + 'build' + '.sh'
& 'C:\Program Files\Git\bin\bash.exe' $b -t $Tag *> $Log
"EXIT=$LASTEXITCODE" | Out-File -Append -FilePath $Log
