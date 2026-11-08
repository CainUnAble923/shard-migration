#Requires -Version 5.1
# Game pause on or off (cc-P819): settings.json gamePause. On (the default), the overnight play tests, the Play Test
# Goblin and a Golem's client-opening steps wait on the game PC while Chase plays another game; off, they run whatever
# he plays. Every other key in settings.json is kept as it is (golem.ps1 Set-Setting's way). ASCII only.
param([switch]$On, [switch]$Off, [string]$Root = 'D:\UO\golem')
if ($On -eq $Off) { Write-Host 'Say -On or -Off.' -ForegroundColor Red; exit 1 }
$file = Join-Path $Root 'settings.json'
$f = [pscustomobject]@{}
if (Test-Path -LiteralPath $file) {
    try { $f = Get-Content -LiteralPath $file -Raw | ConvertFrom-Json }
    catch { Write-Host ('settings.json is unreadable, nothing changed: ' + $_.Exception.Message) -ForegroundColor Red; exit 1 }
}
$f | Add-Member -NotePropertyName 'gamePause' -NotePropertyValue ([bool]$On) -Force
$tmp = $file + '.tmp-gamepause'
$f | ConvertTo-Json | Set-Content -LiteralPath $tmp -Encoding ASCII
Move-Item -LiteralPath $tmp -Destination $file -Force
$msg = $(if ($On) { 'Game pause on: bot play testing waits while Chase plays another game on the game PC.' } else { 'Game pause off: bot play testing runs whatever is being played.' })
Write-Host $msg -ForegroundColor Green
exit 0
