#Requires -Version 5.1
<#
  proof-shard.ps1 (cc-P413, from cc-P412's and cc-P281's): a private test shard reading the NEW map, for the walk to the
  burrow and the step down from every mouth tile. Never the shared Test Shard.

      powershell -NoProfile -ExecutionPolicy Bypass -File proof-shard.ps1 -Work <scratch folder> -Overlay <folder>
          [-Client D:\UO\UltimaOnlineVanilla] [-Image sl-modernuo:cc-P413] [-Port 2596] [-Down]

  Copies the overnight bot shard's Configuration and world (D:\UO\bot-shard, read only here) into -Work, with the Golems'
  accounts fresh from the kit (D:\UO\golem\golem-accounts.json), points the copy at 127.0.0.1:<Port> with testCenter
  on and autosave off, and runs the image as container sl-p413-proof. The map: -Overlay (map1LegacyMUL.uop, statics1.mul,
  staidx1.mul with the patch applied: build_anthill.py's <work>\edited, which mapops.check proves equal to pristine plus
  the shipped trammel.mapops) mounted first, as docker-compose.test.yml mounts sl-map-overlay, then -Client (the pristine
  7.0.117.0 files) for everything else. -it, because a save from newer main can ask (y/n) at load. The container's log
  is copied to <Work>\shard.log before -Down removes it. The caller holds the test-shard lock. Refuses 2593 and 2594.
#>
param(
    [Parameter(Mandatory)][string]$Work,
    [string]$Overlay,
    [string]$Client = 'D:\UO\UltimaOnlineVanilla',
    [string]$Image = 'sl-modernuo:cc-P413',
    [int]$Port = 2596,
    [switch]$Down
)
$ErrorActionPreference = 'Stop'
$name = 'sl-p413-proof'
if ($Port -lt 2595 -or $Port -gt 2599) { throw "port $Port refused: 2595-2599 only (2593 is live, 2594 is the shared Test Shard)" }
$log = Join-Path $Work 'shard.log'

if ($Down) {
    $ErrorActionPreference = 'Continue'
    docker logs $name > $log 2>&1
    docker rm -f $name | Out-Null
    Write-Host "removed $name; its log is $log"
    exit 0
}
if (-not $Overlay) { throw '-Overlay is required to start' }

New-Item -ItemType Directory -Path $Work -Force | Out-Null
$cfg = Join-Path $Work 'Configuration'
$world = Join-Path $Work 'world'
foreach ($d in @($cfg, $world)) { if (Test-Path $d) { Remove-Item -Recurse -Force $d } }
Copy-Item -Recurse 'D:\UO\bot-shard\Configuration' $cfg
Copy-Item -Recurse 'D:\UO\bot-shard\world' $world
Copy-Item -Force 'D:\UO\golem\golem-accounts.json' (Join-Path $world 'golem-accounts.json')

$mj = Join-Path $cfg 'modernuo.json'
$j = Get-Content -Raw $mj | ConvertFrom-Json
$j.listeners = @("0.0.0.0:$Port")
$j.dataDirectories = @('/var/lib/uo/client-data/sl-map-overlay', '/var/lib/uo/client-data/classic-client')
$j.settings.'serverListing.address' = '127.0.0.1'
$j.settings.'serverListing.serverName' = 'Shattered Legacy P413 proof'
$j.settings.'testCenter.enable' = 'True'
$j.settings.'autosave.enabled' = 'False'
[IO.File]::WriteAllText($mj, ($j | ConvertTo-Json -Depth 20), (New-Object Text.UTF8Encoding($false)))

$ErrorActionPreference = 'Continue'
docker rm -f $name 2>$null | Out-Null
$w = ($world -replace '\\', '/')
$c = ($cfg -replace '\\', '/')
$o = ($Overlay -replace '\\', '/')
$k = ($Client -replace '\\', '/')
docker run -d -it --name $name -e SL_SHARD_ROLE=test -p "127.0.0.1:${Port}:${Port}" `
    -v "${c}:/modernuo/Configuration" -v "${w}:/var/lib/uo/modernuo" `
    -v "${o}:/var/lib/uo/client-data/sl-map-overlay:ro" -v "${k}:/var/lib/uo/client-data/classic-client:ro" $Image
for ($i = 0; $i -lt 90; $i++) {
    Start-Sleep -Seconds 2
    $l = docker logs $name 2>&1 | Out-String
    if ($l -match 'Listening') { Write-Host "up: $name on 127.0.0.1:$Port"; exit 0 }
    if ($l -match '\(y/n\)') { Write-Host "waiting at a (y/n) load prompt: answer it on this scratch copy only"; exit 2 }
    if (-not (docker ps -q -f "name=$name")) { break }
}
docker logs $name > $log 2>&1
Write-Host "did not come up; log: $log"
exit 1
