# cc-P26: the edits made to player-package/Build-PlayerPackage.ps1, applied as exact replacements.
p = r'D:\ShatteredLegacy\player-package\Build-PlayerPackage.ps1'
s = open(p, encoding='ascii').read()


def rep(old, new):
    global s
    assert s.count(old) == 1, (old, s.count(old))
    s = s.replace(old, new)


rep(r"""      vendor\fiddle-me-this\   Fiddle-Me-This gump art and XML gumps (CC0), see its SOURCE.txt
""", r"""      vendor\fiddle-me-this\   Fiddle-Me-This gump art and XML gumps (CC0), see its SOURCE.txt
      vendor\shattered-legacy-art\   our own art (art\<id>.png, into app\tazuo\ExternalImages\art\)
                               and our tiledata and animdata records (records.json, shipped as
                               app\art-records.json; Play.ps1 writes them into copies of the
                               player's own files). See its SOURCE.txt and registry.csv.
""")
rep(r"""  Nothing of EA's goes in. The player's own EA install supplies the game data.
""", r"""  Nothing of EA's goes in. The player's own EA install supplies the game data. Gate 4 enforces it
  on the finished zip: no .mul, .uop, .idx or .def file, no file named like any file in the EA
  folder (-UoData, the shard's client-data by default), and nothing under app\uo-overrides\,
  which Play.ps1 makes on a player's computer from their own EA files. A payload folder that holds
  app\uo-overrides\ (someone ran Play.ps1 from payload\) stops the build before anything is staged.
""")
rep(r"""  After the zip is written, gate 4 reopens it and checks what actually shipped (the
  Fiddle-Me-This counts and positions, Data\ holding only XmlGumps, no .unblocked). A""",
    r"""  After the zip is written, gate 4 reopens it and checks what actually shipped (the
  Fiddle-Me-This counts and positions, Data\ holding only XmlGumps, no .unblocked, our art
  exactly the registry's IDs, our records, nothing of EA's). A""")
rep(r"""    [string]$Notes
)""", r"""    [string]$Notes,
    [string]$UoData
)""")
rep(r"""$fmtMaxX = 1280; $fmtMaxY = 720
""", r"""$fmtMaxX = 1280; $fmtMaxY = 720
# Our own art (cc-P26). The registry is the count: one PNG per registered ID, exactly.
$slArt      = Join-Path $PSScriptRoot 'vendor\shattered-legacy-art'
$slRegistry = @(Get-Content -LiteralPath (Join-Path $slArt 'registry.csv') | Where-Object { $_ -and -not $_.StartsWith('#') } | ConvertFrom-Csv)
$slIds      = @($slRegistry | ForEach-Object { [int]$_.id })
# The EA files' names, for gate 4. The shard's own copy of the client data by default.
if (-not $UoData) { $UoData = Join-Path (Split-Path $PSScriptRoot -Parent) 'client-data\classic-client' }
if (-not (Test-Path -LiteralPath (Join-Path $UoData 'tiledata.mul'))) { throw "No EA client data in $UoData (-UoData): gate 4 needs its file names to prove none ships." }
$eaNames = @(Get-ChildItem -LiteralPath $UoData -Recurse -File | ForEach-Object { $_.Name.ToLowerInvariant() })
""")
rep(r"""    if (@('', '.', 'app', 'app\tazuo', 'update-backup', 'app\uo-path.txt') -contains $l""",
    r"""    if (@('', '.', 'app', 'app\tazuo', 'update-backup', 'app\uo-path.txt', 'app\uo-overrides') -contains $l""")
rep(r"""        # Data\ holds only XmlGumps\*.xml""", r"""        # Our art: one PNG per registered ID and nothing else, and our records (cc-P26).
        $art = @($names | Where-Object { $_ -like 'app/tazuo/ExternalImages/art/*' })
        if ($art.Count -ne $slIds.Count) { $fail += "$($art.Count) files under app/tazuo/ExternalImages/art/, expected $($slIds.Count) (registry.csv)" }
        foreach ($n in $art) {
            if ($n -notmatch '/(\d+)\.png$' -or $slIds -notcontains [int]$Matches[1]) { $fail += "$n is not a registered art ID" }
        }
        $ar = $rel['app/art-records.json']
        if (-not $ar) { $fail += 'no app/art-records.json' } else {
            try {
                $j = (Read-ZipText $ar) | ConvertFrom-Json
                foreach ($id in @($j.tiledata | ForEach-Object id) + @($j.animdata | ForEach-Object id)) {
                    if ($slIds -notcontains [int]$id) { $fail += "app/art-records.json has a record for $id, which registry.csv does not list" }
                }
            } catch { $fail += "app/art-records.json does not parse: $($_.Exception.Message)" }
        }

        # Nothing of EA's: no EA data file by type or by name, nothing made from one (cc-P26).
        foreach ($n in $names) {
            $leaf = ($n -split '/')[-1].ToLowerInvariant()
            if ($leaf -match '\.(mul|uop|idx|def)$') { $fail += "$n is an EA data file type" }
            elseif ($eaNames -contains $leaf) { $fail += "$n has the name of an EA file" }
            if ($n -like 'app/uo-overrides/*') { $fail += "$n is made on a player's computer and must never ship" }
        }

        # Data\ holds only XmlGumps\*.xml""")
rep(r"""$here    = $PSScriptRoot
$payload = Join-Path $here 'payload'
""", r"""$here    = $PSScriptRoot
$payload = Join-Path $here 'payload'
# Made by Play.ps1 from a computer's own EA files, with that computer's paths in it. Someone ran
# Play.ps1 from payload\: refuse, rather than leave it to gate 4, because it is not ours to ship.
if (Test-Path -LiteralPath (Join-Path $payload 'app\uo-overrides')) { throw "payload\app\uo-overrides\ exists: Play.ps1 was run from payload\. Delete that folder (it holds patched EA files and local paths). Not building." }
""")
rep(r"""foreach ($p in $vendored) { Copy-Item -LiteralPath $p[0] -Destination $p[1] }
""", r"""
# --- our own art (cc-P26) -----------------------------------------------------------------
# art\<id>.png into ExternalImages\art\, exactly the registered IDs, never over a file already
# there; records.json as app\art-records.json. Checked byte for byte in gate 3 with the rest.
$slArtOut = Join-Path $tazOut 'ExternalImages\art'
$slPngs   = @(Get-ChildItem -LiteralPath (Join-Path $slArt 'art') -File)
$extra    = @($slPngs | Where-Object { $_.Name -notmatch '^(\d+)\.png$' -or $slIds -notcontains [int]$Matches[1] } | ForEach-Object Name)
if ($extra.Count) { throw "vendor\shattered-legacy-art\art holds files registry.csv does not list: $($extra -join ', '). Not building." }
if ($slPngs.Count -ne $slIds.Count) { throw "vendor\shattered-legacy-art\art holds $($slPngs.Count) PNGs, registry.csv lists $($slIds.Count). Not building." }
if (Test-Path -LiteralPath $slArtOut) {
    $pre = @(Get-ChildItem -LiteralPath $slArtOut -File | Where-Object { $slPngs.Name -contains $_.Name } | ForEach-Object Name)
    if ($pre.Count) { throw "app\tazuo\ExternalImages\art already held $($pre.Count) of our art files before the copy, first: $($pre[0]). Not building." }
}
New-Item -ItemType Directory -Path $slArtOut -Force | Out-Null
foreach ($f in $slPngs) { $vendored += ,@($f.FullName, (Join-Path $slArtOut $f.Name)) }
$vendored += ,@((Join-Path $slArt 'records.json'), (Join-Path $stage 'app\art-records.json'))
foreach ($p in $vendored) { Copy-Item -LiteralPath $p[0] -Destination $p[1] }
""")
rep(r"""if ($changed.Count) { throw "GATE 3: $($changed.Count) Fiddle-Me-This files differ from vendor\, first: $($changed[0]). Not building." }""",
    r"""if ($changed.Count) { throw "GATE 3: $($changed.Count) vendored files (Fiddle-Me-This, our art) differ from vendor\, first: $($changed[0]). Not building." }""")
open(p, 'w', encoding='ascii', newline='\n').write(s)
print('ok')
