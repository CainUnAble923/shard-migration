# October 22 patch notes (draft)

Draft for package 2026.10.22.0855, covering changes since 2026.10.21.0825. Update through the launcher for the new artwork and farm map.

## New

- The League Register brings your guilds into one book. Dull Copper Citizens can get it free from the League Registrar, bind guilds into it, and check their standing, currencies, and bank supplies.
- As your League rank rises, the Register opens remote contracts at Bronze, combined order turn-ins at Verite, and repairs for equipped, carried, and banked gear at Blaze.
- League goods include backpack item-limit upgrades, a Field Satchel for your guild satchels, and a Combined Logbook for mining and forestry. Backpack upgrades leave your weight limit unchanged.
- Smiths with Arms Lore can craft field repair deeds, charged repair kits, and remote repair deeds from the smithing menu.
- The League Shop's Hall page sells display cases, statues, wall trophies, and mounted heads. Achievement Points unlock them, Renown buys them, and their account-bound deeds let you decorate a house you own.
- Tinkers can craft snare nets, caltrops, gas traps, blast traps, dart traps, bear traps, alarms, and shackles. Remove Trap helps you set and disarm them. Under the default rules they catch monsters, spare players and pets, and require you nearby, except for alarms. Spent traps need resetting by hand.
- New creatures bring monster parts and first-kill bestiary entries to New Haven's surroundings, Yew, and several dungeons. The Siegebreaker in Covetous and the Hollow Oak in Yew offer fights for a group (coming once placed).
- The Exodus Encounter adds dungeon enemies, hidden supply caches, machinery puzzles, and a party ritual leading to Clockwork Exodus and his artifact rewards (coming once placed).
- The Valley of Eodon gains a public moongate, wildlife and dinosaurs, tribal encounters, wandering healers, and climbable vines near the Barako village (coming once placed).
- New Haven's tutorial farm has crops, livestock, a farmhouse, and Wren Tallow. Trainees can choose an evolution dog or cat, fight crop pests together, and practice healing (coming once placed).
- The Rootdeep Stacks gain a practice-net lesson, and the Burrows gain more floor traps (coming once placed).
- Guild halls have new decorations ready, including alchemy tanks and vats, smithing scenes, floating crystals, towers, and railings (coming once placed).
- Crafted weapons, armor, shields, and jewelry can become levelable with a Smith's Seal, earning XP in combat and points for supported properties and resistances. Seals have no normal player source yet (coming once placed).
- New Haven's winter decorations are scheduled for December 1 through January 6, with trees, lights, garlands, snow, and a bank advent calendar offering small December gifts.
- The System has more secret achievements to discover, with keepsakes and titles among their rewards.
- Extra jewelry slots are available through the accessories window. Valorite Citizens can wear a second bracelet, and toe-ring slots open through secret achievements. Tinkers can craft toe rings after learning the required recipe.
- An exhausted grove now gets a temporary stump marker at the last tree chopped. The marker disappears when its wood returns.

## Changed

- Tutorial graduation now records your first loop, awards its Loop box and fanfare, and permits travel off Haven island. It keeps your remaining Young time, skills, and stats.
- Before graduation, island exits direct you back to the League recruiter. Skipping provisionally opens island travel too, and remedial training remains available.
- Achievement lists now have category headings and icons.
- Opening a loot box sends an item animation arcing out before the fanfare. Higher-tier boxes show the effect to nearby players too.
- Bulk orders and smith commissions now require player-crafted gear.
- Abandoning a smith commission starts a short wait before another small request is offered.

## Fixed

- Fixed a server startup error that could prevent the shard from opening.
- Graduation no longer offers a second starter pet if you already chose one at the farm (coming once placed).

## Unsure

- The exact starting commit is unverified. Neither local checkout has the package tag requested by the brief. The provisional comparison starts after `5d29bfa`, the latest main merge before October 21 at 08:25, and ends at `1ecd9f3`. The older package's local release record already mentions early fog of war, so it is not listed as new here.
- Live deployment, settings, and world placement were not checked. Entries marked "(coming once placed)" need world setup or a player source before players can encounter them. The farm and guild hall placement tools are restricted by default, and Smith's Seals still have no chosen normal source.
- The stump marker's height on map trees remains unverified in a client. P380 confirms a known height issue in the source, so correct placement at the tree's foot is not promised.
- Custom area and combat music support is built, but its track list and assignments are empty at this release commit. There is no new soundtrack to announce yet.
- Companion groundwork is built, but hiring is not available. Extra ring slots also remain closed despite graduation now recording a loop. Neither is advertised as newly playable.
- The Exodus crafting recipes are registered, but recipe availability and the robe ingredient supply are unresolved in the source notes. No crafting route is promised here.
- The winter calendar's gifts are placeholders pending review. Exact gifts are not promised.

## Sources

Commit hashes below are main merge commits in ShatteredLegacy. Note links are in shard-migration.

- Release boundaries: ShatteredLegacy `CHANGELOG.md`, `VERSION` (`2026.10.21.24`), and first-parent log `5d29bfa..1ecd9f3`. Local package records: `D:/ShatteredLegacy/player-package/dist/ShatteredLegacy-2026.10.21.0825.version.json` and `ShatteredLegacy-2026.10.22.0855.version.json` in the same folder.
- `47b3eae`: [P280, League Register and repairs](cc-P280-league-register-build.md).
- `48191cd`: [P243, Hall rewards](cc-P243-league-hall-decor-rewards.md).
- `59fb338`: [P275, deployable traps](cc-P275-deployable-traps-build.md).
- `2d9fea4`: [P364, new bestiary creatures](cc-P364-league-bestiary-batch-2.md).
- `53c7829`: [P271, Exodus merge](cc-P271-cont-fixup-port-exodus-encounter.md), [P195, encounter implementation](cc-P195-port-exodus-encounter.md).
- `b240bb4`: [P354, Eodon merge](cc-P354-cont-fixup-port-eodon-remainder.md), [P198, Eodon implementation](cc-P198-port-eodon-remainder.md).
- `484cf7e`: [P276, tutorial farm](cc-P276-tutorial-farm-build.md).
- `94eabb0`: [P265, hall decorations and startup fix](cc-P265-guild-hall-decor-packs.md).
- `1c39977`: [P285, levelable gear merge](cc-P285-cont-fixup-levelable-gear-build.md), [P261, item leveling](cc-P261-levelable-gear-build.md).
- `7b11ab4`: [P266, winter decorations](cc-P266-new-haven-winter-decor.md).
- `460f0e2`: [P361, achievement merge](cc-P361-cont-fixup-noted-by-the-system-achievements.md), [P263, achievement implementation and order changes](cc-P263-noted-by-the-system-achievements.md).
- `b92e08c`: [P355, accessories merge](cc-P355-cont-fixup-accessory-slots.md), [P262, accessories](cc-P262-accessory-slots.md).
- `1ecd9f3`: [P380, stump merge and known height issue](cc-P380-cont-fixup-chopped-tree-stumps.md), [P359, stump implementation](cc-P359-chopped-tree-stumps.md).
- `02c46e8`: [P371, graduation and island travel](cc-P371-graduation-is-the-first-loop.md).
- `9b9bea3`: [P241, achievement icons](cc-P241-achievement-category-icons.md).
- `e7e5dbd`: [P366, flying loot merge](cc-P366-cont-fixup-cont-loot-box-flying-loot.md).
- Availability and boundary cautions: `222f0b8`, [P368, music](cc-P368-added-music-areas-monsters-bosses.md); `0076ce4`, [P369, companion groundwork](cc-P369-cont-fixup-companions-b1-base-and-record.md); `62c675d`, [P357, fog changelog only](cc-P357-cont-fog-of-war-client-half.md); baseline `5d29bfa`, [P352, fog client already built](cc-P352-cont-fog-of-war-client-half.md).
- Wiki drafts: [New Haven](wiki-drafts/new-haven-start.md), [levels and loops](wiki-drafts/levels-loops-and-scrolls.md), [League](wiki-drafts/league.md), [crafting](wiki-drafts/crafting-changes.md), [dungeons](wiki-drafts/dungeons.md), [Thieves' Den](wiki-drafts/thieves-den.md), [achievements and boxes](wiki-drafts/achievements-and-loot-boxes.md), [companions](wiki-drafts/companions-and-evo-pets.md), [Register](wiki-drafts/pages/uo/systems/league_register.txt), [Hall shop](wiki-drafts/pages/uo/systems/league_shop.txt), [accessories](wiki-drafts/pages/uo/systems/accessories.txt), [traps](wiki-drafts/pages/uo/professions/traps.txt), [levelable gear](wiki-drafts/pages/uo/drafts/levelable_gear.txt), and [draft cross-check](wiki-drafts/cross-check-2026-10-22.md). Draft discrepancies remain unresolved.
