r"""cc-P817: adds the Prof.txt step to player-package\payload\app\Build-UoOverrides.ps1 (ASCII only, as the file asks).

    python -P add_build_prof.py <Build-UoOverrides.ps1>
"""
import sys

p = sys.argv[1]
s = open(p, encoding='ascii', newline='').read()
nl = '\r\n' if '\r\n' in s else '\n'


def rep(a, b):
    global s
    a, b = a.replace('\n', nl), b.replace('\n', nl)
    assert s.count(a) == 1, (a[:70], s.count(a))
    s = s.replace(a, b)


rep("""  Then files-override.txt lists whichever copies were made.""",
    """  cc-P817 (Chase 2026-11-07: "I also want to remove the trade choice"): Prof.txt, the creation screen's professions.
    1. Skipped if the player has no Prof.txt, or if it already lists none of the professions in $ProfRemoved.
    2. If app\\uo-overrides\\prof-stamp.txt matches the player's Prof.txt (size and time) and the list, it is done.
    3. Otherwise writes the player's Prof.txt with each Begin ... End block whose Desc (the profession number the
       client sends) is in $ProfRemoved left out, everything else byte for byte, to app\\uo-overrides\\Prof.txt, then
       the stamp. The list names it "prof.txt=..."; TazUO reads the file through its override map
       (ProfessionLoader.Load: FileManager.GetUOFilePath("Prof.txt")). The server refuses the same numbers
       (server\\customizations\\ClusterFStartChoices.cs, RemovedProfessions), so the screen offers only what is made.

  Then files-override.txt lists whichever copies were made.""")

rep("""$MusicStampFormat = 'uo-music 2'""",
    """$MusicStampFormat = 'uo-music 2'
$ProfStampFormat = 'uo-prof 1'
# cc-P817: the professions the server refuses at creation (ClusterFStartChoices.RemovedProfessions), by Desc number:
# 3 Blacksmith (the shard's Maker: Chase's "trade choice"), 4 Necromancer, 5 Paladin, 6 Samurai, 7 Ninja.
$ProfRemoved = @(3, 4, 5, 6, 7)""")

rep("""# cc-P368: returns the music's override lines""",
    """# cc-P817: returns the Prof.txt override line, or none: the player's own Prof.txt without the refused professions.
function Build-Prof {
    $src = Join-Path $UoDir 'Prof.txt'
    if (-not (Test-Path -LiteralPath $src)) { return }
    $outFile  = Join-Path $OutDir 'Prof.txt'
    $stampOut = Join-Path $OutDir 'prof-stamp.txt'
    $f = Get-Item -LiteralPath $src
    $stamp = "$ProfStampFormat`nProf.txt $($f.Length) $($f.LastWriteTimeUtc.Ticks)`nremoved $($ProfRemoved -join ',')"
    $lines = { "prof.txt=$(Join-Path $ListRoot 'Prof.txt')" }

    if ((Test-Path -LiteralPath $stampOut) -and (Test-Path -LiteralPath $outFile) -and
        [IO.File]::ReadAllText($stampOut) -ceq $stamp) {
        & $lines
        return
    }
    if ($CheckOnly) { $script:Stale.Add('prof'); return }

    Start-Step 'prof'
    # Latin-1 both ways: every byte comes back as it was, whatever the file's encoding.
    $latin = [Text.Encoding]::GetEncoding(28591)
    $text = $latin.GetString([IO.File]::ReadAllBytes($src))
    $kept = New-Object Text.StringBuilder
    $dropped = 0
    $at = 0
    foreach ($m in [regex]::Matches($text, '(?ims)^[ \\t]*Begin[ \\t]*\\r?\\n.*?^[ \\t]*End[ \\t]*(\\r?\\n|$)')) {
        $desc = [regex]::Match($m.Value, '(?im)^[ \\t]*Desc[ \\t]+(\\d+)')
        if ($desc.Success -and ($ProfRemoved -contains [int]$desc.Groups[1].Value)) {
            [void]$kept.Append($text.Substring($at, $m.Index - $at))
            $at = $m.Index + $m.Length
            $dropped++
        }
    }
    [void]$kept.Append($text.Substring($at))
    if ($dropped -eq 0) { Stop-Step; return }    # nothing of ours to take out: the player's own file is used

    if (-not (Test-Path -LiteralPath $OutDir)) { New-Item -ItemType Directory -Path $OutDir -Force | Out-Null }
    if (Test-Path -LiteralPath $stampOut) { Remove-Item -LiteralPath $stampOut -Force }
    [IO.File]::WriteAllBytes($outFile, $latin.GetBytes($kept.ToString()))
    [IO.File]::WriteAllText($stampOut, $stamp, (New-Object Text.ASCIIEncoding))
    Stop-Step
    & $lines
}

# cc-P368: returns the music's override lines""")

rep("""    try { $lines += @(Build-Map) }""",
    """    try { $lines += @(Build-Prof) }
    catch { Skip-Part 'prof' "Shattered Legacy professions could not be prepared ($($_.Exception.Message)). Starting with every profession listed." }

    try { $lines += @(Build-Map) }""")

s.encode('ascii')
open(p, 'w', encoding='ascii', newline='').write(s)
print('ok')
