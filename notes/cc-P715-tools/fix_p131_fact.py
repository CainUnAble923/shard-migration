# cc-P715: the P131 fact said any tool call after a STOPPED is Chase answering (the rule P715 replaces). Chase answers by
# typing in the session; that prompt, then its tool call, clears the STOPPED.
import sys
path = r'D:\UO\golem\tests\Golem.Tests.ps1'
t = open(path, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in t[:4000] else '\n'
old = ("        # Chase answers CC: its next tool use clears the STOPPED." + nl +
       "        [void](Invoke-Hook $w 'Activity' @{ hook_event_name = 'PostToolUse'; tool_name = 'Read' })" + nl)
new = ("        # Chase answers CC: his words in the session, then its next tool use, clear the STOPPED (cc-P715: a tool use alone" + nl +
       "        # does not; a background task can wake a stopped session for a turn of its own)." + nl +
       "        [void](Invoke-Hook $w 'Activity' @{ hook_event_name = 'PostToolUse'; tool_name = 'Read'; session_id = 'sess-a' })" + nl +
       "        Assert-True ((Get-WStatus $w).state -eq 'STOPPED') 'a tool use alone leaves it STOPPED'" + nl +
       "        [void](Invoke-Hook $w 'Prompt' @{ prompt = 'The second layout.'; session_id = 'sess-a' })" + nl +
       "        [void](Invoke-Hook $w 'Activity' @{ hook_event_name = 'PostToolUse'; tool_name = 'Read'; session_id = 'sess-a' })" + nl)
if new in t: print('already'); sys.exit(0)
if t.count(old) != 1: print('anchor count', t.count(old)); sys.exit(1)
open(path, 'w', encoding='utf-8', newline='').write(t.replace(old, new))
print('updated')
