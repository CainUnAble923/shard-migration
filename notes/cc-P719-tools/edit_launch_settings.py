"""cc-P719: add Initialize-NewProfileDefaults to Launch-Settings.ps1, after Write-LaunchSettings."""
import sys

path = sys.argv[1]
with open(path, 'rb') as f:
    data = f.read()
crlf = b'\r\n' in data
text = data.decode('utf-8').replace('\r\n', '\n')

anchor = "    [IO.File]::WriteAllText($Path, ($s | ConvertTo-Json -Depth 10), (New-Object Text.UTF8Encoding $false))\n}\n"
assert text.count(anchor) == 1, 'anchor count %d' % text.count(anchor)
assert 'Initialize-NewProfileDefaults' not in text, 'already applied'

add = r"""
# cc-P719: what a NEW character's TazUO profile starts with. TazUO builds a character's first profile.json from
# <profiles>\default.json when there is one, else from its own defaults, and a key the file leaves out keeps TazUO's
# default (ProfileManager.Load, NewFromDefault). Its own defaults run all the time (Profile.AlwaysRun = true) and
# open the paperdoll at every login (LoginComplete; client patch 0009 adds the switch). New players start walking,
# with the paperdoll closed; Options > Gameplay > Movement > Always run turns running on.
$NewProfileDefaults = [ordered]@{ always_run = $false; sl_open_paperdoll_at_login = $false }

# Writes $ProfilesDir\default.json only where there is none, so a default the player saved (Options > Profile,
# "Set as default") is kept, and a character that already has a profile.json never reads it: a returning player's
# settings and layout stay theirs. Returns $true when it wrote the file.
function Initialize-NewProfileDefaults {
    param([string]$ProfilesDir)
    $f = Join-Path $ProfilesDir 'default.json'
    if (Test-Path -LiteralPath $f) { return $false }
    New-Item -ItemType Directory -Path $ProfilesDir -Force | Out-Null
    # No BOM, as Write-LaunchSettings.
    [IO.File]::WriteAllText($f, ($NewProfileDefaults | ConvertTo-Json), (New-Object Text.UTF8Encoding $false))
    return $true
}
"""
text = text.replace(anchor, anchor + add)
if crlf:
    text = text.replace('\n', '\r\n')
with open(path, 'wb') as f:
    f.write(text.encode('utf-8'))
print('ok, crlf=%s' % crlf)
