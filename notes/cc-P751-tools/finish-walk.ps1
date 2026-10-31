# cc-P751: the last step left (the P748 review's item 6, the real TazUO walk), in one go. The first try on 2026-10-31 was
# stopped by Claude Code for low memory (Windows had about 4 GB free) before the walk started. Check free memory first
# (8 GB or more), then:
#     powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golems\Iron\shard-migration\notes\cc-P751-tools\finish-walk.ps1
# It takes the test-shard lock, starts the private proof shard (127.0.0.1:2596, a fresh copy of the bot world, image
# sl-modernuo:cc-P751, this branch's map overlay), walks Iron the Tester along walk-paths.json with IsleWalk751.py
# (292 steps in 19 legs, a shot at each door, a frame every 8 s), copies the log and the shots into
# notes\cc-P751-review\, takes the shard down and releases the lock.
$ErrorActionPreference = 'Continue'
$tools = 'D:\UO\golems\Iron\shard-migration\notes\cc-P751-tools'
$review = 'D:\UO\golems\Iron\shard-migration\notes\cc-P751-review'
$proof = 'D:\UO\golems\Iron\p751-proof'
$free = [math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1MB, 1)
Write-Host "free memory: $free GB"
if ($free -lt 6) { Write-Host 'under 6 GB free: close something first'; exit 3 }
& powershell -NoProfile -ExecutionPolicy Bypass -File 'D:\UO\golem\Use-GolemLock.ps1' -Take test-shard -Minutes 60 -Wait
try {
    & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $tools 'proof-shard.ps1') -Work (Join-Path $proof 'shard') -Overlay (Join-Path $proof 'overlay') -Port 2596
    Remove-Item -LiteralPath (Join-Path $proof 'walk-signal.txt') -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 60   # the seed on load
    & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $tools 'isle-shots751.ps1') -Spec (Join-Path $tools 'walk751.json') `
        -Out (Join-Path $proof 'walk') -Port 2596 -Bot (Join-Path $proof 'bot') -Work (Join-Path $proof 'shots-work')
    Copy-Item -LiteralPath (Join-Path $proof 'isle-walk.log') -Destination $review -Force
    New-Item -ItemType Directory -Path (Join-Path $review 'shots') -Force | Out-Null
    Get-ChildItem -LiteralPath (Join-Path $proof 'walk') -Filter 'walk-*.jpg' | Copy-Item -Destination (Join-Path $review 'shots') -Force
    Get-ChildItem -LiteralPath (Join-Path $proof 'walk') -Filter 'isle-walk-f*.jpg' | Where-Object { $_.BaseName -match '-f(\d+)$' -and ([int]$Matches[1] % 5) -eq 0 } |
        Copy-Item -Destination (Join-Path $review 'shots') -Force
    Copy-Item -LiteralPath (Join-Path $proof 'walk\proof-log.txt') -Destination (Join-Path $tools 'walk-proof-log.txt') -Force
} finally {
    & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $tools 'proof-shard.ps1') -Work (Join-Path $proof 'shard') -Down
    & powershell -NoProfile -ExecutionPolicy Bypass -File 'D:\UO\golem\Use-GolemLock.ps1' -Release test-shard
}
Get-Content -LiteralPath (Join-Path $review 'isle-walk.log') -Tail 3
