# cc-P750: the live proof in one go (finish-walk.ps1's shape, P751). Checks free memory, takes the test-shard lock, builds
# this branch's map overlay, starts the private proof shard (127.0.0.1:2596, a fresh copy of the bot world, image
# sl-modernuo:cc-P750), runs shots750.json with shots750.ps1 (P708's runner, windows off-screen), takes the shard down
# and releases the lock.
#     powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golems\Iron\shard-migration\notes\cc-P750-tools\run-shots750.ps1
$ErrorActionPreference = 'Continue'
$tools = 'D:\UO\golems\Iron\shard-migration\notes\cc-P750-tools'
$proof = 'D:\UO\golems\Iron\p750-proof'
$free = [math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1MB, 1)
Write-Host "free memory: $free GB"
if ($free -lt 6) { Write-Host 'under 6 GB free: close something first'; exit 3 }
New-Item -ItemType Directory -Path $proof -Force | Out-Null
& powershell -NoProfile -ExecutionPolicy Bypass -File 'D:\UO\golem\Use-GolemLock.ps1' -Take test-shard -Minutes 45 -Wait
try {
    & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $tools 'overlay.ps1')
    & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $tools 'proof-shard.ps1') -Work (Join-Path $proof 'shard') -Overlay (Join-Path $proof 'overlay') -Port 2596
    Start-Sleep -Seconds 30
    & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $tools 'shots750.ps1') -Spec (Join-Path $tools 'shots750.json') `
        -Out (Join-Path $proof 'shots') -Port 2596 -OffScreen
} finally {
    & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $tools 'proof-shard.ps1') -Work (Join-Path $proof 'shard') -Down
    & powershell -NoProfile -ExecutionPolicy Bypass -File 'D:\UO\golem\Use-GolemLock.ps1' -Release test-shard
}
Write-Host 'run-shots750 done'
