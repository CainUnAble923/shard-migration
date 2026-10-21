# Art requests: guild menu crests (cc-P177, for the art lane, cc-P152 / cc-P158)

The shared guild menu (`GuildMenuGump`, cc-P177) draws each guild's crest at the top left of every menu, guild book
and League page. Fourteen guilds use the client's own gold guild medallions (gump art 5545 to 5592, below). Five need
new art: two have nothing and draw a placeholder, three use a stock medallion that only roughly fits.

## What ships now

`crests.png` here: every guild's crest (or placeholder) beside its name in its accent hue, on the menu's panel.
`stock-medallions.png`: the whole stock set, 5545 to 5592, at 2x (each odd ID is the normal state; the even ID after
it is the same medallion pressed, which the menus do not use).

| Guild | Crest now | Status |
|---|---|---|
| Society of Smiths | 5555 anvil | stock, fits |
| Miners' Compact | 5567 pick | stock, fits |
| Arcane Society | 5569 wizard's hat | stock, fits |
| Tailors' Circle | 5579 scissors | stock, fits |
| Tinkers' Union | 5581 gears | stock, fits |
| Healers' Covenant | 5563 ankh | stock, fits |
| Bards' Consortium | 5553 lute | stock, fits |
| Thieves' Den | 5575 hooded figure | stock, fits |
| Warriors' Brotherhood | 5577 crossed swords | stock, fits |
| Rangers' League | 5551 bow | stock, fits |
| Maritime Brotherhood | 5565 fish | stock, fits |
| Merchants' Exchange | 5571 coins | stock, fits |
| Foresters' Union | 5557 tree | stock, fits |
| Twin Paths Dojo | 5589 shuriken | stock, fits |
| **The Custodians** | none: placeholder (frame 9270 and a broom, item 0xB025) | **request 1** |
| **Keepers of the Last Door** | none: placeholder (frame 9270 and a skull, item 0x1853) | **request 2** |
| **Artificers' Order** | 5585 glowing blade (stand-in) | **request 3** |
| **Order of the Alembic** | 5583 provisioner's table (stand-in) | **request 4** |
| **League of Extraordinary Citizens** | 5545 Britannia's sigil (stand-in) | **request 5** |

## Size and style (all five)

- **60 x 60 pixels**, one PNG each, RGBA, transparent outside the disc (the client treats colour 0 as transparent).
- **Match the stock medallions exactly**: a brushed gold disc with a darker bevelled rim, lit from the upper left, and
  the emblem as a **flat black silhouette** in the middle (about 36 px across), with a 1 px light edge where the stock
  ones have it. Put one stock medallion (5555, the anvil) beside the new one at 100 percent: they must read as one set.
- No text, no colour other than the gold and the black (the menu adds the guild's colour to its name, not to the crest).
- Must read at 1x on a 1080p screen: simple, bold shapes. Hand-placed pixels, no blur.
- Normal state only. The menus draw the crest as an image, not a button.

## One line per crest

1. **The Custodians** (city cleaners, the Sanitation Warden's guild): a broom crossed with a dustpan, or a broom over
   a small trash barrel. Reference: item art 0xB025 (broom) and 0xE77 (barrel) in `crests.png`'s placeholder.
2. **Keepers of the Last Door** (necromancy, spirit speak and forensics, the old Necromancers' hall): a skull in an
   open doorway, or a keyhole with a skull in it. Reference: the gold-square necromancy icon 1003 (character creation)
   and item 0x1853 (skull).
3. **Artificers' Order** (imbuing): a gem or soul-forge flame over an anvil, or a single cut gem with rays. The stock
   5585 (a glowing sword) is the closest stock emblem; it says "magic weapon", not "imbuing".
4. **Order of the Alembic** (alchemy): an alembic or a round flask with a bubble rising from it. The stock 5583 is a
   provisioner's table with bottles, close but not alchemy.
5. **League of Extraordinary Citizens** (the guild of guilds, metal ranks Iron to Celestial): a ring of small
   linked links or a laurel around a star. Today it uses 5545, Britannia's eight-path sigil, which also suits; keep it
   if the art lane prefers.

## IDs

Gump IDs **22459 to 22463** (one per request, in the order above) read FREE in
`python scripts/find-free-art.py --explain-gump 22459 22460 22461 22462 22463` on the Gold PC (2026-10-21), right after
the Achievements button's 22456 to 22458. Two checks could not run there: the shipped art overrides (the vendor packs
are not on that PC, "0 shipped art overrides") and the TazUO source ("TazUO source not found"). Run it again on the game
PC before registering them in `player-package\vendor\shattered-legacy-art\registry.csv` (kind `gump`).

## Deliverable

Five PNGs named `22459.png` to `22463.png`, 60 x 60, RGBA, into
`D:\ShatteredLegacy\player-package\vendor\shattered-legacy-art\gumps\`, with a `SOURCE.txt` line each ("style after
the client's guild medallions 5545 to 5592"). Then each guild's `CrestGump` in `GuildMenuThemes`
(`server\customizations\GuildMenuGump.cs`) changes from 0 or the stand-in to its new ID: one number per guild.

## Not requested

Banners, borders and backgrounds: the menus keep the stock frame (9270), panel (2624) and rules (9304), which is what
makes them read as one set. The crest and the accent-coloured name are the per-guild difference. If Chase wants more
(a coloured header band per guild), that is a later request.
