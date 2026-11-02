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


# ---------------------------------------------------------------- Answer-Question.ps1 (E)
edit('Answer-Question.ps1', [
(r"""$r = Submit-GolemAnswer -Root $Root -Id $Id -Choice $Choice -Text $Text -Who $Who -Source $Source""",
r"""# cc-P770: a question from a Golem on another PC lives there (questions\ on that PC); its agent sends a copy here as
# remote\<Golem>\questions.json. Answered here, the answer goes to that agent as the web console's Answer does, and that PC
# writes it and resumes. Checked here first with the same rules, so a wrong choice is refused at once.
if (-not (Test-Path -LiteralPath (Join-Path (Get-QuestionDir $Root) ($Id + '.json')))) {
    $rq = Find-RemoteQuestion $Root $Id
    if ($rq) {
        if (-not $rq.Open) { Write-Host ('Not answered: ' + $Id + ' on ' + $rq.Golem + ' is closed (' + $rq.State + '), as ' + $rq.Golem + '''s agent last reported at ' + $rq.ReceivedAt + '.'); exit 1 }
        $q = $rq.Question
        $ch = @($q.choices | Where-Object { $_ })
        if ($Choice -ge $ch.Count -or $Choice -lt -1) { Write-Host ('Not answered: not one of its choices: ' + $Choice); exit 1 }
        $Text = ([string]$Text -replace "`r`n", "`n" -replace '[\x00-\x08\x0b-\x1f\x7f]', ' ').Trim()
        if ($Text -and -not [bool]$q.freeText) { Write-Host 'Not answered: this question takes one of its choices, not text'; exit 1 }
        if ($Choice -lt 0 -and -not $Text) { Write-Host 'Not answered: pick a choice or write an answer'; exit 1 }
        $Who = ([string]$Who -replace '[^A-Za-z0-9@._+ ()-]', '').Trim(); if ($Who.Length -gt 80) { $Who = $Who.Substring(0, 80) }
        if ($Who -match '^[ ()-]') { $Who = 'overseer ' + $Who }
        . (Join-Path $Here 'Golems.ps1')
        $reg = $null; try { $reg = Read-GolemRegistry (Join-Path $Root 'golems.json') } catch {}
        $g = $(if ($reg) { Get-GolemByName $reg $rq.Golem } else { $null })
        $pc = $(if ($g) { [string]$g.machine } else { 'its PC' })
        $b64 = $(if ($Text) { [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($Text)) } else { '' })
        $f = Add-RemoteCommand $Root $rq.Golem 'answer' ('Answer ' + $Id) $(if ($Who) { $Who } else { 'Answer-Question on ' + $env:COMPUTERNAME }) (Get-Date) 60 @{ question = $Id; choice = [string]$Choice; textb64 = $b64; who = $Who }
        $lbl = $(if ($Choice -ge 0) { '"' + [string]$ch[$Choice].label + '"' } else { '' }) + $(if ($Text) { $(if ($Choice -ge 0) { ' and ' } else { '' }) + 'your words' } else { '' })
        Write-Host ('Sent to ' + $rq.Golem + '''s agent on ' + $pc + ': ' + $Id + ' answered ' + $lbl + ' (' + $f + '). ' + $rq.Golem + ' writes the answer there at its agent''s next poll (seconds while it is awake, a minute asleep) and resumes; its questions here show it answered at its next report.')
        Write-Host ('If ' + $pc + ' is off, it is answered when it next comes on (the command keeps an hour), or answer it on ' + $pc + ': Answer-Question.ps1 -Id ' + $Id + ' -Choice ' + $Choice)
        exit 0
    }
}
$r = Submit-GolemAnswer -Root $Root -Id $Id -Choice $Choice -Text $Text -Who $Who -Source $Source"""),
(r"""if ($NoWake) { Write-Host 'Not woken (-NoWake): wake the Golem when you are ready.'; exit 0 }""",
r"""if ($NoWake) { Write-Host 'Not woken (-NoWake): wake the Golem when you are ready.'; exit 0 }
# cc-P770: from the agent (-Source remote) the wake is the watch's: the agent's own process could not start the terminal
# (Gold, 11-01 14:39: "wt.exe ... Access is denied", and the window it opened instead never reported). The answer put the
# prompt first (RUN-NEXT), and the watch wakes an idle Golem for its Run next pick; the agent runs the watch at once.
if ($Source -eq 'remote') { Write-Host 'The watch wakes the Golem for it (the agent runs the watch now; else within 10 minutes).'; exit 0 }"""),
])

# ---------------------------------------------------------------- Questions.ps1: Find-RemoteQuestion
edit('Questions.ps1', [
(r"""# The answers a session for that Golem and prompt has not been given yet (oldest first).""",
r"""# cc-P770: a question asked on another PC, from the copy its agent sends here (remote\<Golem>\questions.json: the open ones
# in full, the last closed ones with their answers). $null when no remote copy names it.
function Find-RemoteQuestion([string]$Root, [string]$Id) {
    if (-not (Test-QuestionId $Id)) { return $null }
    $rd = Join-Path $Root 'remote'
    if (-not (Test-Path -LiteralPath $rd)) { return $null }
    foreach ($f in @(Get-ChildItem -LiteralPath $rd -Directory -ErrorAction SilentlyContinue | ForEach-Object { Join-Path $_.FullName 'questions.json' } | Where-Object { Test-Path -LiteralPath $_ })) {
        $doc = Read-QFile $f
        if (-not $doc) { continue }
        foreach ($q in @($doc.open)) { if ($q -and [string]$q.id -ceq $Id) { return [pscustomobject]@{ Golem = [string]$doc.golem; Open = $true; State = 'open'; Question = $q; ReceivedAt = [string]$doc.receivedAt } } }
        foreach ($q in @($doc.history)) { if ($q -and [string]$q.id -ceq $Id) { return [pscustomobject]@{ Golem = [string]$doc.golem; Open = $false; State = [string]$q.state; Question = $q; ReceivedAt = [string]$doc.receivedAt } } }
    }
    $null
}
# cc-P770: every open question on the other PCs, from the copies their agents send (for the Sweep and the overseer).
function Get-RemoteOpenQuestions([string]$Root) {
    $out = @()
    $rd = Join-Path $Root 'remote'
    if (-not (Test-Path -LiteralPath $rd)) { return $out }
    foreach ($f in @(Get-ChildItem -LiteralPath $rd -Directory -ErrorAction SilentlyContinue | ForEach-Object { Join-Path $_.FullName 'questions.json' } | Where-Object { Test-Path -LiteralPath $_ })) {
        $doc = Read-QFile $f
        foreach ($q in @($doc.open)) { if ($q) { $out += [pscustomobject]@{ Golem = [string]$doc.golem; Id = [string]$q.id; Prompt = [string]$q.prompt; AskedAt = [string]$q.askedAt; Question = [string]$q.question; Choices = @($q.choices | ForEach-Object { [string]$_.label }); ReceivedAt = [string]$doc.receivedAt } } }
    }
    $out
}

# The answers a session for that Golem and prompt has not been given yet (oldest first)."""),
])

# ---------------------------------------------------------------- Remote-Agent.ps1 (G)
raw = open('Remote-Agent.ps1', encoding='utf-8', newline='').read()
print('agent run lines:')
for i, l in enumerate(raw.replace('\r\n', '\n').split('\n')):
    if 'Script' in l and ('& powershell' in l or 'Start-Process' in l or '$code' in l):
        print(i + 1, l[:160])
