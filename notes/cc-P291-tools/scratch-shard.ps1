#Requires -Version 5.1
<#
  scratch-shard.ps1 (cc-P291, a copy of cc-P290's): P289's private play-through shard, never the shared Test Shard.

      powershell -NoProfile -ExecutionPolicy Bypass -File scratch-shard.ps1 -Work <scratch folder> [-Image sl-modernuo:cc-P291]
          [-Port 2596] [-Down]

  Copies the overnight bot shard's Configuration and world (D:\UO\bot-shard, read only here; not its Archives, Backups
  or the AccountWipe save, so the Golem accounts are kept) into -Work, points the copy at 127.0.0.1:<Port> with
  autosave off, builds P276's map overlay into <Work>\overlay from D:\UO\UltimaOnlineVanilla (read only), and runs the
  image as container sl-modernuo-p291 (compose project sl-uo-p291). -Down saves the container log to <Work>\shard.log
  and removes the container. The caller holds the test-shard lock. Ports 2595-2599 only (2593 live, 2594 shared).
#>
param(
    [Parameter(Mandatory)][string]$Work,
    [string]$Image = 'sl-modernuo:cc-P291',
    [int]$Port = 2596,
    [string]$CodeRepo = 'D:\UO\golems\Iron\ShatteredLegacy',
    [switch]$Down
)
$ErrorActionPreference = 'Stop'
$name = 'sl-modernuo-p291'
if ($Port -lt 2595 -or $Port -gt 2599) { throw "port $Port refused: 2595-2599 only" }
$log = Join-Path $Work 'shard.log'
$compose = Join-Path $Work 'compose.yml'

if ($Down) {
    $ErrorActionPreference = 'Continue'
    docker logs $name > $log 2>&1
    docker compose -f $compose down | Out-Null
    Write-Host "removed $name; its log is $log"
    exit 0
}

New-Item -ItemType Directory -Path $Work -Force | Out-Null
$cfg = Join-Path $Work 'Configuration'
$world = Join-Path $Work 'world'
foreach ($d in @($cfg, $world)) { if (Test-Path $d) { Remove-Item -Recurse -Force $d } }
Copy-Item -Recurse 'D:\UO\bot-shard\Configuration' $cfg
New-Item -ItemType Directory -Path $world -Force | Out-Null
Copy-Item -Recurse 'D:\UO\bot-shard\world\Saves' (Join-Path $world 'Saves')
Copy-Item 'D:\UO\bot-shard\world\golem-accounts.json' $world
Remove-Item -Recurse -Force (Join-Path $world 'Saves\AccountWipe')

$mj = Join-Path $cfg 'modernuo.json'
$j = Get-Content -Raw $mj | ConvertFrom-Json
$j.listeners = @("0.0.0.0:$Port")
$j.settings.'serverListing.serverName' = 'Shattered Legacy P291 scratch'
$j.settings.'autosave.enabled' = 'False'
[IO.File]::WriteAllText($mj, ($j | ConvertTo-Json -Depth 20), (New-Object Text.UTF8Encoding($false)))

$overlay = Join-Path $Work 'overlay'
& (Join-Path $CodeRepo 'docker\uo\Build-MapOverlay.ps1') -UoData 'D:\UO\UltimaOnlineVanilla' -Out $overlay | Out-Host

$f = { param($p) ($p -replace '\\', '/') }
$yml = @"
name: sl-uo-p291
services:
  modernuo-p291:
    image: $Image
    container_name: $name
    restart: "no"
    stop_grace_period: 60s
    ports: ["127.0.0.1:${Port}:${Port}"]
    volumes:
      - $(& $f (Join-Path $CodeRepo 'server\customizations')):/modernuo-projects:ro
      - $(& $f $cfg):/modernuo/Configuration
      - $(& $f $world):/var/lib/uo/modernuo
      - D:/UO/UltimaOnlineVanilla:/var/lib/uo/client-data/classic-client:ro
      - $(& $f $overlay):/var/lib/uo/client-data/sl-map-overlay:ro
    environment: {TZ: America/Chicago, SL_SHARD_ROLE: test}
    stdin_open: true
    tty: true
    security_opt: [seccomp:unconfined]
"@
[IO.File]::WriteAllText($compose, $yml, (New-Object Text.UTF8Encoding($false)))
$ErrorActionPreference = 'Continue'
docker compose -f $compose up -d | Out-Host
for ($i = 0; $i -lt 150; $i++) {
    Start-Sleep -Seconds 2
    $l = docker logs $name 2>&1 | Out-String
    if ($l -match 'Listening') { Write-Host "up: $name on 127.0.0.1:$Port"; exit 0 }
    if ($l -match '\(y/n\)') { Write-Host "waiting at a (y/n) prompt: see docker logs $name"; exit 3 }
    if (-not (docker ps -q -f "name=$name")) { break }
}
docker logs $name > $log 2>&1
Write-Host "did not come up; log: $log"
exit 1
