"""cc-P713: move the README's app\\map\\ removal into a function (Remove-SosMapReadme) the tests can reach."""
import sys

p = sys.argv[1]
s = open(p, 'rb').read().decode('ascii')


def sub(old, new):
    global s
    assert s.count(old) == 1, (s.count(old), old[:70])
    s = s.replace(old, new)


sub(r"""$sosOn = $SosMap -eq 'on'
""", r"""$sosOn = $SosMap -eq 'on'
# cc-P713: the README with its app\map\ entry left out (the line naming the folder and the indented ones under it), for
# a package with the switch off. Exactly one entry, or the build stops: a reworded README must not ship a stale credit.
function Remove-SosMapReadme([string]$text) {
    $rx = [regex]'(?m)^  app\\map\\ [^\r\n]*\r?\n(?: {15}[^\r\n]*\r?\n)*'
    if ($rx.Matches($text).Count -ne 1) { throw "SOS MAP SWITCH: payload\README.txt has no single app\map\ entry to leave out. Not building." }
    return $rx.Replace($text, '')
}
""")
sub(r"""    $rmPath = Join-Path $stage 'README.txt'
    $rmText = [IO.File]::ReadAllText($rmPath)
    $rmRx = [regex]'(?m)^  app\\map\\ [^\r\n]*\r?\n(?: {15}[^\r\n]*\r?\n)*'
    if ($rmRx.Matches($rmText).Count -ne 1) { throw "SOS MAP SWITCH: payload\README.txt has no single app\map\ entry to leave out. Not building." }
    [IO.File]::WriteAllText($rmPath, $rmRx.Replace($rmText, ''), (New-Object Text.ASCIIEncoding))
""", r"""    $rmPath = Join-Path $stage 'README.txt'
    [IO.File]::WriteAllText($rmPath, (Remove-SosMapReadme ([IO.File]::ReadAllText($rmPath))), (New-Object Text.ASCIIEncoding))
""")
sub(r"""# cc-P713: only with vendor\sos-trammel-map\switch.txt on. Off, files\ is not read, and the staged README loses its
# app\map\ entry (the line naming the folder and the indented ones under it), so it reads as it did before cc-P674.
""", r"""# cc-P713: only with vendor\sos-trammel-map\switch.txt on. Off, files\ is not read, and the staged README loses its
# app\map\ entry (Remove-SosMapReadme), so it reads as it did before cc-P674.
""")
open(p, 'wb').write(s.encode('ascii'))
print('ok')
