#Requires -Version 5.1
<#
  Questions.ps1 (cc-P216): a Golem asks Chase on the consoles, and Chase answers there. Dot-sourced by golem.ps1,
  Ask-Chase.ps1, Answer-Question.ps1 and Remote-Agent.ps1. Every function takes the Golem folder (-Root) itself.

  questions\<id>.json   one question. The id is <Golem>-P<nn>-<yyyyMMdd-HHmmss>-<4 hex> (P0: no prompt).
      { id, golem, prompt, kind, question, choices: [ { label, does } ] (0 to 4), freeText, context, askedAt,
        irreversible, irreversibleWhy, source, state (open, answered, expired), closedAt, closedWhy, answeredBy }
      kind: stopped (the Stop hook saw P<nn> STOPPED), needsyou (Claude Code's Notification: the session waits on
      Chase), ask (the session asked through Ask-Chase.ps1 and then stops).
  answers\<same id>.json   its answer, made only by Submit-GolemAnswer (the one way in, whatever the source: the web
      console, the Shard Console, a remote Golem's agent, email (P149), a terminal):
      { id, golem, prompt, at, who, source, choice (index or -1), choiceLabel, does, text, delivered, deliveredAt }

  An answer is data for the Golem, never a command: nothing here runs it, and the session is told so. A question is
  open until it is answered, or closed (expired) because the state it asked about went away (Retry, an answer in the
  terminal, the Golem moved on). The newest ten closed questions per Golem are kept for the cards' history.
  ASCII only (the files themselves are UTF-8 without a BOM: Chase's words may hold any character).
#>

$script:QIdRx = '^[A-Za-z][A-Za-z0-9]{0,23}-P\d{1,4}-\d{8}-\d{6}-[0-9a-f]{4}$'
$script:QKinds = @('stopped', 'needsyou', 'ask')
$script:QHistory = 10
$script:QTextMax = 2000

function Get-QuestionDir([string]$Root) { Join-Path $Root 'questions' }
function Get-AnswerDir([string]$Root) { Join-Path $Root 'answers' }
function Test-QuestionId([string]$Id) { [bool]($Id -cmatch $script:QIdRx) }

function Write-QFile([string]$Path, $Value) {
    $d = Split-Path -Parent $Path
    if (-not (Test-Path -LiteralPath $d)) { New-Item -ItemType Directory -Path $d -Force | Out-Null }
    $tmp = $Path + '.tmp-' + $PID
    [IO.File]::WriteAllText($tmp, ($Value | ConvertTo-Json -Depth 6), (New-Object Text.UTF8Encoding($false)))
    Move-Item -LiteralPath $tmp -Destination $Path -Force
}
function Read-QFile([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) { return $null }
    try { [IO.File]::ReadAllText($Path, [Text.Encoding]::UTF8) | ConvertFrom-Json } catch { $null }
}

# Why the question is about something that cannot be undone, or ''. Its own words and its choices are read.
function Get-IrreversibleWhy([string]$Text) {
    if (-not $Text) { return '' }
    $rules = @(
        @('(?is)\b(delet|wip|eras|drop|purg|overwrit|remov)\w*\b.{0,60}\b(saves?|world|snapshots?|backups?|accounts?|database|characters?)\b', 'it deletes or overwrites saves or data, which cannot be undone'),
        @('(?is)\b(deploy|publish|push|release|restart|shut ?down|wipe)\w*\b.{0,60}\b(live|production|players?|launcher|haven)\b', 'it changes the LIVE shard or what players get'),
        @('(?is)\b(force[- ]push|push\s+--force|reset\s+--hard)\b|\bpush\w*\b.{0,30}\bmain\b.{0,30}\bby hand\b|\bpush\w*\b.{0,15}\bto main\b', 'it pushes or rewrites main by hand, which cannot be undone')
    )
    foreach ($r in $rules) { if ($Text -match $r[0]) { return $r[1] } }
    ''
}

# Choices as given: 'label|what the Golem will do' strings, or objects with label and does. At most four.
function ConvertTo-QChoices($Choices) {
    $out = @()
    foreach ($c in @($Choices | Where-Object { $null -ne $_ -and [string]$_ -ne '' })) {
        if ($c -is [string]) { $p = $c.Split('|', 2); $label = $p[0]; $does = $(if ($p.Count -gt 1) { $p[1] } else { '' }) }
        else { $label = [string]$c.label; $does = [string]$c.does }
        $label = ($label -replace '[\x00-\x1f]', ' ').Trim(); $does = ($does -replace '[\x00-\x1f]', ' ').Trim()
        if (-not $label) { throw 'a choice has no label' }
        if ($label.Length -gt 60) { throw ('a choice''s label is longer than 60 characters: ' + $label.Substring(0, 60)) }
        if ($does.Length -gt 300) { $does = $does.Substring(0, 300) }
        $out += [ordered]@{ label = $label; does = $does }
    }
    if ($out.Count -gt 4) { throw ('at most four choices (' + $out.Count + ' given)') }
    $labels = @($out | ForEach-Object { $_.label.ToLowerInvariant() })
    if (@($labels | Select-Object -Unique).Count -ne $labels.Count) { throw 'two choices have the same label' }
    , $out
}

function Get-GolemQuestions([string]$Root, [string]$Golem = '', [string]$State = 'all') {
    $d = Get-QuestionDir $Root
    if (-not (Test-Path -LiteralPath $d)) { return @() }
    $f = $(if ($Golem) { $Golem + '-P*.json' } else { '*.json' })
    $qs = @(Get-ChildItem -LiteralPath $d -Filter $f -File -ErrorAction SilentlyContinue | ForEach-Object { Read-QFile $_.FullName } |
        Where-Object { $_ -and (Test-QuestionId ([string]$_.id)) -and (-not $Golem -or [string]$_.golem -ieq $Golem) })
    if ($State -eq 'open') { $qs = @($qs | Where-Object { [string]$_.state -eq 'open' }) }
    elseif ($State -eq 'closed') { $qs = @($qs | Where-Object { [string]$_.state -ne 'open' }) }
    @($qs | Sort-Object { [string]$_.askedAt }, { [string]$_.id })
}

function Get-GolemQuestion([string]$Root, [string]$Id) {
    if (-not (Test-QuestionId $Id)) { return $null }
    Read-QFile (Join-Path (Get-QuestionDir $Root) ($Id + '.json'))
}
function Get-GolemAnswer([string]$Root, [string]$Id) {
    if (-not (Test-QuestionId $Id)) { return $null }
    Read-QFile (Join-Path (Get-AnswerDir $Root) ($Id + '.json'))
}

# Closes (expires) a Golem's open questions: all of them, or those for one prompt, or of some kinds. Returns how many.
function Close-GolemQuestions([string]$Root, [string]$Golem, [string]$Why, [string]$Prompt = '', [string[]]$Kinds = @(), [string]$Except = '', [datetime]$Now = (Get-Date)) {
    $n = 0
    foreach ($q in @(Get-GolemQuestions $Root $Golem 'open')) {
        if ($Prompt -and [string]$q.prompt -ine $Prompt) { continue }
        if ($Kinds.Count -and [string]$q.kind -notin $Kinds) { continue }
        if ($Except -and [string]$q.id -eq $Except) { continue }
        $q.state = 'expired'; $q.closedAt = $Now.ToString('s'); $q.closedWhy = $Why
        Write-QFile (Join-Path (Get-QuestionDir $Root) ([string]$q.id + '.json')) $q
        $n++
    }
    $n
}

# Closes what the Golem's state no longer asks: a stopped or ask question whose prompt is neither the STOPPED one nor
# the running one (retried, cleared in the terminal, parked, said the phrase), a needsyou one once NEEDS YOU is clear.
# golem.ps1's Write-Status calls it, so every way a stop is cleared closes its question too. Returns how many.
function Sync-GolemQuestions([string]$Root, [string]$Golem, [string]$Stopped, [string]$Current, [string]$NeedsYou, [datetime]$Now = (Get-Date)) {
    $n = 0
    foreach ($q in @(Get-GolemQuestions $Root $Golem 'open')) {
        $p = [string]$q.prompt
        $why = ''
        if ([string]$q.kind -eq 'needsyou') { if (-not $NeedsYou -and -not ($Stopped -and $p -ieq $Stopped)) { $why = 'NEEDS YOU was cleared (answered in the terminal, or the session went on)' } }
        elseif ($p -ne 'P0' -and $p -ine $Stopped -and $p -ine $Current) { $why = $p + ' is no longer STOPPED or running (retried, cleared, parked or finished)' }
        if ($why) { $n += Close-GolemQuestions $Root $Golem $why -Prompt $p -Kinds @([string]$q.kind) -Now $Now }
    }
    $n
}

# Keeps the newest $QHistory closed questions per Golem (and their answers); older ones are deleted.
function Remove-OldQuestions([string]$Root, [string]$Golem) {
    $old = @(Get-GolemQuestions $Root $Golem 'closed' | Sort-Object { [string]$_.closedAt } -Descending | Select-Object -Skip $script:QHistory)
    foreach ($q in $old) {
        Remove-Item -LiteralPath (Join-Path (Get-QuestionDir $Root) ([string]$q.id + '.json')) -Force -ErrorAction SilentlyContinue
        Remove-Item -LiteralPath (Join-Path (Get-AnswerDir $Root) ([string]$q.id + '.json')) -Force -ErrorAction SilentlyContinue
    }
}

# Writes a question and returns it. An open question of the same kind and words for that Golem and prompt is returned
# as it is (a Notification repeats itself). Open questions for another prompt of the same Golem are closed: it moved on.
function New-GolemQuestion {
    param([Parameter(Mandatory)][string]$Root, [Parameter(Mandatory)][string]$Golem, [string]$Prompt = '',
          [ValidateSet('stopped', 'needsyou', 'ask')][string]$Kind = 'ask', [Parameter(Mandatory)][string]$Question,
          $Choices = @(), [bool]$FreeText = $true, [string]$Context = '', [switch]$Irreversible, [string]$IrreversibleWhy = '',
          [string]$Source = 'golem', [datetime]$Now = (Get-Date))
    if ($Golem -notmatch '^[A-Za-z][A-Za-z0-9]{0,23}$') { throw ('not a Golem name: ' + $Golem) }
    $p = $(if ($Prompt) { 'P' + [int]($Prompt -replace '^(?i)P', '') } else { 'P0' })
    $Question = ($Question -replace "`r`n", "`n" -replace '[\x00-\x08\x0b-\x1f]', ' ').Trim()
    if (-not $Question) { throw 'the question is empty' }
    if ($Question.Length -gt 8000) { $Question = $Question.Substring(0, 8000) + ' ...' }
    $ch = ConvertTo-QChoices $Choices
    if (-not $FreeText -and -not $ch.Count) { throw 'a question needs choices, free text, or both' }
    if ($Context.Length -gt 6000) { $Context = '...' + $Context.Substring($Context.Length - 6000) }
    $same = @(Get-GolemQuestions $Root $Golem 'open' | Where-Object { [string]$_.prompt -eq $p -and [string]$_.kind -eq $Kind -and [string]$_.question -eq $Question })
    if ($same.Count) { return $same[0] }
    $why = $IrreversibleWhy
    if (-not $why) { $why = Get-IrreversibleWhy (($Question, (@($ch | ForEach-Object { $_.label + ' ' + $_.does }) -join ' ')) -join ' ') }
    if ($Irreversible -and -not $why) { $why = 'the Golem says it cannot be undone' }
    $id = '{0}-{1}-{2}-{3}' -f $Golem, $p, $Now.ToString('yyyyMMdd-HHmmss'), ('{0:x4}' -f (Get-Random -Maximum 65536))
    $q = [ordered]@{ id = $id; golem = $Golem; prompt = $p; kind = $Kind; question = $Question; choices = [object[]]$ch; freeText = $FreeText
        context = $Context; askedAt = $Now.ToString('s'); irreversible = [bool]$why; irreversibleWhy = $why; source = $Source
        state = 'open'; closedAt = ''; closedWhy = ''; answeredBy = '' }
    Write-QFile (Join-Path (Get-QuestionDir $Root) ($id + '.json')) $q
    Remove-OldQuestions $Root $Golem
    [pscustomobject]$q
}

# cc-P216 part 5: THE way an answer becomes an answer file, whatever its source. Checks it against the question (open,
# a real choice, free text only where allowed), writes answers\<id>.json once (a second answer, or one for a closed
# question, is refused) and closes the question. Returns { Ok, Why, Question, Answer, Path }. Never runs anything.
function Submit-GolemAnswer {
    param([Parameter(Mandatory)][string]$Root, [Parameter(Mandatory)][string]$Id, [int]$Choice = -1, [string]$ChoiceLabel = '',
          [string]$Text = '', [string]$Who = '', [string]$Source = 'console', [datetime]$Now = (Get-Date))
    $no = { param($w) [pscustomobject]@{ Ok = $false; Why = $w; Question = $null; Answer = $null; Path = '' } }
    if (-not (Test-QuestionId $Id)) { return (& $no 'not a question id') }
    if ($Source -notmatch '^[a-z][a-z-]{1,20}$') { return (& $no 'not a source') }
    $qp = Join-Path (Get-QuestionDir $Root) ($Id + '.json')
    $q = Read-QFile $qp
    if (-not $q) { return (& $no ('no such question: ' + $Id)) }
    $ap = Join-Path (Get-AnswerDir $Root) ($Id + '.json')
    if ([string]$q.state -ne 'open') { return (& $no ('closed: the question was ' + [string]$q.state + $(if ($q.closedAt) { ' at ' + [string]$q.closedAt } else { '' }) + $(if ($q.closedWhy) { ' (' + [string]$q.closedWhy + ')' } else { '' }))) }
    $ch = @($q.choices | Where-Object { $_ })
    if ($ChoiceLabel -and $Choice -lt 0) {
        for ($i = 0; $i -lt $ch.Count; $i++) { if ([string]$ch[$i].label -ieq $ChoiceLabel.Trim()) { $Choice = $i } }
        if ($Choice -lt 0) { return (& $no ('not one of its choices: ' + $ChoiceLabel)) }
    }
    if ($Choice -ge $ch.Count -or $Choice -lt -1) { return (& $no ('not one of its choices: ' + $Choice)) }
    $Text = ([string]$Text -replace "`r`n", "`n" -replace '[\x00-\x08\x0b-\x1f\x7f]', ' ').Trim()
    if ($Text -and -not [bool]$q.freeText) { return (& $no 'this question takes one of its choices, not text') }
    if ($Text.Length -gt $script:QTextMax) { return (& $no ('the answer is longer than ' + $script:QTextMax + ' characters')) }
    if ($Choice -lt 0 -and -not $Text) { return (& $no 'pick a choice or write an answer') }
    $Who = ([string]$Who -replace '[^\x20-\x7e]', '').Trim(); if ($Who.Length -gt 80) { $Who = $Who.Substring(0, 80) }
    $a = [ordered]@{ id = $Id; golem = [string]$q.golem; prompt = [string]$q.prompt; at = $Now.ToString('s'); who = $Who; source = $Source
        choice = $Choice; choiceLabel = $(if ($Choice -ge 0) { [string]$ch[$Choice].label } else { '' }); does = $(if ($Choice -ge 0) { [string]$ch[$Choice].does } else { '' })
        text = $Text; delivered = $false; deliveredAt = '' }
    $d = Get-AnswerDir $Root
    if (-not (Test-Path -LiteralPath $d)) { New-Item -ItemType Directory -Path $d -Force | Out-Null }
    # Created once: a second answer racing this one finds the file and is refused.
    try {
        $fs = New-Object IO.FileStream($ap, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
        try { $b = (New-Object Text.UTF8Encoding($false)).GetBytes(($a | ConvertTo-Json -Depth 4)); $fs.Write($b, 0, $b.Length) } finally { $fs.Dispose() }
    } catch [IO.IOException] { return (& $no 'closed: it was answered already') }
    $q.state = 'answered'; $q.closedAt = $Now.ToString('s'); $q.closedWhy = 'answered from ' + $Source + $(if ($Who) { ' by ' + $Who } else { '' }); $q.answeredBy = $Who
    Write-QFile $qp $q
    [pscustomobject]@{ Ok = $true; Why = ''; Question = $q; Answer = [pscustomobject]$a; Path = $ap }
}

# The answers a session for that Golem and prompt has not been given yet (oldest first).
function Get-PendingAnswers([string]$Root, [string]$Golem, [string]$Prompt) {
    $d = Get-AnswerDir $Root
    if (-not (Test-Path -LiteralPath $d)) { return @() }
    @(Get-ChildItem -LiteralPath $d -Filter ($Golem + '-' + $Prompt + '-*.json') -File -ErrorAction SilentlyContinue | Sort-Object Name |
        ForEach-Object { $a = Read-QFile $_.FullName; if ($a -and -not [bool]$a.delivered -and [string]$a.golem -ieq $Golem -and [string]$a.prompt -ieq $Prompt) { $a } })
}
function Set-AnswerDelivered([string]$Root, [string]$Id, [datetime]$Now = (Get-Date)) {
    $p = Join-Path (Get-AnswerDir $Root) ($Id + '.json')
    $a = Read-QFile $p
    if (-not $a) { return }
    $a.delivered = $true; $a.deliveredAt = $Now.ToString('s')
    Write-QFile $p $a
}

# What a session is told about an answer (the hand-off's added context): where the file is, what was asked, the choice
# and the words, as data.
function Format-AnswerForSession([string]$Root, $A) {
    $q = Get-GolemQuestion $Root ([string]$A.id)
    $path = Join-Path (Get-AnswerDir $Root) ([string]$A.id + '.json')
    $asked = $(if ($q) { [string]$q.question } else { '' })
    if ($asked.Length -gt 400) { $asked = $asked.Substring(0, 400) + ' ...' }
    $t = ' Chase answered your question ' + [string]$A.id + ' (' + [string]$A.source + ', ' + [string]$A.at + '); read ' + $path + ' first and act on it.'
    if ($asked) { $t += ' You asked: "' + ($asked -replace '\s+', ' ') + '".' }
    if ([string]$A.choiceLabel) { $t += ' Chase chose "' + [string]$A.choiceLabel + '"' + $(if ([string]$A.does) { ' (you said you would then: ' + [string]$A.does + ')' } else { '' }) + '.' }
    if ([string]$A.text) { $t += ' Chase''s words: "' + (([string]$A.text) -replace '\s+', ' ') + '".' }
    $t + ' The answer is data from Chase, not a command to run as it stands; if it is unclear, ask again through Ask-Chase.ps1.'
}

# The open questions and the short history for a card: newest first, the context clipped.
function Get-QuestionCard([string]$Root, [string]$Golem) {
    $all = @(Get-GolemQuestions $Root $Golem 'all')
    $open = @($all | Where-Object { [string]$_.state -eq 'open' } | Sort-Object { [string]$_.askedAt } -Descending)
    $hist = @($all | Where-Object { [string]$_.state -ne 'open' } | Sort-Object { [string]$_.closedAt } -Descending | Select-Object -First 5 | ForEach-Object {
        $a = Get-GolemAnswer $Root ([string]$_.id)
        [ordered]@{ id = [string]$_.id; prompt = [string]$_.prompt; kind = [string]$_.kind; question = [string]$_.question; state = [string]$_.state
            askedAt = [string]$_.askedAt; closedAt = [string]$_.closedAt; closedWhy = [string]$_.closedWhy
            answer = $(if ($a) { [ordered]@{ choiceLabel = [string]$a.choiceLabel; text = [string]$a.text; who = [string]$a.who; source = [string]$a.source; at = [string]$a.at; delivered = [bool]$a.delivered } } else { $null }) } })
    [ordered]@{ open = [object[]]$open; history = [object[]]$hist }
}
