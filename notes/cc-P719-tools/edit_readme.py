import os
p = r"D:\UO\golems\Iron\ShatteredLegacy\client\README.md"
s = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
anchor = "| none (client-side only) |" + nl + nl + "## Rebasing"
assert s.count(anchor) == 1, s.count(anchor)
row = ("| `0009-new-character-defaults.patch` | `3212623f` plus 0001 to 0008 | **New character defaults** (cc-P719): "
       "`Profile.SlOpenPaperdollAtLogin` (saved as `sl_open_paperdoll_at_login`), on unless a profile says otherwise, so every "
       "profile saved before it keeps asking for its own paperdoll at login; off, `LoginComplete` skips that request "
       "(a paperdoll saved open still comes back with the saved gumps). The launcher writes `Data\Profiles\default.json` "
       "(`always_run` and this switch, both false) only where there is none, and TazUO builds each new character's profile "
       "from it (`player-package\payload\app\Launch-Settings.ps1`, `Initialize-NewProfileDefaults`). One line in each of "
       "two upstream files, 4 unit tests | none (client-side only) |")
s = s.replace(anchor, "| none (client-side only) |" + nl + row + nl + nl + "## Rebasing")
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
