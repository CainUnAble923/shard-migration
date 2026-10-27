# cc-P706: install the edited Commit-ShardWork.ps1 and Golems.ps1. Each live file must still have the MD5 it had when the
# scratch copy was made from it; it is backed up beside itself (.bak-20261027-P706), the new file is copied to a temp
# name in the same folder, checked, and renamed over the live one.
param([Parameter(Mandatory)][string]$Scratch)
$ErrorActionPreference = 'Stop'
$items = @(
    @{ Live = 'D:\UO\Commit-ShardWork.ps1'; New = (Join-Path $Scratch 'Commit-ShardWork.ps1'); Md5 = 'E1E10820FCFA95EBF5CB68EDFD208387' },
    @{ Live = 'D:\UO\golem\Golems.ps1';     New = (Join-Path $Scratch 'Golems.ps1');           Md5 = 'D65FC54A8BB3B8985F77042728CBD648' })
foreach ($i in $items) {
    $now = (Get-FileHash -LiteralPath $i.Live -Algorithm MD5).Hash
    if ($now -ne $i.Md5) { throw "$($i.Live) changed since the scratch copy ($now); not installed" }
}
foreach ($i in $items) {
    $bak = $i.Live + '.bak-20261027-P706'
    if (-not (Test-Path -LiteralPath $bak)) { Copy-Item -LiteralPath $i.Live -Destination $bak }
    if ((Get-FileHash -LiteralPath $bak -Algorithm MD5).Hash -ne $i.Md5) { throw "backup $bak does not match" }
    $tmp = $i.Live + '.new-P706'
    Copy-Item -LiteralPath $i.New -Destination $tmp -Force
    if ((Get-FileHash -LiteralPath $tmp -Algorithm MD5).Hash -ne (Get-FileHash -LiteralPath $i.New -Algorithm MD5).Hash) { throw "copy of $($i.New) does not match" }
    Move-Item -LiteralPath $tmp -Destination $i.Live -Force
    "installed $($i.Live) ($((Get-FileHash -LiteralPath $i.Live -Algorithm MD5).Hash)), backup $bak"
}
