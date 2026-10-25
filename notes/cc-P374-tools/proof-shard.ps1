#Requires -Version 5.1
<#
  proof-shard.ps1 (cc-P374): a private test shard for the guild hall screenshots, never the shared Test Shard.

      powershell -NoProfile -ExecutionPolicy Bypass -File proof-shard.ps1 -Work <scratch folder> [-Image sl-modernuo:cc-P374]
          [-Port 2596] [-Down] [-Live]

  Copies the overnight bot shard's Configuration and world (D:\UO\bot-shard, read only here) into -Work, points the copy
  at 127.0.0.1:<Port> with testCenter.enable on and autosave off, and runs the image as container sl-p374-proof with
  the client files from D:\UO\tool-trials\client-data-copy (map, statics and multis SHA-256 equal to the shard's). The
  container's log is copied to <Work>\shard.log before -Down removes it. The caller holds the test-shard lock.
  -Live writes testCenter.enable false (the copy then reads as live: the seeders' refusal). Adapted from cc-P281.
  On Chases-Tower port 2594 is the real Test Shard Chase and the play-testers use: this script refuses 2593 and 2594.
#>
param(
    [Parameter(Mandatory)][string]$Work,
    [string]$Image = 'sl-modernuo:cc-P374',
    [int]$Port = 2596,
    [switch]$Down,
    [switch]$Live
)
$ErrorActionPreference = 'Stop'
$name = 'sl-p374-proof'
if ($Port -lt 2595 -or $Port -gt 2599) { throw "port $Port refused: 2595-2599 only (2593 is live, 2594 is the shared Test Shard)" }
$log = Join-Path $Work 'shard.log'

if ($Down) {
    $ErrorActionPreference = 'Continue'
    docker logs $name > $log 2>&1
    docker rm -f $name | Out-Null
    Write-Host "removed $name; its log is $log"
    exit 0
}

New-Item -ItemType Directory -Path $Work -Force | Out-Null
$cfg = Join-Path $Work 'Configuration'
$world = Join-Path $Work 'world'
foreach ($d in @($cfg, $world)) { if (Test-Path $d) { Remove-Item -Recurse -Force $d } }
Copy-Item -Recurse 'D:\UO\bot-shard\Configuration' $cfg
Copy-Item -Recurse 'D:\UO\bot-shard\world' $world

$mj = Join-Path $cfg 'modernuo.json'
$j = Get-Content -Raw $mj | ConvertFrom-Json
$j.listeners = @("0.0.0.0:$Port")
$j.dataDirectories = @('/var/lib/uo/client-data/classic-client')
$j.settings.'serverListing.address' = '127.0.0.1'
$j.settings.'serverListing.serverName' = 'Shattered Legacy TEST'
$j.settings.'testCenter.enable' = $(if ($Live) { 'False' } else { 'True' })
$j.settings.'autosave.enabled' = 'False'
[IO.File]::WriteAllText($mj, ($j | ConvertTo-Json -Depth 20), (New-Object Text.UTF8Encoding($false)))

$ErrorActionPreference = 'Continue'
docker rm -f $name 2>$null | Out-Null
$w = ($world -replace '\\', '/')
$c = ($cfg -replace '\\', '/')
docker run -d -t --name $name -e SL_SHARD_ROLE=test -p "127.0.0.1:${Port}:${Port}" `
    -v "${c}:/modernuo/Configuration" -v "${w}:/var/lib/uo/modernuo" `
    -v 'D:/UO/tool-trials/client-data-copy:/var/lib/uo/client-data/classic-client:ro' $Image
for ($i = 0; $i -lt 90; $i++) {
    Start-Sleep -Seconds 2
    $l = docker logs $name 2>&1 | Out-String
    if ($l -match 'Listening') { Write-Host "up: $name on 127.0.0.1:$Port"; exit 0 }
    if (-not (docker ps -q -f "name=$name")) { break }
}
docker logs $name > $log 2>&1
Write-Host "did not come up; log: $log"
exit 1
