#Requires -Version 5.1
<#
  LegionTest.ps1 (cc-P219): the pieces of Test-LegionScript.ps1 that the facts test on their own. Dot-source it; it
  defines functions only. ASCII only.

  Test-LegionTarget   the never-live guard: this PC's own test shard (loopback or this PC's own name or address, port
                      2594 to 2599) and nothing else; 2593 is refused from any host
                      cc-P819: and, on the game PC, not while Chase plays another game (GamePause.ps1): it refuses
                      with "waiting: Chase is playing <game>" and how to wait (Test-GameRunning.ps1 -Wait, in the
                      background); every client-opening driver calls it first, so proof shots and two-client tests wait
  Get-LegionCapability  can this PC run it: Docker, the client data, our TazUO build, the play-test bot (for the
                      Admin's setup), and this Golem's test accounts
  ConvertTo-CuoPassword  the password as TazUO's settings.json keeps it (ClassicUO.Utility.Crypter, keyed on the PC)
  Read-LegionPlan, Set-LegionOverrides, New-LegionSettings, Get-LegionLines, Save-LegionShot, Format-LegionReport
#>

$script:LegionLivePort = 2593
$script:LegionTestPorts = 2594..2599
# Names that are never this PC's test shard, whatever they resolve to: the live shard and Haven.
$script:LegionNeverHosts = @('shatteredlegacyuo.com', 'get.shatteredlegacyuo.com', 'haven', 'haven.tail81098d.ts.net')
# cc-P819: the game pause (GamePause.ps1 beside this file); the facts turn the real look off.
$script:LegionKitRoot = $(if ($PSScriptRoot) { $PSScriptRoot } else { 'D:\UO\golem' })
$script:LegionGameCheck = $true
if (-not (Get-Command Get-GamePauseState -ErrorAction SilentlyContinue)) {
    $gpz = Join-Path $script:LegionKitRoot 'GamePause.ps1'
    if (Test-Path -LiteralPath $gpz) { . $gpz } else { $script:LegionGameCheck = $false }
}

# This PC's own addresses and names: loopback, its computer name, and every IP address on it.
function Get-LegionOwnHosts {
    $h = New-Object System.Collections.Generic.List[string]
    foreach ($x in @('127.0.0.1', '::1', 'localhost', [string]$env:COMPUTERNAME)) { if ($x) { $h.Add($x.ToLowerInvariant()) } }
    try { foreach ($a in [Net.Dns]::GetHostAddresses([Net.Dns]::GetHostName())) { $h.Add($a.ToString().ToLowerInvariant()) } } catch {}
    @($h | Select-Object -Unique)
}

# { Ok, Why }. The harness only ever talks to the test shard on this PC.
function Test-LegionTarget([string]$TargetHost, [int]$Port, [string[]]$OwnHosts = $null, $GameState = $null) {
    $no = { param($w) [pscustomobject]@{ Ok = $false; Why = $w } }
    if ($Port -eq $script:LegionLivePort) { return (& $no ("refused: port $Port is the live shard; the harness runs on this PC's test shard only")) }
    if ($script:LegionTestPorts -notcontains $Port) { return (& $no ("refused: port $Port is not a test shard port (2594 to 2599)")) }
    $h = ([string]$TargetHost).Trim().ToLowerInvariant()
    if (-not $h) { return (& $no 'refused: no host') }
    if ($script:LegionNeverHosts -contains $h -or $h -like '*.shatteredlegacyuo.com') { return (& $no ("refused: $TargetHost is the live shard or Haven, never a test target")) }
    if ($null -eq $OwnHosts) { $OwnHosts = Get-LegionOwnHosts }
    if (@($OwnHosts | ForEach-Object { ([string]$_).ToLowerInvariant() }) -notcontains $h) {
        return (& $no ("refused: $TargetHost is not this PC; the harness runs on this PC's own test shard only (127.0.0.1)"))
    }
    # cc-P819: on the game PC, no client opens while Chase plays another game (the pause's switch: settings.json
    # gamePause). $script:LegionGameCheck off (the facts) or -GameState given (a fact's fake) skips the real look.
    if ($script:LegionGameCheck -or $GameState) {
        $gs = $GameState
        if (-not $gs) { try { $gs = Get-GamePauseState -Root $script:LegionKitRoot } catch { $gs = $null } }
        if ($gs -and $gs.Applies -and $gs.Running) {
            return (& $no ($gs.Why + ': no game client opens on the game PC while he plays. Wait with D:\UO\golem\Test-GameRunning.ps1 -Wait (in the background; it ends when the game closes), then run this again'))
        }
    }
    [pscustomobject]@{ Ok = $true; Why = ('this PC''s test shard, ' + $TargetHost + ':' + $Port) }
}

# { Ok, Rows: [{ What, Ok, Detail }] }: what a PC needs to run a Legion script test.
function Get-LegionCapability([string]$Root, [string]$Golem, [string]$CodeRepo, [hashtable]$Paths = @{}) {
    $p = @{ TazUO = 'D:\UO\tazuo-sl-build\client\TazUO.exe'; ClientData = 'D:\UO\UltimaOnlineVanilla' }
    foreach ($k in $Paths.Keys) { $p[$k] = $Paths[$k] }
    $rows = New-Object System.Collections.Generic.List[object]
    $add = { param($w, $ok, $d) $rows.Add([pscustomobject]@{ What = $w; Ok = [bool]$ok; Detail = $d }) }
    $dk = $null; try { $dk = Get-Command docker -ErrorAction Stop } catch {}
    & $add 'Docker' ([bool]$dk) $(if ($dk) { $dk.Source } else { 'docker is not on this PC' })
    $cd = [string]$p.ClientData
    $cdOk = (Test-Path -LiteralPath (Join-Path $cd 'client.exe')) -and (Test-Path -LiteralPath (Join-Path $cd 'artLegacyMUL.uop'))
    & $add 'client data' $cdOk $(if ($cdOk) { $cd } else { 'no UO client files (client.exe, artLegacyMUL.uop) in ' + $cd })
    $tz = [string]$p.TazUO
    & $add 'TazUO' (Test-Path -LiteralPath $tz) $(if (Test-Path -LiteralPath $tz) { $tz } else { 'our TazUO build is not at ' + $tz })
    $bot = Join-Path $CodeRepo 'tools\playtest-bot\uobot\legionsetup.py'
    & $add 'play-test bot' (Test-Path -LiteralPath $bot) $(if (Test-Path -LiteralPath $bot) { $bot } else { 'no ' + $bot + ' (the work copy predates cc-P219)' })
    $py = $null; try { $py = Get-Command python -ErrorAction Stop } catch {}
    & $add 'Python' ([bool]$py) $(if ($py) { $py.Source } else { 'python is not on this PC' })
    $key = Join-Path $Root ('test-accounts-' + $Golem.ToLowerInvariant() + '.key')
    & $add 'test accounts' (Test-Path -LiteralPath $key) $(if (Test-Path -LiteralPath $key) { $Golem + '-admin and ' + $Golem + '-player' } else { 'no ' + $key + ' (cc-P215)' })
    $all = $rows.ToArray()
    [pscustomobject]@{ Ok = (@($all | Where-Object { -not $_.Ok }).Count -eq 0); Rows = $all }
}

# ClassicUO.Utility.Crypter.Encrypt: "1-" and each byte XOR the PC's name, in hex. Not secret, only not plain text; the
# harness clears it from the settings when the run ends.
function ConvertTo-CuoPassword([string]$Password, [string]$Machine = $env:COMPUTERNAME) {
    if (-not $Password -or -not $Machine) { return '' }
    $b = [Text.Encoding]::ASCII.GetBytes($Password)
    $sb = New-Object Text.StringBuilder
    [void]$sb.Append('1-')
    for ($i = 0; $i -lt $b.Length; $i++) { [void]$sb.Append(('{0:X2}' -f ($b[$i] -bxor [byte][char]$Machine[$i % $Machine.Length]))) }
    $sb.ToString()
}

# The plan file, checked: { script, timeLimitMinutes, overrides, setup[], steps[], failOn }.
function Read-LegionPlan([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) { throw ('no plan file at ' + $Path) }
    $p = Get-Content -LiteralPath $Path -Raw | ConvertFrom-Json
    if (-not [string]$p.script) { throw 'the plan names no script' }
    $mins = 10; if ($p.PSObject.Properties.Name -contains 'timeLimitMinutes') { $mins = [double]$p.timeLimitMinutes }
    if ($mins -le 0 -or $mins -gt 60) { throw ('timeLimitMinutes must be 1 to 60, not ' + $mins) }
    foreach ($c in @($p.setup)) { if ($c -and ([string]$c) -notmatch '^\[') { throw ('a setup line is not a staff command: ' + $c) } }
    foreach ($s in @($p.steps)) {
        if (-not $s) { continue }
        if ([string]$s.type -notin @('journal', 'items', 'at')) { throw ('a step''s type must be journal, items or at: ' + ($s | ConvertTo-Json -Compress)) }
        if ([string]$s.type -eq 'journal') { try { [void][regex]::new([string]$s.pattern) } catch { throw ('a step''s pattern is not a regex: ' + $s.pattern) } }
    }
    $p
}

# The script's text with each CONFIG line the plan overrides ("NAME = value") rewritten. { Text, Applied, Missing }.
function Set-LegionOverrides([string]$Text, $Overrides) {
    $applied = @(); $missing = @()
    if ($Overrides) {
        foreach ($pr in $Overrides.PSObject.Properties) {
            $rx = '(?m)^' + [regex]::Escape($pr.Name) + '\s*=.*$'
            if ([regex]::IsMatch($Text, $rx)) {
                $Text = ([regex]$rx).Replace($Text, ($pr.Name + ' = ' + [string]$pr.Value + '  # cc-P219 test override'), 1)
                $applied += ($pr.Name + ' = ' + [string]$pr.Value)
            } else { $missing += $pr.Name }
        }
    }
    [pscustomobject]@{ Text = $Text; Applied = $applied; Missing = $missing }
}

# TazUO's settings for the test client: this PC's test shard, the Player account, auto-login, and relay redirects
# ignored, so the shard can never send the client anywhere else (D8).
function New-LegionSettings([string]$TargetHost, [int]$Port, [string]$User, [string]$EncPassword, [string]$ClientData) {
    [ordered]@{
        username = $User; password = $EncPassword; ip = $TargetHost; port = $Port
        ignore_relay_ip = $true
        ultimaonlinedirectory = $ClientData; profilespath = ''; clientversion = '7.0.117.0'; lang = 'ENU'
        lastservernum = 1; last_server_name = 'Shattered Legacy TEST'; fps = 30
        window_position = [ordered]@{ X = 40; Y = 40 }; window_size = [ordered]@{ X = 1280; Y = 800 }; is_win_maximized = $false
        saveaccount = $true; autologin = $true; reconnect = $false; reconnect_time = 1000
        login_music = $false; login_music_volume = 0; fixed_time_step = $true; run_mouse_in_separate_thread = $true
        force_driver = 0; use_verdata = $false; maps_layouts = $null; encryption = 0
        plugins = @()
    }
}

# The lines of a text file written since a time (a whole file when it was made since then), the last $Max of them.
function Get-LegionLines([string]$Path, [datetime]$Since, [int]$Max = 80, [string]$Match = '') {
    if (-not $Path -or -not (Test-Path -LiteralPath $Path)) { return @() }
    $f = Get-Item -LiteralPath $Path
    if ($f.LastWriteTime -lt $Since) { return @() }
    $l = @(Get-Content -LiteralPath $Path -ErrorAction SilentlyContinue)
    if ($Match) { $l = @($l | Where-Object { $_ -match $Match }) }
    @($l | Select-Object -Last $Max)
}

# A screenshot of a window (PrintWindow, which also works for a DirectX window), as a JPEG at most 1280 wide.
function Save-LegionShot([IntPtr]$Window, [string]$Path) {
    if ($Window -eq [IntPtr]::Zero) { return $false }
    if (-not ('LegionShot' -as [type])) {
        Add-Type -AssemblyName System.Drawing
        Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public static class LegionShot {
    [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left, Top, Right, Bottom; }
    [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
    [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr dc, uint flags);
}
'@
    }
    $r = New-Object LegionShot+RECT
    if (-not [LegionShot]::GetWindowRect($Window, [ref]$r)) { return $false }
    $w = $r.Right - $r.Left; $h = $r.Bottom - $r.Top
    if ($w -le 0 -or $h -le 0) { return $false }
    $bmp = New-Object System.Drawing.Bitmap $w, $h
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $dc = $g.GetHdc()
    $ok = [LegionShot]::PrintWindow($Window, $dc, 2)
    $g.ReleaseHdc($dc); $g.Dispose()
    if (-not $ok) { $bmp.Dispose(); return $false }
    $scale = [Math]::Min(1.0, 1280.0 / $w)
    $out = $bmp
    if ($scale -lt 1.0) { $out = New-Object System.Drawing.Bitmap $bmp, ([int]($w * $scale)), ([int]($h * $scale)); $bmp.Dispose() }
    $enc = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.MimeType -eq 'image/jpeg' } | Select-Object -First 1
    $ep = New-Object System.Drawing.Imaging.EncoderParameters 1
    $ep.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter ([System.Drawing.Imaging.Encoder]::Quality), 80L
    $out.Save($Path, $enc, $ep)
    $out.Dispose()
    $true
}

# The report: pass or fail per step, the setup, the journal, the Legion log, the screenshots, the client and server
# errors. $R: { Script, Golem, Host, Port, Plan, PlanFile, Result, Why, Steps, Setup, Overrides, Journal, LegionLog,
# RunnerLog, ClientErrors, ServerErrors, Shots, Started, Ended, Branch, ScriptFile }.
function Format-LegionReport($R) {
    $nl = "`r`n"
    $o = New-Object System.Collections.Generic.List[string]
    $o.Add('# Legion script test: ' + $R.Script + ' (' + $R.Golem + ', ' + $R.Started.ToString('yyyy-MM-dd HH:mm') + ')')
    $o.Add('')
    $o.Add('**Result: ' + $(if ($R.Result -eq 'pass') { 'PASS' } else { 'FAIL' }) + '**: ' + $R.Why + '.')
    $o.Add('')
    $o.Add('- Script: `' + $R.ScriptFile + '`' + $(if ($R.Branch) { ' (branch `' + $R.Branch + '` of the scripts repo)' } else { '' }))
    $o.Add('- Plan: `' + $R.PlanFile + '` (time limit ' + $R.Plan.timeLimitMinutes + ' min)')
    $o.Add('- Shard: this PC''s test shard, ' + $R.Host + ':' + $R.Port + ' (the never-live guard passed; relay redirects ignored)')
    $o.Add('- Account: `' + $R.Golem.ToLowerInvariant() + '-player`, character ' + $R.Golem + ' the Tester; setup by `' + $R.Golem.ToLowerInvariant() + '-admin`')
    $o.Add('- Ran: ' + $R.Started.ToString('HH:mm:ss') + ' to ' + $R.Ended.ToString('HH:mm:ss') + ' (' + [int]($R.Ended - $R.Started).TotalSeconds + ' s, the client start included)')
    if (@($R.Overrides).Count) { $o.Add('- Test overrides in the script''s CONFIG: ' + ((@($R.Overrides) | ForEach-Object { '`' + $_ + '`' }) -join ', ')) }
    $o.Add('')
    $o.Add('## Steps')
    $o.Add('')
    $o.Add('| Step | Result | Detail |')
    $o.Add('|---|---|---|')
    foreach ($s in @($R.Steps)) { $o.Add('| ' + $s.name + ' | ' + $(if ($s.result -eq 'pass') { 'pass' } else { '**' + $s.result + '**' }) + ' | ' + ([string]$s.detail -replace '\|', '/') + ' |') }
    if (@($R.Setup).Count) {
        $o.Add(''); $o.Add('## Setup (the Golem''s Admin, on the test shard)'); $o.Add('')
        foreach ($c in @($R.Setup)) { $o.Add('- `' + $c.command + '`: ' + $(if (@($c.replies).Count) { (@($c.replies) -join ' / ') } else { '(no answer)' }) + $(if ($c.ok) { '' } else { ' **(failed)**' })) }
    }
    if (@($R.Shots).Count) {
        $o.Add(''); $o.Add('## Screenshots'); $o.Add('')
        foreach ($s in @($R.Shots)) { $o.Add('![' + $s.What + '](' + $s.Rel + ')'); $o.Add('') }
    }
    foreach ($sec in @(@('Journal (the client, last lines)', $R.Journal), @('Legion log (the script''s own log, this run)', $R.LegionLog), @('Runner log', $R.RunnerLog), @('Client errors', $R.ClientErrors), @('Server errors (the test shard''s log, this run)', $R.ServerErrors))) {
        $o.Add(''); $o.Add('## ' + $sec[0]); $o.Add('')
        $l = @($sec[1] | Where-Object { $_ -ne $null })
        if ($l.Count) { $o.Add('```'); foreach ($x in $l) { $o.Add(([string]$x -replace '[^\x09\x20-\x7E]', '?')) }; $o.Add('```') } else { $o.Add('None.') }
    }
    ($o -join $nl) + $nl
}
