"""cc-P707: writes proof-shard.ps1 here from cc-P281's, with the isle's map overlay mounted first in dataDirectories."""
import os

here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, '..', 'cc-P281-tools', 'proof-shard.ps1')).read()


def sub(old, new):
    global src
    assert src.count(old) == 1, old
    src = src.replace(old, new)


sub("proof-shard.ps1 (cc-P281): a private test shard for the guild hall screenshots, never the shared Test Shard.",
    "proof-shard.ps1 (cc-P707, from cc-P281's): a private test shard for the Wakening Isle play-through, never the shared\n"
    "  Test Shard. Adds the isle: <Work>\\..\\overlay (docker\\uo\\Build-MapOverlay.ps1 run on the client data copy, overlay.ps1)\n"
    "  is mounted at /var/lib/uo/client-data/sl-map-overlay and listed first in dataDirectories, as Start-TestShard.ps1 does.")
src = src.replace("sl-modernuo:cc-P281", "sl-modernuo:cc-P707")
sub("$name = 'sl-p281-proof'", "$name = 'sl-p707-proof'")
sub("'Shattered Legacy P281 proof'", "'Shattered Legacy P707 proof'")
sub("$j.dataDirectories = @('/var/lib/uo/client-data/classic-client')",
    "$j.dataDirectories = @('/var/lib/uo/client-data/sl-map-overlay', '/var/lib/uo/client-data/classic-client')")
sub("$c = ($cfg -replace '\\\\', '/')",
    "$c = ($cfg -replace '\\\\', '/')\n"
    "$ovDir = Join-Path (Split-Path $Work -Parent) 'overlay'\n"
    "if (-not (Test-Path (Join-Path $ovDir 'map1LegacyMUL.uop'))) { throw \"no isle overlay at $ovDir (run overlay.ps1)\" }\n"
    "$ov = ($ovDir -replace '\\\\', '/')")
sub("    -v 'D:/UO/tool-trials/client-data-copy:/var/lib/uo/client-data/classic-client:ro' $Image",
    "    -v 'D:/UO/tool-trials/client-data-copy:/var/lib/uo/client-data/classic-client:ro' `\n"
    "    -v \"${ov}:/var/lib/uo/client-data/sl-map-overlay:ro\" $Image")
sub("$j.settings.'autosave.enabled' = 'False'",
    "$j.settings.'autosave.enabled' = 'False'\n"
    "# cc-P707: the copy hold, shortened so the play-through can watch a copy reset (TutorialCopies.HoldAfterLeaving)\n"
    "$j.settings | Add-Member -NotePropertyName 'clusterf.tutorial.copyHoldMinutes' -NotePropertyValue \"$HoldMinutes\" -Force")
sub("    [int]$Port = 2596,", "    [int]$Port = 2596,\n    [int]$HoldMinutes = 2,")
open(os.path.join(here, 'proof-shard.ps1'), 'w', newline='\r\n').write(src)
print('wrote proof-shard.ps1')
