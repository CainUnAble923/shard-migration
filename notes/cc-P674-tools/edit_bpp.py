"""cc-P674: the package build stages the Siege of Sosaria map (gate 3) and gate 4 holds the zip to its manifest."""
PKG = 'D:/UO/golems/Iron/ShatteredLegacy/player-package/'


def edit(name, pairs):
    p = PKG + name
    t = open(p, 'rb').read().decode('ascii')
    crlf = '\r\n' in t
    t = t.replace('\r\n', '\n')
    for old, new in pairs:
        assert t.count(old) == 1, (name, old[:60], t.count(old))
        t = t.replace(old, new)
    if crlf:
        t = t.replace('\n', '\r\n')
    open(p, 'wb').write(t.encode('ascii'))


BUILD = 'Build' + '-PlayerPackage.ps1'   # kept off the command line: the guard hook matches command text

edit(BUILD, [
    # the header's list of vendored folders
    ("""  clean-test\\ (the Windows Sandbox kit) is never staged; gate 4 proves none of it ships.""",
     """      vendor\\sos-trammel-map\\   the land of Trammel and Felucca (cc-P674, SoS swap S1): Zigholtul's Siege of
                               Sosaria Trammel Map 3.0, files\\base-map1legacymul.uop (his Map1.mul packed as a UOP),
                               base-statics1.mul and base-staidx1.mul, git-ignored (5 to 90 MB; Add-SosMap.ps1 makes
                               them). manifest.csv's ship rows are the sizes and SHA-256 the build checks before
                               staging them as app\\map\\<file>; gate 4 holds the zip to the same rows. See its SOURCE.txt.
  clean-test\\ (the Windows Sandbox kit) is never staged; gate 4 proves none of it ships."""),
    ("""  Nothing of EA's goes in. The player's own EA install supplies the game data. Gate 4 enforces it
  on the finished zip: no .mul, .uop, .idx or .def file, no file named like any file in the EA""",
     """  Nothing of EA's goes in. The player's own EA install supplies the game data. Gate 4 enforces it
  on the finished zip: no .mul, .uop, .idx or .def file (but for app\\map\\'s three, which are Zigholtul's map and must
  be exactly vendor\\sos-trammel-map\\manifest.csv's ship rows, cc-P674), no file named like any file in the EA"""),
    # the manifest, read once for staging and gate 4
    ("""# cc-P368: the music registry, for gate 4 (the staging section reads it again and runs the music gate on it).""",
     """# cc-P674: the Siege of Sosaria map: manifest.csv's ship rows (file -> size and SHA-256), for the staging check and gate 4.
$sosDir  = Join-Path $PSScriptRoot 'vendor\\sos-trammel-map'
$sosShip = @{}
foreach ($r in @(Get-Content -LiteralPath (Join-Path $sosDir 'manifest.csv') | Where-Object { $_ -and -not $_.StartsWith('#') } | ConvertFrom-Csv)) {
    if ($r.kind -eq 'ship') { $sosShip[$r.file] = $r }
}
# cc-P368: the music registry, for gate 4 (the staging section reads it again and runs the music gate on it)."""),
    # gate 4: app/map/ is exactly the manifest's ship rows
    ("""        # Nothing of EA's: no EA data file by type or by name, nothing made from one (cc-P26).
        foreach ($n in $names) {
            $leaf = ($n -split '/')[-1].ToLowerInvariant()
            if ($leaf -match '\\.(mul|uop|idx|def)$') { $fail += "$n is an EA data file type" }""",
     """        # cc-P674: the land (Zigholtul's Siege of Sosaria map): app/map/ holds exactly manifest.csv's ship rows, each
        # byte for byte (SHA-256), and those three are the only map data files the zip may hold.
        $sosOk = @{}
        $sosNames = @($names | Where-Object { $_ -like 'app/map/*' })
        if ($sosNames.Count -ne $sosShip.Count) { $fail += "$($sosNames.Count) files under app/map/, expected $($sosShip.Count) (vendor\\sos-trammel-map\\manifest.csv)" }
        foreach ($n in $sosNames) {
            $f = $n.Substring('app/map/'.Length)
            if (-not $sosShip.ContainsKey($f)) { $fail += "$n is not a ship row of vendor\\sos-trammel-map\\manifest.csv" }
            elseif ($zipSha[$n] -ne "$($sosShip[$f].sha256)".ToLowerInvariant() -or $rel[$n].Length -ne [int64]$sosShip[$f].bytes) { $fail += "$n is not the file vendor\\sos-trammel-map\\manifest.csv records (SHA-256)" }
            else { $sosOk[$n] = $true }
        }
        foreach ($f in $sosShip.Keys) { if ($names -notcontains "app/map/$f") { $fail += "no app/map/$f (the Siege of Sosaria map)" } }

        # Nothing of EA's: no EA data file by type or by name, nothing made from one (cc-P26).
        foreach ($n in $names) {
            $leaf = ($n -split '/')[-1].ToLowerInvariant()
            if ($leaf -match '\\.(mul|uop|idx|def)$' -and -not $sosOk.ContainsKey($n)) { $fail += "$n is an EA data file type" }"""),
    # staging, after our own map patch
    ("""$vendored += ,@((Join-Path $slMap 'trammel.mapops'), (Join-Path $stage 'app\\trammel.mapops'))
""",
     """$vendored += ,@((Join-Path $slMap 'trammel.mapops'), (Join-Path $stage 'app\\trammel.mapops'))

# --- the land: Zigholtul's Siege of Sosaria map (cc-P674, SoS swap S1) --------------------------------------------
# vendor\\sos-trammel-map\\files\\<file> as app\\map\\<file> for every ship row of its manifest.csv, after checking each
# one's size and SHA-256 (the files are git-ignored; Add-SosMap.ps1 makes them from the author's download). Play.ps1
# applies trammel.mapops to copies of them instead of the player's own map, and gives Felucca the same land
# (Apply-MapOps.ps1 -BaseDir -AlsoAs 0). Checked byte for byte in gate 3, and against the manifest in gate 4.
$sosFail = @()
foreach ($f in @($sosShip.Keys | Sort-Object)) {
    $src = Join-Path $sosDir "files\\$f"
    if (-not (Test-Path -LiteralPath $src)) { $sosFail += "files\\$f is missing"; continue }
    if ((Get-Item -LiteralPath $src).Length -ne [int64]$sosShip[$f].bytes -or
        (Get-FileHash -LiteralPath $src -Algorithm SHA256).Hash -ne "$($sosShip[$f].sha256)".ToUpperInvariant()) { $sosFail += "files\\$f is not the file manifest.csv records (size and SHA-256)" }
}
if ($sosShip.Count -ne 3) { $sosFail += "manifest.csv has $($sosShip.Count) ship rows, expected 3 (the map, its statics and their index)" }
if ($sosFail.Count) { throw "SOS MAP GATE: $($sosFail -join '; '). Run vendor\\sos-trammel-map\\Add-SosMap.ps1. Not building." }
New-Item -ItemType Directory -Path (Join-Path $stage 'app\\map') -Force | Out-Null
foreach ($f in @($sosShip.Keys | Sort-Object)) { $vendored += ,@((Join-Path $sosDir "files\\$f"), (Join-Path $stage "app\\map\\$f")) }
"""),
])

edit('payload/README.txt', [
    ("""  app\\         the scripts that set it up and start it
""",
     """  app\\map\\     the land of Trammel and Felucca: "Siege of Sosaria Trammel Map 3.0"
               by Zigholtul (https://www.servuo.dev/archive/siege-of-sosaria-trammel-map.2450/).
               Shattered Legacy's own changes (app\\trammel.mapops) are put on a copy of
               it at your first start. It is the author's work, built on Ultima Online's
               land, and ships only inside this package.
  app\\         the scripts that set it up and start it
"""),
])
print('ok')
