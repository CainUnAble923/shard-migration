#Requires -Version 5.1
# cc-P28 probe: what the shipped TazUO (26.0909.63, 3212623f) does at startup with a profile's settings.
# A TcpListener on 127.0.0.1 stands in for the login server and counts connections; it accepts and closes
# each one, so a login that was attempted fails at once. Nothing is sent anywhere else. The client is a
# scratch copy (no Data\, no Cache\) and the UO folder is D:\ShatteredLegacy\client-data\classic-client,
# read only.
#
#     powershell -NoProfile -ExecutionPolicy Bypass -File probe-autologin.ps1 -Taz <scratch copy of the client>
param([Parameter(Mandatory = $true)][string]$Taz, [int]$Port = 27594, [int]$Seconds = 25)

$ErrorActionPreference = 'Stop'
$uo = 'D:\ShatteredLegacy\client-data\classic-client'
$fv = (Get-Item (Join-Path $uo 'client.exe')).VersionInfo
$cv = '{0}.{1}.{2}.{3}' -f $fv.FileMajorPart, $fv.FileMinorPart, $fv.FileBuildPart, $fv.FilePrivatePart

function Invoke-Case([string]$name, [string]$username, [bool]$skip) {
    $settings = Join-Path $Taz "settings.test.$name.json"
    $s = [ordered]@{ username = $username; password = ''; saveaccount = $true; autologin = $true; encryption = 0; plugins = @()
                     ip = '127.0.0.1'; port = $Port; ultimaonlinedirectory = $uo; clientversion = $cv
                     last_server_name = 'Shattered Legacy TEST'; ignore_relay_ip = $true }
    [IO.File]::WriteAllText($settings, ($s | ConvertTo-Json), (New-Object Text.UTF8Encoding $false))

    $l = New-Object Net.Sockets.TcpListener ([Net.IPAddress]::Loopback), $Port
    $l.Start()
    $tazArgs = @('-settings', "`"$settings`"")
    if ($skip) { $tazArgs += '-skiploginscreen' }
    $p = Start-Process -FilePath (Join-Path $Taz 'TazUO.exe') -ArgumentList $tazArgs -WorkingDirectory $Taz -PassThru
    $hits = New-Object 'System.Collections.Generic.List[double]'
    $sw = [Diagnostics.Stopwatch]::StartNew()
    while ($sw.Elapsed.TotalSeconds -lt $Seconds) {
        if ($l.Pending()) { $c = $l.AcceptTcpClient(); $hits.Add([Math]::Round($sw.Elapsed.TotalSeconds, 1)); $c.Close() }
        Start-Sleep -Milliseconds 50
    }
    $l.Stop()
    $alive = -not $p.HasExited
    if ($alive) { Stop-Process -Id $p.Id -Force }
    $saved = [IO.File]::ReadAllText($settings) | ConvertFrom-Json
    '{0,-28} skiploginscreen={1,-5} username=[{2}]  connections={3} at [{4}] s  alive after {5} s={6}  username after=[{7}]' -f `
        $name, $skip, $username, $hits.Count, ($hits -join ', '), $Seconds, $alive, $saved.username
}

Invoke-Case 'empty-skip'      ''      $true    # a profile's first launch
Invoke-Case 'saved-skip'      'probe' $true    # every launch after: must connect once, and not loop when it fails
Invoke-Case 'saved-noskip'    'probe' $false   # autologin alone, no -skiploginscreen
