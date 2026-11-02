# cc-P715: adds the P715 facts to D:\UO\golem\tests\Golem.Tests.ps1, after the last P216 fact.
import sys

path = r'D:\UO\golem\tests\Golem.Tests.ps1'
anchor = '# ---- cc-P157: every email in plain English, in one shape'
facts = r'''
    # cc-P715: Iron asked P707's question at 18:39:25 on 10-27 and said P707 STOPPED at 18:40:43. A Monitor of that session
    # then expired, its notification woke the session for one more turn (a TaskStop, 18:40:49), and the Activity hook took
    # that tool call for Chase answering: it cleared the STOPPED and closed the question as "no longer STOPPED or
    # running". The session said P707 STOPPED again, which the Stop hook skipped as already handled.
    Fact 'P715_AQuestionStaysOpenWhileItsStoppedPromptWaits' {
        $w = New-AskWorld
        [void](& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $p216Here 'Ask-Chase.ps1') -Question 'The run was killed for low memory. How should I go on?' `
            -Choice 'Resume now|I restart the run' -Choice2 'Resume tonight|I wait for the night' -Root $w.Root -PromptDir $w.Prompts -NoMail)
        $id = (@(Get-WQuestions $w 'open'))[0].id
        $line = 'P100 STOPPED: asked Chase (' + $id + ')'
        [void](Invoke-HookX $w 'Stop' @{ last_assistant_message = $line; session_id = 'sess-a' } $w.CliArgs)
        Assert-True ((Get-WState $w).stoppedPrompt -eq 'P100') 'STOPPED recorded'
        # The session's own background task wakes it: a machine notification, then one tool call and the same line again.
        [void](Invoke-HookX $w 'Prompt' @{ prompt = "<task-notification>`n<task-id>bok7ze2rm</task-id>`n<summary>Monitor event</summary>`n</task-notification>"; session_id = 'sess-a' } $w.CliArgs)
        [void](Invoke-HookX $w 'Activity' @{ hook_event_name = 'PreToolUse'; tool_name = 'TaskStop'; session_id = 'sess-a' } $w.CliArgs)
        [void](Invoke-HookX $w 'Activity' @{ hook_event_name = 'PostToolUse'; tool_name = 'TaskStop'; session_id = 'sess-a' } $w.CliArgs)
        [void](Invoke-HookX $w 'Stop' @{ last_assistant_message = ('P100 is still stopped and waiting.' + "`n`n" + $line); session_id = 'sess-a' } $w.CliArgs)
        $q = Get-GolemQuestion $w.Root $id
        Assert-True ($q.state -eq 'open') ('the question stays open: ' + $q.state + ' ' + $q.closedWhy)
        $st = Get-WState $w
        Assert-True ($st.stoppedPrompt -eq 'P100') ('still STOPPED: "' + $st.stoppedPrompt + '"')
        $s = Get-WStatus $w
        Assert-True ($s.state -eq 'STOPPED' -and $s.questionsOpen -eq 1) ('status.json: ' + $s.state + ' ' + $s.questionsOpen)
        Assert-True ((Get-WLog $w) -notmatch 'activity after P100 STOPPED: Chase answered') 'no "Chase answered" from the session''s own turn'
        # Chase's answer on the card is taken, and P100 is retried with it.
        $r = Invoke-Answer $w $id 0
        Assert-True ($r.Code -eq 0) ('answered: ' + $r.Out)
        Assert-True ((Get-GolemQuestion $w.Root $id).state -eq 'answered') 'closed as answered'
        Assert-True (-not (Get-WState $w).stoppedPrompt -and (Test-Path -LiteralPath (Join-Path $w.Queue 'cc-P100-a.md'))) 'P100 back in the queue'
    }

    Fact 'P715_ChaseTypingInTheStoppedSessionStillClearsIt' {
        $w = New-AskWorld
        [void](Invoke-HookX $w 'Stop' @{ last_assistant_message = 'P100 STOPPED: which world'; session_id = 'sess-a' } $w.CliArgs)
        $id = (@(Get-WQuestions $w 'open'))[0].id
        [void](Invoke-HookX $w 'Prompt' @{ prompt = 'Keep the Tokuno world and carry on.'; session_id = 'sess-a' } $w.CliArgs)
        [void](Invoke-HookX $w 'Activity' @{ hook_event_name = 'PostToolUse'; tool_name = 'Bash'; session_id = 'sess-a' } $w.CliArgs)
        Assert-True (-not (Get-WState $w).stoppedPrompt) ('cleared by Chase''s words: "' + (Get-WState $w).stoppedPrompt + '"')
        $q = Get-GolemQuestion $w.Root $id
        Assert-True ($q.state -eq 'expired') ('the question closes: ' + $q.state)
        Assert-True ((Get-WLog $w) -match 'activity after P100 STOPPED: Chase answered') 'logged'
        # Chase's words were taken and the session stopped on the same prompt again: that is a new stop, recorded.
        [void](Invoke-HookX $w 'Stop' @{ last_assistant_message = 'P100 STOPPED: the Tokuno world is missing too'; session_id = 'sess-a' } $w.CliArgs)
        Assert-True ((Get-WState $w).stoppedPrompt -eq 'P100') ('the second stop is recorded: "' + (Get-WState $w).stoppedPrompt + '"')
        Assert-True (@(Get-WQuestions $w 'open').Count -eq 1) 'with a question of its own'
        Assert-True ((Get-WStatus $w).state -eq 'STOPPED') 'STOPPED'
        # Another session of this Golem typing does not clear a stop it did not see.
        [void](Invoke-HookX $w 'Prompt' @{ prompt = 'hello'; session_id = 'sess-z' } $w.CliArgs)
        [void](Invoke-HookX $w 'Activity' @{ hook_event_name = 'PostToolUse'; tool_name = 'Bash'; session_id = 'sess-a' } $w.CliArgs)
        Assert-True ((Get-WState $w).stoppedPrompt -eq 'P100') 'still STOPPED'
    }
'''

t = open(path, encoding='utf-8', newline='').read()
if 'P715_AQuestionStaysOpen' in t:
    print('already there'); sys.exit(0)
i = t.index(anchor)
# the facts belong inside the P216 block, before its closing brace
j = t.rindex('}', 0, i)
nl = '\r\n' if '\r\n' in t[:2000] else '\n'
block = facts.replace('\r\n', '\n').replace('\n', nl)
t = t[:j] + block.lstrip('\r\n').rstrip() .join(['', '']) + nl + t[j:] if False else t[:j] + block.lstrip('\r\n') + t[j:]
open(path, 'w', encoding='utf-8', newline='').write(t)
print('added')
