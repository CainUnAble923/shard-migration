# cc-P362: container and scroll skins as player options in the client

## In plain words

- Our TazUO gets a new options page, Options > Interface > **Appearance**. On it each player can pick a look for
  their backpack, bags, metal chests (and the bank box), crates and spell scrolls, with a small picture of the pick.
  "Classic (stock)" stays the default, and only the player who picks a look sees it.
- 18 looks from your look book picks: 8 backpacks (Fancy and Gothic, each full or compact, by Carl Hamilton; Bloody,
  Celtic, Dragon and Leather by Safera), 3 bags (Castiel), 5 colored bank-chest linings and 2 crates (Erachiro), and
  CorvaeOboro's 64 Magic Scrolls. Each artist is credited in the game folder's README and in the art credits.
- Nothing replaces the stock art: every piece has a new number of its own, and a check proves no stock number was
  taken. The client build passed with the new patch (1,308 client tests); the package checks pass, apart from older
  checks that fail the same way without this change.
- For you: three choices near the end (whether Safera's EA-derived Celtic, Dragon and Leather sets may ship; whether
  to also lock some looks for later rewards; and you will want to see the looks in a real client once the package is
  rebuilt). Nothing is deployed or published.

2026-10-23, the Iron Golem (Opus 5.5), branch `golem/Iron/P362` of both repos. Prompt:
`D:\UO\cc-prompts\claimed\Iron\cc-P362-ui-skins-player-options.md`. Not committed (the Golem commits). Both repos were
clean at the start. The player package was not built or published; the client was built into
`D:\UO\tazuo-sl-build-iron-p362` (outside both repos) only to prove the patch.

## What each skin is

All under NEW IDs, registered in `player-package\vendor\shattered-legacy-art\registry.csv` (93 rows), PNGs in its
`gumps\` and `art\`. Pixels: BMP to PNG with pure black made transparent, the canvas kept, nothing else changed
(`scripts\anchor-art-frames.py --black-transparent --keep-geometry`). The table is `skins.json` beside the registry.

| Kind | Skin | Author | Stock ID it stands in for | Our IDs |
|---|---|---|---|---|
| Backpack | Fancy | Carl Hamilton | open backpack 60 (0x3C), minimized 80 (0x50), on the paperdoll 50422 (0xC4F6) | 23052, 23053, 23054 |
| Backpack | Fancy, compact | Carl Hamilton | the same, with the compact open backpack | 23055 (+ 23053, 23054) |
| Backpack | Gothic | Carl Hamilton | 60, 80, 50422 | 23056, 23057, 23058 |
| Backpack | Gothic, compact | Carl Hamilton | the same, compact | 23059 (+ 23057, 23058) |
| Backpack | Bloody | Safera (his own) | 60, 50422 (no minimized icon: stock's stays) | 23060, 23061 |
| Backpack | Celtic | Safera (a UO Desktop theme: EA-derived) | 60, 80, 50422 | 23062, 23063, 23064 |
| Backpack | Dragon | Safera (a UO Desktop theme: EA-derived) | 60, 80, 50422 | 23065, 23066, 23067 |
| Backpack | Leather | Safera (his "Fancy" folder, likely the KR client's strappy pack: EA-derived) | 60, 80, 50422 | 23068, 23069, 23070 |
| Bags | Celtic, Primitive, Snowy | Castiel | open bag 61 (0x3D) | 23071, 23072, 23073 |
| Metal chests and the bank box | Blue, Pink, Red, Teal, Yellow lining | Erachiro | metal chest 74 (0x4A), which every bank box (item 0xE7C) uses | 23074-23078 |
| Crates | Refurbished, Weathered | Erachiro | crate 68 (0x44) | 23079, 23080 |
| Spell scrolls | Magic Scrolls | CorvaeOboro | the 64 Magery scroll arts, 0x1F2D (Reactive Armor) to 0x1F6C (Summon Water Elemental) | art 13049-13112, in stock order |

Which stock gump each piece stands in for: the authors' own file names (Carl Hamilton's "Gump 60", "Gump 80",
"Gump 50422"; Safera's "0x3c", "0x50", "0xc4f6"), checked against pinned `Distribution\Data\containers.cfg` (0x3C
backpack, 0x3D bag, 0x44 crates, 0x4A metal chest and bank box) and TazUO's `ContainerManager` (0x3C's minimized icon
is 0x50) and `PaperDollInteractable` (the player's backpack on the paperdoll is 0xC4F6). The pieces measure 230 x 204
(open backpacks, the same canvas in every set), 52 x 59 and 56 x 50 (minimized), 260 x 237 (paperdoll), 176 x 194
(bags), 180 x 240 (chests) and 190 x 140 (crates). The authors drew them as replacements for those stock gumps, so
TazUO's container bounds for the stock ID should fit; the stock sizes were not measured here (this session could not
decode the client's compressed gumps), so it is one of the things to look at in a client (For Chase 3).

IDs: chosen with `scripts\find-free-art.py`'s rules (`notes\cc-P362-tools\free_ids.py`): the second free runs, not
the first, so a Golem registering at the same time is less likely to take the same numbers. `--check-registry`
afterwards: **0 of 720 registered IDs are no longer free**.

Terms (each folder's `SOURCE.txt`, and every registry row says it):
- Carl Hamilton, Safera, Castiel: none stated; community work: credit, ship only inside the player package or the
  private repo, do not repost.
- Safera's Celtic, Dragon and Leather sets are EA-derived. They ship as the earlier EA-derived sets do (cc-P243): only
  as our PNG under a new ID inside the package, never as an EA file. See For Chase 1.
- Safera's **Primitive, Snowy and Strappy** sets are EA's own alternate backpacks, gumps 30558-30563, which the client
  already has (gumpartLegacyMUL.uop has all six) and which TazUO already offers as Options > Containers > backpack
  style (Suede, Polar Bear, Ghoul Skin: 0x775E, 0x7760, 0x7762). Nothing of them ships; players already have them.
- Erachiro: "Everything you see in this pack is free to use." Credit Erachiro.
- CorvaeOboro: **CC0 1.0.** The prompt asked to check his GitHub first: the repository `CorvaeOboro/ultima_online_mods`
  states CC0 1.0 for the repository ("free to all, creative commons zero CC0 1.0, free to re-distribute, attribution
  not required"), and `ART/ART_MagicScrolls` is in it with the same file names. Credited anyway.

Credits: `player-package\vendor\shattered-legacy-art\SOURCE.txt` has a new section naming every author, ID range and
page, and the package README's "What is in here" names all five.

Not registered (on purpose):
- Carl Hamilton's minimized backpacks 2 and 3 (his stock 9810, 9811): TazUO never draws those IDs for a backpack.
- Safera's backpack item icons (item 0x9B2): remapping that art would change every backpack on the ground and on
  corpses too.
- Castiel's `Bags.bmp` (a preview picture of his three bags).

Erad's pack, the rest of it (listed, not registered): two status/paperdoll gump editions (Basalt and Marble, 2 files
each); a game board (1, "LOTR inspired": Tolkien reference, check before use); clothing gump art for humans, elves and
gargoyles (374 files, 128 of them in "Inspired Assets" folders: armor sets Lunar Guardian and Wolvesbane, outer layers, headwear, holiday sets; many
"Inspired Assets" folders copy other games' and films' designs: Zelda, Star Wars, Marvel, Mortal Kombat, Minecraft,
Yu-Gi-Oh, World of Warcraft, Path of Exile, Middle Earth, which we should not ship); item art (gems 6, spellbooks 8,
books, essences, flora, food, home decor, holiday barrels); tiles (Cosmic, Marble, Pattern, Sandstone, Stone) and walls
(Kalavain thick walls 10, red sandstone walls 32). The holiday barrels and the gem and spellbook items would suit later
decor or reward prompts.

## The client patch (`client\patches\0005-ui-skins-appearance.patch`)

On TazUO `3212623f` plus 0001-0004:
- `Game\Managers\SlSkins.cs` (new): the kinds, the 19 skins (the table, generated by `notes\cc-P362-tools\skins.py`
  from the same data as `skins.json`), the profile's choices ("kind=key;..."; Classic is never saved), which skins this
  client can offer (all its files present), and Apply/Choose.
- `ExternalImageLoader`: `SetGumpRemap` and `SetArtRemap` (stock ID to our ID; each returns what changed and drops its
  cached pixels), `ResolveGumpPath` (0002's paperdoll override first, then a skin, then the ID's own PNG) and
  `ResolveArtPath`, `GetGumpFilePath`/`GetArtFilePath`, and `ScanImages` (Load's folder scan on its own, for tests).
- `Art.Invalidate` beside 0002's `Gump.Invalidate`, so a switch redraws at once.
- `Profile.SlSkins` (per profile, saved with it). `World.CreatePlayer` applies the profile's skins at every login.
- `Options\Tabs\AppearanceTab.cs` (new), added to the Interface tab group after Containers: one row per kind, a list
  ("Classic (stock)" first, then "Label (Author)"), and a 96-pixel preview of the picked skin, read from its own PNG.
  The preview was cheap (TazUO's Myra `Image` with a `TextureRegion`, as the World Map's marker list does), so it is in.
- A backpack skin draws over stock backpack 0x3C: it shows while Containers > backpack style is Default (TazUO's
  Suede, Polar Bear and Ghoul Skin styles use their own gumps). The tooltip says so.
- `tests\ClassicUO.UnitTests\Game\SlSkinsTests.cs` (new): 6 facts.

`client\README.md` has the patch's row.

## The lock hook, for later (not built)

The prompt asks to leave a hook: a skin "locked" until a server flag unlocks it (a loot box or League shop cosmetic).
The place is `SlSkins.Available(kind, hasGump, hasArt)`: every list the page shows and every remap Apply makes goes
through it. A later prompt would:
1. add `"lock": "<flag>"` to a skin in `skins.json` (and its C# row);
2. have the server send the account's unlocked cosmetics. 0001's enhanced packet 0xCE (id 4, ClientCommand) is the
   existing server-to-client path; a new whitelisted command, or a small packet of its own as 0004 did with 0xF4,
   would carry a list of unlocked keys at login and when one is earned;
3. keep that set in memory (not the profile: it is the server's to grant) and filter `Available` by it, so a locked
   skin is neither listed nor drawn, and a choice saved earlier falls back to Classic until it is unlocked.
The server side would sit beside `TazUOClientCommand.cs` and read the unlock from the account (loot box contents or a
League shop purchase).

## Tests

| What | Result |
|---|---|
| Client unit tests, red: the six new facts against stubs (an empty skin table, no remap in the loader, empty labels) | 6 failed, 0 passed |
| Client unit tests, green (my clone, then `Build-Client.ps1`'s own run) | 1,308 passed, 0 failed |
| `client\Build-Client.ps1 -Out D:\UO\tazuo-sl-build-iron-p362` | applied 0001-0005, tests green, `Built: ...\client\TazUO.exe`; `sl-build.txt` lists patch 0005 (sha256 2192926076...) |
| Package: `Ui-Skins.Tests.ps1` (new, 4 facts), red on a copy of the tree before the change | 4 failed |
| The same, red on a mutation (a registry row on stock gump 60) | the stock-ID fact and the registry fact both failed ("1 of 721 registered IDs are no longer free"); the credits fact too |
| The same, green | 4 of 4 passed |
| `Build-UoOverrides.Tests.ps1` (counts updated: 720 rows, 45 gumps, 634 art) | passed |
| `Launch-Settings`, `Legion-Scripts`, `Map-Overrides`, `Music-Overrides`, `Paperdoll-Bodies` | passed |
| `Cliloc-Overrides.Tests.ps1` | 1 failed, `AMissingClilocIsOneYellowLineAndTheArtStillShips`: the same fact fails on a copy of the tree before this change (the sandbox's tiledata ends before P265's art IDs). Not this prompt's |
| `Package-Client.Tests.ps1` | 6 failed, the P124 facts: "No EA client data in ...\client-data\classic-client". This work copy has no client data, and they fail the same way before this change. Not this prompt's |

The new package facts:
1. Every skin draws from a new, registered ID with its PNG; no skin's ID is a stock ID any skin draws over; no stock
   ID is one of our registry IDs; all 93 cc-P362 rows are drawn by a skin; the ranges are 23052-23080 and 13049-13112;
   the scrolls are the 64 Magery scrolls in stock order.
2. Every row names its author and terms, the EA-derived ones say they ship only as our PNG, and SOURCE.txt credits all
   five authors.
3. The client's table (in patch 0005) is `skins.json`, skin by skin; the patch's files carry our header.
4. **No registered ID is a stock gump or art ID**: `find-free-art.py --check-registry` against the EA client's files
   (`-UoData`, else `SL_UO_DATA`, else `D:\UO\UltimaOnlineVanilla`; says SKIP without one).

## Screenshots

Not taken. This PC has no way to run the client against a world with our package installed (the package was not
built, and the client folder `D:\UO\tazuo-sl-build-iron-p362` has no Ultima Online data beside it). Contact sheets of
the source art were looked at in the session scratchpad only; they are not committed, because three sets are
EA-derived.

## For Chase

1. **Safera's Celtic, Dragon and Leather backpacks are EA-derived** (two UO Desktop themes, and likely the KR client's
   strappy pack). The prompt says to ship EA-derived sets "as our patch records only"; they ship the way cc-P243's
   trophies do, as our own PNG under new IDs inside the package. If you would rather not ship them, they come out by
   deleting nine rows and PNGs (23062-23070) and their three skins.
2. **Locks for later.** Nothing is locked now; every installed look is open to everyone. The hook for a loot box or
   League shop unlock is above.
3. **See them in a client.** The looks reach players with the next player package built from our TazUO. Worth a look:
   the compact Fancy and Gothic backpacks, and whether the chest linings read well as the bank box.

## Deviations and decisions for Chase

- `Build-Client.ps1` refused the session scratchpad as its output folder, because the scratchpad's path contains
  "shard-migration" (its repo guard). The build went to `D:\UO\tazuo-sl-build-iron-p362` instead, outside both repos
  and not the shared default `D:\UO\tazuo-sl-build`.
- Kinds: the prompt names three (backpack, other containers, scrolls). "Other containers" is split into bags, metal
  chests and crates, because one container look cannot fit all three (each is its own stock gump with its own shape).
- The patch was written in a private clone of the TazUO source in the session scratchpad (patches 0001-0004 committed
  there as a base), then `git format-patch` into `client\patches\`. `Build-Client.ps1` then built it from the usual
  shared clone, which it only reads (plus its usual worktree).
- VERSION is `2026.10.23.7`: main moved to .6 (P291) after this branch was cut.

## Files

- Code (`D:\UO\golems\Iron\ShatteredLegacy`): `client\patches\0005-ui-skins-appearance.patch` (new), `client\README.md`;
  `player-package\vendor\shattered-legacy-art\`: `registry.csv` (+93 rows), `skins.json` (new), 29 gump and 64 art
  PNGs (new), `SOURCE.txt`; `player-package\payload\README.txt`; `player-package\tests\Ui-Skins.Tests.ps1` (new),
  `Build-UoOverrides.Tests.ps1` (counts); `CHANGELOG.md`, `VERSION`.
- This repo: this note; `notes\cc-P362-tools\` (`skins.py` writes the registry rows, the PNGs, `skins.json` and the C#
  table; `client_edits.py` and `SlSkins.cs.template` make the TazUO edits; `free_ids.py`, `probe_stock.py`,
  `contact_sheet.py`, `readme_row.py`, `skintable.cs.txt`).
- Nothing running; no lock was needed or held (no Docker, test shard or package build).

P362 DONE
