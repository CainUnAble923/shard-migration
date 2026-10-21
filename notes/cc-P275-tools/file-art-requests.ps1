# cc-P275: the deployable traps' art requests (P201 design section 7.2), through P152's helper.
$ErrorActionPreference = 'Stop'
$helper = 'D:\ShatteredLegacy\scripts\art\New-ArtRequest.ps1'
$style = 'UO classic isometric statics, 2:1 dimetric, hard black outline, 16-bit palette, no anti-aliased halo. Size and shading key: the stock bear trap 0xB2C5 and the floor spikes 0x119A.'
$dest = @{ kind = 'game-item'; folder = 'player-package\vendor\shattered-legacy-art\art' }
$note = 'cc-P275 (design: shard-migration notes\cc-P201-deployable-traps-design.md section 7.2). Placeholders stand in until these land (DeployableTraps.SetArt / SpentArt); register the IDs with scripts\find-free-art.py and registry.csv, then swap the art ids in DeployableTraps.cs.'

function Slot([string]$file) { @{ file = $file; sizes = @(, @(44, 44)); transparent = $true; budgetKB = 8; margin = 1 } }

$requests = @(
    @{ Id = 'trap-snare-net'; Title = 'Snare net, sprung'
       Subject = 'A rope net bundled tight round nothing, its pegs pulled, lying on stone (the snare net after it has fired). Icon: a folded net with a wooden peg.'
       Slots = @((Slot 'snare-sprung.png'), (Slot 'snare-icon.png')) },
    @{ Id = 'trap-dart-launcher'; Title = 'Dart trap, floor launcher'
       Subject = 'A palm-sized iron plate with a spring tube and a dart tip showing, half-buried in the floor. Sprung: the tube open and empty, the spring out. Icon: the launcher on its side.'
       Slots = @((Slot 'dart-set.png'), (Slot 'dart-sprung.png'), (Slot 'dart-icon.png')) },
    @{ Id = 'trap-gas-canister'; Title = 'Gas trap, canister'
       Subject = 'A squat iron canister with a cork and a tiny bellows, a green glass window. Sprung: cracked, a green stain round it. Icon: the canister.'
       Slots = @((Slot 'gas-set.png'), (Slot 'gas-sprung.png'), (Slot 'gas-icon.png')) },
    @{ Id = 'trap-shackle-ring'; Title = 'Shackle trap, rune ring'
       Subject = 'A faint chalk rune circle on the floor with four small rune marks, blue-grey, one tile suggesting a 3 x 3 ring. Sprung: the circle scuffed through and broken. Icon: a rolled chalk and rune.'
       Slots = @((Slot 'shackle-set.png'), (Slot 'shackle-sprung.png'), (Slot 'shackle-icon.png')) },
    @{ Id = 'trap-icons'; Title = 'Pack icons for the stock traps'
       Subject = '44 x 44 pack icons matching the ground art of each: the bear trap (0xB2C5), caltrops (floor spikes 0x119A), the blast keg (0x1940, dark), the alarm cowbell (0x4C5A) and the practice net (a fishing net 0x0DC8 in a pale blue).'
       Slots = @((Slot 'icon-bear.png'), (Slot 'icon-caltrops.png'), (Slot 'icon-blast.png'), (Slot 'icon-alarm.png'), (Slot 'icon-practice-net.png')) }
)

foreach ($r in $requests) {
    & $helper -Id $r.Id -Title $r.Title -AskedBy 'P275' -Subject $r.Subject -Slots $r.Slots -Destination $dest -Style $style -Note $note | Out-String | Write-Output
}
