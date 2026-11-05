# cc-P796: assess pet leveling, follower and pack-pet systems

## In plain words

- **Of the seven downloads, none should come in as written.** The shard already has most of what they offer: the Compact Mule (a rideable pack animal with breeding), evo pets, companions, Pet Training and a follower curve that grows with loops.
- **The best find is a way to build something you already asked for.** The Picky Beetle's pick-up loop is a good starting point for the Clockwork Scavenger, the League's auto-loot reward, which you decided on 10-05 and which was never built.
- **Two small extras are worth having:** a perch for a pet bird or chicken lizard in a house, using art already in the client, and crafted armor for horses, using the armored horse the client already has.
- **For you:** pick which of the three to queue. The ranked list and prompt sketches are below. Horse barding needs one call from you: how strong it should be on an easy-to-tame horse. Nothing was built or changed in the game.

## Ranked list

| Rank | Item | Recommendation | Rough size | Why |
|---|---|---|---|---|
| 1 | **Picky Beetle** | **Rebuild as ours**, as the Clockwork Scavenger | about 300 lines, 2 saved types, facts | A Chase decision with an empty slot waiting. Only the loop's idea carries over. |
| 2 | **Pet perches** | **Rebuild as ours**, one generic perch | about 200 lines, 3 saved types | Safe house decoration, art on disk, and a use for hatched chicken lizards. |
| 3 | **Horse barding** | **Rebuild as ours**, weaker than the dragon's, no pooping | about 300 lines, 1 pinned patch, 1 craft row | A smith's sink and a look we already have. Needs a balance call. |
| 4 | **Jako pet leveling** | **Idea only** | none | It would be a fourth way for pets to grow, and needs core edits. One idea is worth taking. |
| 5 | **Soul crystals** | **Skip** | none | Stores a number that nothing uses, and needs XmlSpawner. |
| 6 | **Max followers by Int** | **Skip** | none | Fights the loop curve, and lowers stock 5 for most new players. |
| 7 | **Ridable pack mule** | **Skip** | none | The Compact Mule and the stock Giant Beetle already do this. |

## 1. Each item

All seven: `SOURCE.txt` states no license terms of its own, so each is community work: credit the author, ship only inside the player package or the private repo, do not repost. Soul crystals' and Jako's authors also credit others (Lord Zeus's request; Jako, of RunUO). None ships new art. "Lines" are the `.cs` files, without `_zips`; "Ser" is hand-written `Serialize` overrides.

### Jako pet leveling (ObiOne, from Jako on RunUO)

- **What it does:** every tamed pet gains experience from kills it damaged and loses some when it dies. Levels run to a random max of 9-15. Each level gives a trait point (2 at level 10), and the owner spends points on hits, stamina, mana or resists from Animal Lore's gump. Caps: hits 550, mana 500, each resist 65, and any stat up to 1.25 times its base. A breeder NPC mates two pets for gold (owner needs Taming 95, 7-14 day cooldown) and gives babies by ticket.
- **Size:** 15 files, 8,962 lines, 3 Ser. Only 1,461 lines are its own (`Jerbal\Jako`). The rest are whole replacement copies of `BaseCreature.cs` (ServUO 54) and `AnimalLore.cs`.
- **Core edits:** 4 `#region Jako` blocks in `BaseCreature` plus scattered calls (serialization, death, tooltips), and 6 in `AnimalLore`. In ModernUO that is pinned patches on `BaseCreature`, and its save data lands on every creature in the world. We already carry several `BaseCreature` patches.
- **Art:** none.
- **Overlap:** evo pets (`EvoPet.cs`: XP from a damage share, stages, gates); companions (levels, loops, lineage, breeding designed in its own chat); stock Pet Training (the table P793 kept exact); `ClusterFPetGainSpeed` (pets learn faster); Compact Mule breeding. Our Animal Lore gump is our own too (`NewAnimalLoreGump`), so the gump edit would not apply.

### Max followers by Int (Felladrin)

- **What it does:** sets `FollowersMax` from Int on every equipment check: Int / 15 + 1, between 2 and 8.
- **Size:** 1 file, 47 lines, 0 Ser. One core edit, in `PlayerMobile.ValidateEquipment_Sandbox`. No art.
- **Conflict:** it overwrites `FollowersMax` outright. Ours comes from the loop curve in `CompanionParty.ApplyFollowersMax` (5 at loop 0, 19 at loop 21) and is never below 5. Its top of 8 would undo the curve. Under Int 60 it gives fewer than the stock 5, against the settled rule that a new player keeps a pet or mount beside two squires. Int jewelry would change it too.

### Picky Beetle (Xanthor, from Charon)

- **What it does:** a tamable pack beetle (Taming 80, 2 slots, must be beaten down first) that lifts stackable items within 3 tiles into its pack, up to 3 at a time, on every think. The description says "just about everything", but the code takes **stackable items only**.
- **Size:** 1 file, 189 lines, 1 Ser. No core edits. Art: stock Giant Beetle, body 0x317, mount 0x3EBC.
- **Problems as written:**
  - The pick-up runs whether or not it is tamed, so a wild one vacuums.
  - It has no looting rights check: it takes other players' drops, and anything movable and stackable on a house floor.
  - Its timer is zero seconds, so it runs on every think. Str 0 and Int 500 are odd numbers too.
- **Fit:** two things already exist. The Salvage Bin module's tier II picks up loose items near the owner by a filter (`MuleModules.PickupTick`, built). The **Clockwork Scavenger** is designed, and not built: "the League auto-loot reward" (Chase 10-05, `docs\feature-queue.md`, Option A). It loots into the backpack, and Clockwork Load Harness III redirects it to the mule; the module's data says the redirect hook is there.

### Pet perches (Hammerhand)

- **What it does:** two house addons, an eagle perch and a chicken lizard perch. Use the bird item on a perch you own or co-own, and a blessed, unmoving, renamable pet sits on it, showing its age in weeks.
- **Size:** 6 files, 881 lines, 8 Ser (perch, deed, item and pet for each). No core edits. It copies the ML parrot perch pattern twice.
- **Art, all in our client's tiledata or used by stock:** perch 12214 (0x2FB6, "parrot perch"), eagle item 0x211D, chicken lizard item 0x428A, eagle body 5, chicken lizard body 716. No new art.
- **Fit:** pinned has `ParrotPerchAddon` and its deed, but no pet parrot to sit on it. We already have chicken lizards with eggs and an incubator, which give the perch a natural source. No overlap with the leash, the hitching post or stabling.

### Horse barding (ATruGod; he says he did not write it)

- **What it does:** a blacksmith craftable deed (72.5 skill, 350 iron) that armors your own horse. The horse takes the hue of the metal and absorbs 10% of the rider's damage, 20% if exceptional, until 1,000 or 2,500 barding points run out. A bladed item removes it.
- **Size:** 5 files, 4,259 lines, 4 Ser. Almost all are whole copies of `AOS.cs`, `DefBlacksmithy.cs`, `BladedItemTarget.cs` and `Horse.cs`, so 4 core edits. The real content is about 150 lines.
- **Art:** it changes the horse to body 284, which is Mondain's Steed in `mobtypes.txt`, with mount item 0x3E92, the same pair stock uses for the Charger of the Fallen ethereal. So we have it, but every barded horse looks like that one armored horse. Not seen in a client here.
- **Extra it brings:** `Horse.cs` also has a joke system: a hurt horse drops dung, which renames your shoes and gives "Fertalizer". It should stay out.
- **Fit:** pinned's `AOS.Damage` has exactly this branch for the swamp dragon (only when the attacker is not a player). The Compact Mule has Expedition Barding as a module, so mule riders are covered; horses are not. **Balance problem:** a horse needs only Taming 29.1, while the swamp dragon needs 93.9, so the same 10-20% undercuts it.

### Soul crystals (Ravenwolfe)

- **What it does:** target an undamaged creature, kill it within 10 minutes, and the crystal gains charge of Fame / 100, up to 50,000. Crystals combine and can be sold.
- **Size:** 2 files, 240 lines, 2 Ser. **Needs XmlSpawner** attachments, which we do not have on ModernUO. Art: 0x1ED0, a tiledata "light" tile, with a red hue. No core edits.
- **Fit:** nothing. The author says so: how players get crystals and how the charges are used is left to you. It is a number with no use. The nearest use would be evo XP, but the evo design says XP comes only from fights the pet deals damage in.

### Ridable pack mule (Milva)

- **What it does:** a mount with a strong pack. Taming 95, 2 slots, 298-315 hits, 16-22 damage, casts spells and **breathes fire**, Fame 14,000, Karma -14,000.
- **Size:** 1 file, 165 lines, 1 Ser. No core edits. Art: the stock horse body 0xE2 in four hues, so it is not a mule to look at.
- **Fit:** none left. The Compact Mule is our rideable pack animal, with tiers, breeding and modules at 1 slot. The stock Giant Beetle rides and carries too. The class is also named `PackMule` in `Server.Mobiles`, the same as ours.

## 2. Rules check

| Item | Skill or stat points | Power scrolls, bless deeds, property artifacts | Usable now | Mostly helpful |
|---|---|---|---|---|
| Jako | **Flag.** Traits are stat points for pets, not players. The rule as written in the feature queue is about players, but a pet raised this way is the same shortcut. Chase's call if it ever comes back. | None | Yes | Mixed: pets lose XP on death |
| Max followers | None. It changes follower slots, which are a loop reward. | None | Yes | No: harms low-Int players |
| Picky Beetle | None | None | Yes | Yes, once it respects looting rights |
| Pet perches | None | None | Yes | Yes, decoration |
| Horse barding | None | None. A hued horse, no item property | Yes | Yes, with lower numbers |
| Soul crystals | None | None, as it does nothing | No: no use, and needs XmlSpawner | No |
| Ridable mule | None | None | Yes | No: a strong fire-breathing mount is off-theme |

## 3. Recommendations and prompt sketches

**1. Clockwork Scavenger (rebuild, from the Picky Beetle's idea).** Sketch: "Build the Clockwork Scavenger, the League's auto-loot reward (F-33 Option A): a small follower that picks up the owner's own loot near them into their backpack, respecting looting rights, houses and a filter (reuse `MuleModules.PickupCategories`); Clockwork Load Harness III sends it to the mule." About 300 lines, a body to choose from existing art, and facts. **First check** whether a Scavenger still needs to be a separate creature now that the Salvage Bin's tier II does part of this, and which League rank grants it. Those are for the prompt to settle.

**2. Pet perch (rebuild).** Sketch: "One generic `PetPerchAddon` with a deed, and one blessed, unmoving perched pet taking its body from the item placed on it (chicken lizard, eagle, and the parrot stock lacks); house owners and co-owners only, renamable, age shown; sold in the League shop or crafted by Carpentry, and a hatched chicken lizard can be turned into a perch pet." About 200 lines and 3 saved types, against the original's 881 and 8.

**3. Horse barding (rebuild).** Sketch: "Crafted horse barding: a blacksmith deed that armors your own horse, hued by the metal, absorbing a share of the rider's damage from monsters until worn out; a pinned `AOS.Damage` patch beside the swamp dragon's branch; survives the leash's figurine; no dung." About 300 lines, a pinned patch and a craft row. Stock `Horse` has several bodies, so taking the barding off has to bring the same one back. **Chase's call:** how strong. I suggest 5% and 10%, half the dragon's, as the horse is far easier to tame. Say so in `docs\fidelity-principle.md` when built.

**4. Jako (idea only).** The one idea worth taking: letting the owner **choose** where a pet's growth goes. An evo stage-up, or a companion's rank, could offer a small pick (hits or a resist), within caps, as the evo line's hue and body picks already do. It needs the rule call above. Do not port the levels, the breeder or the `BaseCreature` edits. Breeding stays with the mule's system and the companions' own design.

**5. Soul crystals, 6. Max followers, 7. Ridable mule (skip).** Reasons in the table.

## How this was checked

- Read every pack's `SOURCE.txt` and the code, except Jako's `BaseCreature` and `AnimalLore`, where I read the Jako regions and the calls. Compared the barding files with `D:\UO\ServUO-pub57`.
- Read our side in `D:\UO\golems\Iron\ShatteredLegacy`: `PackMule.cs`, the breeding system, `EvoPet.cs`, `CompanionSettings.cs`, `CompanionParty.cs`, `ClusterFPetGainSpeed.cs`, `ClusterFPetLeash.cs`, the mule module files, `docs\companions\companions-squire-evo-research.md`, and `docs\feature-queue.md` for the rules and the Scavenger.
- Art IDs read from the client copy's tiledata and `mobtypes.txt`; stock ones from `D:\UO\ModernUO-pinned`.

**Not verified.** Nothing was built or run, from `D:\UO\third-party` or anywhere else. No art was seen in a client: body 284 under a rider, and a chicken lizard on a perch, still need a look. Sizes for the rebuilds are my estimates. "Int under 60 gives fewer than 5" is worked from the formula.

## Other

- **`D:\UO\third-party\CODE-INTAKE.md`:** none of the seven had a row, so I added seven, marked `assess (P796)`. Backup: `CODE-INTAKE.md.bak-20261105-p796`.
- **Follow-ups:** none queued. Chase picks.

P796 DONE
