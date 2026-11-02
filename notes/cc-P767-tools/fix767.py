import os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kit767'))

p = 'Codex.ps1'
raw = open(p, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in raw else '\n'
s = raw.replace('\r\n', '\n')
a = r"""    [pscustomobject]@{ usedPct = $used; resets = $resets; text = ([string]$used + '% (resets ' + $resets + ')') }"""
b = r"""    [pscustomobject]@{ usedPct = $used; resets = $resets; text = $(if ($passed) { '0% (a new window: it reset after the reading)' } else { [string]$used + '% (resets ' + $resets + ')' }) }"""
assert s.count(a) == 1
s = s.replace(a, b)
open(p, 'w', encoding='utf-8', newline='').write(s.replace('\n', nl))

p = r'join/Sweep.ps1'
raw = open(p, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in raw else '\n'
s = raw.replace('\r\n', '\n')
a = "Get-Content D:\\UO\\golem\\golem-ShadowIron.log -Tail 3\n"
b = a + r"""# cc-P767: both Codex lanes side by side: each account's 5-hour and week percent and resets, fresh or the last good
# reading's age, today's runs, and idle time today with the reasons.
'Codex lanes:'; & powershell.exe -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Codex.ps1 -Action lanes | ForEach-Object { '  ' + $_ }
"""
assert s.count(a) == 1
s = s.replace(a, b)
open(p, 'w', encoding='utf-8', newline='').write(s.replace('\n', nl))
print('ok', repr(nl))
