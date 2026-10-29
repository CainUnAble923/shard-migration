#Requires -Version 5.1
<#
  bot-run.ps1 (cc-P688, SoS swap S15): one nightly bot run on a PRIVATE world, as Run-OvernightPlaytests.ps1 makes it,
  from this Golem's desk (the runner itself reads the real repo's test world and Configuration, another desk).

      powershell -NoProfile -ExecutionPolicy Bypass -File bot-run.ps1 [-Work D:\UO\golems\Iron\p688-work\bot]
          [-Image sl-modernuo:cc-P688] [-Code D:\UO\golems\Iron\ShatteredLegacy] [-Runs 1] [-Only T-039,P175-2] [-Down]

  1. Refuses while the nightly's own scratch shard (sl-modernuo-bot) or a uobot.run is up: they share 127.0.0.1:2595.
  2. The world: a copy of the nightly bot's own world and Configuration (D:\UO\bot-shard, read only here; last night's
     copy of the test world, its accounts already wiped) in -Work, with Iron's TestAccountWipe request leaving one admin
     slbot-admin whose random password goes only to <Work>\secrets.json (outside both repos), and golem-accounts.json.
  3. The map: <Work>\sl-map-overlay, docker\uo\Build-MapOverlay.ps1 from the code copy (the SoS base files plus its
     trammel.mapops), first in the Configuration copy's dataDirectories, as the fixed runner now builds it.
  4. The container sl-p688-bot from -Image on 127.0.0.1:2595 only (SL_SHARD_ROLE=test, the bot compose file's mounts).
  5. The checks: uobot.run through botrun.py (Cliloc from the tool-trials client data), GOLEM_NAME's own accounts,
     --runs -Runs, no soak; then uobot.report. Results in <Work>\run.
  -Down: the container's log to <Work>\shard.log, stopped with 60 s for its save, removed.
  The caller holds the test-shard lock. Never 2593 or 2594. ASCII only.
#>
param(
    [string]$Work = 'D:\UO\golems\Iron\p688-work\bot',
    [string]$Image = 'sl-modernuo:cc-P688',
    [string]$Code = 'D:\UO\golems\Iron\ShatteredLegacy',
    [string]$ClientData = 'D:\UO\tool-trials\client-data-copy',
    [int]$Runs = 1,
    [string]$Only = '',
    [switch]$Down
)
$ErrorActionPreference = 'Stop'
$name = 'sl-p688-bot'
$port = 2595
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
if ($Work -match 'ShatteredLegacy|shard-migration') { throw "the private world would be inside a repo: $Work" }

if ($Down) {
    $ErrorActionPreference = 'Continue'
    docker logs $name > (Join-Path $Work 'shard.log') 2>&1
    docker stop -t 60 $name | Out-Null
    docker logs $name > (Join-Path $Work 'shard.log') 2>&1
    docker rm -f $name | Out-Null
    Write-Host "stopped and removed $name"
    exit 0
}

# 1. the nightly's shard and port
$ErrorActionPreference = 'Continue'
$busy = @(docker ps --format '{{.Names}} {{.Ports}}' | Where-Object { $_ -match '^sl-modernuo-bot |:2595->' })
$ErrorActionPreference = 'Stop'
if ($busy) { throw ('127.0.0.1:2595 is in use: ' + ($busy -join '; ')) }
$procs = @(Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'uobot\.run|Run-OvernightPlaytests' -and $_.ProcessId -ne $PID })
if ($procs) { throw ('a bot run is up: ' + (($procs | ForEach-Object { $_.ProcessId }) -join ', ')) }

# 2. the world
New-Item -ItemType Directory -Force -Path $Work | Out-Null
$conf = Join-Path $Work 'Configuration'
$world = Join-Path $Work 'world'
$run = Join-Path $Work 'run'
foreach ($d in @($conf, $world, $run)) { if (Test-Path -LiteralPath $d) { Remove-Item -LiteralPath $d -Recurse -Force } }
Copy-Item -LiteralPath 'D:\UO\bot-shard\Configuration' -Destination $conf -Recurse
New-Item -ItemType Directory -Force -Path $world | Out-Null
Copy-Item -LiteralPath 'D:\UO\bot-shard\world\Saves' -Destination (Join-Path $world 'Saves') -Recurse
Copy-Item -LiteralPath 'D:\UO\golem\golem-accounts.json' -Destination (Join-Path $world 'golem-accounts.json') -Force
$mj = Join-Path $conf 'modernuo.json'
$j = Get-Content -Raw -LiteralPath $mj | ConvertFrom-Json
$j.listeners = @("0.0.0.0:$port")
$j.dataDirectories = @('/var/lib/uo/client-data/sl-map-overlay', '/var/lib/uo/client-data/classic-client')
$j.settings.'serverListing.address' = '127.0.0.1'
$j.settings.'serverListing.serverName' = 'Shattered Legacy BOT (P688 private)'
$j.settings.'clusterf.testShard.allowAccountWipe' = 'True'
[IO.File]::WriteAllText($mj, ($j | ConvertTo-Json -Depth 20), (New-Object Text.UTF8Encoding $false))

. (Join-Path $Code 'scripts\Shard-Console.ps1') -LoadOnly
$bytes = New-Object byte[] 18
([Security.Cryptography.RandomNumberGenerator]::Create()).GetBytes($bytes)
$adminPw = ([Convert]::ToBase64String($bytes) -replace '[+/=]', 'x')
([Security.Cryptography.RandomNumberGenerator]::Create()).GetBytes($bytes)
$playerPw = ([Convert]::ToBase64String($bytes) -replace '[+/=]', 'y')
$stamp = (Get-Date).ToString('yyyy-MM-dd-HHmm')
$secrets = Join-Path $Work 'secrets.json'
$sec = [ordered]@{ admin = 'slbot-admin'; adminPassword = $adminPw; player = 'slbot-player'; playerPassword = $playerPw; madeAt = $stamp }
[IO.File]::WriteAllText($secrets, ($sec | ConvertTo-Json), (New-Object Text.UTF8Encoding $false))
$req = New-WipeRequestText -Admin 'slbot-admin' -Hash (New-WipePasswordHash -Password $adminPw) -Id ('p688-' + $stamp) -Now (Get-Date) -By 'cc-P688 bot-run.ps1'
[IO.File]::WriteAllText((Join-Path $world 'account-wipe-request.json'), $req, (New-Object Text.UTF8Encoding $false))
Write-Host "world: $world (D:\UO\bot-shard's copy); wipe requested; the password is in $secrets only"

# 3. the map
$overlay = Join-Path $Work 'sl-map-overlay'
New-Item -ItemType Directory -Force -Path $overlay | Out-Null
$ops = Join-Path $Code 'player-package\vendor\shattered-legacy-map\trammel.mapops'
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $Code 'docker\uo\Build-MapOverlay.ps1') -UoData $ClientData -Out $overlay -Ops $ops -Base (Join-Path $Code 'player-package\vendor\sos-trammel-map\files')
if ($LASTEXITCODE -ne 0) { throw "the map overlay failed ($LASTEXITCODE)" }

# 4. the container
$ErrorActionPreference = 'Continue'
docker rm -f $name 2>$null | Out-Null
$f = { param($p) $p -replace '\\', '/' }
docker run -d -t -i --name $name -e SL_SHARD_ROLE=test -e TZ=America/Chicago -p "127.0.0.1:${port}:${port}" --security-opt seccomp=unconfined `
    -v "$(& $f (Join-Path $Code 'server\customizations')):/modernuo-projects:ro" `
    -v "$(& $f $conf):/modernuo/Configuration" -v "$(& $f $world):/var/lib/uo/modernuo" `
    -v "$(& $f $ClientData):/var/lib/uo/client-data/classic-client:ro" `
    -v "$(& $f $overlay):/var/lib/uo/client-data/sl-map-overlay:ro" $Image | Out-Null
$ready = $false
for ($i = 0; $i -lt 120; $i++) {
    Start-Sleep -Seconds 5
    $logs = docker logs $name 2>&1 | Out-String
    if ($logs -match "Listening:.*$port" -and (ConvertFrom-WipeLog $logs).Outcome) { $ready = $true; break }
    if ((docker inspect --format '{{.State.Status}}' $name) -ne 'running') { break }
}
docker logs $name > (Join-Path $Work 'shard-start.log') 2>&1
$wipe = ConvertFrom-WipeLog (Get-Content -Raw -LiteralPath (Join-Path $Work 'shard-start.log'))
Write-Host ('wipe: ' + $wipe.Outcome + ' | ' + $wipe.Line)
if (-not $ready -or $wipe.Outcome -ne 'done') { throw "the private shard did not come up with the wipe done: see $Work\shard-start.log" }
Write-Host "up: $name on 127.0.0.1:$port"

# 5. the checks
New-Item -ItemType Directory -Force -Path $run | Out-Null
$runArgs = @('-B', (Join-Path $here 'botrun.py'), $ClientData, '--secrets', $secrets, '--out', $run, '--runs', [string]$Runs, '--container', $name)
if ($Only) { $runArgs += @('--only', $Only) }
Push-Location (Join-Path $Code 'tools\playtest-bot')
try {
    & python @runArgs 2>&1 | ForEach-Object { "$_" } | Tee-Object -FilePath (Join-Path $run 'checks.log')
    $checksExit = $LASTEXITCODE
    & python -B -m uobot.report --out $run 2>&1 | ForEach-Object { "$_" }
} finally { Pop-Location }
Write-Host "checks exit $checksExit; report: $run\report.md"
exit 0
