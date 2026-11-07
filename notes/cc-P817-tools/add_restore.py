r"""cc-P817: the shot runners restore a minimized client window without activating it (SW_SHOWNOACTIVATE) before each
capture: Chase was using this PC (a game in front), new client windows came up minimized, and a minimized window
captures as its title bar. The window never takes focus from him.

    python -P add_restore.py creation817.ps1 shots817.ps1
"""
import sys

HELPER = r'''
# cc-P817: restore a minimized client window without activating it (it never takes focus), then capture.
if (-not ('P817.Win' -as [type])) {
    Add-Type -Namespace P817 -Name Win -MemberDefinition '[DllImport("user32.dll")] public static extern bool IsIconic(IntPtr h); [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int c);'
}
function Save-LegionShot817([IntPtr]$Window, [string]$Path) {
    if ($Window -ne [IntPtr]::Zero -and [P817.Win]::IsIconic($Window)) { [void][P817.Win]::ShowWindow($Window, 4); Start-Sleep -Milliseconds 900 }
    Save-LegionShot $Window $Path
}
'''

for p in sys.argv[1:]:
    s = open(p, encoding='utf-8').read()
    anchor = ". 'D:\\UO\\golem\\LegionTest.ps1'\n"
    assert s.count(anchor) == 1, (p, s.count(anchor))
    s = s.replace(anchor, anchor + HELPER, 1)
    lines = s.split('\n')
    out = []
    for line in lines:
        if 'Save-LegionShot ' in line and not line.lstrip().startswith('#') and 'function Save-LegionShot817' not in line \
                and 'Save-LegionShot $Window $Path' not in line and 'Save-LegionShot)' not in line:
            line = line.replace('Save-LegionShot ', 'Save-LegionShot817 ')
        out.append(line)
    open(p, 'w', encoding='utf-8').write('\n'.join(out))
    print(p, sum('Save-LegionShot817 ' in l for l in out))
