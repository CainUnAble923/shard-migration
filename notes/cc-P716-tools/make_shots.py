"""cc-P716: shots.ps1 = P675's, plus -OffScreen (the windows open off the desktop; PrintWindow still captures them)."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(HERE, '..', 'cc-P675-tools', 'shots.ps1'), encoding='utf-8').read()
s = s.replace("shots.ps1 (cc-P675, from P661", "shots.ps1 (cc-P716: P675's with -OffScreen; cc-P675, from P661", 1)
a = "    [int]$SettleSeconds = 30,\n"
assert s.count(a) == 1
s = s.replace(a, a + "    [switch]$OffScreen,   # cc-P716: windows off the desktop (Chase may be at the PC); PrintWindow still captures them\n")
a = "        $set = New-LegionSettings "
i = s.index(a)
j = s.index('\n', i) + 1
s = s[:j] + "        if ($OffScreen) { $set.window_position = [ordered]@{ X = -4000; Y = 40 } }\n" + s[j:]
open(os.path.join(HERE, 'shots.ps1'), 'w', encoding='utf-8', newline='').write(s)
print('wrote shots.ps1')
