"""cc-P674: PowerShell facts for the shipped base map (Map-Overrides.Tests.ps1, Launch-Overrides.Tests.ps1)."""
T = 'D:/UO/golems/Iron/ShatteredLegacy/player-package/tests/'


def edit(name, pairs):
    p = T + name
    t = open(p, 'rb').read().decode('ascii')
    crlf = '\r\n' in t
    t = t.replace('\r\n', '\n')
    for old, new in pairs:
        assert t.count(old) == 1, (name, old[:60], t.count(old))
        t = t.replace(old, new)
    if crlf:
        t = t.replace('\n', '\r\n')
    open(p, 'wb').write(t.encode('ascii'))


MAP_FACTS = r'''
# cc-P674 (SoS swap S1): a shipped base map (app\map\base-<name>) in place of the player's files, and Felucca's copy.
# Copies a synthetic facet's three files to a folder under the shipped names, with one cell changed so its land differs
# from the "player's" (block 0, cell 0 becomes tile 9 at z 4: the data starts at 74, the block header is 4 bytes).
function New-ShippedBase([string]$facetDir, [string]$dir, [int]$tile = 9) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
    $m = [IO.File]::ReadAllBytes((Join-Path $facetDir 'map1LegacyMUL.uop'))
    [BitConverter]::GetBytes([uint16]$tile).CopyTo($m, 78); $m[80] = 4
    [IO.File]::WriteAllBytes((Join-Path $dir 'base-map1legacymul.uop'), $m)
    Copy-Item (Join-Path $facetDir 'statics1.mul') (Join-Path $dir 'base-statics1.mul')
    Copy-Item (Join-Path $facetDir 'staidx1.mul') (Join-Path $dir 'base-staidx1.mul')
    return $dir
}

Fact 'P674_AShippedBaseIsPatchedInsteadOfThePlayersFilesAndFeluccaGetsTheSameLand' {
    $ea = New-MapFacet (Join-Path $work 'ea7')
    $base = New-ShippedBase (New-MapFacet (Join-Path $work 'sos7')) (Join-Path $work 'app-map7')
    $ops = Join-Path $work 'seven.mapops'
    [IO.File]::WriteAllText($ops, "F 1 0`nL 10 20 581 -3`n", (New-Object Text.ASCIIEncoding))
    $out = Join-Path $work 'out7'
    $lines = @(Build-MapOverride -UoDir $ea -Ops $ops -OutDir $out -BaseDir $base -AlsoAs 0)
    Assert-Equal 6 $lines.Count ($lines -join ' | ')
    Assert-Equal "map0legacymul.uop=$out\map0LegacyMUL.uop" $lines[3]
    Assert-Equal "statics0.mul=$out\statics1.mul" $lines[4] "Felucca reads Trammel's statics"
    Assert-Equal "staidx0.mul=$out\staidx1.mul" $lines[5]
    $m1 = [IO.File]::ReadAllBytes((Join-Path $out 'map1LegacyMUL.uop'))
    Assert-Equal 9 $m1[78] "the base's cell, not the player's tile 3"
    Assert-Equal 4 $m1[80]
    $o = 74 + 514 * 196 + 4 + 34 * 3
    Assert-Equal 69 $m1[$o] 'our patch on the base'
    $m0 = [IO.File]::ReadAllBytes((Join-Path $out 'map0LegacyMUL.uop'))
    Assert-Equal $m1.Length $m0.Length
    $diff = @(for ($i = 0; $i -lt $m1.Length; $i++) { if ($m1[$i] -ne $m0[$i]) { $i } })
    Assert-Equal 8 $diff.Count 'only the one entry name hash differs'
    Assert-Equal 60 $diff[0] 'the hash of the first entry: table at 28, 12-byte head, 20 bytes into the entry'
    Assert-Equal (Get-UopNameHash 'build/map0legacymul/00000000.dat') ([BitConverter]::ToUInt64($m0, 60))
    Assert-True (-not (Test-Path (Join-Path $out 'statics0.mul'))) 'no second statics file is written'
}

Fact 'P674_TheStampNamesTheBaseSoANewBaseRebuildsAndAnUnchangedOneDoesNot' {
    $ea = New-MapFacet (Join-Path $work 'ea8')
    $sos = New-MapFacet (Join-Path $work 'sos8')
    $base = New-ShippedBase $sos (Join-Path $work 'app-map8')
    $ops = Join-Path $work 'eight.mapops'
    [IO.File]::WriteAllText($ops, "F 1 0`nL 1 1 5 0`n", (New-Object Text.ASCIIEncoding))
    $out = Join-Path $work 'out8'
    $null = Build-MapOverride -UoDir $ea -Ops $ops -OutDir $out
    Assert-True (-not (Test-Path (Join-Path $out 'map0LegacyMUL.uop'))) 'no base: no Felucca copy (EA Felucca as before)'
    $null = Build-MapOverride -UoDir $ea -Ops $ops -OutDir $out -BaseDir $base -AlsoAs 0
    Assert-Equal 9 ([IO.File]::ReadAllBytes((Join-Path $out 'map1LegacyMUL.uop'))[78]) 'a base arriving rebuilds'
    $t0 = (Get-Item (Join-Path $out 'map0LegacyMUL.uop')).LastWriteTimeUtc
    Start-Sleep -Milliseconds 50
    $lines = @(Build-MapOverride -UoDir $ea -Ops $ops -OutDir $out -BaseDir $base -AlsoAs 0)
    Assert-Equal 6 $lines.Count
    Assert-Equal $t0 (Get-Item (Join-Path $out 'map0LegacyMUL.uop')).LastWriteTimeUtc 'the same base: nothing rewritten'
    $null = New-ShippedBase $sos (Join-Path $work 'app-map8') 11
    $null = Build-MapOverride -UoDir $ea -Ops $ops -OutDir $out -BaseDir $base -AlsoAs 0
    Assert-Equal 11 ([IO.File]::ReadAllBytes((Join-Path $out 'map0LegacyMUL.uop'))[78]) 'a new base rebuilds Felucca too'
    Remove-Item -LiteralPath (Join-Path $out 'map0LegacyMUL.uop')
    $null = Build-MapOverride -UoDir $ea -Ops $ops -OutDir $out -BaseDir $base -AlsoAs 0
    Assert-True (Test-Path (Join-Path $out 'map0LegacyMUL.uop')) 'a missing Felucca copy is rebuilt'
}

Fact 'P674_AFeluccaCopyRefusesAFileThatIsNotTrammelsMapAndAFacetOfAnotherSize' {
    $ea = New-MapFacet (Join-Path $work 'ea9')
    $out = Join-Path $work 'out9'
    New-Item -ItemType Directory -Path $out -Force | Out-Null
    Assert-Equal 1 (Copy-UopRenamed (Join-Path $ea 'map1LegacyMUL.uop') (Join-Path $out 'map0.uop') 1 0)
    $threw = $null
    try { $null = Copy-UopRenamed (Join-Path $out 'map0.uop') (Join-Path $out 'again.uop') 1 0 } catch { $threw = $_.Exception.Message }
    Assert-True ($threw -match 'not a map1 chunk') "a Felucca file is not Trammel's map: $threw"
    $ops = Join-Path $work 'nine.mapops'
    [IO.File]::WriteAllText($ops, "F 1 0`nL 1 1 5 0`n", (New-Object Text.ASCIIEncoding))
    $threw = $null
    try { $null = Build-MapOverride -UoDir $ea -Ops $ops -OutDir (Join-Path $work 'out9b') -AlsoAs 2 } catch { $threw = $_.Exception.Message }
    Assert-True ($threw -match 'cannot read') "Ilshenar is not Trammel's size: $threw"
}

Remove-Item -LiteralPath $work -Recurse -Force -ErrorAction SilentlyContinue'''

edit('Map-Overrides.Tests.ps1', [
    ("\nRemove-Item -LiteralPath $work -Recurse -Force -ErrorAction SilentlyContinue", MAP_FACTS),
    ("# facts prove the pieces a player's launch depends on, on their own.\n",
     "# facts prove the pieces a player's launch depends on, on their own.\n"
     "#\n"
     "# cc-P674 (SoS swap S1): a shipped base map (-BaseDir, app\\map\\base-<name>) is patched instead of the player's own\n"
     "# files, Felucca gets the same land (-AlsoAs 0: map0LegacyMUL.uop with map0's entry names, Trammel's statics), and the\n"
     "# stamp names the base, so a new one rebuilds.\n"),
])

LAUNCH_FACT = r'''
# cc-P674 (SoS swap S1): with app\map\ holding the shipped base, a real launch lists Trammel's and Felucca's map, both
# from the base, and the next start only checks. The base is a synthetic one-chunk facet (Map-Overrides.Tests.ps1's
# layout), the patch one cell.
Fact 'P674_AShippedBaseMapReachesTheListForTrammelAndFeluccaAndTheNextStartOnlyChecks' {
    $uo = New-UoDir 'sos-uo'
    $app = New-Install 'sos'
    . (Join-Path $appSrc 'Apply-MapOps.ps1')
    $mapDir = Join-Path $app 'map'
    New-Item -ItemType Directory -Path $mapDir -Force | Out-Null
    $block = New-Object byte[] 196
    for ($i = 0; $i -lt 64; $i++) { $block[4 + $i * 3] = 9 }
    $ms = New-Object IO.MemoryStream; $w = New-Object IO.BinaryWriter($ms)
    $w.Write([uint32]0x50594D); $w.Write([int]5); $w.Write([uint32]4246727747); $w.Write([int64]28); $w.Write([int]100); $w.Write([int]1)
    $w.Write([int]1); $w.Write([int64]0)
    $w.Write([int64]74); $w.Write([int]0); $w.Write([int](196 * 4096)); $w.Write([int](196 * 4096))
    $w.Write([uint64](Get-UopNameHash 'build/map1legacymul/00000000.dat')); $w.Write([uint32]0); $w.Write([int16]0)
    for ($b = 0; $b -lt 4096; $b++) { $w.Write($block, 0, 196) }
    $w.Flush()
    [IO.File]::WriteAllBytes((Join-Path $mapDir 'base-map1legacymul.uop'), $ms.ToArray())
    $idx = New-Object byte[] (4096 * 12)
    for ($b = 0; $b -lt 4096; $b++) { [BitConverter]::GetBytes([int]-1).CopyTo($idx, $b * 12); [BitConverter]::GetBytes([int]-1).CopyTo($idx, $b * 12 + 4) }
    [IO.File]::WriteAllBytes((Join-Path $mapDir 'base-staidx1.mul'), $idx)
    [IO.File]::WriteAllBytes((Join-Path $mapDir 'base-statics1.mul'), (New-Object byte[] 0))
    [IO.File]::WriteAllText((Join-Path $app 'trammel.mapops'), "F 1 0`nL 1 1 5 0`n")
    $r = Invoke-Prepare $app $uo 60
    Assert-True ($r.Result) "built: $($r.Said)"
    $live = Join-Path $app 'uo-overrides'
    $list = [IO.File]::ReadAllText((Join-Path $live 'files-override.txt'))
    foreach ($k in 'map1legacymul.uop', 'map0legacymul.uop', 'statics0.mul', 'staidx0.mul') {
        Assert-True ($list -match "(?m)^$([regex]::Escape($k))=") "the list names $k`: $list"
    }
    Assert-True ($list -match '(?m)^statics0\.mul=.*statics1\.mul\r?$') "Felucca reads Trammel's statics: $list"
    Assert-True (Test-Path (Join-Path $live 'map0LegacyMUL.uop')) 'the Felucca copy is in the live set'
    Assert-Equal 9 ([IO.File]::ReadAllBytes((Join-Path $live 'map0LegacyMUL.uop'))[78]) "the base's land"
    $again = Invoke-Prepare $app $uo 60
    Assert-True ($again.Said -notmatch 'Preparing') "the next start only checks: $($again.Said)"
}

# --- the real Play.ps1, and the updater handing over to it, in a sandbox ----------------------------------------'''

edit('Launch-Overrides.Tests.ps1', [
    ("\n# --- the real Play.ps1, and the updater handing over to it, in a sandbox ----------------------------------------", LAUNCH_FACT),
])
print('ok')
