# cc-P715: the fix in D:\UO\golem\golem.ps1. Each edit must match exactly once.
import sys

path = r'D:\UO\golem\golem.ps1'
t = open(path, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in t[:4000] else '\n'

def sub(old, new):
    global t
    old = old.replace('\n', nl); new = new.replace('\n', nl)
    c = t.count(old)
    if c != 1:
        print('edit matched %d times:\n%s' % (c, old[:200])); sys.exit(1)
    t = t.replace(old, new)

if 'cc-P715' in t:
    print('already applied'); sys.exit(0)

# 1. Helpers beside Clear-SessionHeld.
sub('''# Minutes since a UTC 's' stamp (huge when there is none).
function Get-AgeMin($t) {''',
'''# cc-P715: a prompt Claude Code queued into the session itself (a background task's or a subagent's notice), not words
# Chase typed. Such a turn is the session's own; it never answers a STOPPED.
function Test-MachinePrompt([string]$p) {
    $x = ([string]$p).TrimStart()
    return ($x -match '^(?i)<(task-notification|agent-message)\\b' -or $x -match '^(?i)Another Claude session sent a message')
}
# cc-P715: has Chase typed in session $sid since the stop at $atUtc (a round-trip UTC stamp)? Only that is an answer in the
# terminal; a tool call alone is not (P707, 10-27: a Monitor's notice woke the stopped session for one more turn).
function Test-ChaseSpokeSince([string]$sid, [string]$atUtc) {
    $p = [string](Get-Prop (Get-Session $sid) 'lastChasePromptUtc' '')
    if (-not $p) { return $false }
    if (-not $atUtc) { return $true }
    try { return ([datetime]::Parse($p, $null, [Globalization.DateTimeStyles]::RoundtripKind) -gt [datetime]::Parse($atUtc, $null, [Globalization.DateTimeStyles]::RoundtripKind)) } catch { return $true }
}
# Minutes since a UTC 's' stamp (huge when there is none).
function Get-AgeMin($t) {''')

# 2. The Prompt hook records when Chase (not a notification) typed, and only that ends a session's hold.
sub('''    Save-Session $SessionId @{ lastPromptUtc = (Get-Date).ToUniversalTime().ToString('s') }   # cc-P161: Chase typing there is activity
    if (Test-Path -LiteralPath $SessBook) { Clear-SessionHeld }
    $what = Test-GolemPhrase ([string]$h.prompt)''',
'''    # cc-P715: a queued notification (a background task's, a subagent's) is the session's own turn, not Chase.
    $byChase = -not (Test-MachinePrompt ([string]$h.prompt))
    $sv = @{ lastPromptUtc = (Get-Date).ToUniversalTime().ToString('s') }   # cc-P161: Chase typing there is activity
    if ($byChase) { $sv.lastChasePromptUtc = (Get-Date).ToUniversalTime().ToString('o') }
    Save-Session $SessionId $sv
    if ($byChase -and (Test-Path -LiteralPath $SessBook)) { Clear-SessionHeld }
    $what = Test-GolemPhrase ([string]$h.prompt)''')

# 3. The Activity hook clears a STOPPED only when Chase typed in that session after the stop.
sub('''    if (Test-Path -LiteralPath $SessBook) { Clear-SessionHeld }
    # Activity after a NEEDS YOU (or cc-P131 a STOPPED) means Chase answered: clear it.
    $ns = $null
    if (Test-Path -LiteralPath $StatFile) { try { $ns = Get-Content -LiteralPath $StatFile -Raw | ConvertFrom-Json } catch {} }
    $sp = [string](Get-Prop $ns 'stoppedPrompt' '')
    if ($sp) { Use-Lock { $sx = Get-State; $sx | Add-Member -NotePropertyName stoppedPrompt -NotePropertyValue '' -Force; Save-State $sx }; Log "activity after $sp STOPPED: Chase answered" }
    if ([string](Get-Prop $ns 'needsYou' '') -or $sp) { Write-Status '' } else { Write-Status }
    exit 0''',
'''    # Activity after a NEEDS YOU (or cc-P131 a STOPPED) means Chase answered: clear it.
    $ns = $null
    if (Test-Path -LiteralPath $StatFile) { try { $ns = Get-Content -LiteralPath $StatFile -Raw | ConvertFrom-Json } catch {} }
    $sp = [string](Get-Prop $ns 'stoppedPrompt' '')
    # cc-P715: for a STOPPED only when Chase typed in this session after the stop. A tool call of the session's own turn
    # (a background task's notice woke it) leaves the STOPPED, its question and the session's hold as they are.
    $kept = $false
    if ($sp -and -not (Test-ChaseSpokeSince $SessionId ([string](Get-Prop (Get-State) 'stoppedAt' '')))) { $kept = $true }
    if (-not $kept -and (Test-Path -LiteralPath $SessBook)) { Clear-SessionHeld }
    if ($sp -and -not $kept) { Use-Lock { $sx = Get-State; $sx | Add-Member -NotePropertyName stoppedPrompt -NotePropertyValue '' -Force; Save-State $sx }; Log "activity after $sp STOPPED: Chase answered" }
    if ($kept) { Write-Status } elseif ([string](Get-Prop $ns 'needsYou' '') -or $sp) { Write-Status '' } else { Write-Status }
    exit 0''')

# 4. The Stop hook: a STOPPED records when it stopped; the same prompt STOPPED again after Chase's words is a new stop.
sub('''    # D90: already handled only when it is not the one running.
    if ($n -eq [int]$state.lastHandled -and [string]$state.current -ne "P$n") { exit 0 }''',
'''    # D90: already handled only when it is not the one running.
    if ($n -eq [int]$state.lastHandled -and [string]$state.current -ne "P$n") {
        # cc-P715: unless its STOPPED was cleared by Chase's words in the terminal, nothing else runs and the prompt is
        # still claimed here: the session took his words and stopped again, so that is a new stop and is recorded.
        if ([string](Get-Prop $state 'stoppedPrompt' '') -or [string]$state.current -or -not (Find-PromptFile $HandedDir "P$n")) { exit 0 }
        Log "P$n STOPPED again after Chase's words in the terminal: a new stop"
    }''')

sub('''    $state | Add-Member -NotePropertyName stoppedWhy -NotePropertyValue $why -Force   # cc-P183: a wake re-checks it
    Save-State $state
    Set-SessionHeld "P$n STOPPED"   # cc-P161''',
'''    $state | Add-Member -NotePropertyName stoppedWhy -NotePropertyValue $why -Force   # cc-P183: a wake re-checks it
    $state | Add-Member -NotePropertyName stoppedAt -NotePropertyValue ((Get-Date).ToUniversalTime().ToString('o')) -Force   # cc-P715
    Save-State $state
    Set-SessionHeld "P$n STOPPED"   # cc-P161''')

open(path, 'w', encoding='utf-8', newline='').write(t)
print('applied')
