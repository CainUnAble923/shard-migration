# cc-P858 review: what is placed in the world

Two things are placed, both only while a festival season is on (FestivalMarket, `RewardStores/FestivalStore.cs`):
the Festival stall as before (P760's six things, unchanged, `notes/cc-P760-review/placed.md`) and now the fortune
teller's wagon beside it. The lamps are store items, placed by players; nothing seeds a lamp.

## The wagon (addon `FortuneTellerWagon`)

- Origin **3647,2632,0** Trammel (setting `clusterf.festival.wagonAt`, default), main's New Haven (the Siege of Sosaria
  land): the west edge of the paved square, south of the open forge, 8 tiles east of the stall's barrel. Its long side
  runs north-south; the stair comes down the south end onto the street, climbing north. One variant only (no east/south
  versions of this design exist); nothing turned.
- Footprint x 3645..3650, y 2626..2641 (with the stair); the stair's foot is 3647,2642 and 3648,2642.
- Seeded with the stall, by serial, taken down with it; a world whose stall is already up gets it at the next load or
  hourly check (`TopUpWagon`).

### Our change: the stair (14 parts, light wood 0x0721 block / 0x0722 north step, hue 2418 as the wagon's wood)

| Item | Location | Facing | What |
|---|---|---|---|
| 0x0722 wooden stairs | 3647,2641,0 | climbs north | step |
| 0x0722 wooden stairs | 3647,2640,5 | climbs north | step |
| 0x0722 wooden stairs | 3647,2639,10 | climbs north | step |
| 0x0722 wooden stairs | 3647,2638,15 | climbs north | step |
| 0x0721 wood | 3647,2639,0 | - | block under the upper steps |
| 0x0721 wood | 3647,2638,0 | - | block under the upper steps |
| 0x0721 wood | 3647,2638,5 | - | block under the upper steps |
| 0x0722 wooden stairs | 3648,2641,0 | climbs north | step |
| 0x0722 wooden stairs | 3648,2640,5 | climbs north | step |
| 0x0722 wooden stairs | 3648,2639,10 | climbs north | step |
| 0x0722 wooden stairs | 3648,2638,15 | climbs north | step |
| 0x0721 wood | 3648,2639,0 | - | block under the upper steps |
| 0x0721 wood | 3648,2638,0 | - | block under the upper steps |
| 0x0721 wood | 3648,2638,5 | - | block under the upper steps |

The author's ladder 0x3DB4 (a 10-high block at 0,6, z 10) is left out.

### Proof in this folder

- `main-stall-wagon-3647-2632.jpg`: isorender of main's SoS ground with the stall and the wagon (hues not drawn).
- `main-wagon-cutaway.jpg`: the same with the roof off (parts below z 35): the inside and the stair to the porch.
- `wagon-design.jpg`: the wagon alone, our design; `lamp-art-1..3.jpg`: every lamp's unlit and lit art.
- `release-vanilla-stall-yard.jpg`: the release's map (vanilla) at the stall's spot: the ruin yard (see the notes).
- `shots/`: the TazUO shots from the default camera; `walk-log.txt`: the stair walked up and down, each step's z.

### Every part (212), one line each

| # | Item | Name (tiledata) | Location | Hue | Light | Shown name |
|---|---|---|---|---|---|---|
| 1 | 0x5C73 | BritanianShip Ladder | 3649,2627,21 | 0 | - | - |
| 2 | 0x5C75 | BritanianShip PropsD | 3649,2626,0 | 0 | - | - |
| 3 | 0x0FAE | barrel | 3649,2636,24 | 0 | - | - |
| 4 | 0x1E40 | bearskin rug | 3648,2633,19 | 0 | - | - |
| 5 | 0x1E41 | bearskin rug | 3648,2632,19 | 0 | - | - |
| 6 | 0x1E42 | bearskin rug | 3648,2631,19 | 0 | - | - |
| 7 | 0x11F1 | hammock | 3648,2629,21 | 0 | - | - |
| 8 | 0x2995 | wooden wall | 3649,2630,15 | 0 | - | - |
| 9 | 0x0ADA |  | 3649,2634,19 | 0 | - | - |
| 10 | 0x0ADA |  | 3649,2635,19 | 0 | - | - |
| 11 | 0x0ADA |  | 3648,2634,19 | 0 | - | - |
| 12 | 0x0ADA |  | 3649,2633,19 | 0 | - | - |
| 13 | 0x0ADA |  | 3648,2632,19 | 0 | - | - |
| 14 | 0x0ADA |  | 3648,2631,19 | 0 | - | - |
| 15 | 0x0ADA |  | 3648,2633,19 | 0 | - | - |
| 16 | 0x0ADA |  | 3649,2632,19 | 0 | - | - |
| 17 | 0x0ADA |  | 3649,2631,19 | 0 | - | - |
| 18 | 0x0B2D | wooden bench | 3648,2627,21 | 0 | - | - |
| 19 | 0x26F9 | bark roofing | 3650,2631,41 | 0 | - | - |
| 20 | 0x2995 | wooden wall | 3649,2634,15 | 0 | - | - |
| 21 | 0x26F9 | bark roofing | 3650,2629,41 | 0 | - | - |
| 22 | 0x0ADA |  | 3649,2630,18 | 0 | - | - |
| 23 | 0x0ADA |  | 3649,2629,18 | 0 | - | - |
| 24 | 0x26F9 | bark roofing | 3649,2629,44 | 0 | - | - |
| 25 | 0x0ADA |  | 3648,2629,18 | 0 | - | - |
| 26 | 0x0ADA |  | 3648,2630,18 | 0 | - | - |
| 27 | 0x299B | wooden wall | 3649,2635,38 | 0 | - | - |
| 28 | 0x0ADA |  | 3648,2635,19 | 0 | - | - |
| 29 | 0x1E24 | books | 3646,2634,24 | 0 | - | - |
| 30 | 0x1F13 | worldgem bit | 3646,2633,30 | 0 | - | - |
| 31 | 0x1F1B | magical crystal | 3646,2634,33 | 0 | - | - |
| 32 | 0x4C3B | Wall_Shelves_wood | 3646,2633,19 | 0 | - | - |
| 33 | 0x4C3B | Wall_Shelves_wood | 3646,2632,19 | 0 | - | - |
| 34 | 0x5C75 | BritanianShip PropsD | 3647,2626,1 | 0 | - | - |
| 35 | 0x1E21 | books | 3646,2634,19 | 0 | - | - |
| 36 | 0xA586 | Mage_Throne_SOUTH | 3647,2631,19 | 0 | - | - |
| 37 | 0xA495 | pillow_moon_South | 3646,2629,25 | 0 | - | - |
| 38 | 0x4A93 | Daemon Mask EAST | 3646,2633,20 | 0 | - | - |
| 39 | 0x1E48 | bearskin rug | 3646,2631,19 | 0 | - | - |
| 40 | 0x1E43 | bearskin rug | 3647,2631,19 | 0 | - | - |
| 41 | 0x1E44 | bearskin rug | 3647,2632,19 | 0 | - | - |
| 42 | 0x1E45 | bearskin rug | 3647,2633,19 | 0 | - | - |
| 43 | 0x1E46 | bearskin rug | 3646,2633,19 | 0 | - | - |
| 44 | 0x1E47 | bearskin rug | 3646,2632,19 | 0 | - | - |
| 45 | 0x2937 | abacus | 3646,2632,31 | 0 | - | - |
| 46 | 0x0ADA |  | 3647,2632,19 | 0 | - | - |
| 47 | 0x0ADA |  | 3647,2631,19 | 0 | - | - |
| 48 | 0x0ADA |  | 3646,2631,19 | 0 | - | - |
| 49 | 0x0ADA |  | 3646,2634,19 | 0 | - | - |
| 50 | 0x0ADA |  | 3647,2635,19 | 0 | - | - |
| 51 | 0x0ADA |  | 3646,2635,19 | 0 | - | - |
| 52 | 0x0ADA |  | 3647,2634,19 | 0 | - | - |
| 53 | 0x0ADA |  | 3646,2633,19 | 0 | - | - |
| 54 | 0x0ADA |  | 3647,2633,19 | 0 | - | - |
| 55 | 0x0ADA |  | 3646,2632,19 | 0 | - | - |
| 56 | 0x423F | Soulforge Base East | 3647,2632,19 | 0 | - | - |
| 57 | 0x104C | clock | 3646,2629,31 | 0 | - | - |
| 58 | 0x11F0 | hammock | 3646,2629,21 | 0 | - | - |
| 59 | 0x0B2D | wooden bench | 3647,2627,21 | 0 | - | - |
| 60 | 0x2C35 | wooden shingles | 3646,2635,38 | 0 | - | - |
| 61 | 0x2C35 | wooden shingles | 3646,2634,38 | 0 | - | - |
| 62 | 0x2C35 | wooden shingles | 3646,2633,38 | 0 | - | - |
| 63 | 0x2C35 | wooden shingles | 3646,2632,38 | 0 | - | - |
| 64 | 0x2C35 | wooden shingles | 3646,2631,38 | 0 | - | - |
| 65 | 0x2C35 | wooden shingles | 3646,2630,38 | 0 | - | - |
| 66 | 0x2C35 | wooden shingles | 3646,2629,38 | 0 | - | - |
| 67 | 0x0ADA |  | 3647,2629,18 | 0 | - | - |
| 68 | 0x0ADA |  | 3646,2629,18 | 0 | - | - |
| 69 | 0x3EAC | deck | 3645,2634,16 | 0 | - | - |
| 70 | 0x0ADA |  | 3646,2630,18 | 0 | - | - |
| 71 | 0x0ADA |  | 3647,2630,18 | 0 | - | - |
| 72 | 0x3EAC | deck | 3645,2629,16 | 0 | - | - |
| 73 | 0xA5F8 | Windows | 3650,2630,20 | 0 | Circle150 | a stained glass window |
| 74 | 0x403E | gargoyle painting (e | 3650,2634,27 | 0 | - | Fortune's For Tell, Lucky Charms |
| 75 | 0x4689 | BlackCat East | 3650,2629,47 | 0 | - | You notice a black cat looking down at you |
| 76 | 0x3DAD |  | 3649,2631,18 | 2076 | - | - |
| 77 | 0x3DAD |  | 3648,2631,18 | 2076 | - | - |
| 78 | 0x0A57 | bedroll | 3648,2629,28 | 2076 | - | - |
| 79 | 0x1EF3 | magical door | 3650,2635,31 | 0 | - | Grizelda The Fortune Teller |
| 80 | 0x0A2A | stool | 3649,2637,22 | 2418 | - | - |
| 81 | 0x0A22 | lantern | 3649,2636,30 | 0 | Circle300 | - |
| 82 | 0x9B2A | brick wall | 3648,2628,18 | 2418 | - | - |
| 83 | 0x2995 | wooden wall | 3649,2631,15 | 2412 | - | - |
| 84 | 0x2995 | wooden wall | 3649,2632,15 | 2412 | - | - |
| 85 | 0x2995 | wooden wall | 3649,2633,15 | 2412 | - | - |
| 86 | 0x26F8 | bark roofing | 3648,2633,48 | 2418 | - | - |
| 87 | 0x2995 | wooden wall | 3649,2628,16 | 2412 | - | - |
| 88 | 0x2995 | wooden wall | 3649,2629,15 | 2412 | - | - |
| 89 | 0x2419 | sculpture | 3648,2633,53 | 2418 | - | A Vent |
| 90 | 0x1E7D | table leg | 3648,2626,15 | 2418 | - | Wagon Hitch |
| 91 | 0x26F8 | bark roofing | 3648,2635,48 | 2418 | - | - |
| 92 | 0x4862 | Rune East | 3649,2630,52 | 0 | ArchedWindowEast | - |
| 93 | 0x4856 | Rune East | 3649,2635,50 | 0 | ArchedWindowEast | - |
| 94 | 0x6392 | Napa Valley Shield E | 3650,2630,3 | 2218 | - | Fancy Wagon Wheel |
| 95 | 0x26F9 | bark roofing | 3649,2634,44 | 2418 | - | - |
| 96 | 0x2995 | wooden wall | 3649,2635,16 | 2412 | - | - |
| 97 | 0x190F | bar door | 3650,2633,27 | 2218 | - | - |
| 98 | 0x0443 | marble wall | 3648,2626,21 | 2418 | - | - |
| 99 | 0x26F9 | bark roofing | 3650,2636,41 | 2418 | - | - |
| 100 | 0x26F9 | bark roofing | 3650,2635,41 | 2418 | - | - |
| 101 | 0x26F9 | bark roofing | 3650,2634,41 | 2418 | - | - |
| 102 | 0x26F9 | bark roofing | 3650,2633,41 | 2418 | - | - |
| 103 | 0x26F9 | bark roofing | 3650,2632,41 | 2418 | - | - |
| 104 | 0x26F9 | bark roofing | 3650,2630,41 | 2418 | - | - |
| 105 | 0x26F8 | bark roofing | 3648,2636,48 | 2418 | - | - |
| 106 | 0x0443 | marble wall | 3648,2635,38 | 2418 | - | - |
| 107 | 0x26F8 | bark roofing | 3648,2632,48 | 2418 | - | - |
| 108 | 0x26F8 | bark roofing | 3648,2631,48 | 2418 | - | - |
| 109 | 0x26F8 | bark roofing | 3648,2630,48 | 2418 | - | - |
| 110 | 0x26F8 | bark roofing | 3648,2629,48 | 2418 | - | - |
| 111 | 0x63DA | Sleeping Cat01 Frame | 3648,2636,18 | 2076 | - | Miss Sassy Pants |
| 112 | 0x9B17 | brick wall | 3649,2634,18 | 2418 | - | - |
| 113 | 0x0443 | marble wall | 3649,2635,38 | 2418 | - | - |
| 114 | 0x3E9C | ship | 3649,2627,16 | 2418 | - | - |
| 115 | 0x3E9E | ship | 3649,2628,18 | 2418 | - | - |
| 116 | 0x3E98 | deck | 3648,2627,17 | 2418 | - | - |
| 117 | 0x3EAD | deck | 3648,2628,17 | 2418 | - | - |
| 118 | 0x26F9 | bark roofing | 3649,2632,44 | 2418 | - | - |
| 119 | 0x3EA6 | ship | 3649,2636,18 | 2418 | - | - |
| 120 | 0x3EA8 | ship | 3649,2637,18 | 2418 | - | - |
| 121 | 0x26F9 | bark roofing | 3649,2635,44 | 2418 | - | - |
| 122 | 0x26F9 | bark roofing | 3649,2631,44 | 2418 | - | - |
| 123 | 0x26F9 | bark roofing | 3649,2630,44 | 2418 | - | - |
| 124 | 0x3EB0 | deck | 3648,2636,18 | 2418 | - | - |
| 125 | 0x3EAC | deck | 3649,2632,18 | 2076 | - | - |
| 126 | 0x3EB0 | deck | 3648,2637,18 | 2418 | - | - |
| 127 | 0x9B17 | brick wall | 3649,2629,18 | 2418 | - | - |
| 128 | 0x9B15 | brick wall | 3649,2635,18 | 2418 | - | - |
| 129 | 0x9B25 | brick wall | 3649,2633,18 | 2418 | - | - |
| 130 | 0x9B25 | brick wall | 3649,2632,18 | 2418 | - | - |
| 131 | 0x9B17 | brick wall | 3649,2631,18 | 2418 | - | - |
| 132 | 0x26F9 | bark roofing | 3649,2633,44 | 2418 | - | - |
| 133 | 0x26F8 | bark roofing | 3648,2634,48 | 2418 | - | - |
| 134 | 0x9B16 | brick wall | 3649,2630,18 | 2418 | - | - |
| 135 | 0x9B17 | brick wall | 3649,2630,18 | 2418 | - | - |
| 136 | 0x190F | bar door | 3650,2631,27 | 2218 | - | - |
| 137 | 0x9B2A | brick wall | 3648,2635,18 | 2418 | - | - |
| 138 | 0x9B16 | brick wall | 3649,2628,18 | 2418 | - | - |
| 139 | 0x6392 | Napa Valley Shield E | 3650,2634,3 | 2218 | - | Fancy Wagon Wheel |
| 140 | 0x26F9 | bark roofing | 3649,2636,44 | 2418 | - | - |
| 141 | 0x9E36 | miniwinebarrel SOUTH | 3646,2636,26 | 0 | - | a potion keg |
| 142 | 0x9E36 | miniwinebarrel SOUTH | 3646,2636,21 | 0 | - | a potion keg |
| 143 | 0x0A2A | stool | 3647,2633,19 | 2418 | - | - |
| 144 | 0x15BE | banner | 3645,2636,21 | 1141 | - | - |
| 145 | 0xA778 | opal_branch | 3647,2632,25 | 0 | - | a crystal ball |
| 146 | 0x4C53 | Lamp Stand Classic O | 3646,2631,20 | 0 | Circle300 | - |
| 147 | 0x1AE4 | skull | 3646,2631,21 | 2213 | - | - |
| 148 | 0x3DAD |  | 3647,2631,18 | 2076 | - | - |
| 149 | 0x1AE2 | skull | 3646,2633,22 | 2213 | - | - |
| 150 | 0x9B29 | brick wall | 3647,2628,18 | 2418 | - | - |
| 151 | 0x0443 | marble wall | 3647,2635,40 | 2418 | - | - |
| 152 | 0x1E7D | table leg | 3646,2626,15 | 2418 | - | Wagon Hitch |
| 153 | 0x0443 | marble wall | 3647,2635,38 | 2418 | - | - |
| 154 | 0x9B25 | brick wall | 3645,2632,18 | 2418 | - | - |
| 155 | 0x0443 | marble wall | 3646,2635,38 | 2418 | - | - |
| 156 | 0x4856 | Rune East | 3647,2631,56 | 0 | ArchedWindowEast | - |
| 157 | 0x190E | bar door | 3645,2632,27 | 2218 | - | - |
| 158 | 0x190E | bar door | 3645,2633,27 | 2218 | - | - |
| 159 | 0x0443 | marble wall | 3647,2626,21 | 2418 | - | - |
| 160 | 0x9B16 | brick wall | 3646,2635,18 | 2418 | - | - |
| 161 | 0x26FA | bark roofing | 3647,2636,45 | 2418 | - | - |
| 162 | 0x26FA | bark roofing | 3647,2632,45 | 2418 | - | - |
| 163 | 0x26FA | bark roofing | 3647,2631,45 | 2418 | - | - |
| 164 | 0x26FA | bark roofing | 3647,2630,45 | 2418 | - | - |
| 165 | 0x26FA | bark roofing | 3647,2629,45 | 2418 | - | - |
| 166 | 0x26FA | bark roofing | 3646,2636,42 | 2418 | - | - |
| 167 | 0x3DAD |  | 3646,2631,18 | 2076 | - | - |
| 168 | 0x26FA | bark roofing | 3647,2633,45 | 2418 | - | - |
| 169 | 0x3E9B | ship | 3646,2627,17 | 2418 | - | - |
| 170 | 0x3E98 | deck | 3647,2627,17 | 2418 | - | - |
| 171 | 0x3EAD | deck | 3647,2628,17 | 2418 | - | - |
| 172 | 0x3EA5 | ship | 3646,2636,18 | 2418 | - | - |
| 173 | 0x3EA7 | ship | 3646,2637,18 | 2418 | - | - |
| 174 | 0x9B16 | brick wall | 3646,2630,18 | 2418 | - | - |
| 175 | 0x3EAD | deck | 3646,2628,17 | 2418 | - | - |
| 176 | 0x9D5E | turtle tribe banner | 3646,2634,21 | 0 | - | Britania Worlds Faire |
| 177 | 0x26FA | bark roofing | 3647,2635,45 | 2418 | - | - |
| 178 | 0x26FA | bark roofing | 3647,2634,46 | 2418 | - | - |
| 179 | 0x3EB0 | deck | 3647,2636,18 | 2418 | - | - |
| 180 | 0x9B17 | brick wall | 3645,2629,18 | 2418 | - | - |
| 181 | 0x9B17 | brick wall | 3645,2630,18 | 2418 | - | - |
| 182 | 0x9B17 | brick wall | 3645,2634,18 | 2418 | - | - |
| 183 | 0x9B17 | brick wall | 3645,2635,18 | 2418 | - | - |
| 184 | 0x3EB0 | deck | 3647,2637,18 | 2418 | - | - |
| 185 | 0x9B17 | brick wall | 3645,2631,18 | 2418 | - | - |
| 186 | 0x9B25 | brick wall | 3645,2633,18 | 2418 | - | - |
| 187 | 0x9B18 | brick wall | 3645,2628,18 | 2418 | - | - |
| 188 | 0x9B29 | brick wall | 3647,2635,18 | 2418 | - | - |
| 189 | 0x9B16 | brick wall | 3646,2628,18 | 2418 | - | - |
| 190 | 0x4844 | Rune East | 3647,2635,56 | 0 | ArchedWindowEast | - |
| 191 | 0x0443 | marble wall | 3647,2635,41 | 2418 | - | - |
| 192 | 0x26FA | bark roofing | 3646,2629,42 | 2418 | - | - |
| 193 | 0x26FA | bark roofing | 3646,2630,42 | 2418 | - | - |
| 194 | 0x26FA | bark roofing | 3646,2631,42 | 2418 | - | - |
| 195 | 0x26FA | bark roofing | 3646,2632,42 | 2418 | - | - |
| 196 | 0x26FA | bark roofing | 3646,2633,42 | 2418 | - | - |
| 197 | 0x26FA | bark roofing | 3646,2634,42 | 2418 | - | - |
| 198 | 0x26FA | bark roofing | 3646,2635,42 | 2418 | - | - |
| 199 | 0x0722 | wooden stairs | 3647,2641,0 | 2418 | - | - |
| 200 | 0x0722 | wooden stairs | 3647,2640,5 | 2418 | - | - |
| 201 | 0x0722 | wooden stairs | 3647,2639,10 | 2418 | - | - |
| 202 | 0x0722 | wooden stairs | 3647,2638,15 | 2418 | - | - |
| 203 | 0x0721 | wood | 3647,2639,0 | 2418 | - | - |
| 204 | 0x0721 | wood | 3647,2638,0 | 2418 | - | - |
| 205 | 0x0721 | wood | 3647,2638,5 | 2418 | - | - |
| 206 | 0x0722 | wooden stairs | 3648,2641,0 | 2418 | - | - |
| 207 | 0x0722 | wooden stairs | 3648,2640,5 | 2418 | - | - |
| 208 | 0x0722 | wooden stairs | 3648,2639,10 | 2418 | - | - |
| 209 | 0x0722 | wooden stairs | 3648,2638,15 | 2418 | - | - |
| 210 | 0x0721 | wood | 3648,2639,0 | 2418 | - | - |
| 211 | 0x0721 | wood | 3648,2638,0 | 2418 | - | - |
| 212 | 0x0721 | wood | 3648,2638,5 | 2418 | - | - |
