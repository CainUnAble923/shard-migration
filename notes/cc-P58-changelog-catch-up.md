# cc-P58: patch notes catch-up, 2026.10.02 to 2026.10.05

2026-10-05. Brief: `D:\UO\cc-prompts\cc-P58-changelog-catch-up.md`. Wrote only `D:\ShatteredLegacy\CHANGELOG.md` and
`D:\ShatteredLegacy\VERSION`. No build, no test, nothing committed, wiki not published. Git read with `--no-optional-locks`.

## Headlines

1. Four new sections above 2026.10.01: **2026.10.05, 2026.10.04, 2026.10.03, 2026.10.02**. Player lines (counted from the
   file): 10.05 Added 2 / Changed 16 / Fixed 4; 10.04 Added 4 / Fixed 2; 10.03 Added 4 / Changed 5 / Fixed 6; 10.02
   Added 2 / Changed 5 / Fixed 7. **77 player lines** plus **7 Staff lines** (10.05: 1, 10.04: 2, 10.03: 1, 10.02: 3).
   `VERSION` = `2026.10.05` (LF, as before). Both files ASCII (`file` says ASCII text).
2. **`### Staff` is invisible to players and to the wiki.** `ShardVersion.cs:111-121` maps only added/changed/fixed;
   any other `###` heading sets the list to null, so its lines are skipped. `Publish-PatchNotes.ps1` does not parse the
   file (its line 9). So the Staff lists are a record only, as the brief allows.
3. **Clash: P57 is running beside me in `D:\ShatteredLegacy`.** At my last check the tree had P57's uncommitted changes
   (`ClusterFSmithBODSystem.cs`, `SmithSealCatalogGump.cs`, four tests, a new `SmithSealPriceVerification.cs`, untracked
   `design\satchel-icons\`), none in my two files. P57's brief has its own Patch notes section, so it may also edit
   `CHANGELOG.md` and `VERSION`. If it writes a `2026.10.05` section of its own, the two must be merged (one section per
   version; a second update the same day is `2026.10.05.2`). I avoided Seal numbers in lines P57 will change (catalog
   prices, bank value), so mine stay true after it.
4. Every line describes the **final** committed behavior; where a later prompt in the window changed an earlier one,
   only the final form is written, under the day of the final change (list below).

## Prompts read

Notes in `notes\`: cc-P27, P28, P29, P31, P32, P33, P35, P37, P38, P39, P42, P43, P44, P46, P48, P51, P52, P53, P55,
P56, and `shrunkpet-follow-and-followers.md` (the 10-03 ShrunkPet commit). Headlines, "What changed", "For Chase" /
checklists, and the parts each line cites. Also `docs\fidelity-principle.md` D-105 to D-120, `docs\bug-list.md` D44 to
D79, `notes\passdown-overseer-2026-10-05.md`, `notes\p42-checks-2026-10-03.md`, `docker\wiki\macros\README.md`.

**P37 was in the brief's research-only list but it shipped code** (`a529979`: permanent groves, the purge command, the
Docker mount). I read it and wrote its player-facing part (groves). Research-only, skipped as briefed: P25, P30, P40,
P41, P47, P49, P54. P26 (`0f4c989`, 2026-10-01 15:13:41) is the runestone, already in 2026.10.01.

## Commit to prompt map (`git log --since="2026-10-01 15:13"` in `D:\ShatteredLegacy`)

Matched by time to the shard-migration commit that carried each prompt's notes, and by the files changed.

| Day | Commit | Prompt |
|---|---|---|
| 10-01 | 0f4c989 15:13 | P26 (already in 2026.10.01) |
| 10-02 | eccf5af 08:05 | P27 |
| 10-02 | e2ca43d 08:28 | P28 |
| 10-02 | 56cae9d 10:17 | P29 |
| 10-02 | e092a3d 11:19 | P31 |
| 10-02 | 045b313 12:07 | P32 |
| 10-02 | 5d1e15a 14:40 | P33 |
| 10-02 | a529979 15:48 | P37 |
| 10-02 | 52df305 16:38 | P38 |
| 10-02 | a7c5d3b 18:21 | P39 / P43 (compose stop timeout) |
| 10-03 | d22a649 09:36 | P42 |
| 10-03 | 69830a7 10:57 | ShrunkPet |
| 10-03 | 1f2b899 11:26 | P46, plus wiki Macros pages (not from a CC prompt) |
| 10-03 | 8825eb8 13:15 | P44 |
| 10-03 | 92f8f5f 19:17 | P35 |
| 10-04 | aa61227 18:54 | P48 (plus `design\tutorial-farm\` files, design only) |
| 10-04 | 39a2da8 20:10 | P51 |
| 10-05 | 881a67e 05:36 | P52 |
| 10-05 | a8cf0e5 06:03, 411a922 06:18 | P53 |
| 10-05 | 5f6a194 07:35 | P55 |
| 10-05 | b8e525d 08:15 | P56 |

## Each line and its source

### 2026.10.05

Added
- Bank / cash out / ask setting: P55 Part H, "For Chase" 12; D-116.
- Knowledge entry on the Hammer of Hephaestus: P52 Part B, "For Chase" 5.

Changed
- Skill cap 200, no loss: P53 headline 3, Part A.
- Platinum..Celestial Blacksmithy 112.5..200; orders, commissions, salvage follow: P53 Part B table.
- Post-Valorite smelting at the same steps; harvest still 100: P56 Part B, headline 5; D-119. (Final form of P55 B,
  which had put them at 50.)
- Item and temporary skill bonuses above the cap: P53 Part C; D-113.
- Armored meditation 150: P53 Part B table (`Meditation.cs`), headline 7(b).
- Town smiths offer small or large: P55 Part H item 1; D-115.
- Members paid the guild's way at every smith: P55 Part H; D-105 amend.
- Banking pays far more Seals, at least OSI's non-member value: P56 Part A, headline 3; D-116 amend.
- Metal Familiarity pace 1,000 / 2,500, exceptional 3: P55 Part A, headline 3; D-118.
- Hammer bonus only while held: P52 Part A (D59).
- Achievements say what earned them: P55 Part F (D73).
- Six achievements retired, kept by holders: P55 Part G (D75).
- Satchel and pickaxe tier hues: P55 Part E (D72).
- Title Case material names: P53 Part D; D-114.
- "Society of Smiths" everywhere: P52 Part G (D68).
- Satchel smelting like the forge, tiers 3 to 5 smelt: P55 Parts B and D (D70, D71); D-117.

Fixed
- Graphics fallback: P52 Part C, headline 3 (D61); passdown 10-05 "graphics fallback proven".
- Back buttons and the catalog note: P52 Part E (D65), "For Chase" 6.
- Category paging, Blacksmithy and Inscription: P53 Part E, headline 6 (D63).
- Menu labels: P55 Part C (satchels), P56 Part C (trash bag, pet mimic, pack mule), D-120.

Staff
- Staff Hub readability and travel: P52 Part F (D67), "For Chase" 7.

### 2026.10.04

Added
- 17 League ranks and promotion: P48 Parts B and D.
- Bank +100 per milestone rank: P48 Part E.
- League row in the Guild Directory, welcome page line: P48 Part A.
- Raptor packs and pottery fragments: P51 headline 3, "For Chase" 5, Part A (ServUO's 25% `AncientPotteryFragments`).

Fixed
- Registrar ambient speech: P48 headline 4.
- Miners' Compact rank names in the directory: P48 Part C.

Staff
- `[SL` Staff Hub: P51 Parts B to D.
- `[LeagueLadder reload` and dev reset: P48 Part D, headline 9.

### 2026.10.03

Added
- Bulk Orders choice anywhere, large at 70.1 with no rank: P42 Part F; D-108.
- "Orders that still teach me", default on: P42 Part G1 and P46 Part B; D-109.
- Large deeds filled by crafted items: P42 Part H; D-110.
- Wiki Macros page: commit `1f2b899` (`docker\wiki\content\pages\uo\macros\`, sidebar and hub links); not a CC prompt.

Changed
- Bulk orders x2 standing; commissions x3 Seals, x2 standing: P42 Part G2, P46 Part D. (The deeds' x3 Seals is not
  written: P56 replaced how deeds bank Seals. Standing is unchanged by P56, its line 92.)
- Runic hammers from Gold up cost more Seals: P46 Part E. No prices written, since P57 is changing catalog prices.
- Self Repair imbue at Master Artificer, priced above every other property: P42 Part A and P46 Part C; D-107.
- Trammel Despise revamp only: P42 Part J; D-111; real run passed (`p42-checks-2026-10-03.md` 8b).
- Installer waits for EA's patch: P44 headline 1.

Fixed
- Shrunk pet: `shrunkpet-follow-and-followers.md` section 1 items 1 to 4.
- Wisp Orb possession and logout: P42 Parts I and K (D52, D54); D-112.
- Master attacking the possessed creature, karma on its death: P46 Part H (D58).
- Post-Valorite deeds take only their own ore: P46 Part A (D55).
- Familiarity on default iron: P46 Part G (D57).
- Visual C++ runtime shipped: P35 headlines 1 and 2 ("the game should fail at start" on a PC without it).

Staff
- Old Haven cleanup and Despise cleanup commands: P42 Parts B and J.

### 2026.10.02

Added
- Clean Up Britannia: P33 sections 1.4, 4.1, 4.2 (house barrels pay through the trash barrel patch).
- Fountain of Fortune and stepping stones: P27 Part A, P29 Part D.

Changed
- Custodians on Clean Up points, Civic Tokens retired, free trash bag: P33 sections 1.3, 4.3, 4.4.
- Imbuing essences pack, satchel, bank: P27 Part B, headline 3.
- Permanent groves: P37 section 5.
- Self Repair 1 in 500 from high-end sources: P32 Part C; D-106.
- Registrar office decor: P31.

Fixed
- Starwood and Celestial: P37 section 5 (the defect), P38 headline 3 (D49, measured after the fix).
- Stat bonus stacking (talisman, quiver, Pet Mimic): P29 Part A (D44).
- Meditation at high Int: P29 Part B (D45).
- Durability on extract: P29 Part C (D48).
- Essence Satchel usable for imbuing: P27 headline 3.
- "Imbue Item" label: P29 Part F.
- Player corpse not litter: P33 section 4.4.

Staff
- `[GuildStanding`: P29 Part E.
- Spawner import keyed by guid: P32 Part A.
- `[ClusterFPlaceCleanUp`, `[ClusterFSeedRegistrarOffice replace`: P33 section 1.4, P31 section 3.3.

## Left out on purpose

Undone or replaced inside the window:
- P32 B: the Journeyman gate on guild large-deed turn-ins (10-02). P42 F (10-03) made 70.1 Blacksmithy the only gate.
- P42 G2: bulk order Seals x3 (10-03). P56 A (10-05) replaced how deeds bank Seals; only the standing x2 survives.
- P42 A: Self Repair imbue at 40 shards / 40,000 gold. P46 C put a floor above every other property; the line says that.
- P55 B: post-Valorite ore smelting at 50 Mining (10-05 07:35). P56 B (08:15) made it tiered.
- P55 C: no label change for trash bag and pet mimic at 07:35; P56 C fixed them at 08:15. Written once, final form.
- P55 A familiarity pace replaced P52's unchanged pace and P46 G's fix still stands; the earlier 100 / 250 caps are not
  mentioned.
- P37's `[ClusterFPurgeUpgradeCollisions` (10-02 15:48) was deleted by P38 (16:38); staff tool, gone the same day.
- P27's "five shore tiles" reach claim: P29 D found them unreachable and added the stepping stones; one line covers both.

Internal or invisible to players:
- P38 engine bump to ModernUO d4531cd9, the craft replacements turned into patches, the 11 collision types deleted in
  favor of upstream's own (Raptor, Slith, Spellbinder, StormCaller and the rest). The upstream versions are the same
  content by name; I did not compare their stats, so I wrote nothing about them.
- P37 Docker mount and save location, P39 and P43 stop timeout and cutover (the shutdown save now finishes: real, but
  players see nothing unless a restart lost a save, and no player-facing claim was proven), the purge.
- P28 launcher account profiles: `-Test -Account` is for the test shard only.
- P35 gate 6 and the clean-machine kit, P52 Part D (sandbox kit), P52 Part H (Shard-Console DNS tile), P53 Part F,
  P42 Parts C, D, E, P27 Parts C and D (content index, SOURCE.txt), P46 Part F (test order), every test fix, Docker
  timeouts, the commit script.
- P42 Part B New Haven Healer and P32's restored spawners: these depend on a staff re-run of the import or the cleanup;
  the tools are in Staff, the world outcome is not claimed.
- `design\tutorial-farm\` and `design\registrar-office\` files in `aa61227` and `e092a3d`: design sources, nothing in game.
- P46 commissions were "dropped pending a commissions rework" in testing (passdown 10-05), but the code shipped, so the
  commission line stays. Remove it if that rework lands first.

Not verified: whether the Fountain of Fortune, the stepping stones, the Cleanup Officer and the new Registrar decor are
placed on the test world (each is a staff command). The lines describe what the build ships, as the 2026.10.01 runestone
line did.

P58 DONE
