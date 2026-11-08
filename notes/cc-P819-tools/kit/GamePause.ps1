#Requires -Version 5.1
<#
  GamePause.ps1 (cc-P819; Chase 11-07: "pause bot play testing when im playing other games"). Dot-source it; it defines
  functions only. The one game check every bot and every client-opening Golem step uses on the game PC: GolemPower's game
  detection (Get-GolemOwnerActivity: the known game names, the registry's extra games, or a process under steamapps\
  common, Epic Games, EA Games, Riot Games or Battle.net game folders; launchers left out), less our own UO clients.
  GolemPower's back-off stays off on the game PC by design (the Golems' builds, tests and code go on while he plays);
  this pause covers only what drives game clients or loads the PC: the overnight play tests, the Play Test Goblin, and
  a Golem's proof shots, two-client tests and playtest-bot runs.

  Get-GamePauseConfig    settings.json: gamePause (default on) and gamePausePc (default CHASES-TOWER); on another PC
                         the pause never applies ("Other PCs are unaffected")
  Test-GolemGameRunning  { Running, Game, Games, Why }: a game running now, our own clients left out
  Get-GamePauseState     { Applies, On, Pc, Running, Game, Why }: what a bot should do now, one line in Why
  Wait-GolemNoGame       waits while a game runs, checking every -IntervalSeconds, until it clears or -Until; writes
                         game-wait-<who>.json in the kit root while it waits (the consoles' "waiting: Chase is playing
                         <game>" line) and removes it after. Returns { Outcome: clear|timeout|off|elsewhere, Game, Waited }

  No Windows API (the kit's SentinelOne rule): Get-Process names and paths only. ASCII only.
#>

$script:GpzHere = $PSScriptRoot
if (-not (Get-Command Get-GolemOwnerActivity -ErrorAction SilentlyContinue)) { . (Join-Path $script:GpzHere 'GolemPower.ps1') }

# Our own Ultima Online clients never count as "another game": TazUO, ClassicUO (and its bootstrap), the UO Enhanced
# Client (UOSA), the classic client (client.exe under an Ultima Online folder), and anything run from their folders.
$script:GpzOwnNames = @('TazUO', 'ClassicUO', 'ClassicUO.Bootstrap', 'cuo', 'UOSA', 'UO', 'ClassicUOLauncher', 'TazUOLauncher')
# Tools that run all day from a game folder and are not a game: Wallpaper Engine (its ui, seen on the game PC
# 2026-11-07 as wallpaperui under steamapps\common\wallpaper_engine: GolemPower's launcher list has only its wallpaper32/64)
# and SteamVR's helpers. Left out like our own clients.
$script:GpzNotGameNames = @('wallpaperui', 'wallpaper32', 'wallpaper64', 'webwallpaper32', 'webwallpaper64', 'ui32', 'vrserver', 'vrmonitor', 'vrcompositor', 'vrdashboard', 'vrwebhelper')
$script:GpzNotGamePaths = @('\wallpaper_engine', '\SteamVR')
$script:GpzOwnPaths = @('\Ultima Online', '\UltimaOnline', '\tazuo', '\ClassicUO', '\uo-client', '\ShatteredLegacy', '\UO\tool-trials\', '\UO\golems\', '\UO\golem\')

function Get-GpzProp($o, [string]$name, $default) {
    if ($null -eq $o) { return $default }
    if ($o -is [hashtable]) { if ($o.ContainsKey($name) -and $null -ne $o[$name]) { return $o[$name] } else { return $default } }
    if ($o.PSObject.Properties.Name -contains $name -and $null -ne $o.$name) { return $o.$name }
    $default
}

function Test-GpzOwnClient($p) {
    $n = [string](Get-GpzProp $p 'Name' ''); $path = [string](Get-GpzProp $p 'Path' '')
    if ($script:GpzOwnNames -contains $n) { return $true }
    if ($script:GpzNotGameNames -contains $n) { return $true }
    foreach ($frag in $script:GpzNotGamePaths) { if ($path -and $path.IndexOf($frag, [StringComparison]::OrdinalIgnoreCase) -ge 0) { return $true } }
    foreach ($frag in $script:GpzOwnPaths) { if ($path -and $path.IndexOf($frag, [StringComparison]::OrdinalIgnoreCase) -ge 0) { return $true } }
    $false
}

# settings.json gamePause (bool, default true) and gamePausePc (default CHASES-TOWER, the game PC).
function Get-GamePauseConfig([string]$Root = 'D:\UO\golem') {
    $s = $null
    $f = Join-Path $Root 'settings.json'
    if (Test-Path -LiteralPath $f) { try { $s = Get-Content -LiteralPath $f -Raw | ConvertFrom-Json } catch { $s = $null } }
    $pc = [string](Get-GpzProp $s 'gamePausePc' 'CHASES-TOWER')
    [pscustomobject]@{ On = [bool](Get-GpzProp $s 'gamePause' $true); Pc = $pc; File = $f }
}

# The extra game names every Golem entry in golems.json lists (backoff.games), as GolemPower's back-off reads them.
function Get-GpzRegistryGames([string]$Root = 'D:\UO\golem') {
    $f = Join-Path $Root 'golems.json'
    if (-not (Test-Path -LiteralPath $f)) { return @() }
    try { $j = Get-Content -LiteralPath $f -Raw | ConvertFrom-Json } catch { return @() }
    $list = $(if ($j.PSObject.Properties.Name -contains 'golems') { @($j.golems) } else { @($j) })
    @($list | ForEach-Object { @(Get-GpzProp (Get-GpzProp $_ 'backoff' $null) 'games' @()) } | Where-Object { $_ } | Select-Object -Unique)
}

# { Running, Game, Games, Why }. -Fake @{ Processes = @(@{ Name; Path }) } for the facts.
function Test-GolemGameRunning([string]$Root = 'D:\UO\golem', [hashtable]$Fake) {
    if ($Fake -and $Fake.ContainsKey('Processes')) { $procs = @($Fake.Processes | Where-Object { $_ }) }
    else { $procs = @(Get-Process -ErrorAction SilentlyContinue | ForEach-Object { [pscustomobject]@{ Name = $_.ProcessName; Path = $(try { $_.Path } catch { '' }) } }) }
    $others = @($procs | Where-Object { -not (Test-GpzOwnClient $_) })
    $o = Get-GolemOwnerActivity -Games (Get-GpzRegistryGames $Root) -Fake @{ Quser = ''; Processes = $others; Me = [Environment]::UserName }
    $games = @($o.Games)
    [pscustomobject]@{
        Running = [bool]$games.Count; Game = $(if ($games.Count) { [string]$games[0] } else { '' }); Games = $games
        Why = $(if ($games.Count) { 'a game is running: ' + ($games -join ', ') } else { 'no game running' })
    }
}

# What a bot should do now. Applies is false on another PC or with the pause off: then Running is not even looked at.
function Get-GamePauseState([string]$Root = 'D:\UO\golem', [string]$Computer = $env:COMPUTERNAME, [hashtable]$Fake) {
    $c = Get-GamePauseConfig $Root
    if (-not $c.On) { return [pscustomobject]@{ Applies = $false; On = $false; Pc = $c.Pc; Running = $false; Game = ''; Why = 'game pause off (settings.json gamePause)' } }
    if ($Computer -and $c.Pc -and ($Computer -ine $c.Pc)) { return [pscustomobject]@{ Applies = $false; On = $true; Pc = $c.Pc; Running = $false; Game = ''; Why = ('not the game PC (' + $c.Pc + '): no pause here') } }
    $g = Test-GolemGameRunning -Root $Root -Fake $Fake
    [pscustomobject]@{ Applies = $true; On = $true; Pc = $c.Pc; Running = $g.Running; Game = $g.Game
        Why = $(if ($g.Running) { 'waiting: Chase is playing ' + $g.Game } else { 'no game running' }) }
}

function Get-GpzWaitFile([string]$Root, [string]$Who) {
    $safe = ([string]$Who) -replace '[^A-Za-z0-9_-]', '-'
    if (-not $safe) { $safe = 'bot' }
    Join-Path $Root ('game-wait-' + $safe + '.json')
}

<#
  Waits while a game runs on the game PC. Every -IntervalSeconds it looks again (the night bots: 600). -Until: the
  latest time to wait (the night window's end, 06:30); none waits as long as it takes. While it waits it keeps
  game-wait-<Who>.json in -Root ({ who, what, game, since, until, checkedAt }) for the consoles' status line, and removes
  it when it returns. -Log gets one line at the start, one per game change and one at the end. -Sleep and -Clock are
  the facts' seams.
#>
function Wait-GolemNoGame {
    param(
        [string]$Root = 'D:\UO\golem', [string]$Who = 'bot', [string]$What = 'play testing', [Nullable[datetime]]$Until = $null,
        [int]$IntervalSeconds = 600, [scriptblock]$Log = { param($t) Write-Host $t }, [scriptblock]$Sleep = { param($s) Start-Sleep -Seconds $s },
        [scriptblock]$Clock = { Get-Date }, [string]$Computer = $env:COMPUTERNAME, [scriptblock]$Probe = $null
    )
    $start = & $Clock
    $st = $(if ($Probe) { & $Probe } else { Get-GamePauseState -Root $Root -Computer $Computer })
    if (-not $st.Applies) { return [pscustomobject]@{ Outcome = $(if (-not $st.On) { 'off' } else { 'elsewhere' }); Game = ''; Waited = [TimeSpan]::Zero; Why = $st.Why } }
    if (-not $st.Running) { return [pscustomobject]@{ Outcome = 'clear'; Game = ''; Waited = [TimeSpan]::Zero; Why = $st.Why } }
    $file = Get-GpzWaitFile $Root $Who
    $game = $st.Game
    & $Log ('waiting: Chase is playing ' + $game + '; ' + $What + ' waits, looking again every ' + $(if ($IntervalSeconds -ge 60) { [string][int]($IntervalSeconds / 60) + ' min' } else { [string]$IntervalSeconds + ' s' }) + $(if ($Until) { ' until ' + ([datetime]$Until).ToString('HH:mm') } else { '' }))
    $outcome = 'clear'
    try {
        while ($true) {
            $now = & $Clock
            $rec = [ordered]@{ who = $Who; what = $What; game = $game; line = ('waiting: Chase is playing ' + $game); since = $start.ToString('s'); until = $(if ($Until) { ([datetime]$Until).ToString('s') } else { '' }); checkedAt = $now.ToString('s') }
            try { [IO.File]::WriteAllText($file, ($rec | ConvertTo-Json -Compress), (New-Object Text.UTF8Encoding $false)) } catch {}
            if ($Until -and $now -ge ([datetime]$Until)) { $outcome = 'timeout'; break }
            $wait = $IntervalSeconds
            if ($Until) { $left = [int][Math]::Ceiling((([datetime]$Until) - $now).TotalSeconds); if ($left -lt $wait) { $wait = [Math]::Max(1, $left) } }
            & $Sleep $wait
            $st = $(if ($Probe) { & $Probe } else { Get-GamePauseState -Root $Root -Computer $Computer })
            if (-not $st.Applies) { $outcome = $(if (-not $st.On) { 'off' } else { 'elsewhere' }); break }
            if (-not $st.Running) { $outcome = 'clear'; break }
            if ($st.Game -ne $game) { $game = $st.Game; & $Log ('still waiting: Chase is playing ' + $game) }
        }
    } finally { Remove-Item -LiteralPath $file -ErrorAction SilentlyContinue }
    $waited = (& $Clock) - $start
    $mins = [int][Math]::Round($waited.TotalMinutes)
    switch ($outcome) {
        'clear'   { & $Log ('the game closed: ' + $What + ' goes on (waited ' + $mins + ' min)') }
        'off'     { & $Log ('game pause turned off: ' + $What + ' goes on (waited ' + $mins + ' min)') }
        'timeout' { & $Log ('still playing ' + $game + ' at ' + ([datetime]$Until).ToString('HH:mm') + ': ' + $What + ' is skipped (waited ' + $mins + ' min)') }
    }
    [pscustomobject]@{ Outcome = $outcome; Game = $game; Waited = $waited; Why = $st.Why }
}
