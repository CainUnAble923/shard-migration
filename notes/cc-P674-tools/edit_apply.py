"""cc-P674: Apply-MapOps.ps1 and Build-UoOverrides.ps1 take a shipped base map (the Siege of Sosaria map) and give
Felucca the same land. Edits by exact replacement (Read is denied on the code copy in unattended runs)."""
APP = 'D:/UO/golems/Iron/ShatteredLegacy/player-package/payload/app/'


def edit(name, pairs):
    p = APP + name
    t = open(p, 'rb').read().decode('ascii')
    crlf = '\r\n' in t
    t = t.replace('\r\n', '\n')
    for old, new in pairs:
        assert t.count(old) == 1, (name, old[:70], t.count(old))
        t = t.replace(old, new)
    if crlf:
        t = t.replace('\n', '\r\n')
    t.encode('ascii')
    open(p, 'wb').write(t.encode('ascii'))


edit('Apply-MapOps.ps1', [
    ("""  Returns the override lines for files-override.txt (lowercase names, as TazUOs UOFilesOverrideMap keys them):""".replace('TazUOs', "TazUO's"),
     """  cc-P674 (the Siege of Sosaria swap, S1): -BaseDir names a folder whose base-<name> files (base-map1legacymul.uop,
  base-statics1.mul, base-staidx1.mul: the shipped app\\map\\) replace the player's own as the map the patch applies to.
  -AlsoAs 0 then also gives Felucca the result: map0LegacyMUL.uop is a copy of the patched map1LegacyMUL.uop with
  each entry's name hash rewritten from build/map1legacymul/ to build/map0legacymul/ (the client finds a UOP's
  entries by those hashes only; the data is the same), and Felucca's statics lines name Trammel's two files, which
  the client opens read-only and shared. The stamp names the base files and the extra facets, so a new base rebuilds.

  Returns the override lines for files-override.txt (lowercase names, as TazUO's UOFilesOverrideMap keys them):"""),
    ("""$MapStampFormat = 'uo-map 1'""",
     """$MapStampFormat = 'uo-map 2'   # cc-P674: 2 names each base file by its full path and adds the facets it is also"""),
    ("""function Get-MapStamp([string]$uoDir, [string[]]$files, [string]$ops) {
    $parts = @($MapStampFormat)
    foreach ($f in $files) {
        $i = Get-Item -LiteralPath (Join-Path $uoDir $f)
        $parts += "$f $($i.Length) $($i.LastWriteTimeUtc.Ticks)"
    }
    $parts += "ops $((Get-FileHash -LiteralPath $ops -Algorithm SHA256).Hash)"
    return ($parts -join "`n")
}
""",
     """function Get-MapStamp([string[]]$paths, [string]$ops, [int[]]$also) {
    $parts = @($MapStampFormat)
    foreach ($p in $paths) {
        $i = Get-Item -LiteralPath $p
        $parts += "$([IO.Path]::GetFullPath($p)) $($i.Length) $($i.LastWriteTimeUtc.Ticks)"
    }
    $parts += "ops $((Get-FileHash -LiteralPath $ops -Algorithm SHA256).Hash)"
    $parts += "also $(@($also) -join ',')"
    return ($parts -join "`n")
}

# cc-P674: the shipped base's name for one of the facet's files (base-map1legacymul.uop and so on). Never an EA name,
# so the package's gate 4 can still refuse any file named like one of EA's.
function Get-MapBaseName([string]$f) { 'base-' + $f.ToLowerInvariant() }

# cc-P674: copies a facet's UOP map to another facet's name: the same bytes, with every entry's name hash
# build/map<From>legacymul/<chunk>.dat rewritten to build/map<To>legacymul/<chunk>.dat. Throws on an entry whose hash
# is none of the From names (a file this was not made for).
function Copy-UopRenamed([string]$Source, [string]$Destination, [int]$From, [int]$To) {
    Copy-Item -LiteralPath $Source -Destination $Destination -Force
    $fs = [IO.File]::Open($Destination, 'Open', 'ReadWrite', 'None')
    try {
        $r = New-Object IO.BinaryReader($fs)
        $w = New-Object IO.BinaryWriter($fs)
        if ($r.ReadUInt32() -ne 0x50594D) { throw "$Source is not a UOP file" }
        $fs.Position = 12
        $next = $r.ReadInt64()
        $rename = @{}; $named = 0; $done = 0
        while ($next -ne 0) {
            $fs.Position = $next
            $count = $r.ReadInt32(); $next = $r.ReadInt64()
            $table = $fs.Position
            for ($i = 0; $i -lt $count; $i++) {
                $fs.Position = $table + $i * 34
                $off = $r.ReadInt64()
                if ($off -eq 0) { continue }
                $fs.Position = $table + $i * 34 + 20
                $h = $r.ReadUInt64()
                while (-not $rename.ContainsKey($h) -and $named -lt 4096) {
                    $rename[(Get-UopNameHash ('build/map{0}legacymul/{1:D8}.dat' -f $From, $named))] = Get-UopNameHash ('build/map{0}legacymul/{1:D8}.dat' -f $To, $named)
                    $named++
                }
                if (-not $rename.ContainsKey($h)) { throw "$Source holds an entry that is not a map$From chunk" }
                $fs.Position = $table + $i * 34 + 20
                $w.Write([uint64]$rename[$h])
                $done++
            }
        }
        $w.Flush()
    } finally { $fs.Close() }
    return $done
}
"""),
    ("""          [string]$ListDir, [switch]$CheckOnly)""",
     """          [string]$ListDir, [switch]$CheckOnly,
          [string]$BaseDir,    # cc-P674: the shipped base map (app\\map\\), in place of the player's own files
          [int[]]$AlsoAs = @())  # cc-P674: the facets that also read the result (0: Felucca on the SoS land)"""),
    ("""    $files = @("map${facet}LegacyMUL.uop", "statics$facet.mul", "staidx$facet.mul")
    foreach ($f in $files) { if (-not (Test-Path -LiteralPath (Join-Path $UoDir $f))) { throw "$f is not in $UoDir" } }
""",
     """    $files = @("map${facet}LegacyMUL.uop", "statics$facet.mul", "staidx$facet.mul")
    $src = @(foreach ($f in $files) { if ($BaseDir) { Join-Path $BaseDir (Get-MapBaseName $f) } else { Join-Path $UoDir $f } })
    for ($i = 0; $i -lt 3; $i++) { if (-not (Test-Path -LiteralPath $src[$i])) { throw "$(Split-Path $src[$i] -Leaf) is not in $(Split-Path $src[$i] -Parent)" } }
    foreach ($a in $AlsoAs) { if ($a -eq $facet -or -not $MapBlocksHigh.ContainsKey($a) -or $MapBlocksHigh[$a] -ne $MapBlocksHigh[$facet]) { throw "facet $a cannot read facet $facet's map" } }
    $alsoFiles = @(foreach ($a in $AlsoAs) { "map${a}LegacyMUL.uop" })
"""),
    ("""    $stamp = Get-MapStamp $UoDir $files $Ops
    $lines = { $o = $(if ($ListDir) { [IO.Path]::GetFullPath($ListDir) } else { (Resolve-Path -LiteralPath $OutDir).Path }); foreach ($f in $files) { "$($f.ToLowerInvariant())=$(Join-Path $o $f)" } }
    if ((Test-Path -LiteralPath $stampOut) -and [IO.File]::ReadAllText($stampOut) -ceq $stamp -and
        @($files | Where-Object { -not (Test-Path -LiteralPath (Join-Path $OutDir $_)) }).Count -eq 0) {""",
     """    $stamp = Get-MapStamp $src $Ops $AlsoAs
    $lines = {
        $o = $(if ($ListDir) { [IO.Path]::GetFullPath($ListDir) } else { (Resolve-Path -LiteralPath $OutDir).Path })
        foreach ($f in $files) { "$($f.ToLowerInvariant())=$(Join-Path $o $f)" }
        foreach ($a in $AlsoAs) {   # cc-P674: Felucca's own map, and Trammel's statics, read by both
            "map${a}legacymul.uop=$(Join-Path $o "map${a}LegacyMUL.uop")"
            "statics$a.mul=$(Join-Path $o $files[1])"
            "staidx$a.mul=$(Join-Path $o $files[2])"
        }
    }
    if ((Test-Path -LiteralPath $stampOut) -and [IO.File]::ReadAllText($stampOut) -ceq $stamp -and
        @($files + $alsoFiles | Where-Object { -not (Test-Path -LiteralPath (Join-Path $OutDir $_)) }).Count -eq 0) {"""),
    ("""    Copy-Item -LiteralPath (Join-Path $UoDir $files[0]) -Destination $mapOut -Force""",
     """    Copy-Item -LiteralPath $src[0] -Destination $mapOut -Force"""),
    ("""    $idx = [IO.File]::ReadAllBytes((Join-Path $UoDir $files[2]))
    $sta = [IO.File]::ReadAllBytes((Join-Path $UoDir $files[1]))""",
     """    $idx = [IO.File]::ReadAllBytes($src[2])
    $sta = [IO.File]::ReadAllBytes($src[1])"""),
    ("""    [IO.File]::WriteAllBytes((Join-Path $OutDir $files[2]), $idx)
    [IO.File]::WriteAllText($stampOut, $stamp, (New-Object Text.ASCIIEncoding))""",
     """    [IO.File]::WriteAllBytes((Join-Path $OutDir $files[2]), $idx)
    foreach ($a in $AlsoAs) {
        & $step "map.copy$a"   # cc-P674: Felucca's copy of the patched land
        $null = Copy-UopRenamed $mapOut (Join-Path $OutDir "map${a}LegacyMUL.uop") $facet $a
    }
    [IO.File]::WriteAllText($stampOut, $stamp, (New-Object Text.ASCIIEncoding))"""),
])

edit('Build-UoOverrides.ps1', [
    ("""    [string]$MapOps,
""", """    [string]$MapOps,
    [string]$MapBase,  # cc-P674: the shipped base map (app\\map, base-<name> files); when there, Felucca reads it too
"""),
    ("""if (-not $MapOps)  { $MapOps  = Join-Path $PSScriptRoot 'trammel.mapops' }
""", """if (-not $MapOps)  { $MapOps  = Join-Path $PSScriptRoot 'trammel.mapops' }
if (-not $MapBase) { $MapBase = Join-Path $PSScriptRoot 'map' }
"""),
    ("""    $r = @(Build-MapOverride -UoDir $UoDir -Ops $MapOps -OutDir $OutDir -ListDir $ListRoot -CheckOnly:$CheckOnly)""",
     """    # cc-P674: with the shipped base (the Siege of Sosaria map) the patch goes on it instead of the player's own files,
    # and Felucca (map 0) gets the same land.
    $base = @{}
    if (Test-Path -LiteralPath (Join-Path $MapBase 'base-map1legacymul.uop')) { $base = @{ BaseDir = $MapBase; AlsoAs = @(0) } }
    $r = @(Build-MapOverride -UoDir $UoDir -Ops $MapOps -OutDir $OutDir -ListDir $ListRoot -CheckOnly:$CheckOnly @base)"""),
])
print('ok')
