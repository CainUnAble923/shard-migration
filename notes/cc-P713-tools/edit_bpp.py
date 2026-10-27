"""cc-P713: put the Siege of Sosaria land in Build-PlayerPackage.ps1 behind one switch (vendor\\sos-trammel-map\\switch.txt).

    python -P edit_bpp.py D:/UO/golems/Iron/ShatteredLegacy

Each replacement must match exactly once, or nothing is written.
"""
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
bpp = root / 'player-package' / 'Build-PlayerPackage.ps1'
text = bpp.read_bytes().decode('ascii')
nl = '\r\n' if '\r\n' in text else '\n'


def sub(old, new):
    global text
    old = old.replace('\n', nl)
    new = new.replace('\n', nl)
    n = text.count(old)
    if n != 1:
        raise SystemExit(f'expected one match, found {n}: {old[:80]!r}')
    text = text.replace(old, new)


# 1. The header: the switch, and how to turn it on for the swap.
sub("""                               staging them as app\\map\\<file>; gate 4 holds the zip to the same rows. See its SOURCE.txt.
""", """                               staging them as app\\map\\<file>; gate 4 holds the zip to the same rows. See its SOURCE.txt.
                               cc-P713: ONLY WHEN SWITCHED ON. vendor\\sos-trammel-map\\switch.txt holds one word, off
                               (the default) or on. Off: no app\\map\\, nothing of files\\ is read or needed, the README's
                               app\\map\\ lines are left out, and Play.ps1 puts app\\trammel.mapops on the player's own
                               stock Trammel, exactly as before cc-P674. Gate 4 then refuses any app\\map\\ file.
                               TO TURN IT ON for the swap's go-live release (and not before: the server must run the
                               SoS land too), change switch.txt's word to on, run vendor\\sos-trammel-map\\Add-SosMap.ps1
                               if files\\ is empty, and build. -SosMap on|off overrides the file for one run (tests,
                               or -CheckZip of a package built the other way); a release build leaves it out.
""")
sub("""on the finished zip: no .mul, .uop, .idx or .def file (but for app\\map\\'s three, which are Zigholtul's map and must
  be exactly vendor\\sos-trammel-map\\manifest.csv's ship rows, cc-P674), no file""",
    """on the finished zip: no .mul, .uop, .idx or .def file (but for app\\map\\'s three, which are Zigholtul's map and must
  be exactly vendor\\sos-trammel-map\\manifest.csv's ship rows, cc-P674, and only with the switch on, cc-P713), no file""")

# 2. The parameter.
sub("""    [string]$ScriptsBase = 'https://get.shatteredlegacyuo.com/scripts/'
)""", """    [string]$ScriptsBase = 'https://get.shatteredlegacyuo.com/scripts/',
    # cc-P713: empty means vendor\\sos-trammel-map\\switch.txt decides (off until the swap goes live). For tests and for
    # -CheckZip of a package built the other way; a release build leaves it out.
    [ValidateSet('', 'on', 'off')][string]$SosMap
)""")

# 3. Reading the switch, beside the manifest.
sub("""    if ($r.kind -eq 'ship') { $sosShip[$r.file] = $r }
}
""", """    if ($r.kind -eq 'ship') { $sosShip[$r.file] = $r }
}
# cc-P713: the switch. switch.txt's one word (off or on; # lines are comments); anything else stops the build, so a
# typo never ships the wrong land. Off: the package carries no app\\map\\ and the player's own stock Trammel is patched.
function Get-SosMapSwitch([string]$path) {
    if (-not (Test-Path -LiteralPath $path)) { throw "SOS MAP SWITCH: $path is missing; it must hold off or on. Not building." }
    $w = @(Get-Content -LiteralPath $path | ForEach-Object { $_.Trim() } | Where-Object { $_ -and -not $_.StartsWith('#') })
    if ($w.Count -ne 1 -or @('on', 'off') -cnotcontains $w[0]) { throw "SOS MAP SWITCH: $path must hold one line, off or on (got: $($w -join ' | ')). Not building." }
    return $w[0]
}
if (-not $SosMap) { $SosMap = Get-SosMapSwitch (Join-Path $sosDir 'switch.txt') }
$sosOn = $SosMap -eq 'on'
""")

# 4. Gate 4: the zip holds the land the switch says.
sub("""        # cc-P674: the land (Zigholtul's Siege of Sosaria map): app/map/ holds exactly manifest.csv's ship rows, each
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
""", """        # cc-P674: the land (Zigholtul's Siege of Sosaria map): app/map/ holds exactly manifest.csv's ship rows, each
        # byte for byte (SHA-256), and those three are the only map data files the zip may hold.
        # cc-P713: only with the switch on. Off, app/map/ holds nothing (no exemption below) and the README does not
        # credit the map; on, the README credits it.
        $sosOk = @{}
        $sosNames = @($names | Where-Object { $_ -like 'app/map/*' })
        $readme = $rel['README.txt']
        $credits = $readme -and ((Read-ZipText $readme) -match 'Siege of Sosaria Trammel Map')
        if ($sosOn) {
            if ($sosNames.Count -ne $sosShip.Count) { $fail += "$($sosNames.Count) files under app/map/, expected $($sosShip.Count) (vendor\\sos-trammel-map\\manifest.csv)" }
            foreach ($n in $sosNames) {
                $f = $n.Substring('app/map/'.Length)
                if (-not $sosShip.ContainsKey($f)) { $fail += "$n is not a ship row of vendor\\sos-trammel-map\\manifest.csv" }
                elseif ($zipSha[$n] -ne "$($sosShip[$f].sha256)".ToLowerInvariant() -or $rel[$n].Length -ne [int64]$sosShip[$f].bytes) { $fail += "$n is not the file vendor\\sos-trammel-map\\manifest.csv records (SHA-256)" }
                else { $sosOk[$n] = $true }
            }
            foreach ($f in $sosShip.Keys) { if ($names -notcontains "app/map/$f") { $fail += "no app/map/$f (the Siege of Sosaria map)" } }
            if (-not $credits) { $fail += 'README.txt does not credit the Siege of Sosaria Trammel Map that app/map/ ships' }
        } else {
            foreach ($n in $sosNames) { $fail += "$n shipped, but the Siege of Sosaria map is switched off (vendor\\sos-trammel-map\\switch.txt)" }
            if ($credits) { $fail += 'README.txt credits the Siege of Sosaria Trammel Map, which is switched off (vendor\\sos-trammel-map\\switch.txt)' }
        }
""")

# 5. Staging: only with the switch on; off, the README's app\map\ lines go.
sub("""$sosFail = @()
foreach ($f in @($sosShip.Keys | Sort-Object)) {
    $src = Join-Path $sosDir "files\$f"
    if (-not (Test-Path -LiteralPath $src)) { $sosFail += "files\$f is missing"; continue }
    if ((Get-Item -LiteralPath $src).Length -ne [int64]$sosShip[$f].bytes -or
        (Get-FileHash -LiteralPath $src -Algorithm SHA256).Hash -ne "$($sosShip[$f].sha256)".ToUpperInvariant()) { $sosFail += "files\$f is not the file manifest.csv records (size and SHA-256)" }
}
if ($sosShip.Count -ne 3) { $sosFail += "manifest.csv has $($sosShip.Count) ship rows, expected 3 (the map, its statics and their index)" }
if ($sosFail.Count) { throw "SOS MAP GATE: $($sosFail -join '; '). Run vendor\sos-trammel-map\Add-SosMap.ps1. Not building." }
New-Item -ItemType Directory -Path (Join-Path $stage 'app\map') -Force | Out-Null
foreach ($f in @($sosShip.Keys | Sort-Object)) { $vendored += ,@((Join-Path $sosDir "files\$f"), (Join-Path $stage "app\map\$f")) }
""", """# cc-P713: only with vendor\sos-trammel-map\switch.txt on. Off, files\ is not read, and the staged README loses its
# app\map\ entry (the line naming the folder and the indented ones under it), so it reads as it did before cc-P674.
if ($sosOn) {
    $sosFail = @()
    foreach ($f in @($sosShip.Keys | Sort-Object)) {
        $src = Join-Path $sosDir "files\$f"
        if (-not (Test-Path -LiteralPath $src)) { $sosFail += "files\$f is missing"; continue }
        if ((Get-Item -LiteralPath $src).Length -ne [int64]$sosShip[$f].bytes -or
            (Get-FileHash -LiteralPath $src -Algorithm SHA256).Hash -ne "$($sosShip[$f].sha256)".ToUpperInvariant()) { $sosFail += "files\$f is not the file manifest.csv records (size and SHA-256)" }
    }
    if ($sosShip.Count -ne 3) { $sosFail += "manifest.csv has $($sosShip.Count) ship rows, expected 3 (the map, its statics and their index)" }
    if ($sosFail.Count) { throw "SOS MAP GATE: $($sosFail -join '; '). Run vendor\sos-trammel-map\Add-SosMap.ps1. Not building." }
    New-Item -ItemType Directory -Path (Join-Path $stage 'app\map') -Force | Out-Null
    foreach ($f in @($sosShip.Keys | Sort-Object)) { $vendored += ,@((Join-Path $sosDir "files\$f"), (Join-Path $stage "app\map\$f")) }
    Write-Host '  land: the Siege of Sosaria map (switched on, vendor\sos-trammel-map\switch.txt)'
} else {
    $rmPath = Join-Path $stage 'README.txt'
    $rmText = [IO.File]::ReadAllText($rmPath)
    $rmRx = [regex]'(?m)^  app\\map\\ [^\r\n]*\r?\n(?: {15}[^\r\n]*\r?\n)*'
    if ($rmRx.Matches($rmText).Count -ne 1) { throw "SOS MAP SWITCH: payload\README.txt has no single app\map\ entry to leave out. Not building." }
    [IO.File]::WriteAllText($rmPath, $rmRx.Replace($rmText, ''), (New-Object Text.ASCIIEncoding))
    Write-Host '  land: stock Trammel and Felucca (the Siege of Sosaria map is switched off, vendor\sos-trammel-map\switch.txt)'
}
""")

bpp.write_bytes(text.encode('ascii'))
print('edited', bpp)
