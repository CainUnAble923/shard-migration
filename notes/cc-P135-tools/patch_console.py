"""cc-P135: add the Map and Art tab to Shard-Console.ps1 and its facts. Exact-anchor edits; aborts if an anchor
is missing or ambiguous, so a partial patch is never written."""
import sys

CONSOLE = r'D:\ShatteredLegacy\scripts\Shard-Console.ps1'
TESTS = r'D:\ShatteredLegacy\scripts\tests\Shard-Console.Tests.ps1'


def edit(text, anchor, replacement, count=1, label=''):
    n = text.count(anchor)
    if n != count:
        sys.exit('anchor found %d times (wanted %d): %s\n%s' % (n, count, label, anchor[:200]))
    return text.replace(anchor, replacement)


def main():
    s = open(CONSOLE, encoding='ascii', newline='').read()
    assert '\r' not in s

    # A. the param block
    s = edit(s, """    # cc-P96: Fix test shard > Rebuild's commit (a hash from its list, or HEAD).
    [string]$Commit
)""", """    # cc-P96: Fix test shard > Rebuild's commit (a hash from its list, or HEAD).
    [string]$Commit,
    # cc-P135: Map and Art. The .vd file and body for art.checkvd, the other hues.mul for art.hues.
    [string]$VdFile,
    [string]$Body,
    [string]$HuesFile
)""", label='param block')

    # B. the actions
    s = edit(s, """        # cc-P86: beside the PUBLIC DNS tile and on the Diagnostics tab. 'here': it opens Proton or ends a WireGuard
        # tunnel from this console, then the tile re-checks.
        [pscustomobject]@{ Key = 'vpn.disconnect';   Group = 'Network';     Label = 'Disconnect VPN';                     Mutates = $true;  RunIn = 'here' }
    )""", """        # cc-P86: beside the PUBLIC DNS tile and on the Diagnostics tab. 'here': it opens Proton or ends a WireGuard
        # tunnel from this console, then the tile re-checks.
        [pscustomobject]@{ Key = 'vpn.disconnect';   Group = 'Network';     Label = 'Disconnect VPN';                     Mutates = $true;  RunIn = 'here' }
        # cc-P135: the Map and Art tab. The four art checks run scripts\\validate-art.py (read only) in the pane or a window
        # of their own; the six map buttons only print an in-game command's syntax here.
        [pscustomobject]@{ Key = 'art.registry';     Group = 'Map and Art';  Label = 'Check the art registry';            Mutates = $false; RunIn = 'window' }
        [pscustomobject]@{ Key = 'art.bodies';       Group = 'Map and Art';  Label = 'Body table';                        Mutates = $false; RunIn = 'window' }
        [pscustomobject]@{ Key = 'art.checkvd';      Group = 'Map and Art';  Label = 'Check a .vd';                       Mutates = $false; RunIn = 'window' }
        [pscustomobject]@{ Key = 'art.hues';         Group = 'Map and Art';  Label = 'Compare a hues.mul with ours';      Mutates = $false; RunIn = 'window' }
        [pscustomobject]@{ Key = 'map.footprint';    Group = 'Map commands'; Label = '[CheckFootprint';                   Mutates = $false; RunIn = 'here' }
        [pscustomobject]@{ Key = 'map.spots';        Group = 'Map commands'; Label = '[ValidateSpots';                    Mutates = $false; RunIn = 'here' }
        [pscustomobject]@{ Key = 'map.statics';      Group = 'Map commands'; Label = '[FindStaticProblems';               Mutates = $false; RunIn = 'here' }
        [pscustomobject]@{ Key = 'map.walkable';     Group = 'Map commands'; Label = '[Walkable';                         Mutates = $false; RunIn = 'here' }
        [pscustomobject]@{ Key = 'map.shore';        Group = 'Map commands'; Label = '[ShoreCheck';                       Mutates = $false; RunIn = 'here' }
        [pscustomobject]@{ Key = 'map.export';       Group = 'Map commands'; Label = '[ExportPoints';                     Mutates = $false; RunIn = 'here' }
    )""", label='actions')

    # C. the config
    s = edit(s, """        OpsFile            = $opsFile
        Ops                = (ConvertFrom-OpsConfig $opsJson)
    }""", """        OpsFile            = $opsFile
        Ops                = (ConvertFrom-OpsConfig $opsJson)
        # cc-P135, the Map and Art tab: validate-art.py (cc-P134; read only), the python it runs with, our own hues.mul
        # the diff compares against, and the subcommands the console may run (never render, the one that writes PNGs).
        ValidateArt        = (Join-Path $RepoRoot 'scripts\\validate-art.py')
        Python             = 'python'
        OurHues            = (Join-Path $RepoRoot 'client-data\\classic-client-7.0.117.0\\hues.mul')
        ArtSubcommands     = @('bodies', 'check-registry', 'check-vd', 'propose', 'hues-diff')
    }""", label='config')

    # D. the banner
    s = edit(s, """    if ($Action -like 'vpn.*') { $what = $Action + ' (this PC''s VPN)' }
""", """    if ($Action -like 'vpn.*') { $what = $Action + ' (this PC''s VPN)' }
    if ($Action -like 'art.*' -or $Action -like 'map.*') { $what = $Action + ' (map and art)' }
""", label='banner what')
    s = edit(s, """        { $_ -eq 'execute' -and $Action -eq 'package.publish' } {""", """        { $_ -eq 'execute' -and ($Action -like 'art.*' -or $Action -like 'map.*') } {
            # cc-P135: validate-art.py reads the client data and writes nothing; the map buttons only print.
            [pscustomobject]@{ Color = 'amber'; Title = ('MAP AND ART - ' + $what + ' - Shard Console'); Lines = @(
                $bar, ('  MAP AND ART  ' + $what), '  Runs scripts\\validate-art.py, which reads the client data and writes nothing, or prints a command''s syntax. No shard is touched.', $bar) }
            break
        }
        { $_ -eq 'execute' -and $Action -eq 'package.publish' } {""", label='banner case')

    # E. Get-ActionPlan: params and dispatch
    s = edit(s, """        $WipeFacts, [string]$WipeAdmin, $AutopilotFacts, $VpnFacts, $FixFacts, [string]$Commit, [string]$Site
    )
    # cc-P101: the Websites buttons read websites.json only (it is in $Config).
    if ($Action -like 'web.*') { return (Get-WebsitePlan -Action $Action -Config $Config -Site $Site) }
""", """        $WipeFacts, [string]$WipeAdmin, $AutopilotFacts, $VpnFacts, $FixFacts, [string]$Commit, [string]$Site,
        [string]$VdFile, [string]$Body, [string]$HuesFile
    )
    # cc-P101: the Websites buttons read websites.json only (it is in $Config).
    if ($Action -like 'web.*') { return (Get-WebsitePlan -Action $Action -Config $Config -Site $Site) }
    # cc-P135: the Map and Art buttons read nothing but the file names they are given.
    if ($Action -like 'art.*' -or $Action -like 'map.*') { return (Get-MapArtPlan -Action $Action -Config $Config -VdFile $VdFile -Body $Body -HuesFile $HuesFile) }
""", label='plan dispatch')

    # F. the new plan functions, before Get-ActionPlan
    s = edit(s, """function Get-ActionPlan {
    # Every button is a plan""", MAPART_FUNCS + """function Get-ActionPlan {
    # Every button is a plan""", label='plan functions')

    # G. the safety rule
    s = edit(s, """        if ($s.Kind -eq 'answer') {
            # cc-P106: an answer goes only to a shard's console""", """        # cc-P135: python runs here only as scripts\\validate-art.py with one of its read-only subcommands, as an exec step
        # (so its output lands in the pane or the window), never render (the one that writes files) and never another
        # script; and that script is reached only that way.
        $named135 = @(@($s.Exe) + @($s.Arguments) + @($s.Path) | Where-Object { $_ } | ForEach-Object { [string]$_ })
        $isPy = ([string]$s.Exe -match '(?i)(^|[\\\\/])python(\\d(\\.\\d+)?)?(\\.exe)?$')
        $namesVa = [bool]($Config.ValidateArt -and @($named135 | Where-Object { $_ -ieq $Config.ValidateArt -or $_ -match '(?i)validate-art\\.py$' }).Count)
        if ($isPy -or $namesVa) {
            $sa = @($s.Arguments)
            $sub = ''
            if ($sa.Count -ge 2) { $sub = [string]$sa[1] }
            $ok = ($s.Kind -eq 'exec' -and $isPy -and $Config.ValidateArt -and $sa.Count -ge 2 -and [string]$sa[0] -ieq $Config.ValidateArt -and @($Config.ArtSubcommands) -ccontains $sub -and -not @($sa | Where-Object { $_ -match '^--out' }).Count)
            if (-not $ok) { $v.Add('python runs here only as ' + $Config.ValidateArt + ' with one of ' + (@($Config.ArtSubcommands) -join ', ') + ', never render: ' + $line) }
        }
        if ($s.Kind -eq 'answer') {
            # cc-P106: an answer goes only to a shard's console""", label='safety')

    # H. the child argument line
    s = edit(s, """        [string]$ImageTag, [switch]$CommitForce, [string]$WipeAdmin, [switch]$ForPane, [string]$Commit
    )
    $mode = 'Execute'""", """        [string]$ImageTag, [switch]$CommitForce, [string]$WipeAdmin, [switch]$ForPane, [string]$Commit,
        [string]$VdFile, [string]$Body, [string]$HuesFile
    )
    $mode = 'Execute'""", label='child params')
    s = edit(s, """    if ($Commit -match '^([0-9a-fA-F]{7,40}|HEAD)$') { $a += ' -Commit ' + $Commit }
    $a
}""", """    if ($Commit -match '^([0-9a-fA-F]{7,40}|HEAD)$') { $a += ' -Commit ' + $Commit }
    # cc-P135: the .vd and hues.mul paths are picked in a file dialog or typed; quoted so a space cannot split them, a
    # quote in a path dropped (the plan then refuses a file that is not there). The body crosses only as digits.
    if ($VdFile) { $a += ' -VdFile "' + ($VdFile -replace '"', '') + '"' }
    if ($Body -match '^\\d{1,5}$') { $a += ' -Body ' + $Body }
    if ($HuesFile) { $a += ' -HuesFile "' + ($HuesFile -replace '"', '') + '"' }
    $a
}""", label='child line')

    # I. Invoke-ConsoleButton
    s = edit(s, """        [string]$PackageNotes, [string]$PackageZip, [string]$ImageTag, [switch]$CommitForce, [string]$WipeAdmin, [string]$Commit, [string]$Site,
        $Prefetched)""", """        [string]$PackageNotes, [string]$PackageZip, [string]$ImageTag, [switch]$CommitForce, [string]$WipeAdmin, [string]$Commit, [string]$Site,
        $Prefetched, [string]$VdFile, [string]$Body, [string]$HuesFile)""", label='button params')
    s = edit(s, """if ($ActionKey -like 'web.*') { $ShardKey = 'websites' } }""",
             """if ($ActionKey -like 'web.*') { $ShardKey = 'websites' }; if ($ActionKey -like 'art.*' -or $ActionKey -like 'map.*') { $ShardKey = 'mapart' } }""", label='button shardkey')
    s = edit(s, """        if (-not $Prefetched -and $script:BackgroundRefresh -and $ActionKey -notlike 'links.*' -and $ActionKey -notlike 'web.*') {""",
             """        if (-not $Prefetched -and $script:BackgroundRefresh -and $ActionKey -notlike 'links.*' -and $ActionKey -notlike 'web.*' -and $ActionKey -notlike 'art.*' -and $ActionKey -notlike 'map.*') {""", label='button precheck')
    s = edit(s, """        if ($ActionKey -like 'links.*' -or $ActionKey -like 'web.*') {
            # cc-P83: a link reads nothing. cc-P101: nor does a Websites button (websites.json is in the config).
        } elseif ($isVpn) {""", """        if ($ActionKey -like 'links.*' -or $ActionKey -like 'web.*' -or $ActionKey -like 'art.*' -or $ActionKey -like 'map.*') {
            # cc-P83: a link reads nothing. cc-P101: nor does a Websites button (websites.json is in the config). cc-P135: nor a Map and Art one.
        } elseif ($isVpn) {""", label='button reads')
    s = edit(s, """-FixFacts $fxFacts -Commit $Commit -Site $Site)""", """-FixFacts $fxFacts -Commit $Commit -Site $Site -VdFile $VdFile -Body $Body -HuesFile $HuesFile)""", label='button plan call')
    s = edit(s, """-ForPane:($route -eq 'pane') -Commit $Commit
""", """-ForPane:($route -eq 'pane') -Commit $Commit -VdFile $VdFile -Body $Body -HuesFile $HuesFile
""", label='button child line')

    # J. Get-ActionFacts
    s = edit(s, """    if ($ActionKey -like 'links.*' -or $ActionKey -like 'web.*') {
        # cc-P83: a link reads nothing. cc-P101: nor does a Websites button (websites.json is in the config).
    } elseif ($ActionKey -like 'vpn.*') {""", """    if ($ActionKey -like 'links.*' -or $ActionKey -like 'web.*' -or $ActionKey -like 'art.*' -or $ActionKey -like 'map.*') {
        # cc-P83: a link reads nothing. cc-P101: nor does a Websites button (websites.json is in the config). cc-P135: nor a Map and Art one.
    } elseif ($ActionKey -like 'vpn.*') {""", label='action facts')

    # K. the headless entry
    s = edit(s, """    if ($Action -like 'web.*') { $sk = 'websites' }
    # The mode is decided and shown before anything is read or run (D37).""", """    if ($Action -like 'web.*') { $sk = 'websites' }
    if ($Action -like 'art.*' -or $Action -like 'map.*') { $sk = 'mapart' }
    # The mode is decided and shown before anything is read or run (D37).""", label='entry sk')
    s = edit(s, """    if ($Action -like 'links.*' -or $Action -like 'web.*') {
        # cc-P83: a link reads nothing. cc-P101: nor does a Websites action.""", """    if ($Action -like 'links.*' -or $Action -like 'web.*' -or $Action -like 'art.*' -or $Action -like 'map.*') {
        # cc-P83: a link reads nothing. cc-P101: nor does a Websites action. cc-P135: nor a Map and Art one.""", label='entry reads')
    s = edit(s, """-FixFacts $fixFacts -Commit $Commit -Site $Site)""", """-FixFacts $fixFacts -Commit $Commit -Site $Site -VdFile $VdFile -Body $Body -HuesFile $HuesFile)""", label='entry plan call')
    s = edit(s, """    Write-Host 'golem.on, .off, .email, .test and .move need -Mode Execute;""", """    Write-Host 'art.registry and art.bodies run scripts\\validate-art.py (read only); art.checkvd takes -VdFile <path> and -Body <n> (no body: a free one is proposed); art.hues takes -HuesFile <the other hues.mul>. map.* print an in-game command''s syntax.'
    Write-Host 'golem.on, .off, .email, .test and .move need -Mode Execute;""", label='list help')

    # L. Invoke-Plan: a reported exit code
    s = edit(s, """                    $code = Invoke-ExecStep -Exe $s.Exe -Arguments @($s.Arguments) -OutFile $outFile -Header ($tag + $line)
                    if ($code -ne 0) { throw ($line + ' exited with ' + $code) }
                }
                'script' {""", """                    $code = Invoke-ExecStep -Exe $s.Exe -Arguments @($s.Arguments) -OutFile $outFile -Header ($tag + $line)
                    # cc-P135: a step may name one exit code that means "found something" (validate-art exits 1 when it
                    # finds problems). That is said, in amber, and the plan goes on; any other non-zero exit fails it.
                    if ($code -ne 0 -and $s.Named -and $s.Named.Contains('ReportExit') -and $code -eq [int]$s.Named['ReportExit']) { Write-ConsoleLine ('      exited with ' + $code + ': it found something; read the lines above. Not a failure.') 'amber' }
                    elseif ($code -ne 0) { throw ($line + ' exited with ' + $code) }
                }
                'script' {""", label='exec report exit')

    # M. tooltips
    s = edit(s, """        'tab.Test shard'   = """, TOOLTIPS + """        'tab.Test shard'   = """, label='tooltips')
    s = edit(s, """        'tab.World setup'  = 'In-game commands to paste into a client, read from the code. The console cannot run them.'
""", """        'tab.World setup'  = 'In-game commands to paste into a client, read from the code. The console cannot run them.'
        'tab.Map and Art'  = 'Art checks that run validate-art here, and the syntax of the in-game map checks to type in a client.'
""", label='tab tooltip')

    # N. the page
    s = edit(s, """    } else { $worldPage.Controls.Add((New-WorldSetupTable $Config)) }

    $diagPage = New-ButtonPage 'Diagnostics'""", """    } else { $worldPage.Controls.Add((New-WorldSetupTable $Config)) }
""" + PAGE + """
    $diagPage = New-ButtonPage 'Diagnostics'""", label='page')
    s = edit(s, """    $tabs.TabPages.AddRange(@($testPage, $fixPage, $qPage, $snapPage, $worldPage, $diagPage, $commitPage, $pkgPage, $apPage, $webPage, $livePage))""",
             """    $tabs.TabPages.AddRange(@($testPage, $fixPage, $qPage, $snapPage, $worldPage, $artPage, $diagPage, $commitPage, $pkgPage, $apPage, $webPage, $livePage))""", label='tab add')
    # the button helpers, beside New-WebsiteButton
    s = edit(s, """function Get-SelectedQuestionShard {""", HELPERS + """function Get-SelectedQuestionShard {""", label='helpers')

    s.encode('ascii')
    open(CONSOLE, 'w', encoding='ascii', newline='').write(s)

    # ---- the facts
    t = open(TESTS, encoding='ascii', newline='').read()
    assert '\r' not in t
    t = edit(t, """        Assert-Equal 'Test shard,Fix test shard,Shard question,Snapshots,World setup,Diagnostics,Commit,Player package,Golem,Websites,LIVE shard' ($tabs -join ',') 'cc-P74 adds Autopilot (Golem since cc-P99), cc-P101 Websites, cc-P96 Fix test shard beside Test shard, cc-P106 Shard question after it; LIVE stays last'""",
             """        Assert-Equal 'Test shard,Fix test shard,Shard question,Snapshots,World setup,Map and Art,Diagnostics,Commit,Player package,Golem,Websites,LIVE shard' ($tabs -join ',') 'cc-P74 adds Autopilot (Golem since cc-P99), cc-P101 Websites, cc-P96 Fix test shard beside Test shard, cc-P106 Shard question after it, cc-P135 Map and Art after World setup; LIVE stays last'""", label='tab list fact')
    t = edit(t, """        $WipeFacts = $wipeFactsOk, [string]$WipeName = 'newadmin', $FixFacts = $p96Facts, [string]$PickedCommit = '61db33c0a1b2c3d4e5f60718293a4b5c6d7e8f90')
    if ($null -eq $FromCapture) { $FromCapture = $Dry }""", """        $WipeFacts = $wipeFactsOk, [string]$WipeName = 'newadmin', $FixFacts = $p96Facts, [string]$PickedCommit = '61db33c0a1b2c3d4e5f60718293a4b5c6d7e8f90',
        [string]$VdFile, [string]$Body, [string]$HuesFile)
    if ($null -eq $FromCapture) { $FromCapture = $Dry }
    # cc-P135: Check a .vd and Compare a hues.mul need a file to open a window; the facts' throwaway ones unless given.
    if ($ActionKey -eq 'art.checkvd' -and -not $PSBoundParameters.ContainsKey('VdFile')) { $VdFile = $p135Vd }
    if ($ActionKey -eq 'art.hues' -and -not $PSBoundParameters.ContainsKey('HuesFile')) { $HuesFile = $p135Hues }""", label='click capture params')
    t = edit(t, """    try { Invoke-ConsoleButton -ActionKey $ActionKey -ShardKey $ShardKey -SnapshotName $sn -Snapshot $s -CommitMessage $CommitMessage -PackageNotes $PackageNotes -PackageZip $PackageZip -ImageTag $ImageTag -CommitForce:$CommitForce }""",
             """    try { Invoke-ConsoleButton -ActionKey $ActionKey -ShardKey $ShardKey -SnapshotName $sn -Snapshot $s -CommitMessage $CommitMessage -PackageNotes $PackageNotes -PackageZip $PackageZip -ImageTag $ImageTag -CommitForce:$CommitForce -VdFile $VdFile -Body $Body -HuesFile $HuesFile }""", label='click capture call')
    # the throwaway files, defined before the click harness (which the window cases call at load)
    t = edit(t, """function Invoke-ClickCapture {""", P135_FILES + """function Invoke-ClickCapture {""", label='p135 files')
    t = edit(t, """Remove-Item -LiteralPath $shimDir -Recurse -Force -ErrorAction SilentlyContinue

$failed =@($results""", P135_FACTS + """Remove-Item -LiteralPath $shimDir -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath $p135Dir -Recurse -Force -ErrorAction SilentlyContinue

$failed =@($results""", label='facts')
    t.encode('ascii')
    open(TESTS, 'w', encoding='ascii', newline='').write(t)
    print('patched')


MAPART_FUNCS = r"""# --- cc-P135: the Map and Art tab --------------------------------------------------------------------------------
# Four buttons run scripts\validate-art.py (cc-P134) and show its output: the registry check, the body table, a .vd
# check (or a proposal when no body is given) and a hues diff against our own hues.mul. The script reads the client data
# and the art registry and writes nothing; render, its one subcommand that writes PNGs, is never run from here
# (Test-PlanSafety refuses it). Six more print the syntax of the in-game map commands
# (server/customizations/StaffHub/ClusterFMapCheckCommands.cs), which the console cannot run: they are typed in a client,
# as the World setup tab's are. Nothing here reads docker or touches a shard.

function Get-MapCommandSyntax {
    # The six in-game commands: usage and what each says. Kept in step with ClusterFMapCheckCommands.cs by hand; a fact
    # checks each name against that source.
    @(
        [pscustomobject]@{ Key = 'map.footprint'; Command = 'CheckFootprint';     Usage = '[CheckFootprint <width> <height> [maxZSpread=5]'; Then = 'then target the top-left corner'; What = 'CAN or CANNOT a w x h building stand there: the blocked tiles (water, impassable land, an impassable non-surface static within 16 Z) and the land Z spread. Max 64x64.' }
        [pscustomobject]@{ Key = 'map.spots';     Command = 'ValidateSpots';      Usage = '[ValidateSpots <file under Data> [map]';              Then = 'no target';                        What = 'Names each bad spot in a spawn .json, a decoration .cfg (give the map, or Britannia for both) or x,y[,z][,map] lines; at most 500 a file. The full report goes to the map-checks folder beside the saves.' }
        [pscustomobject]@{ Key = 'map.statics';   Command = 'FindStaticProblems'; Usage = '[FindStaticProblems';                                Then = 'then target two corners (max 512x512)'; What = 'Duplicate statics (the same id and Z on a tile), statics buried 10 or more Z under the land, and ids with no tiledata entry.' }
        [pscustomobject]@{ Key = 'map.walkable';  Command = 'Walkable';           Usage = '[Walkable [list|overlay [seconds]|clear]';            Then = 'then target two corners (max 512x512)'; What = 'The tiles a mobile cannot stand on, by cause. overlay marks each with a red rune that deletes itself (default 60 s, max 600; test shard only); clear removes every marker now.' }
        [pscustomobject]@{ Key = 'map.shore';     Command = 'ShoreCheck';         Usage = '[ShoreCheck [stepThreshold]';                         Then = 'then target two corners (max 512x512)'; What = 'Water touching non-water land: coast heights in buckets, the water and shore tile ids, and any water surface outside -120..120.' }
        [pscustomobject]@{ Key = 'map.export';    Command = 'ExportPoints';       Usage = '[ExportPoints <name> [rect|point|clear]';             Then = 'rect: two corners; point: one spot at a time'; What = 'Writes the rectangle (spawnBounds and its centre) or the points as spawn-file JSON to <world folder>\map-checks\<name>.json. [ValidateSpots <name>.json reads it back.' }
    )
}

function Get-MapArtPlan {
    param([string]$Action, $Config, [string]$VdFile, [string]$Body, [string]$HuesFile)
    $steps = New-Object 'System.Collections.Generic.List[object]'
    if ($Action -like 'map.*') {
        $c = @(Get-MapCommandSyntax | Where-Object { $_.Key -eq $Action })[0]
        if (-not $c) { $steps.Add((New-PlanStep -Kind refuse -Text ("Unknown action '" + $Action + "'. -Action list shows them."))); return $steps.ToArray() }
        $steps.Add((New-PlanStep -Kind say -Text ($c.Usage + '   (GameMaster; ' + $c.Then + ')')))
        $steps.Add((New-PlanStep -Kind say -Text $c.What))
        $steps.Add((New-PlanStep -Kind say -Text 'Type it in a client on the shard you mean; the console cannot run in-game commands. It reads and reports, and nothing it places outlives its timer.'))
        return $steps.ToArray()
    }
    $py = $Config.Python
    $va = $Config.ValidateArt
    if (-not (Test-Path -LiteralPath $va -PathType Leaf)) { $steps.Add((New-PlanStep -Kind refuse -Text ('scripts\validate-art.py is not there: ' + $va))); return $steps.ToArray() }
    $note = 'validate-art.py reads the client data and the art registry and writes nothing. Exit 1 means it found problems to read above, not that it failed.'
    $report = [ordered]@{ ReportExit = 1 }
    switch ($Action) {
        'art.registry' {
            $steps.Add((New-PlanStep -Kind say -Text 'Check the art registry: rows registered twice, art ids with EA art in the slot, anim rows mobtypes names or records.json does not route, body rows with no mobtypes entry.'))
            $steps.Add((New-PlanStep -Kind exec -Exe $py -Arguments @($va, 'check-registry') -Text $note -Named $report))
        }
        'art.bodies' {
            $steps.Add((New-PlanStep -Kind say -Text 'The body table: every body the client data names or draws (about 1,300 lines): type, flags, classic or UOP, file, slot, layout, the actions it has frames for, and which line defines it. Copy from the pane, or read the run file in scripts\shard-console-output.'))
            $steps.Add((New-PlanStep -Kind exec -Exe $py -Arguments @($va, 'bodies') -Text $note -Named $report))
        }
        'art.checkvd' {
            if (-not $VdFile) { $steps.Add((New-PlanStep -Kind refuse -Text 'Pick a .vd file first (Browse, or type its path).')); break }
            if ($VdFile -notmatch '(?i)\.vd$' -or -not (Test-Path -LiteralPath $VdFile -PathType Leaf)) { $steps.Add((New-PlanStep -Kind refuse -Text ('Not a .vd file that exists: ' + $VdFile))); break }
            if ($Body) {
                if ($Body -notmatch '^\d{1,5}$') { $steps.Add((New-PlanStep -Kind refuse -Text ('The body is a number in decimal, e.g. 2052: ' + $Body))); break }
                $steps.Add((New-PlanStep -Kind say -Text ('Check ' + (Split-Path -Leaf $VdFile) + ' against body ' + $Body + ': its layout and actions, whether the body is free, where it lands, whether the layout fits, and what mobtypes must say.')))
                $steps.Add((New-PlanStep -Kind exec -Exe $py -Arguments @($va, 'check-vd', $VdFile, $Body) -Text $note -Named $report))
            } else {
                $steps.Add((New-PlanStep -Kind say -Text ('No body given, so propose one: a free server body (from 0x800) and a free anim7 slot of the right layout for ' + (Split-Path -Leaf $VdFile) + ', then the check on it. Registers nothing.')))
                $steps.Add((New-PlanStep -Kind exec -Exe $py -Arguments @($va, 'propose', $VdFile) -Text $note -Named $report))
            }
        }
        'art.hues' {
            if (-not $HuesFile) { $steps.Add((New-PlanStep -Kind refuse -Text 'Pick the other hues.mul first (Browse, or type its path).')); break }
            if ($HuesFile -notmatch '(?i)\.mul$' -or -not (Test-Path -LiteralPath $HuesFile -PathType Leaf)) { $steps.Add((New-PlanStep -Kind refuse -Text ('Not a .mul file that exists: ' + $HuesFile))); break }
            if (-not (Test-Path -LiteralPath $Config.OurHues -PathType Leaf)) { $steps.Add((New-PlanStep -Kind refuse -Text ('Our own hues.mul is not there: ' + $Config.OurHues))); break }
            if ([IO.Path]::GetFullPath($HuesFile) -ieq [IO.Path]::GetFullPath($Config.OurHues)) { $steps.Add((New-PlanStep -Kind refuse -Text 'That is our own hues.mul; pick the other one.')); break }
            $steps.Add((New-PlanStep -Kind say -Text ('Compare ' + $HuesFile + ' with ours (' + $Config.OurHues + '): the hues whose colours differ, and those that differ only in name or table range. Report only; neither file is changed.')))
            $steps.Add((New-PlanStep -Kind exec -Exe $py -Arguments @($va, 'hues-diff', $Config.OurHues, $HuesFile) -Text $note -Named $report))
        }
        default { $steps.Add((New-PlanStep -Kind refuse -Text ("Unknown action '" + $Action + "'. -Action list shows them."))) }
    }
    $steps.ToArray()
}

"""

TOOLTIPS = r"""        # cc-P135: the Map and Art tab.
        'art.registry'     = 'Runs the art registry check of validate-art: rows that collide, art ids with EA art in the slot, anim and body rows the client would misread. Reads only.'
        'art.bodies'       = 'Runs the body table of validate-art: every body the client data names or draws, with its type, file, slot, layout and actions. About 1,300 lines; reads only.'
        'art.checkvd'      = 'Checks the animation file (.vd) against the body given, or proposes a free body and anim7 slot when the body box is empty. Registers nothing.'
        'art.hues'         = 'Compares the hues file given with our own: the hues whose colours differ, and those that differ only in name. Changes neither file.'
        'art.vdfile'       = 'The animation file (.vd) to check or to find a body for; Browse picks one.'
        'art.browsevd'     = 'Picks an animation file (.vd).'
        'art.body'         = 'The body number to check the file against, in decimal (2052); empty proposes a free one.'
        'art.huesfile'     = 'The other hues file (hues.mul), compared against ours in client-data; Browse picks one.'
        'art.browsehues'   = 'Picks a hues file (hues.mul).'
        'map.footprint'    = 'Prints the syntax of [CheckFootprint: can a building footprint stand where you target. Typed in a client; the console only prints it.'
        'map.spots'        = 'Prints the syntax of [ValidateSpots: every spot in a spawn, decoration or x,y file checked, the bad ones named. Typed in a client.'
        'map.statics'      = 'Prints the syntax of [FindStaticProblems: duplicate, buried and unknown map statics in a box. Typed in a client.'
        'map.walkable'     = 'Prints the syntax of [Walkable: blocked tiles in a box, listed or marked with runes that delete themselves (test shard). Typed in a client.'
        'map.shore'        = 'Prints the syntax of [ShoreCheck: water touching land in a box, with coast heights. Typed in a client.'
        'map.export'       = 'Prints the syntax of [ExportPoints: a targeted rectangle or points written as spawn-file JSON. Typed in a client.'
"""

PAGE = r"""
    # cc-P135: Map and Art. The art checks run validate-art.py and show its output in the Action output pane (or a
    # window); the map buttons print an in-game command's syntax. The boxes feed Check a .vd and Compare a hues.mul.
    $artPage = New-Object Windows.Forms.TabPage('Map and Art')
    $artFlow = New-Object Windows.Forms.FlowLayoutPanel
    $artFlow.Dock = 'Fill'
    $artFlow.AutoScroll = $true
    $artFlow.FlowDirection = 'LeftToRight'
    $artFlow.WrapContents = $true
    $artCap = New-Caption ('ART CHECKS run scripts\validate-art.py (read only) and show its output in the Action output pane. Check the art registry and Body table need nothing. Check a .vd takes the file below and a body number (empty: a free body and anim7 slot are proposed). Compare a hues.mul takes the other hues.mul and compares it with ' + $Config.OurHues + '. Exit 1 in the pane means it found problems to read, not that it failed. MAP COMMANDS print the syntax of the six in-game map checks (GameMaster), which are typed in a client: the console cannot run them.') 1100
    $artFlow.Controls.Add($artCap)
    $artFlow.SetFlowBreak($artCap, $true)
    $vdBox = New-Object Windows.Forms.TextBox
    $vdBox.Name = 'art.vdfile'
    $vdBox.Width = 520
    $vdBox.Margin = New-Object Windows.Forms.Padding(6, 12, 6, 6)
    $vdBrowse = New-Object Windows.Forms.Button
    $vdBrowse.Text = 'Browse .vd'
    $vdBrowse.Name = 'art.browsevd'
    $vdBrowse.Width = 110
    $vdBrowse.Height = 28
    $vdBrowse.Margin = New-Object Windows.Forms.Padding(6, 10, 6, 6)
    $vdBrowse.Add_Click({ $f = Show-FilePicker 'Animation file (*.vd)|*.vd|All files (*.*)|*.*' 'Pick a .vd file'; if ($f) { $script:ui.VdFileBox.Text = $f } })
    $bodyLabel = New-Caption 'body' 60
    $bodyLabel.Margin = New-Object Windows.Forms.Padding(6, 16, 0, 6)
    $bodyBox = New-Object Windows.Forms.TextBox
    $bodyBox.Name = 'art.body'
    $bodyBox.Width = 70
    $bodyBox.Margin = New-Object Windows.Forms.Padding(6, 12, 6, 6)
    $artFlow.Controls.AddRange(@($vdBox, $vdBrowse, $bodyLabel, $bodyBox))
    $artFlow.SetFlowBreak($bodyBox, $true)
    $huesBox = New-Object Windows.Forms.TextBox
    $huesBox.Name = 'art.huesfile'
    $huesBox.Width = 520
    $huesBox.Margin = New-Object Windows.Forms.Padding(6, 12, 6, 6)
    $huesBrowse = New-Object Windows.Forms.Button
    $huesBrowse.Text = 'Browse hues.mul'
    $huesBrowse.Name = 'art.browsehues'
    $huesBrowse.Width = 130
    $huesBrowse.Height = 28
    $huesBrowse.Margin = New-Object Windows.Forms.Padding(6, 10, 6, 6)
    $huesBrowse.Add_Click({ $f = Show-FilePicker 'Hues file (*.mul)|*.mul|All files (*.*)|*.*' 'Pick the other hues.mul'; if ($f) { $script:ui.HuesFileBox.Text = $f } })
    $artFlow.Controls.AddRange(@($huesBox, $huesBrowse))
    $artFlow.SetFlowBreak($huesBrowse, $true)
    $artBtns = @()
    foreach ($a in @(Get-ConsoleActions | Where-Object { $_.Group -eq 'Map and Art' })) {
        $b = New-MapArtButton $a.Label $a.Key 230
        $artBtns += $b
        $artFlow.Controls.Add($b)
    }
    $artFlow.SetFlowBreak($artBtns[-1], $true)
    $mapHead = New-Caption 'MAP COMMANDS (in-game, GameMaster): each button prints the syntax and what the command says.' 1100 ([Drawing.Color]::DimGray)
    $artFlow.Controls.Add($mapHead)
    $artFlow.SetFlowBreak($mapHead, $true)
    foreach ($a in @(Get-ConsoleActions | Where-Object { $_.Group -eq 'Map commands' })) {
        $b = New-ConsoleButton $a.Label $a.Key 170
        $artBtns += $b
        $artFlow.Controls.Add($b)
    }
    $artPage.Controls.Add($artFlow)
    $script:ui.MapArtPage = $artPage
    $script:ui.MapArtButtons = $artBtns
    $script:ui.VdFileBox = $vdBox
    $script:ui.BodyBox = $bodyBox
    $script:ui.HuesFileBox = $huesBox
"""

HELPERS = r"""function Get-MapArtInputs {
    # cc-P135: the Map and Art tab's boxes, as a click hands them over.
    $r = @{ VdFile = ''; Body = ''; HuesFile = '' }
    if ($script:ui.VdFileBox) { $r.VdFile = ([string]$script:ui.VdFileBox.Text).Trim() }
    if ($script:ui.BodyBox) { $r.Body = ([string]$script:ui.BodyBox.Text).Trim() }
    if ($script:ui.HuesFileBox) { $r.HuesFile = ([string]$script:ui.HuesFileBox.Text).Trim() }
    $r
}

function New-MapArtButton {
    # cc-P135: a Map and Art button: as New-ConsoleButton, but it hands over the .vd, body and hues.mul boxes.
    param([string]$Text, [string]$ActionKey, [int]$Width = 230)
    $b = New-Object Windows.Forms.Button
    $b.Text = $Text
    $b.Tag = $ActionKey
    $b.Width = $Width
    $b.Height = 36
    $b.Margin = New-Object Windows.Forms.Padding(6)
    $b.Add_Click({ $i = Get-MapArtInputs; Invoke-ConsoleButton -ActionKey $this.Tag -VdFile $i.VdFile -Body $i.Body -HuesFile $i.HuesFile })
    $b
}

function Show-FilePicker {
    # cc-P135: one existing file, picked in the standard dialog; its path, or $null on Cancel.
    param([string]$Filter, [string]$Title)
    $d = New-Object Windows.Forms.OpenFileDialog
    $d.Filter = $Filter
    $d.Title = $Title
    $d.CheckFileExists = $true
    $d.Multiselect = $false
    if ($d.ShowDialog() -eq [Windows.Forms.DialogResult]::OK) { return $d.FileName }
    $null
}

"""

P135_FILES = r"""# cc-P135: throwaway files for the Map and Art plans: a .vd with a valid header and empty records (int16 6, int16 layout
# 0, 110 records of -1), and a few bytes named hues.mul. The plans check the name and that the file is there; nothing
# here runs validate-art on them.
$p135Dir = Join-Path ([IO.Path]::GetTempPath()) ('sl-console-p135-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $p135Dir -Force | Out-Null
$p135Vd = Join-Path $p135Dir 'Sample.vd'
$p135VdBytes = New-Object byte[] (4 + 110 * 12)
$p135VdBytes[0] = 6
for ($i = 4; $i -lt $p135VdBytes.Length; $i++) { $p135VdBytes[$i] = 0xFF }
[IO.File]::WriteAllBytes($p135Vd, $p135VdBytes)
$p135Hues = Join-Path $p135Dir 'hues.mul'
[IO.File]::WriteAllBytes($p135Hues, (New-Object byte[] 64))

"""

P135_FACTS = r"""# --- cc-P135: the Map and Art tab. validate-art.py's checks from the console, read only; the in-game map commands' syntax ---

Write-Host "cc-P135 Map and Art facts" -ForegroundColor Cyan

function Get-MapArtActionPlan { param([string]$Action, [string]$VdFile, [string]$Body, [string]$HuesFile) @(Get-ActionPlan -Action $Action -ShardKey 'mapart' -Config $config -State $state -Now $now -VdFile $VdFile -Body $Body -HuesFile $HuesFile) }

Fact 'P135_TheFourArtChecksRunOnlyValidateArtReadOnlyAndReportExitOne' {
    $va = $config.ValidateArt
    Assert-True (Test-Path -LiteralPath $va) $va
    $want = @{ 'art.registry' = @('check-registry'); 'art.bodies' = @('bodies') }
    foreach ($k in $want.Keys) {
        $p = Get-MapArtActionPlan $k
        $ex = @($p | Where-Object { $_.Kind -eq 'exec' })
        Assert-Equal 1 $ex.Count ($k + ': one exec step')
        Assert-Equal $config.Python $ex[0].Exe $k
        Assert-Equal ($va + ' ' + ($want[$k] -join ' ')) ($ex[0].Arguments -join ' ') $k
        Assert-Equal 1 $ex[0].Named['ReportExit'] ($k + ': exit 1 is problems found, not a failure')
        Assert-Equal 0 @($p | Where-Object { $_.Kind -in @('confirm', 'ask', 'window', 'script', 'copy', 'move', 'remove-snapshot', 'log') }).Count ($k + ': reads only, confirms nothing, logs nothing')
        Assert-Equal 0 @(Test-PlanSafety $p $config).Count ($k + ': ' + (@(Test-PlanSafety $p $config) -join '; '))
    }
    $p = Get-MapArtActionPlan 'art.checkvd' -VdFile $p135Vd -Body '2052'
    $ex = @($p | Where-Object { $_.Kind -eq 'exec' })[0]
    Assert-Equal ($va + ' check-vd ' + $p135Vd + ' 2052') ($ex.Arguments -join ' ') 'a body: check-vd on the file and body'
    $p = Get-MapArtActionPlan 'art.checkvd' -VdFile $p135Vd
    $ex = @($p | Where-Object { $_.Kind -eq 'exec' })[0]
    Assert-Equal ($va + ' propose ' + $p135Vd) ($ex.Arguments -join ' ') 'no body: propose one'
    Assert-True ((@($p | Where-Object { $_.Kind -eq 'say' })[0]).Text -match 'propose one') 'and the plan says so'
    $p = Get-MapArtActionPlan 'art.hues' -HuesFile $p135Hues
    $ex = @($p | Where-Object { $_.Kind -eq 'exec' })[0]
    Assert-Equal ($va + ' hues-diff ' + $config.OurHues + ' ' + $p135Hues) ($ex.Arguments -join ' ') 'ours first, theirs second'
    foreach ($k in 'art.checkvd', 'art.hues') { Assert-Equal 0 @(Test-PlanSafety (Get-MapArtActionPlan $k -VdFile $p135Vd -HuesFile $p135Hues) $config).Count $k }
}

Fact 'P135_CheckVdAndHuesRefuseAMissingWrongOrOwnFileAndANonNumericBody' {
    $refuse = { param($p) @($p | Where-Object { $_.Kind -eq 'refuse' }) }
    Assert-True ((& $refuse (Get-MapArtActionPlan 'art.checkvd'))[0].Text -match 'Pick a \.vd file first') 'no file'
    Assert-True ((& $refuse (Get-MapArtActionPlan 'art.checkvd' -VdFile (Join-Path $p135Dir 'missing.vd')))[0].Text -match 'Not a \.vd file that exists') 'a missing file'
    Assert-True ((& $refuse (Get-MapArtActionPlan 'art.checkvd' -VdFile $p135Hues))[0].Text -match 'Not a \.vd file') 'the wrong kind of file'
    Assert-True ((& $refuse (Get-MapArtActionPlan 'art.checkvd' -VdFile $p135Vd -Body '0x804'))[0].Text -match 'number in decimal') 'hex is refused'
    Assert-True ((& $refuse (Get-MapArtActionPlan 'art.checkvd' -VdFile $p135Vd -Body 'kirin'))[0].Text -match 'number in decimal') 'a word is refused'
    Assert-True ((& $refuse (Get-MapArtActionPlan 'art.hues'))[0].Text -match 'Pick the other hues\.mul first') 'no hues file'
    Assert-True ((& $refuse (Get-MapArtActionPlan 'art.hues' -HuesFile $p135Vd))[0].Text -match 'Not a \.mul file') 'a .vd is not a hues file'
    if (Test-Path -LiteralPath $config.OurHues) { Assert-True ((& $refuse (Get-MapArtActionPlan 'art.hues' -HuesFile $config.OurHues))[0].Text -match 'our own hues\.mul') 'ours against ours is refused' }
    foreach ($p in @((Get-MapArtActionPlan 'art.checkvd'), (Get-MapArtActionPlan 'art.hues'), (Get-MapArtActionPlan 'art.checkvd' -VdFile $p135Vd -Body 'kirin'))) {
        Assert-Equal 0 @($p | Where-Object { $_.Kind -eq 'exec' }).Count 'a refused plan runs nothing'
    }
}

Fact 'P135_TheSafetyCheckRefusesPythonOutsideValidateArtAndRenderOrAnyOtherSubcommand' {
    $va = $config.ValidateArt
    $bad = @(
        @{ Why = 'render writes PNGs';        Step = (New-PlanStep -Kind exec -Exe 'python' -Arguments @($va, 'render', '132', '0', '2', '--out', 'D:\x')) },
        @{ Why = 'another script';            Step = (New-PlanStep -Kind exec -Exe 'python' -Arguments @((Join-Path $repo 'scripts\find-free-art.py'), 'bodies')) },
        @{ Why = 'python with -c';            Step = (New-PlanStep -Kind exec -Exe 'python' -Arguments @('-c', 'print(1)')) },
        @{ Why = 'python3.exe too';           Step = (New-PlanStep -Kind exec -Exe 'C:\Python\python3.exe' -Arguments @('-m', 'http.server')) },
        @{ Why = 'validate-art in a window';  Step = (New-PlanStep -Kind window -Exe 'python' -Arguments @($va, 'bodies')) },
        @{ Why = 'validate-art through cmd';  Step = (New-PlanStep -Kind exec -Exe 'cmd.exe' -Arguments @('/c', 'python', $va, 'bodies')) },
        @{ Why = 'a subcommand not listed';   Step = (New-PlanStep -Kind exec -Exe 'python' -Arguments @($va, 'actions', '132')) },
        @{ Why = 'propose with --out';        Step = (New-PlanStep -Kind exec -Exe 'python' -Arguments @($va, 'propose', $p135Vd, '--out', 'D:\x')) }
    )
    foreach ($b in $bad) {
        $v = @(Test-PlanSafety @($b.Step) $config)
        Assert-True ($v.Count -ge 1 -and ($v -join ' ') -match 'python runs here only as') ($b.Why + ': ' + ($v -join '; '))
    }
    foreach ($sub in $config.ArtSubcommands) {
        $args = @($va, $sub)
        if ($sub -in @('check-vd', 'propose')) { $args += $p135Vd }
        if ($sub -eq 'check-vd') { $args += '2052' }
        if ($sub -eq 'hues-diff') { $args += @($config.OurHues, $p135Hues) }
        Assert-Equal 0 @(Test-PlanSafety @((New-PlanStep -Kind exec -Exe 'python' -Arguments $args)) $config).Count ($sub + ' is allowed')
    }
    Assert-Equal 'bodies,check-registry,check-vd,propose,hues-diff' ($config.ArtSubcommands -join ',') 'and render is not among them'
}

Fact 'P135_EveryMapButtonPrintsItsCommandsSyntaxAndRunsNothing' {
    $src = [IO.File]::ReadAllText((Join-Path $repo 'server\customizations\StaffHub\ClusterFMapCheckCommands.cs'))
    $keys = @(Get-ConsoleActions | Where-Object { $_.Group -eq 'Map commands' } | ForEach-Object { $_.Key })
    Assert-Equal 'map.footprint,map.spots,map.statics,map.walkable,map.shore,map.export' ($keys -join ',')
    foreach ($c in Get-MapCommandSyntax) {
        Assert-True ($keys -contains $c.Key) ($c.Key + ' is a button')
        Assert-True ($src -match ('CommandSystem\.Register\("' + [regex]::Escape($c.Command) + '", AccessLevel\.GameMaster')) ($c.Command + ' is registered GameMaster in ClusterFMapCheckCommands.cs')
        Assert-True ($src -match ('\[Usage\("' + [regex]::Escape($c.Usage.Substring(1)) + '"\)')) ($c.Command + ': the usage printed is the one the command declares: ' + $c.Usage)
        $p = Get-MapArtActionPlan $c.Key
        Assert-Equal 'say,say,say' (@($p | ForEach-Object { $_.Kind }) -join ',') ($c.Key + ' only says')
        Assert-True ($p[0].Text.StartsWith($c.Usage)) ($c.Key + ': ' + $p[0].Text)
        Assert-True ($p[2].Text -match 'the console cannot run in-game commands') $c.Key
        Assert-Equal 0 @(Test-PlanSafety $p $config).Count $c.Key
        $r = Invoke-ClickCapture $c.Key 'mapart' $false
        Assert-Equal 0 $r.Spawned.Count ($c.Key + ' opens no window')
        Assert-Equal 1 $r.Executed.Count ($c.Key + ' prints here')
    }
    Assert-Equal 6 @(Get-MapCommandSyntax).Count
}

Fact 'P135_TheChildLineCarriesTheVdFileBodyAndHuesFileAndOnlyDigitsForTheBody' {
    $l = Get-ChildArgumentLine -SelfPath 'C:\x\Shard-Console.ps1' -ActionKey 'art.checkvd' -ShardKey 'mapart' -VdFile 'D:\art\my kirin.vd' -Body '2052'
    Assert-True ($l -match '-Mode Execute -Action art\.checkvd ') $l
    Assert-True ($l -match ' -VdFile "D:\\art\\my kirin\.vd"') $l
    Assert-True ($l -match ' -Body 2052') $l
    Assert-True ($l -notmatch '-Shard ') 'no shard'
    $l2 = Get-ChildArgumentLine -SelfPath 'C:\x\Shard-Console.ps1' -ActionKey 'art.checkvd' -ShardKey 'mapart' -VdFile 'D:\a".vd' -Body '0x804'
    Assert-True ($l2 -match ' -VdFile "D:\\a\.vd"') ('a quote is dropped: ' + $l2)
    Assert-True ($l2 -notmatch '-Body') ('a body that is not digits does not cross: ' + $l2)
    $l3 = Get-ChildArgumentLine -SelfPath 'C:\x\Shard-Console.ps1' -ActionKey 'art.hues' -ShardKey 'mapart' -HuesFile 'E:\other\hues.mul' -DryRun
    Assert-True ($l3 -match '-Mode DryRun -Action art\.hues ' -and $l3 -match ' -HuesFile "E:\\other\\hues\.mul"') $l3
    # And a click hands the boxes over: dry, one window, with the file and body.
    $r = Invoke-ClickCapture 'art.checkvd' 'mapart' $true -VdFile $p135Vd -Body '2052'
    Assert-Equal 1 $r.Spawned.Count 'one window'
    Assert-True ($r.Spawned[0] -match (' -VdFile "' + [regex]::Escape($p135Vd) + '" -Body 2052')) $r.Spawned[0]
    Assert-True ($r.Spawned[0] -match '-Mode DryRun -Action art\.checkvd') $r.Spawned[0]
    $r = Invoke-ClickCapture 'art.hues' 'mapart' $true -HuesFile $p135Hues
    Assert-True ($r.Spawned[0] -match (' -HuesFile "' + [regex]::Escape($p135Hues) + '"')) $r.Spawned[0]
    $r = Invoke-ClickCapture 'art.checkvd' 'mapart' $true -VdFile ''
    Assert-Equal 0 $r.Spawned.Count 'no file, no window'
    Assert-True (@($r.Lines | Where-Object { $_ -match 'Pick a \.vd file first' }).Count -eq 1) ('and the refusal is said: ' + ($r.Lines -join ' | '))
}

Fact 'P135_AReportedExitCodeIsSaidInAmberAndTheRunIsDoneAnyOtherFails' {
    # A throwaway script that exits as told, as the D38 facts do; never validate-art itself.
    $dir = Join-Path $p135Dir 'exit'
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
    $ps1 = Join-Path $dir 'child.ps1'
    Set-Content -LiteralPath $ps1 -Encoding ASCII -Value @("Write-Output 'p135 found two problems'", 'exit ([int]$args[0])')
    $cfg = Get-ConsoleConfig -RepoRoot $repo
    $cfg.LogFile = Join-Path $dir 'shard-console.log'
    $lines = New-Object 'System.Collections.Generic.List[string]'
    function Write-ConsoleLine { param([string]$Text, [string]$Color) $lines.Add($Color + '|' + $Text) }
    $one = New-PlanStep -Kind exec -Exe 'powershell.exe' -Arguments @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', $ps1, '1') -Text 'exits 1' -Named ([ordered]@{ ReportExit = 1 })
    $two = New-PlanStep -Kind exec -Exe 'powershell.exe' -Arguments @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', $ps1, '2') -Text 'exits 2' -Named ([ordered]@{ ReportExit = 1 })
    $plain = New-PlanStep -Kind exec -Exe 'powershell.exe' -Arguments @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', $ps1, '1') -Text 'exits 1, not reported'
    Assert-Equal $true (Invoke-Plan -Plan @($one) -Config $cfg -ActionKey 'fact' -ShardKey 'mapart') 'the reported exit is done'
    Assert-True (@($lines | Where-Object { $_ -match '^amber\|.*exited with 1: it found something' }).Count -eq 1) ('said in amber: ' + ($lines -join ' | '))
    Assert-True (@($lines | Where-Object { $_ -match 'p135 found two problems' }).Count -ge 1) 'the output is shown'
    $lines.Clear()
    Assert-Equal $false (Invoke-Plan -Plan @($two) -Config $cfg -ActionKey 'fact' -ShardKey 'mapart') 'another exit code fails'
    Assert-True (@($lines | Where-Object { $_ -match 'exited with 2' }).Count -ge 1) ($lines -join ' | ')
    $lines.Clear()
    Assert-Equal $false (Invoke-Plan -Plan @($plain) -Config $cfg -ActionKey 'fact' -ShardKey 'mapart') 'exit 1 with nothing declared fails, as before'
}

Fact 'P135_TheTabIsBuiltWithItsBoxesButtonsAndTooltips' {
    $script:NetProbeDisabled = $true
    $form = New-ConsoleForm -Config $config -DryRun -StatusFrom (Join-Path $fixture 'console-capture-2026-09-29.txt')
    try {
        Assert-Equal 'Map and Art' $script:ui.MapArtPage.Text
        Assert-True ($script:ui.Tabs.TabPages.Contains($script:ui.MapArtPage)) 'in the tab control'
        Assert-Equal ([array]::IndexOf(@($script:ui.Tabs.TabPages | ForEach-Object { $_.Text }), 'World setup') + 1) ([array]::IndexOf(@($script:ui.Tabs.TabPages | ForEach-Object { $_.Text }), 'Map and Art')) 'right after World setup'
        Assert-Equal 'art.registry,art.bodies,art.checkvd,art.hues,map.footprint,map.spots,map.statics,map.walkable,map.shore,map.export' (($script:ui.MapArtButtons | ForEach-Object { $_.Tag }) -join ',')
        Assert-Equal 'Check the art registry,Body table,Check a .vd,Compare a hues.mul with ours,[CheckFootprint,[ValidateSpots,[FindStaticProblems,[Walkable,[ShoreCheck,[ExportPoints' (($script:ui.MapArtButtons | ForEach-Object { $_.Text }) -join ',')
        Assert-Equal 'art.vdfile,art.body,art.huesfile' (@($script:ui.VdFileBox.Name, $script:ui.BodyBox.Name, $script:ui.HuesFileBox.Name) -join ',')
        $script:ui.VdFileBox.Text = ' ' + $p135Vd + ' '
        $script:ui.BodyBox.Text = '2052'
        $script:ui.HuesFileBox.Text = $p135Hues
        $i = Get-MapArtInputs
        Assert-Equal $p135Vd $i.VdFile 'trimmed'
        Assert-Equal '2052' $i.Body
        Assert-Equal $p135Hues $i.HuesFile
        $tips = Get-ConsoleTooltips
        foreach ($k in 'tab.Map and Art', 'art.registry', 'art.bodies', 'art.checkvd', 'art.hues', 'art.vdfile', 'art.browsevd', 'art.body', 'art.huesfile', 'art.browsehues', 'map.footprint', 'map.spots', 'map.statics', 'map.walkable', 'map.shore', 'map.export') { Assert-True ($tips.Contains($k)) ('a tooltip for ' + $k) }
        $browse = @($script:ui.MapArtPage.Controls[0].Controls | Where-Object { $_.Name -in @('art.browsevd', 'art.browsehues') })
        Assert-Equal 2 $browse.Count 'two Browse buttons'
    } finally { $form.Dispose(); $script:NetProbeDisabled = $false }
}

Fact 'P135_EveryMapAndArtButtonRunHeadlessWithDryRunRunsNothing' {
    $cases = @(@('art.registry', @()), @('art.bodies', @()), @('art.checkvd', @('-VdFile', $p135Vd, '-Body', '2052')), @('art.checkvd', @('-VdFile', $p135Vd)), @('art.hues', @('-HuesFile', $p135Hues)), @('map.footprint', @()), @('map.walkable', @()), @('map.export', @()))
    foreach ($c in $cases) {
        $extra = @($c[1])
        $out = (& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Resolve-Path $script).Path -DryRun -Action $c[0] @extra 2>&1 | Out-String)
        Assert-Equal 0 $LASTEXITCODE ($c[0] + ': ' + $out)
        Assert-True ($out -match ('== DRY RUN: ' + [regex]::Escape($c[0]) + ' \(mapart\)')) ($c[0] + ': ' + $out)
        Assert-True ($out -match '\(dry run: nothing was run\)') ($c[0] + ': ' + $out)
        Assert-True ($out -notmatch 'REFUSE') ($c[0] + ': ' + $out)
        if ($c[0] -like 'art.*') { Assert-True ($out -match 'RUN      python ') ($c[0] + ': the RUN line names python: ' + $out) }
    }
    # And without a mode, a read-only action still runs (none of these changes anything); its banner says so.
    $out = (& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Resolve-Path $script).Path -Action map.shore 2>&1 | Out-String)
    Assert-Equal 0 $LASTEXITCODE $out
    Assert-True ($out -match 'MAP AND ART  map\.shore \(map and art\)' -and $out -match '\[ShoreCheck \[stepThreshold\]') $out
}

"""


if __name__ == '__main__':
    main()
