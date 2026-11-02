import os, sys
os.chdir('kit770')
p = 'golem.ps1'
raw = open(p, encoding='utf-8', newline='').read(); nl = '\r\n' if '\r\n' in raw else '\n'; s = raw.replace('\r\n', '\n')
pairs = [
(r"""    # on its way, or within 10 minutes of the last self-wake; Test-SelfWake's own rules (usage, pace, spacing) still hold.
    if (-not $cur -and (Get-RunNextName) -and -not (Get-Prop $st 'wakePending' $null) -and -not [bool](Get-Prop $st 'stoppedByHand' $false) -and""",
r"""    # on its way (a refused wake waits for its retry time); Test-SelfWake's own rules (usage, pace, the autoWakeMinMinutes
    # spacing) still hold, and a refusal is logged and retried at a later watch.
    if (-not $cur -and (Get-RunNextName) -and -not [bool](Get-Prop $st 'stoppedByHand' $false) -and"""),
(r"""        $lwR = Get-Prop $st 'lastSelfWake' $null
        $recentR = $false; if ($lwR) { try { $recentR = (($NowTime - [datetime]::Parse([string]$lwR.at)).TotalMinutes -lt 10) } catch {} }
        if ($rnPick -and -not $recentR) {""",
r"""        # A wake refused for a reason that clears (usage, the spacing) waits until its retry time.
        $wpR = Get-Prop $st 'wakePending' $null
        $waitR = $false; if ($wpR) { try { $waitR = ([datetime]::Parse([string](Get-Prop $wpR 'retryAt' '')) -gt $NowTime) } catch {} }
        if ($rnPick -and -not $waitR) {"""),
]
for old, new in pairs:
    n = s.count(old)
    if n != 1: sys.exit('matches %d for %r' % (n, old[:70]))
    s = s.replace(old, new)
open(p, 'w', encoding='utf-8', newline='').write(s.replace('\n', nl)); print('ok')
