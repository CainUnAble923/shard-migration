#Requires -Version 5.1
<#
  fresh-shard.ps1 (cc-P690, from P740's proof-shard.ps1): a PRIVATE shard on a FRESH world, the way the test shard
  starts on swap day (Chase 10-27: a fresh test world, no migration). Never the shared Test Shard.

      fresh-shard.ps1 -Work <folder> [-Image sl-modernuo:cc-P690] [-Port 2596] [-KeepWorld] [-Down]

  - Configuration: a copy of the overnight bot shard's (D:\UO\bot-shard\Configuration, read only here), which is the
    test shard's (testCenter on, the account-wipe guard on); pointed at 127.0.0.1:<Port>, autosave off, the SoS map
    overlay first in dataDirectories.
  - World: EMPTY (no Saves). With no accounts the server asks for an owner on its console (AccountPrompt.cs), so the
    container runs with -i -t and answer_owner.py answers it. golem-accounts.json is NOT copied in at first boot (it
    would make Iron's Administrator before the prompt, and no account could then run [MoonGen/[TelGen, Developer).
  - The overlay: <Work>\..\overlay, made by overlay.ps1 (docker\uo\Build-MapOverlay.ps1, this branch's mapops on SoS).
  The caller holds the test-shard lock. The log is copied to <Work>\shard.log before -Down removes the container.
#>
param(
    [Parameter(Mandatory)][string]$Work,
    [string]$Image = 'sl-modernuo:cc-P690',
    [string]$Overlay = '',
    [int]$Port = 2596,
    [switch]$KeepWorld,
    [switch]$Down
)
$ErrorActionPreference = 'Stop'
$name = 'sl-p690-proof'
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
if (-not $KeepWorld) {
    foreach ($d in @($cfg, $world)) { if (Test-Path $d) { Remove-Item -Recurse -Force $d } }
    Copy-Item -Recurse 'D:\UO\bot-shard\Configuration' $cfg
    New-Item -ItemType Directory -Path $world -Force | Out-Null
}

$mj = Join-Path $cfg 'modernuo.json'
$j = Get-Content -Raw $mj | ConvertFrom-Json
$j.listeners = @("0.0.0.0:$Port")
$j.dataDirectories = @('/var/lib/uo/client-data/sl-map-overlay', '/var/lib/uo/client-data/classic-client')
$j.settings.'serverListing.address' = '127.0.0.1'
$j.settings.'serverListing.serverName' = 'Shattered Legacy P690 proof'
$j.settings.'autosave.enabled' = 'False'
[IO.File]::WriteAllText($mj, ($j | ConvertTo-Json -Depth 20), (New-Object Text.UTF8Encoding($false)))

$ErrorActionPreference = 'Continue'
docker rm -f $name 2>$null | Out-Null
$w = ($world -replace '\\', '/')
$c = ($cfg -replace '\\', '/')
$ovDir = if ($Overlay) { $Overlay } else { Join-Path (Split-Path $Work -Parent) 'overlay' }
if (-not (Test-Path (Join-Path $ovDir 'map1LegacyMUL.uop'))) { throw "no map overlay at $ovDir (run overlay.ps1)" }
$ov = ($ovDir -replace '\\', '/')
docker run -d -i -t --name $name -e SL_SHARD_ROLE=test -p "127.0.0.1:${Port}:${Port}" `
    -v "${c}:/modernuo/Configuration" -v "${w}:/var/lib/uo/modernuo" `
    -v 'D:/UO/tool-trials/client-data-copy:/var/lib/uo/client-data/classic-client:ro' `
    -v "${ov}:/var/lib/uo/client-data/sl-map-overlay:ro" $Image
for ($i = 0; $i -lt 120; $i++) {
    Start-Sleep -Seconds 2
    $l = docker logs $name 2>&1 | Out-String
    if ($l -match 'create the owner account') { Write-Host "owner prompt: $name"; exit 3 }
    if ($l -match 'Listening on') { Write-Host "up: $name on 127.0.0.1:$Port"; exit 0 }
    if (-not (docker ps -q -f "name=$name")) { break }
}
docker logs $name > $log 2>&1
Write-Host "did not come up; log: $log"
exit 1
