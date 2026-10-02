# Retargets the two TazUO desktop shortcuts at the newest player package in D:\UO\ShatteredLegacy\ShatteredLegacy-*.
# Written by the overseer, 2026-10-02. PowerShell 5.1. Run once:
#   powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\shard-migration\scripts\Update-SLDesktopShortcuts.ps1
# The old shortcuts are copied to Desktop\SL-shortcuts-backup\ first. The ClassicUO ones (SL - Admin, SL - Player,
# SL - TEST shard) and "SL - Start TEST shard" are not touched.

param([string]$Package)

# The newest ShatteredLegacy-* folder under D:\UO\ShatteredLegacy, unless -Package names one.
if (-not $Package) {
    $newest = Get-ChildItem -LiteralPath 'D:\UO\ShatteredLegacy' -Directory -Filter 'ShatteredLegacy-*' -ErrorAction SilentlyContinue |
        Sort-Object Name -Descending | Select-Object -First 1
    if (-not $newest) { Write-Host 'No ShatteredLegacy-* folder in D:\UO\ShatteredLegacy. Nothing changed.' -ForegroundColor Red; exit 1 }
    $Package = $newest.FullName
}
Write-Host "Package: $Package" -ForegroundColor Cyan
$pkg     = $Package
$desktop = [Environment]::GetFolderPath('Desktop')
$icon    = Join-Path $pkg 'app\tazuo\TazUO.exe'

$targets = @(
    @{ Name = 'SL - TazUO LIVE.lnk'; Bat = 'Play Shattered Legacy.bat'; Desc = 'LIVE shard, player package (updates itself).' },
    @{ Name = 'SL - TazUO TEST.lnk'; Bat = 'Play TEST Shard.bat';        Desc = 'TEST shard, player package. Throwaway world.' }
)

foreach ($t in $targets) {
    if (-not (Test-Path -LiteralPath (Join-Path $pkg $t.Bat))) { Write-Host "Missing $($t.Bat) in $pkg. Nothing changed." -ForegroundColor Red; exit 1 }
}

$backup = Join-Path $desktop 'SL-shortcuts-backup'
New-Item -ItemType Directory -Path $backup -Force | Out-Null
$shell = New-Object -ComObject WScript.Shell

foreach ($t in $targets) {
    $path = Join-Path $desktop $t.Name
    if (Test-Path -LiteralPath $path) { Copy-Item -LiteralPath $path -Destination $backup -Force }
    $lnk = $shell.CreateShortcut($path)
    $lnk.TargetPath       = Join-Path $pkg $t.Bat
    $lnk.WorkingDirectory = $pkg
    $lnk.Description      = $t.Desc
    $lnk.Arguments        = ''
    if (Test-Path -LiteralPath $icon) { $lnk.IconLocation = "$icon,0" }
    $lnk.Save()
    Write-Host "$($t.Name) -> $($lnk.TargetPath)" -ForegroundColor Green
}
Write-Host "Old shortcuts saved in $backup"
