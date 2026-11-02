import os, sys
os.chdir('kit770')
p = 'golem.ps1'
raw = open(p, encoding='utf-8', newline='').read(); nl = '\r\n' if '\r\n' in raw else '\n'; s = raw.replace('\r\n', '\n')
old = r"""    if (-not $DryRun -and -not $held) { Use-Lock { [IO.File]::WriteAllText($RunNextFile, $pf.Name + "`r`n", [Text.Encoding]::ASCII); Remove-Item -LiteralPath ($RunNextFile + '.after'), ($RunNextFile + '.answered') -Force -ErrorAction SilentlyContinue } }
    Log "run next: P$n ($($pf.Name)) picked"
"""
new = r"""    if (-not $DryRun -and -not $held) { Use-Lock { [IO.File]::WriteAllText($RunNextFile, $pf.Name + "`r`n", [Text.Encoding]::ASCII); Remove-Item -LiteralPath ($RunNextFile + '.after'), ($RunNextFile + '.answered') -Force -ErrorAction SilentlyContinue } }
    Log "run next: P$n ($($pf.Name)) picked"
    # cc-P770: a Golem that rested because its queue was empty is off (no ENABLED), and an off Golem's watch does nothing.
    # A pick is work asked of it, so it is on again for it; a Golem rested by hand (Stop-Golem.ps1, "Golem, stop") stays off.
    if (-not (Test-Path -LiteralPath $Enabled) -and -not [bool](Get-Prop (Get-State) 'stoppedByHand' $false)) {
        if (-not $DryRun) { New-Item -ItemType File -Path $Enabled -Force | Out-Null }
        Log "run next: the Golem rested with an empty queue; on again for P$n"
    }
"""
n = s.count(old)
if n != 1: sys.exit('matches %d' % n)
s = s.replace(old, new)
open(p, 'w', encoding='utf-8', newline='').write(s.replace('\n', nl)); print('ok')
