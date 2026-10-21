#Requires -Version 5.1
<#
  Answer-Question.ps1 (cc-P216): Chase's answer to a Golem's question, from any console. Submit-GolemAnswer
  (Questions.ps1) writes answers\<id>.json once and closes the question (a closed question, a second answer, a choice it
  does not have, or text where it takes none are refused). Then the Golem resumes: golem.ps1 -Event Answer clears what
  the question held (a STOPPED prompt goes back first in the queue, as Retry stopped prompt; NEEDS YOU is cleared) and,
  when there is something to carry on, a session is woken on the prompt's own model (golem.ps1 -Event SelfWake -Manual,
  as Retry-Stopped.ps1). The new session is given the answer in its hand-off, as data.

      Answer-Question.ps1 -Id <question id> [-Choice <0..3>] [-TextB64 <base64 of UTF-8>] [-Text <words>]
                          [-Who <login>] [-Source console|shard-console|remote|email|terminal] [-NoWake]
                          [-Golem <name>] [-Root D:\UO\golem]

  The web console and the remote agent pass the words as -TextB64, so nothing Chase types is ever parsed by a shell or
  as a parameter. Exit 0: answered (and resumed, or kept for the prompt's next session); 1: refused. ASCII only.
#>
param(
    [Parameter(Mandatory)][string]$Id,
    [int]$Choice = -1,
    [string]$TextB64 = '',
    [string]$Text = '',
    [string]$Who = '',
    [string]$Source = 'console',
    [switch]$NoWake,
    [string]$Golem = '',
    [string]$Root = '',
    [string]$PromptDir = '',   # testing: a fixture prompt folder
    [string]$Cli = '',         # testing: a CLI stub for the wake
    [switch]$NoMail            # testing
)
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $Root) { $Root = $Here }
. (Join-Path $Here 'Questions.ps1')
if ($TextB64) {
    if ($TextB64 -notmatch '^[A-Za-z0-9+/]{1,12000}={0,2}$') { Write-Host 'Not answered: the text is not base64.'; exit 1 }
    try { $Text = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($TextB64)) } catch { Write-Host 'Not answered: the text is not base64.'; exit 1 }
}
$r = Submit-GolemAnswer -Root $Root -Id $Id -Choice $Choice -Text $Text -Who $Who -Source $Source
if (-not $r.Ok) { Write-Host ('Not answered: ' + $r.Why); exit 1 }
Write-Host ('Answered ' + $Id + ': ' + $(if ($r.Answer.choiceLabel) { '"' + $r.Answer.choiceLabel + '"' } else { '' }) + $(if ($r.Answer.text) { $(if ($r.Answer.choiceLabel) { ' and ' } else { '' }) + 'your words' } else { '' }) + ' (' + $r.Path + ').')
if (-not $Golem) { $Golem = [string]$r.Question.golem }
$who = @(); if ($Golem -and $Golem -ne 'Golem') { $who = @('-Golem', $Golem) }
$extra = @(); if ($PromptDir) { $extra += @('-PromptDir', $PromptDir) }; if ($NoMail) { $extra += '-NoMail' }; if ($Cli) { $extra += @('-Cli', $Cli) }
$g = Join-Path $Here 'golem.ps1'
$out = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $g -Event Answer -Question $Id -Root $Root @who @extra
$code = $LASTEXITCODE
Write-Host (($out | Out-String).Trim())
if ($code -eq 3 -or $code -ne 0) { exit $(if ($code -eq 3) { 0 } else { 1 }) }
if ($NoWake) { Write-Host 'Not woken (-NoWake): wake the Golem when you are ready.'; exit 0 }
$w = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $g -Event SelfWake -Manual -Root $Root @who @extra
$code = $LASTEXITCODE
Write-Host (($w | Out-String).Trim())
# The answer is kept either way: a wake refused now (usage, the 2-minute rule) is the console's Wake later.
exit 0
