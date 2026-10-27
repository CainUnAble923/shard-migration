
# cc-P713: the Siege of Sosaria land behind one switch, vendor\sos-trammel-map\switch.txt, off until the swap goes live.
# Off, the package ships no app\map\ and the launcher patches the player's own stock Trammel exactly as before cc-P674;
# on, it ships the base. The build script's own functions are lifted out of it by name (it cannot be dot-sourced: it
# builds when run), and gate 4 runs as the build runs it, with -CheckZip and -SosMap.
$package = Join-Path $pkg 'Build-PlayerPackage.ps1'
$switch  = Join-Path $pkg 'vendor\sos-trammel-map\switch.txt'
function Import-BuildFunction([string]$name) {
    $ast = [Management.Automation.Language.Parser]::ParseFile($package, [ref]$null, [ref]$null)
    $fn = $ast.Find({ param($a) $a -is [Management.Automation.Language.FunctionDefinitionAst] -and $a.Name -eq $name }, $true)
    if (-not $fn) { throw "Build-PlayerPackage.ps1 has no function $name" }
    . ([scriptblock]::Create($fn.Extent.Text.Replace("function $name", "function global:$name")))
}

# A zip under one top folder holding the given entries (name -> text), and gate 4's output on it with -SosMap.
Add-Type -AssemblyName System.IO.Compression, System.IO.Compression.FileSystem
function New-GateZip([string]$name, [hashtable]$entries) {
    $zip = Join-Path $work $name
    $fs = [IO.File]::Open($zip, [IO.FileMode]::CreateNew)
    $za = New-Object IO.Compression.ZipArchive($fs, [IO.Compression.ZipArchiveMode]::Create)
    try {
        foreach ($k in $entries.Keys) { $w = New-Object IO.StreamWriter(($za.CreateEntry("ShatteredLegacy/$k")).Open()); $w.Write($entries[$k]); $w.Dispose() }
    } finally { $za.Dispose(); $fs.Dispose() }
    return $zip
}
function Invoke-Gate4([string]$zip, [string]$sos) {
    $ea = Join-Path $work 'ea-names'
    if (-not (Test-Path $ea)) { New-Item -ItemType Directory -Path $ea -Force | Out-Null; [IO.File]::WriteAllBytes((Join-Path $ea 'tiledata.mul'), (New-Object byte[] 8)) }
    $a = @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', $package, '-CheckZip', $zip, '-UoData', $ea)
    if ($sos) { $a += @('-SosMap', $sos) }
    $ErrorActionPreference = 'Continue'
    $text = & powershell.exe @a 2>&1 | Out-String
    $ErrorActionPreference = 'Stop'
    Assert-True ($text -match 'GATE 4') "gate 4 ran: $text"
    return $text
}
$credit = "  app\map\     the land of Trammel and Felucca: `"Siege of Sosaria Trammel Map 3.0`"`r`n"

Fact 'P713_TheSwitchIsOffUntilTheSwapGoesLive' {
    Import-BuildFunction 'Get-SosMapSwitch'
    Assert-Equal 'off' (Get-SosMapSwitch $switch) 'switch.txt in the repo'
}

Fact 'P713_ASwitchThatIsNotOneWordOffOrOnStopsTheBuild' {
    Import-BuildFunction 'Get-SosMapSwitch'
    $f = Join-Path $work 'switch.txt'
    [IO.File]::WriteAllText($f, "# a comment`r`n  on  `r`n", (New-Object Text.ASCIIEncoding))
    Assert-Equal 'on' (Get-SosMapSwitch $f) 'comments and spaces are skipped'
    foreach ($bad in @("On`r`n", "yes`r`n", "off`r`non`r`n", "# nothing but a comment`r`n")) {
        [IO.File]::WriteAllText($f, $bad, (New-Object Text.ASCIIEncoding))
        $threw = $null
        try { $null = Get-SosMapSwitch $f } catch { $threw = $_.Exception.Message }
        Assert-True ($threw -match 'SOS MAP SWITCH') "refused [$($bad.Trim())]: $threw"
    }
    $threw = $null
    try { $null = Get-SosMapSwitch (Join-Path $work 'no-switch.txt') } catch { $threw = $_.Exception.Message }
    Assert-True ($threw -match 'missing') "a missing switch is refused: $threw"
}

Fact 'P713_SwitchedOffTheReadmeLosesOnlyItsAppMapEntry' {
    Import-BuildFunction 'Remove-SosMapReadme'
    $text = [IO.File]::ReadAllText((Join-Path $pkg 'payload\README.txt'))
    $off = Remove-SosMapReadme $text
    Assert-True ($text -match 'Siege of Sosaria Trammel Map') 'payload\README.txt credits the map (for a package with the switch on)'
    Assert-True ($off -notmatch 'Siege of Sosaria Trammel Map' -and $off -notmatch 'app\\map\\') 'the off README names neither'
    $gone = @($text -split "`n").Count - @($off -split "`n").Count
    Assert-Equal 5 $gone 'the entry is five lines'
    Assert-True ($off -match '(?m)^  app\\music\\ ' -and $off -match '(?m)^  app\\         the scripts') 'the entries around it stay'
    $threw = $null
    try { $null = Remove-SosMapReadme $off } catch { $threw = $_.Exception.Message }
    Assert-True ($threw -match 'no single app\\map\\ entry') "a README with no entry stops the build: $threw"
}

Fact 'P713_WithNoAppMapTheLauncherPatchesThePlayersOwnStockFilesAsBefore' {
    # The launcher's builder, as Play.ps1 runs it, with a package that has no app\map\ (switch off): three lines, our
    # patch on the player's own Trammel, no Felucca copy. With app\map\ (switch on): six, on the base.
    $ea = New-MapFacet (Join-Path $work 'ea10')
    $ops = Join-Path $work 'ten.mapops'
    [IO.File]::WriteAllText($ops, "F 1 0`nL 10 20 581 -3`n", (New-Object Text.ASCIIEncoding))
    $none = Join-Path $work 'no-such-file'
    $run = {
        param($out, $mapBase)
        $res = @(& $builder -UoDir $ea -OutDir $out -MapOps $ops -MapBase $mapBase -Records $none -Clilocs $none -Music $none -AnimMul $none -AnimIdx $none 6>$null)[-1]
        @([IO.File]::ReadAllLines($res) | Where-Object { $_ -and -not $_.StartsWith('#') })
    }
    $out = Join-Path $work 'out10'
    $lines = & $run $out (Join-Path $work 'no-app-map')
    Assert-Equal 3 $lines.Count ($lines -join ' | ')
    Assert-True (-not ($lines -match '^map0')) 'no Felucca line: EA Felucca as before'
    $m1 = [IO.File]::ReadAllBytes((Join-Path $out 'map1LegacyMUL.uop'))
    Assert-Equal 3 $m1[78] "the player's own tile"
    Assert-Equal 69 $m1[74 + 514 * 196 + 4 + 34 * 3] 'our patch on it'
    $base = New-ShippedBase (New-MapFacet (Join-Path $work 'sos10')) (Join-Path $work 'app-map10')
    $out2 = Join-Path $work 'out10b'
    $lines2 = & $run $out2 $base
    Assert-Equal 6 $lines2.Count ($lines2 -join ' | ')
    Assert-Equal 9 ([IO.File]::ReadAllBytes((Join-Path $out2 'map1LegacyMUL.uop'))[78]) "the base's tile"
}

Fact 'P713_Gate4SwitchedOffRefusesAnyAppMapFileAndTheCredit' {
    $zip = New-GateZip 'off-with-map.zip' @{ 'app/map/base-map1legacymul.uop' = 'x'; 'README.txt' = $credit }
    $text = Invoke-Gate4 $zip 'off'
    Assert-True ($text -match 'app/map/base-map1legacymul\.uop shipped, but the Siege of Sosaria map is switched off') $text
    Assert-True ($text -match 'README\.txt credits the Siege of Sosaria Trammel Map, which is switched off') $text
    Assert-True ($text -match 'app/map/base-map1legacymul\.uop is an EA data file type') 'no exemption with the switch off'
    $zip2 = New-GateZip 'off-clean.zip' @{ 'README.txt' = 'no map here' }
    $text2 = Invoke-Gate4 $zip2 ''
    Assert-True ($text2 -notmatch 'app/map|Siege of Sosaria') "the repo's switch (off): a zip with no app/map/ has no map line: $text2"
}

Fact 'P713_Gate4SwitchedOnWantsTheThreeFilesAndTheCredit' {
    $zip = New-GateZip 'on-empty.zip' @{ 'README.txt' = 'no map here' }
    $text = Invoke-Gate4 $zip 'on'
    foreach ($f in 'base-map1legacymul.uop', 'base-statics1.mul', 'base-staidx1.mul') {
        Assert-True ($text -match "no app/map/$([regex]::Escape($f)) \(the Siege of Sosaria map\)") "$f wanted: $text"
    }
    Assert-True ($text -match 'README\.txt does not credit the Siege of Sosaria Trammel Map') $text
    $zip2 = New-GateZip 'on-wrong.zip' @{ 'app/map/base-statics1.mul' = 'not his'; 'README.txt' = $credit }
    $text2 = Invoke-Gate4 $zip2 'on'
    Assert-True ($text2 -match 'app/map/base-statics1\.mul is not the file vendor\\sos-trammel-map\\manifest\.csv records') $text2
    Assert-True ($text2 -notmatch 'README\.txt (does not )?credit') "the credit is there: $text2"
}
