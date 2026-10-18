# cc-P140 render sheet: the Rootdeep Burrows lineup

Made by `scratchpad\p140_sheet.py` with the Burrows Bestiary renderer (`notes\art\bestiary\vd.py`, `render.py`): per
creature a folder with walk / attack / die / hit GIFs (direction 1, south, 1x, 110 ms a frame) and the first walk frame as PNG;
`contact-sheet-walk-1x.png` shows every first walk frame; `flags.json` is the data. Flags: no attack, hit or death frames;
a walk frame over 120 px tall (too big for a 1-tile mob). Hue and scale panels: `panel-*.png`, `hues\`.

| creature | file | layout | bytes | walk w x h | actions with frames | GIFs | flags |
|---|---|---|---|---|---|---|---|
| Gourdling | H-SpookyPumpkin.vd | high | 261,469 | 27 x 33 | 0 walk, 1 stand, 2 die, 3 die 2, 4 attack, 5 attack 2, 6 attack 3, 10 hit, 11 pillage, 15 block R, 16 block L | walk(7) attack(7) die(4) hit(7) | - |
| Crop Crow (stock bird 6, before the 1.5x upscale) | stock-body-6.vd | high | 79,964 | 15 x 8 | 0 walk, 1 stand, 2 die, 3 die 2, 4 attack, 5 attack 2, 6 attack 3, 17 fidget, 18 fidget 2, 19 fly, 20 land, 21 die in flight | walk(10) attack(4) die(4) | no hit frames |
| stock eagle 5 (for scale) | stock-body-5.vd | high | 193,847 | 28 x 19 | 0 walk, 1 stand, 2 die, 3 die 2, 4 attack, 10 hit, 11 pillage, 17 fidget, 19 fly, 20 land, 21 die in flight | walk(10) attack(4) die(4) hit(4) | - |
| Burrow Scamp Slinger | Kobold Bow.vd | high | 159,223 | 41 x 57 | 0 walk, 1 stand, 2 die, 3 die 2, 4 attack, 10 hit, 17 fidget, 18 fidget 2 | walk(10) attack(4) die(4) hit(4) | - |
| Cackler Scrapper | Gnoll.vd | high | 511,881 | 65 x 97 | 0 walk, 1 stand, 2 die, 3 die 2, 4 attack, 5 attack 2, 6 attack 3, 15 block R, 16 block L, 17 fidget, 18 fidget 2 | walk(10) attack(4) die(4) | no hit frames |
| Cackler Slasher | Gnoll Slasher.vd | high | 501,440 | 80 x 84 | 0 walk, 1 stand, 2 die, 3 die 2, 4 attack, 5 attack 2, 6 attack 3, 10 hit, 17 fidget, 18 fidget 2 | walk(10) attack(4) die(4) hit(4) | - |
| Cackler Veteran | Gnoll Veteran.vd | high | 489,937 | 56 x 84 | 0 walk, 1 stand, 2 die, 3 die 2, 4 attack, 5 attack 2, 6 attack 3, 10 hit, 17 fidget, 18 fidget 2 | walk(10) attack(4) die(4) hit(4) | - |
| Cackler Packleader | Gnoll Flind.vd | high | 555,484 | 65 x 97 | 0 walk, 1 stand, 2 die, 3 die 2, 4 attack, 5 attack 2, 6 attack 3, 10 hit, 15 block R, 16 block L, 17 fidget, 18 fidget 2 | walk(10) attack(4) die(4) hit(4) | - |
| Burrow Hog | DND Final Boar Animal.vd | low | 695,408 | 64 x 55 | 0 walk, 1 run, 2 stand, 3 eat, 4 alert, 5 attack, 6 attack 2, 7 hit, 8 die, 9 idle, 10 idle 2, 12 die 2 | walk(8) attack(7) die(8) hit(6) | - |
| Ledger Bat | VampireBat.vd | high | 996,492 | 92 x 100 | 0 walk, 1 stand, 2 die, 3 die 2, 4 attack, 5 attack 2, 6 attack 3, 7 bow, 8 crossbow, 10 hit, 11 pillage, 15 block R, 16 block L, 17 fidget, 18 fidget 2 | walk(8) attack(8) die(16) hit(6) | - |
| Hoarding Rat | Ratman Lord.vd | high | 2,431,848 | 135 x 120 | 0 walk, 1 stand, 2 die, 3 die 2, 4 attack, 5 attack 2, 6 attack 3, 15 block R, 16 block L, 17 fidget, 18 fidget 2 | walk(16) attack(16) die(17) | no hit frames |
| The Overdraft (crate creature, before the 1.5x upscale) | cratecreature_monster_1.vd | high | 950,937 | 53 x 54 | 0 walk, 1 stand, 2 die, 3 die 2, 4 attack, 5 attack 2, 6 attack 3, 10 hit, 12 stomp, 15 block R, 16 block L, 17 fidget, 18 fidget 2, 19 fly | walk(10) attack(6) die(5) hit(4) | - |
| Burrow Grub | Sand Maggot Small.vd | high | 524,020 | 78 x 40 | 0 walk, 1 stand, 2 die, 3 die 2, 4 attack, 5 attack 2, 10 hit, 17 fidget, 18 fidget 2 | walk(8) attack(6) die(8) hit(5) | - |
| Burrow Scamp | Vanguard kobold - L.vd | low | 290,765 | 31 x 37 | 0 walk, 1 run, 2 stand, 3 eat, 4 alert, 5 attack, 6 attack 2, 7 hit, 8 die, 9 idle, 10 idle 2, 12 die 2 | walk(5) attack(5) die(6) hit(5) | - |
| Redcap Scamp | Vanguard redcap kobold - L.vd | low | 296,138 | 31 x 39 | 0 walk, 1 run, 2 stand, 3 eat, 4 alert, 5 attack, 6 attack 2, 7 hit, 8 die, 9 idle, 10 idle 2, 12 die 2 | walk(5) attack(5) die(6) hit(5) | - |
| The Burrow Mother | Sand Maggot Large.vd | high | 2,053,217 | 150 x 76 | 0 walk, 1 stand, 2 die, 3 die 2, 4 attack, 5 attack 2, 6 attack 3, 10 hit, 11 pillage, 17 fidget, 18 fidget 2 | walk(8) attack(6) die(8) hit(5) | - |
| Rootling (Tree Fellow 1) | Tree Fellow 1.vd | high | 16,681,346 | 344 x 390 | 0 walk, 1 stand, 2 die, 3 die 2, 4 attack, 5 attack 2, 6 attack 3, 10 hit, 11 pillage, 15 block R, 16 block L, 17 fidget, 18 fidget 2 | walk(10) attack(5) die(10) hit(4) | walk frame 390 px tall (over 120: too big for a 1-tile mob) |
| Rootling (Tree Fellow 2) | Tree Fellow 2.vd | high | 7,045,826 | 220 x 229 | 0 walk, 1 stand, 2 die, 3 die 2, 4 attack, 5 attack 2, 6 attack 3, 10 hit, 11 pillage, 15 block R, 16 block L, 17 fidget, 18 fidget 2 | walk(10) attack(5) die(10) hit(4) | walk frame 229 px tall (over 120: too big for a 1-tile mob) |
| Rootling (Tree Fellow 3) | Tree Fellow 3.vd | high | 6,095,102 | 198 x 213 | 0 walk, 1 stand, 2 die, 3 die 2, 4 attack, 5 attack 2, 6 attack 3, 10 hit, 11 pillage, 15 block R, 16 block L, 17 fidget, 18 fidget 2 | walk(10) attack(5) die(10) hit(4) | walk frame 213 px tall (over 120: too big for a 1-tile mob) |
| Sporecap (Myconid Red) | Myconid Red.vd | high | 682,762 | 59 x 96 | 0 walk, 1 stand, 2 die, 4 attack, 5 attack 2, 10 hit, 17 fidget | walk(9) attack(8) die(7) hit(6) | - |
| Sporecap (Myconid Blue) | Myconid Blue.vd | high | 1,091,728 | 61 x 97 | 0 walk, 1 stand, 2 die, 4 attack, 5 attack 2, 10 hit, 13 cast, 17 fidget | walk(10) attack(8) die(10) hit(8) | - |
| Bramblehulk | Thorned Hulk.vd | high | 1,868,359 | 127 x 139 | 0 walk, 1 stand, 2 die, 4 attack, 5 attack 2, 10 hit, 17 fidget | walk(7) attack(5) die(12) hit(4) | walk frame 139 px tall (over 120: too big for a 1-tile mob) |
| Dawnshard | CaveElemental.vd | high | 726,591 | 70 x 96 | 0 walk, 1 stand, 2 die, 4 attack, 10 hit, 17 fidget | walk(8) attack(6) die(8) hit(4) | - |
| Seamguard | Stone Golem.vd | high | 1,919,586 | 127 x 147 | 0 walk, 1 stand, 2 die, 4 attack, 5 attack 2, 10 hit, 12 stomp, 17 fidget, 18 fidget 2 | walk(10) attack(7) die(11) hit(8) | walk frame 147 px tall (over 120: too big for a 1-tile mob) |
| Gloomling | Underdark Spider Hatchling.vd | high | 1,088,149 | 96 x 81 | 0 walk, 1 stand, 2 die, 3 die 2, 4 attack, 5 attack 2, 6 attack 3, 10 hit, 11 pillage, 15 block R, 16 block L, 17 fidget, 18 fidget 2, 19 fly | walk(10) attack(4) die(4) hit(4) | - |
| Gloomspinner | Underdark Spider.vd | high | 1,853,286 | 125 x 115 | 0 walk, 1 stand, 2 die, 3 die 2, 4 attack, 5 attack 2, 6 attack 3, 10 hit, 11 pillage, 15 block R, 16 block L, 17 fidget, 18 fidget 2, 19 fly | walk(10) attack(4) die(4) hit(4) | - |
| Gloomweaver | Underdark Spider Mage.vd | high | 1,933,944 | 134 x 109 | 0 walk, 1 stand, 2 die, 3 die 2, 4 attack, 5 attack 2, 6 attack 3, 10 hit, 11 pillage, 15 block R, 16 block L, 17 fidget, 18 fidget 2, 19 fly | walk(10) attack(4) die(4) hit(4) | - |
| The Gloom Queen | Drider Female.vd | high | 1,945,333 | 193 x 166 | 0 walk, 1 stand, 2 die, 3 die 2, 4 attack, 5 attack 2, 6 attack 3, 12 stomp, 15 block R, 16 block L, 17 fidget, 18 fidget 2 | walk(10) attack(4) die(4) | no hit frames; walk frame 166 px tall (over 120: too big for a 1-tile mob) |
