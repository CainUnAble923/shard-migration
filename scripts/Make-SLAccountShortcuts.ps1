# Desktop shortcuts for the TEST shard, one per account profile: Admin, Human, Gargoyle, Elf. Each logs straight in
# once its account has been typed in one time with Save Account ticked (cc-P28's -Account switch).
# Also removes the three ClassicUO shortcuts. Written by the overseer, 2026-10-02. PowerShell 5.1. Run:
#   powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\shard-migration\scripts\Make-SLAccountShortcuts.ps1
# Uses the newest D:\UO\ShatteredLegacy\ShatteredLegacy-* folder unless -Package is given.
# Run it AFTER cc-P28 is built into the package and your install has it. Every shortcut it touches is copied to
# Desktop\SL-shortcuts-backup\ first.

param([string]$Package)

# The newest ShatteredLegacy-* folder under D:\UO\ShatteredLegacy, unless -Package names one.
if (-not $Package) {
    $newest = Get-ChildItem -LiteralPath 'D:\UO\ShatteredLegacy' -Directory -Filter 'ShatteredLegacy-*' -ErrorAction SilentlyContinue |
        Sort-Object Name -Descending | Select-Object -First 1
    if (-not $newest) { Write-Host 'No ShatteredLegacy-* folder in D:\UO\ShatteredLegacy. Nothing changed.' -ForegroundColor Red; exit 1 }
    $Package = $newest.FullName
}
Write-Host "Package: $Package" -ForegroundColor Cyan

$desktop = [Environment]::GetFolderPath('Desktop')
$play    = Join-Path $Package 'app\Play.ps1'
$icon    = Join-Path $Package 'app\tazuo\TazUO.exe'

if (-not (Test-Path -LiteralPath $play)) { Write-Host "No Play.ps1 in $Package. Nothing changed." -ForegroundColor Red; exit 1 }
if (-not (Select-String -LiteralPath $play -Pattern '\$Account' -Quiet)) {
    Write-Host "This install's launcher has no -Account switch yet (cc-P28). Update the install first. Nothing changed." -ForegroundColor Red
    exit 1
}

$backup = Join-Path $desktop 'SL-shortcuts-backup'
New-Item -ItemType Directory -Path $backup -Force | Out-Null

foreach ($old in 'SL - Admin.lnk', 'SL - Player.lnk', 'SL - TEST shard.lnk') {
    $p = Join-Path $desktop $old
    if (Test-Path -LiteralPath $p) {
        Copy-Item -LiteralPath $p -Destination $backup -Force
        Remove-Item -LiteralPath $p
        Write-Host "Removed ClassicUO shortcut: $old" -ForegroundColor Gray
    }
}

$shell = New-Object -ComObject WScript.Shell
foreach ($acct in 'Admin', 'Human', 'Gargoyle', 'Elf') {
    $path = Join-Path $desktop "SL TEST - $acct.lnk"
    if (Test-Path -LiteralPath $path) { Copy-Item -LiteralPath $path -Destination $backup -Force }
    $lnk = $shell.CreateShortcut($path)
    # Play-Test.bat passes its arguments to Play.ps1 -Test and pauses on an error, so a failure stays readable.
    $lnk.TargetPath       = Join-Path $Package 'app\Play-Test.bat'
    $lnk.Arguments        = "-Account $($acct.ToLower())"
    $lnk.WorkingDirectory = Join-Path $Package 'app'
    $lnk.Description      = "TEST shard as the $acct account. Logs straight in after the first login."
    if (Test-Path -LiteralPath $icon) { $lnk.IconLocation = "$icon,0" }
    $lnk.Save()
    Write-Host "SL TEST - $acct" -ForegroundColor Green
}
Write-Host "Backups in $backup. First launch of each: type that account's login once with Save Account ticked."
