import os, sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kit770'))


def edit(path, pairs):
    raw = open(path, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in raw else '\n'
    s = raw.replace('\r\n', '\n')
    for old, new in pairs:
        n = s.count(old)
        if n != 1:
            sys.exit('%s: %d matches for %r' % (path, n, old[:90]))
        s = s.replace(old, new)
    open(path, 'w', encoding='utf-8', newline='').write(s.replace('\n', nl))
    print('edited', path, repr(nl))


edit('golem.ps1', [
# The sync before the held pick is read (Gold, 11-02 00:14: a P765 left in the dirty queue looked held, so P9770 went behind it).
(r"""if ($Event -eq 'RunNext') {
    $held = Get-RunNextHeld   # cc-P747: an answered prompt keeps its place""",
r"""if ($Event -eq 'RunNext') {
    if ($script:QueueMode -eq 'git' -and -not $DryRun) { Sync-PromptsGit $PromptDir }   # cc-P770: an idle Golem's clone only pulls at a claim; before the held pick is read
    [void](Clear-StaleRunNext)   # cc-P770
    $held = Get-RunNextHeld   # cc-P747: an answered prompt keeps its place"""),
(r"""    if ($script:QueueMode -eq 'git' -and -not $DryRun) { Sync-PromptsGit $PromptDir }   # cc-P770: an idle Golem's clone only pulls at a claim
    $pf = $(if ($Prompt) { Find-PromptFile $QueueDir $Prompt } else { $null })""",
r"""    $pf = $(if ($Prompt) { Find-PromptFile $QueueDir $Prompt } else { $null })"""),
# A pick no longer queued gives way to the one waiting behind it.
(r"""# The pick $name was handed: RUN-NEXT is cleared, and a pick waiting behind it (RUN-NEXT.after) becomes the pick.""",
r"""# cc-P770: a pick no longer in the queue (claimed or finished elsewhere, or a STOPPED prompt sent to another Golem) holds
# nothing: RUN-NEXT is cleared and a pick waiting behind it (RUN-NEXT.after), if still queued, becomes the pick. Before,
# a stale held pick kept the pick behind it waiting for a hand-off that never came (Gold, 11-02: P765 held P9770).
# Returns the new pick's file name, or ''.
function Clear-StaleRunNext {
    $pick = Get-RunNextName
    if (-not $pick -or (Test-Path -LiteralPath (Join-Path $QueueDir $pick))) { return '' }
    $after = Get-RunNextAfterName
    $promote = $(if ($after -and $after -ne $pick -and (Test-Path -LiteralPath (Join-Path $QueueDir $after))) { $after } else { '' })
    if ($DryRun) { Log ("dry run: run next $pick is no longer queued: would clear it" + $(if ($promote) { " and pick $promote" } else { '' })); return $promote }
    Remove-Item -LiteralPath $RunNextFile, ($RunNextFile + '.answered'), ($RunNextFile + '.after') -Force -ErrorAction SilentlyContinue
    if ($promote) { [IO.File]::WriteAllText($RunNextFile, $promote + "`r`n", [Text.Encoding]::ASCII) }
    Log ("run next: $pick is no longer in the queue: cleared" + $(if ($promote) { '; P' + [regex]::Match($promote, '^cc-P(\d+)-').Groups[1].Value + ' (' + $promote + ') goes next now' } else { '' }))
    $promote
}
# The pick $name was handed: RUN-NEXT is cleared, and a pick waiting behind it (RUN-NEXT.after) becomes the pick."""),
# The watch: the queue first (a git clone), then a stale pick gives way, then the wake.
(r"""        $rnPick = Get-RunNextName
        $lwR = Get-Prop $st 'lastSelfWake' $null""",
r"""        if ($script:QueueMode -eq 'git' -and -not (Test-Path -LiteralPath (Join-Path $QueueDir (Get-RunNextName)))) { Sync-PromptsGit $PromptDir }
        [void](Clear-StaleRunNext)
        $rnPick = Get-RunNextName
        $lwR = Get-Prop $st 'lastSelfWake' $null"""),
(r"""        if (-not $recentR) {""", r"""        if ($rnPick -and -not $recentR) {"""),
])
