# cc-P128: Port list, Consumables (food, drink, potions) and crafting gaps

2026-10-16. Prompt: `cc-prompts/cc-P128-port-consumables-crafting-gaps.md`. Both repos were clean at the start. Not
committed: the Golem commits after DONE.

## Headlines

- **Consumables: 36 of the row's 44 files are in; crafting gaps: 22 of 33.** Port list (progress.py, stem proxy):
  Food, drink and potions **0 / 44 -> 36 / 44**, Crafting gaps **0 / 33 -> 22 / 33**; all systems 356 / 983 ->
  **417 / 983** (the three forced leaf resources count in the base-items row). The 19 files not ported are listed
  below with what each costs, none silently: 8 rest on a subsystem pinned lacks (engraving, the Gorgon lens, armour
  refinement, item altering, the Silver Sapling's respawn), 7 are equivalents pinned already has under other names, 3
  are store bundles whose contents are in neither tree, 1 has no consumer here.
- **What a player gets.** Cooking: the enchanted apple, grapes of wrath, fruit bowl and parrot wafers (ML), plant
  pigment, natural dye and colour fixative (SA). Alchemy: the elixir of rebirth and five of the six Eodon tribal potions
  with their recipes (the sixth needs the tiger pelt), dye, pigment, fixative, crystal granules and softened reeds.
  Tinkering: clippers, softened reeds, eleven baskets behind the basket-weaving book, the hitching rope. Loot and staff:
  fear essence, shatter and exploding tar potions, three tasty treats, poppies dust, the skin tincture, Valentine
  chocolate, the Thanksgiving table, chocolate nutcrackers, the fifteen begging rewards. Houses: raised garden beds
  (four shapes) whose mounds need no water or pest care, and the potted coffee plant.
- **Nine small patches, each ServUO's own lines at its own place** (`server/patches/`): BasePotion's enum gains the nine
  SA/TOL effects (appended); AOS applies the grapes of wrath; BaseCreature applies a tasty treat's damage; PlayerMobile
  and Spell read the Urali trance tonic; PlantItem, PlantSystem and Seed gain the raised-garden hooks; CraftItem's colour
  tables gain the plant resources so reeds, pigment and baskets keep their colour. Alternatives argued below.
- **Where the port met the shard's rules.** The basket-weaving book: ServUO keeps it as a PlayerMobile flag and refuses
  the craft at make time (the entries stay visible); here it is the account key `flag:BasketWeaving` in the recipe store
  (beside the Masonry and Glassblowing books), checked by the recipe gate, which hides the twelve book-gated entries
  until the book is read and applies with gating on or off. The clippers' three modes, saved flags in ServUO, are a
  per-player table here (clippings by default; a restart resets everyone). Every ported recipe is visible as ServUO has
  it for F-43's gating, listed below.
- Tests: three new fact files, **35 facts**, all 35 seen red across two deliberate break sets (34 breaks, then 5) with the
  tree hashed before and after each (byte-identical both times); shard tests **1,355 of 1,355** (1,320 before this
  prompt); the test world loads, saves and reloads on the image. Port list and progress block regenerated.

## What was ported

### Consumables (ServUO `Scripts/Items/Consumables/` -> `server/customizations/Items/Consumables/`), 36 files

| ServUO | Ours | What |
|---|---|---|
| `Cheese`, `Cookies`, `Dates`, `Fish Steak`, `FrenchBread`, `Pizza`, `Sake`, `Shirt`, `Stew`, `Turnip`, `Wine`, `FlowerGarland`, `LiquorPitcher`, `WaterPitcher`, `WinePitcher` (15) | the same names | the begging rewards (`Beg*`): the stock item with "Acquired by begging" (1075129) on its properties. Pinned's Begging has no SA reward table (ServUO `Skills/Begging.cs:200-300`), so only staff can make one until that skill file is ported |
| `BaseMagicalFood.cs` | same | the ML magical food base: influence and cooldown flags per mobile, in memory (ServUO: static Hashtables) |
| `EnchantedApple.cs` | same | lifts every curse (Cleansing Winds' `RemoveCurses`); cooldown 30 s + the curses removed, to 15. ServUO's two pre-TOL branches are not carried: the shard is fixed at Endless Journey (`Configuration/expansion.json`), so `Core.TOL` is always true and they cannot run (one names `SleepSpell`, absent from pinned) |
| `WrathGrapes.cs` | same (`GrapesOfWrath`, `[TypeAlias("Server.Items.WrathGrapes")]`) | 20 s of +35 weapon / +15 spell damage, 2 min cooldown, the buff icon |
| `FruitBowl.cs` | same | fills 20, +5 to every stat for 120 s |
| `ThanksGivingFood.cs` | same (13 types) | `BaseComplexFood` (pieces left, saved), the pie, basket of rolls and turkey platter, their seven pieces |
| `ValentineChocolate.cs` | same | title and one of 22 messages, saved |
| `ParrotWafer.cs`, `GoldFoil.cs` | same | leaf items (the parrot is patch-backlog P14; the foil is the nutcracker's wrapper) |
| `TastyTreat.cs`, `DeliciouslyTastyTreat.cs`, `IrresistiblyTastyTreat.cs` | same | a pet's stats up 5/10/15% for 20/10/20 min, loyalty to max, cooldown 2/60/120 min; the damage bonus kept on `TastyTreat` (`DamageBonusOf`) and applied by `BaseCreature-tasty-treat-damage.patch` |
| `Nutcrackers.cs` | same | the wrapped chocolate nutcracker, three kinds, unwraps on double-click |
| `BaseExplodingTarPotion.cs`, `ExplodingTarPotion.cs` | same | the 20-tile tar burst: everyone inside walks for a minute (a NetState speed-control packet, as pinned's) |
| `FearEssence.cs` | same | 20-tile burst, Magic Resist against (4r + 150) / 700, 3 s paralysis on failure |
| `ShatterPotion.cs` | same | thrown at a mobile: a fifth of 20+ potions in the pack destroyed |
| `EodonPotions.cs` | same (16 types; `PerfectBanana` is CC3's and not repeated) | `EodonPotionContext`, `EodonianPotion`, the six tribal potions, the eggsac, lava berry and bush, river moss, blue corn, corn stalk, moonstone shard |
| `ElixirOfRebirth.cs` | same | revives a dead bonded pet within 2 tiles whose corpse is gone |
| `HitchingRope.cs` | same | the rope; its target refuses everything until the hitching post (base-items row) lands, with the post's check written in the file |
| `PoppiesDust.cs` | same | 8 charges, identifies a seed, merges with another dust |
| `SkinTingeingTincture.cs` | same | the skin-hue gump (a plain Gump here; ServUO's is its own BaseGump), `Race.ClipSkinHue` |

Three forced leaf dependencies (the port recipe's LuckyCoin rule), in the base-items row: `Items/Resource/PlantClippings.cs`
(clippers and pigment), `ScouringToxin.cs` (softened reeds; its ServUO source is the Underworld maze puzzle) and
`SilverSerpentVenom.cs` (colour fixative; ServUO's silver serpent drops it, pinned's does not: P129's).

### Crafting gaps (`Scripts/Services/`), 22 files

| ServUO | Ours | What |
|---|---|---|
| `BasketWeaving/Baskets/*.cs` (11) | `Services/BasketWeaving/Baskets/` | eleven `BaseContainer` baskets with ServUO's art and labels (ServUO declares most with no namespace; they are `Server.Items` here) |
| `BasketWeaving/BasketWeavingBook.cs` | same, plus `BasketWeaving` (Knows/Learn/Forget on the account key) | the book, GM Tinker only |
| `BasketWeaving/Clippers.cs` | same (`Clippers`, `ClipMode`, `TopiaryGump`) | a `BaseTool` of Tinkering: clippings, reeds or one of nine topiaries, by mode |
| `BasketWeaving/ColorFixative.cs`, `MiscSAResources.cs` (`DryReeds`, `SoftenedReeds`, `CrystalGranules`), `NaturalDye.cs`, `PlantPigment.cs`, `PlantPigmentHue.cs` | same | the resources, the pigment with ServUO's mixing rules, the five-use dye, the 34-hue pigment table and `IPlantHue`/`IPigmentHue`; `PlantHueLookup.FromItemHue` is ours (the plant hue behind an item hue, for crafted reeds) |
| `Plants/FertileDirtGump.cs` | `Services/Plants/FertileDirtGump.cs` | the "use fertile dirt?" question when a seed goes on a plot (the New Magincia branch dropped: `MaginciaPlantItem` is in neither tree) |
| `Plants/PottedCoffeePlant.cs` | same (3 types) | the plant (ISecurable), coffee grounds, coffee pod |
| `Plants/Raised Garden Beds/RaisedGarden.cs` | same (`RaisedGardenAddon`, `RaisedGardenDeed`, `GardenAddonComponent`) | the deed with its direction gump, the four shapes, the plot that knows its mound |
| `Plants/Raised Garden Beds/RaisedGardenPlantItem.cs` | same | the mound: no upkeep, its own art and messages, owner and co-owners only |

### Craft registrations (`server/customizations/Engines/Craft/`, the craft-registrations shape, each at ServerStarted and idempotent)

- `AlchemyCraftRegistrations.cs`: ServUO `DefAlchemy.cs` :147-149 ElixirOfRebirth, :154-217 Barrab (900), Jukari (901),
  Barako (903), Urali (904), Sakkhra (905), :311-346 NaturalDye, PlantPigment, ColorFixative, CrystalGranules,
  SoftenedReeds. ServUO's groups kept verbatim (1116348, 1116349, 1116353, 1044495): pinned's alchemy menu keeps the older
  Refresh-to-Explosion split and has none of them, so they appear as four groups after it (the 1011173 precedent).
- `CookingCraftRegistrations.cs`: `DefCooking.cs` :213-216 ParrotWafer, :222-232 PlantPigment, NaturalDye, ColorFixative,
  :399-410 EnchantedApple, GrapesOfWrath, FruitBowl (group 1073108 verbatim, absent from pinned's cooking).
- `BasketWeavingCraftRegistrations.cs`: `DefTinkering.cs` :259-317 SoftenedReeds and the eleven baskets, :351 Clippers,
  :602-605 HitchingRope (with Animal Lore 15). Registers the twelve book-gated types in `ClusterFRecipeGate.RequiredKeys`.
- `ClusterFRecipeGate.cs`: `RequiredKeys` (type -> key) checked first in `IsKnown`, whatever the band and the gating
  setting; `ClusterFRecipeStore.AllKeys` lists `flag:BasketWeaving`; `RegenRates.cs` reads Barrab's `HPRegenBonus`
  (ServUO `RegenRates.cs:236`). The test craft host (`CleanUpCraftHost.EnsureCraftSystems`) runs the three new
  registrations.

Every group, skill range, resource, amount, message and recipe id is ServUO's. **Left out of the tables:** Kurak (TigerPelt,
neither tree, Q-066), the three chocolate nutcrackers (SweetCocoaButter), FoodEngraver (engraving, below), KhaldunTastyTreat,
EnchantedPicnicBasket, HitchingPost and the coffee mug (all in neither tree). ServUO's `SetRequireResTarget` (pick the reed
stack) and `SetItemHue` have no pinned equivalent: the craft consumes the largest same-hue stack (our CraftItem hooks'
`GetBestGroupAmount`) and the plant-hue tables patch hands its hue to the item, which `OnCraft` turns back into a plant hue.

**For F-43's gating, the recipes this port makes visible** (minimum main skill): Cooking: ParrotWafer 37.5, FruitBowl 55,
EnchantedApple 60, NaturalDye 65, PlantPigment 75, ColorFixative 75, GrapesOfWrath 95. Alchemy: PlantPigment 33, Barrab,
Jukari, Barako, Urali, Sakkhra 51 (each with its own recipe scroll), ElixirOfRebirth 65, NaturalDye 75, ColorFixative 75,
CrystalGranules 75, SoftenedReeds 75. Tinkering: Clippers 50, HitchingRope 60, SoftenedReeds and the eleven baskets 75
(plus the book).

## Dependency walk and what was left out

Every `new`, `typeof`, base and cast in the 77 candidate files against pinned's 6,926 type names (`mu-types.txt` from
`D:\UO\ModernUO-pinned` at d4531cd9, as the port recipe says) and our 1,772, scripted. Then each file read.

### Not ported, with the cost (19 files)

| Files | Why | What it would take |
|---|---|---|
| `EngravingTools.cs` (13 types), `EmbroideryTool.cs` | a subsystem: ServUO's `IEngravable` is implemented by 9 bases (Food, Container, MonsterStatuette, BaseArmor, BaseClothing, Spellbook, BaseWeapon, BaseCreature, RewardSign), each with a saved `EngravedText`; pinned has it on BaseWeapon only (its own vet-reward engraver). Tools that engrave nothing are meaningless | a saved string on 7 more bases: 7 serialization bumps with migrations, plus the property lines. Decline here; worth a decision |
| `GorgonLens.cs` | D-88: needs `GorgonLenseCharges`/`GorgonLenseType` saved on BaseArmor, BaseJewel and BaseClothing, and the gaze check in our `Medusa.cs` (ServUO's 6 consumer files) | 3 serialization bumps plus the Medusa hunk; D-88 stands |
| `Armor Refinement/` (3) | a subsystem: 5 saved resist fields on BaseArmor (52 lines there), the DCI cap, 14 consumer files in ServUO (AOS, PlayerMobile, HitLower, Bola, StoneForm, the chest loot rolls D-38 already records) | a BaseArmor bump and an AOS hunk at least; D-38's "no refinement roll" stands |
| `Craft/Core/AlterItem.cs` | D-20: pinned has no alter-item system; needs `AlterContract` (excluded from the row), the soulforge check, `Altered`/`CanAlter` on three bases | a subsystem |
| `BasketWeaving/SilverSapling.cs` | the sapling is an ankh plus a seed that, in ServUO, moves where you respawn in the Abyss (`PlayerMobile.SSSeedLocation/Map/Expire`, `ResurrectGump`); without that the seed does nothing | 4 saved PlayerMobile fields and a resurrect hunk; the Underworld row's |
| `HealingStone.cs` | pinned ships the Healing Stone scroll but its spell is commented out of the registry (`Spells/Initializer.cs:185`); the stone alone is unreachable and meaningless | the Mysticism spell |
| `GemMiningBook.cs` | an equivalent is already on: pinned's mining gives the six ML gems as a bonus harvest without a book (`Mining.cs:206-217`); the book would be a flag with no consumer | nothing; for the register as "gem mining needs no book here" |
| `TelekinisisScroll.cs` | pinned's `TelekinesisScroll` (the correct spelling) is the same scroll | nothing (the stem proxy will keep counting it) |
| `DecorativeKitchenSet.cs`, `DecorativeStableSet.cs` | store bundles of 6 and 6 deeds and statues, every one in neither tree | their contents (reward-pool row) |
| `Craft/Core/AutoCraft.cs` | an equivalent: the shard's Make X run (cc-P18, `ClusterFCraftRun`) | nothing |
| `Craft/Core/CraftGroupCol.cs`, `CraftItemCol.cs`, `CraftResCol.cs`, `CraftSkillCol.cs` | equivalents: pinned's `List<T>` and `CraftCollectionExtensions` | nothing (four stems the proxy will keep counting) |
| `Plants/DisplayHelpTopic.cs` | a packet only ServUO's plant gumps send; pinned's gumps do not, and nothing ported here needs it | nothing |

### Behaviour that could not come across (for the register)

- **Kurak Ambusher's Essence** shows its buff and does nothing: its only consumer is the Myrmidex invasion battle
  (ServUO `BattleRegion.cs:58`), not ported, as on a ServUO shard with the invasion off; and it cannot be brewed
  (TigerPelt). The other five are whole.
- **Barrab's `GetHitBuff` and Jukari's `GetStamBuff`** are defined and called by nothing in ServUO either; kept as they are.
- **Fear essence and the tar potion effects** are `SendLocationParticles`/`SendMovingEffect` with ServUO's ids where ServUO
  sends raw `ParticleEffect`/`HuedEffect` packets; the tar potion's slow reaches only a mobile with a client (so a creature
  is not slowed), as the packet does in ServUO.
- **The clippers' modes** reset to clippings on a restart (ServUO saves them on the player).
- **The basket entries are hidden until the book is read** (ServUO shows them and refuses the craft), the shard's gate's
  rule; the refusal cliloc 1112253 is still the scouring toxin's by hand.
- **Cooking's `GetChanceAtMin`** gives the apple and the grapes 50% at minimum skill in ServUO (`DefCooking.cs:64-70`);
  pinned's DefCooking has no hook, so they start at 0% like every other entry.
- **The hitching rope** has nothing to supply until the hitching post lands.

## Alternatives for each patch, argued before patching

The subsystem policy: a failing patch beats copied upstream logic, and every patch names what it rejected.

1. **`BasePotion-sa-potion-effects.patch`** (9 enum members appended). Rejected: reusing pinned's unused `MaskOfDeath`
   values (two slots for nine potions, and a saved potion would read as the wrong kind); a parallel enum (BasePotion's
   constructor and saved field take `PotionEffect`). Appending after `FlintsPungentBrew` keeps every saved value.
2. **`AOS-grapes-of-wrath.patch`** (one hunk at the end of `AosAttributes.GetValue`, after our Pet Training term).
   Rejected: a StatMod or AosAttribute on the player (there is no attribute that reaches weapon and spell damage both
   without equipment); applying the bonus in `BaseMagicalFood` by hand (there is no damage hook on a Food). ServUO's own
   two lines, in the method ServUO puts them in.
3. **`BaseCreature-tasty-treat-damage.patch`** (one hunk in `AlterMeleeDamageTo`). Rejected: a `TempDamageBonus` field
   on BaseCreature (a serialization change for a 20-minute in-memory value; ServUO does not save it either). The value
   lives on `TastyTreat`; the hunk reads it.
4. **`PlayerMobile-urali-mana.patch`** and **`Spell-urali-trance.patch`** (one line each). Rejected: a StatMod for the
   mana (max mana is not a stat) and skipping the casting rule (Urali is then a quarter of itself). Both are ServUO's own
   lines at ServUO's own places.
5. **`PlantItem-raised-garden-hooks.patch`** (8 hunks: ServUO's six virtuals, `ValidGrowthLocation` and `IsUsableBy`
   made virtual, the art and three messages read through them, `RequiresUpkeep` in `PlantSeed`, `Pour` and
   `ApplyPotion`), **`PlantSystem-raised-garden-upkeep.patch`** (3 hunks: soft dirt, no malady damage, no new maladies
   without upkeep), **`Seed-raised-garden-plot.patch`** (the garden-plot branch of the seed's target). Rejected: a
   replacement of `PlantItem.cs` (a 700-line pinned file with its own old-client property list; a replacement hides
   drift, and these are 40 lines); a `RaisedGardenPlantItem` that copies pinned's `PlantSeed` (the water check, the
   labels and `Update` are private or non-virtual, so the copy would be most of the class). Pinned's static
   `GetLocalizedContainerType()` (the "bowl" the gumps name) is left as it is: making it an instance call ripples into
   four gumps, and the mound says "mound" in the three messages ServUO changes.
6. **`CraftItem-plant-hue-tables.patch`** (2 hunks: ServUO's four plant resources in `m_ColoredResourceTable`, and the
   pigment, reeds, clippings and `BaseContainer` in `m_ColoredItemTable`, `CraftItem.cs:395, :415-416`). Rejected:
   overriding `RetainsColorFrom` (the three Def* systems are pinned classes); `OnCraft` guessing the hue from the first
   stack left in the pack (the consumed stack is gone by then; the registrations' first draft did this and a two-colour
   pack came out wrong). With the tables, pinned's consume-by-hue groups and `resHue` do what ServUO's
   `SetRequireResTarget` does.

## Decisions taken inside the port (fidelity principle, D-4 rule)

- **Fixed:** Barako's Draft of Might adds its physical mod twice and never its cold mod, then removes each once, leaving
  +10 physical on the player for good (`EodonPotions.cs:367-374`); here the two mods it names are added and removed.
- **Fixed:** the shatter potion's three messages go to the thrower in ServUO ("X's shatter potion hits you" to X);
  they go to the victim.
- **Fixed:** ServUO's `PlantSeed` on a mound reads "This bowl of dirt already has a ~1_val~ in it" for the second seed;
  ServUO's own `1150441` ("This mound of dirt already has a seed in it!") is used, as its code intends.
- **Copied:** `ExplodingTarPotion`'s label is "a Greater Confusion Blast potion" (1095147), as in ServUO.
- **Copied:** the pigment `Mix` table's non-primary rules, which ServUO's own comment calls a guess.
- **Copied:** `TopiaryGump`'s buttons 7 and 8 give the same art as 6 and 1 (ServUO's table).
- **Copied:** the Valentine chocolate stacks (it is a `Food`), so two with different messages merge.

## Tests

Three new fact files, all `[Collection("Sequential UOContent Tests")]`:

- `server/tests/Items/Consumables/ConsumablesVerification.cs`, 16 facts: the enum values; the fifteen begging items; the
  fruit bowl; the grapes' damage, refusal and cooldown; the apple's 30 seconds; the platter and the pie; the tasty treat on
  your own pet, its refusal, the damage bonus and its end; the Eodon potions (resistances, Barrab's regen window, Urali's
  max mana and ticks, refusal, expiry, death); the shatter potion at 25, 20 and 19 potions; fear essence at resist 137.5;
  the elixir on a dead bonded pet; poppies dust; the tincture; the nutcracker; a round trip of the chocolate, the
  nutcracker and the dust; the five patched files in the build tree.
- `server/tests/Services/BasketWeaving/BasketWeavingVerification.cs`, 12 facts: the baskets' art; reeds stacking by colour;
  the mixing rules and a real mix; the dye's five uses and refusals; the toxin for a weaver and a non-weaver; the book at
  99.9 and 100; the clippers by mode; every craft entry's values and the left-out ones; the gate's key with gating on and
  off; a red basket woven from red reeds and red reeds softened at the menu; a round trip of the dye and the reeds; the
  CraftItem tables in the build tree.
- `server/tests/Services/Plants/RaisedGardenVerification.cs`, 7 facts: the four shapes; a seed on a plot in a house
  (planted dry, the plot and the mound linked, a second seed refused, a stock bowl refusing dry dirt); growth with no
  water and no damage against a stock bowl damaged by the same check; the occupied bed; the coffee plant; a round trip of
  a mound and its plot; the three plant files in the build tree.

**Seen failing first.** Two break sets on the real tree (`breaks.py` and `breaks2.py` in my scratchpad: each break a
one-line change in a ported file or in a patch's `+` lines, applied, built through `build.sh --tests-only`, reversed, the
touched files hashed before and after: byte-identical both times):

- 34 breaks at once (the enum order, the fruit bowl's fill, the grapes' +35 in the AOS patch, the apple's cooldown, the
  platter's pieces, the treat's loyalty and the damage divisor in the BaseCreature patch, Barako's cold mod, the Urali
  mana line in the PlayerMobile patch, the shatter threshold, the fear paralysis, the elixir's revive, the dust merge,
  the tincture's flag, the nutcracker's art and its white label, the Spell patch's Urali line, a basket's art, the mix
  of two primaries, the dye's uses and its hue, the toxin's two reeds, the book's 100, the clippers' reed mode, a
  basket entry's reeds, the gate's key check, `BaseContainer` in the colour-table patch, a fifth small-bed plot, the seed
  plot's fertile flag in the Seed patch, the no-upkeep guard in the PlantSystem patch, the dry-planting guard in the
  PlantItem patch, the coffee plant's stage, the mound's saved plot link): **30 failed, 1,325 passed** of 1,355: 30 of
  the 35 new facts red, every other fact green.
- The 5 that stayed green had no effective break aimed at them (one break was absorbed by pinned's own hue check on
  stacking; four had none). A second set of 5 (a begging item's art, the reeds' hue, the colour-table patch's line order,
  the PlantItem patch's `RequiresUpkeep` line, the bed's plant check): **8 failed, 1,347 passed**: those 5 red (plus three
  neighbours that read the same code).

Greens: builds 1 to 4 were compile fixes (usings, the serialization generator's property names, pinned's
`PlayerMobile.AddBuff`, an xUnit analyzer rule); build 5 ran the suite with 8 of the 35 red (4 wrong expectations of mine:
stacked pieces, the mound's dirt art until stage 4, one toxin for a two-toxin entry, a worn pack as a target; 2 host
differences: pinned's zero-rate mana regen in the host, and TreasuresOfTokuno's config that the server loads and the
host did not; 1 ServUO bug, the pigment's bottle, fixed in the code; 1 control-case setup); builds 6 and 7 narrowed
those; build 8 and the final build 9 after the restores: **1,355 of 1,355**.

**The test shard boots clean, and the test world loads, saves and reloads.** `sl-modernuo:cc-p128` on a copy of the
test world's newest automatic backup (`2026-10-16-14-05-00`, saved by the running image), the parent folder mounted as
the compose file does, no port published (the running test shard was not touched):
- boot 1: `[ShardVersion] Shattered Legacy 2026.10.16.2 (64 version(s) in the changelog)`, `Loading world done (207066
  items, 35056 mobiles)`; stopped: `Saving world done`, `Writing world save snapshot done`;
- boot 2 on that save: `Loading world done (208308 items, 35158 mobiles)` (the seeders' additions), saved the same way,
  no error or exception in either log.
- Nothing in the world is a type of this port yet, so the patched `PlantItem` and `Seed` serialization (no field was
  added to either; `PlantSystem` and `Seed` keep their versions) is exercised by every bowl and seed the world holds
  loading and saving as before. No migration JSON was needed: no pinned type's serialized shape changed.

**Not done:** a client. Nothing here was seen in game.

## Play-test items added

Through the For Chase list below; Who and steps in `testing/bot-triage.md` (P128 group) and `testing/playtest-steps.json`:
P128-1 BOT-PARTIAL (magical foods), P128-2 BOT-PARTIAL (elixir and tribal potions), P128-3 BOT-PARTIAL (thrown potions),
P128-4 BOT (tasty treats), P128-5 BOT-PARTIAL (basket weaving), P128-6 BOT (pigments and dye), P128-7 BOT-PARTIAL
(raised garden), P128-8 CHASE (the small items), P128-9 CC (test world boot).

## Deviations and decisions for Chase

1. **Four subsystems declined, each worth a decision** (table above): engraving (7 serialization bumps), the Gorgon
   lens (3 bumps plus Medusa; D-88), armour refinement (a BaseArmor bump plus AOS; D-38), item altering (D-20). None was
   built inside this task, as AGENTS.md says. Say which, if any, you want built, and it gets its own prompt.
2. **The basket-weaving book is an account key** (`flag:BasketWeaving`), shared by the account's characters like every
   recipe here, and the gate hides the twelve entries until it is read. ServUO shows them and refuses the craft.
3. **The clippers' mode is not saved** (clippings after a restart).
4. **Kurak Ambusher's Essence is an icon only** and cannot be brewed until the tiger pelt exists.
5. **Cooking's 50%-at-minimum chance for the apple and the grapes is not here** (pinned has no hook; they start at 0%).
6. **The register entries this needs** (agents do not edit `docs/`): items 2 to 5, the fixed Barako and shatter bugs, the
   begging rewards without a Begging table, the hitching rope without a post, and the 19 left-out files as one entry each
   with the cost above as "reverses when".

## For Chase

**Rebuild the test shard** (console, Test shard, Rebuild) before trying these.

1. **Cook the magical foods:** with Cooking 95, an apple, grapes, a greater heal and a greater strength potion, an empty wooden bowl and three each of pears, apples and bananas, make an enchanted apple, grapes of wrath and a fruit bowl under Magical Foods; eat the grapes (your status shows +35 damage for 20 seconds, a second bunch is refused, two minutes later it is not) and the bowl while hungry (+5 to each stat for two minutes).
2. **Brew and drink:** with Alchemy 100, Medusa blood, spiders' silk and a bottle make an elixir of rebirth and use it on a dead bonded pet; `[add BarrabHemolymphConcentrate` and drink it (an icon; a second is refused), `[add SakkhraProphylaxisPotion` and drink it (poison +10, energy +5 for ten minutes). The five tribal potions are in the alchemy menu, each wanting a recipe scroll.
3. **Throw:** `[add FearEssence`, `[add ShatterPotion`, `[add ExplodingTarPotion`; throw each near or at a second character carrying 25 potions: three seconds of paralysis on a failed resist, a fifth of the potions gone, a minute at a walk; each refuses a second throw for a minute.
4. **Feed a pet:** `[add TastyTreat` and `[add IrresistiblyTastyTreat`; double-click and target your pet (stats +5% for 20 minutes, loyalty full), a second at once is refused; after 22 minutes drop the irresistibly tasty treat on it (+15%, and it hits a tenth harder).
5. **Weave:** with Tinkering 100, `[add BasketWeavingBook`, `[add Clippers`, `[add ScouringToxin` and two decorative plants of one colour: read the book (below 100 it refuses), set the clippers to cut reeds from their context menu and clip both, double-click the toxin on the reeds, then at the tinkering menu with the softened reeds and shafts weave a round basket of the reeds' colour. Without the book the baskets are not offered.
6. **Pigment and dye:** with Alchemy 75, `[add PlantClippings` set to Red and another to Blue (`[props` PlantHue), bottles and `[add ColorFixative`: make a pigment from each (Ingredients), double-click the red and target the blue (purple, an empty bottle left; the same colour twice is refused), make a natural dye from the purple and the fixative, dye a shirt five times (an ingot is refused).
7. **Garden:** in your house, `[add RaisedGardenDeed`, choose a shape and place it; use a seed on a plot (with fertile dirt in the pack it asks whether to use 20): a mound rises planted with no watering, its dirt reads soft, it grows a stage a day (`[props` the mound and set ForceGrow to hurry) with no pests, the bed refuses to be chopped while planted, and a stranger cannot open the mound.
8. **The small items:** `[add PottedCoffeePlant` in a house (set PlantStatus to Stage4, double-click: a pod), `[add PoppiesDust` on an unidentified seed, `[add SkinTingeingTincture` (a hue gump over your paperdoll; OK changes your skin), `[add ChocolateNutcracker` (unwraps), `[add TurkeyPlatter` (eight roast pieces then gone), `[add ValentineChocolate` (a message), `[add BegCookies` (Acquired by begging).
9. **Test world boot:** done by CC on a scratch copy (below).

## Repo size rule

No pending file in either repo is over 5 MB; the largest new one is `EodonPotions.cs` (about 18 KB). Build logs, the
type dumps, the patch generator and the break set stayed in the session scratchpad.

## Commit preflight

`Commit-ShardWork.ps1 -DryRun`, after the last edit:

```
Repo Result
---- ------
code dry run
docs dry run
```

code, 83 files: `CHANGELOG.md`, `VERSION`, `docker/uo/apply-patches.sh`, the recipe gate, the recipe store, `RegenRates.cs`,
the test craft host, the three registrations, the 36 consumables, the 3 leaf resources, the 22 basket-weaving and plant
files, the 9 patches, the 3 fact files. docs, 9 files: this note, `testing/bot-triage.md`, `testing/playtest-steps.json`,
`README.md`, `dashboard.html`, `tools/progress.json` and `tools/expansion-coverage.json` from `progress.py`, and the
machine output (`testing/SUMMARY.md`, `testing/play-tests.json`). No file is near 5 MB.

P128 DONE
