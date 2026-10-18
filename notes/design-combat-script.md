# Shattered Legacy combat script for TazUO Legion: design and roadmap

Written by cc-P145 (2026-10-18) from the 2026-10-16 features chat with Chase. Agents never edit `docs\`; the overseer
moves this into `docs\design\` and marks it in progress in `docs\feature-queue.md`. Phase 1 (melee core and the item
rater) is built by P145; every later phase is designed here so the prompts that build them have a structure to plug
into, not a rewrite.

The shard allows unattended (AFK) farming (Chase, 2026-10-11), so AFK mode is a first-class mode, not a hidden one.

## 1. What it is

One Legion (Python) script a player runs in TazUO that fights for them, keeps them and their companions alive, and
rates the magic loot they pick up. It is a *player-side* tool: the server knows nothing about it except one small
command the loot rater asks (`[artificerrank`, section 8.5). It lives in the Legion scripts repo
(`CainUnAble923/shattered-legacy-scripts`, cloned at `D:\UO\sl-scripts`), where P144's updater publishes scripts from,
so players get it and its updates the same way they get `SL_Mining.py`.

Everything here is checked against the Legion API as the installed client exposes it
(`ShatteredLegacy-2026.10.02.0840\app\tazuo\LegionScripts\API.py`, 3,723 lines) and TazUO's source in
`D:\UO\tazuo-sl-build\src`. The online docs at https://tazuo.org/legion/legionapi/ describe the newest client; the
installed stub is the one that binds, and the newer build (`D:\UO\tazuo-sl-build\client`) adds only `CreateSlider`,
`RequestHotkey`, `CreateEffect` and slider callbacks, none of which the script uses.

## 2. Files and where they live

P144 is DONE: scripts live at the top of the scripts repo, and P144's publisher ships **top-level `*.py` only**
(`Get-LegionSourceFiles`, `player-package\payload\app\LegionScripts.ps1`; the manifest check refuses paths). So the
script is one entry file and seven sibling modules, all top level, all prefixed `SL_Combat` so they sort together in
TazUO's script list:

| File | Module | Holds |
|---|---|---|
| `SL_Combat.py` | entry | Settings load, hotkeys, the control gump, the main loop. The only one to run. |
| `SL_Combat_Settings.py` | settings | Defaults, per-character persistence (`API.SavePersistentVar`, scope `Char`, JSON), profiles store, the shared-var names. |
| `SL_Combat_Core.py` | core | The state machine (Idle, Engage, Heal, Recover, Loot), the per-tick priority, shared vars other scripts read. |
| `SL_Combat_Targeting.py` | targeting | The notoriety rules, the hunt list, companions, "who is attacking me", target selection. |
| `SL_Combat_Survival.py` | survival | Bandage self, heal and cure potions, companion care, panic. |
| `SL_Combat_Melee.py` | melee | Weapon specials by mana and cooldown, the stance hook interface. |
| `SL_Combat_Rater.py` | rater | The property table, tooltip parsing, scoring, compare mode, tiers, unravel against known imbues, Suggest. |
| `SL_Combat_Gump.py` | gump | The control gump, the settings page, the profile editor, the rated-items list. |

Modules import each other by name (`import SL_Combat_Rater`): TazUO puts the `LegionScripts` folder and the script's
own folder on the Python search path (`ScriptFile.SetupPythonEngine`, `LegionScripting\ScriptFile.cs:170-176`).
Running a module on its own prints one line saying to run `SL_Combat.py` and stops. The repo's `tests\` folder holds
CPython unit tests for the pure parts (rater, targeting rules) against a fake `API`; the publisher never ships it.

Why not a subfolder: TazUO would list it as one group, which is tidier, but P144's publisher and its manifest check
are top-level only, and changing them is a P144 follow-up, not a P145 change (Deviations in the P145 notes).

**Module cache.** TazUO keeps one Python engine per script unless "Disable module cache" is on in Legion settings
(`LScriptSettings.DisableModuleCache`). After editing a `SL_Combat_*` module, stop and start `SL_Combat.py` with that
setting on, or restart the client; the entry file alone always reloads.

## 3. Modes

| Mode | Who moves | What the script does |
|---|---|---|
| **Assist** | the player | Targeting, specials and healing. The script attacks what the rules allow within `engage range` and never pathfinds except to step back to a companion it is bandaging. |
| **AFK** | the script | Assist plus: seeks targets within `seek range` of an **anchor** point, pathfinds to them (`API.PathfindEntity`), and returns to the anchor when nothing is left. Never wanders past `leash range` from the anchor. |

The mode is a gump radio and a hotkey. Switching to AFK sets the anchor where the player stands unless one is pinned.

Hotkeys (defaults, all editable in Settings; the `OnHotKey` format, `CTRL+SHIFT+F1` style):

| Action | Default | Does |
|---|---|---|
| Toggle on/off | `CTRL+F9` | Enabled or disabled; disabled keeps the gump and hotkeys, fights nothing, heals nothing. |
| Switch mode | `CTRL+F10` | Assist and AFK. |
| Pause | `CTRL+F11` | Freezes the loop in place (no targeting, no healing) until pressed again; for talking to an NPC mid-hunt. |
| Panic | `CTRL+F12` | Stop attacking, drop war mode, heal (bandage and potions on their own rules), then **recall** to the configured rune or runebook entry, or **run** to the anchor, as configured; or neither, just stand and heal. |

## 4. The core loop

A state machine ticked every 0.2 s (`API.Pause(0.2)` with `API.ProcessCallbacks()` each tick so hotkeys and gump
buttons run). States:

| State | Meaning | Leaves when |
|---|---|---|
| Idle | nothing to fight | a target is chosen (Engage) or a heal is due (Heal) |
| Engage | fighting the current target | it dies or is lost (Loot or Idle), HP crosses the heal threshold (Heal), panic |
| Heal | a heal action is in flight (bandage timer, potion delay) | the bandage timer ends or HP is back above threshold; fighting continues underneath in Assist, pauses pathfinding in AFK |
| Recover | after a fight: wait for HP and stamina to recover before seeking the next target (AFK only), walk back to the anchor | thresholds met |
| Loot | open the corpse so TazUO autoloot takes the basics, then hand new magic items to the rater | done, or a new attacker appears |

The per-tick priority is fixed, whatever the state:

1. **Stay alive:** self bandage, cure, heal potion, panic trigger.
2. **Protect companions:** vet or bandage a companion under its threshold; "all guard me" once when the player drops under the guard threshold.
3. **Fight:** keep or pick a target, attack, specials.
4. **Loot:** only with no live hostile within `engage range`.

Shared vars (prefix `SLC_`), set every tick so a looter or pet manager can read them:
`SLC_Enabled` (0/1), `SLC_Paused`, `SLC_Mode` ("assist"/"afk"), `SLC_State`, `SLC_Target` (serial or 0),
`SLC_Anchor` ("x,y,z,map" or ""), `SLC_Companions` (comma-separated serials), `SLC_HuntList` (semicolon-separated
names), `SLC_InDanger` (1 while under the heal threshold or poisoned), `SLC_LastRated` (serial of the last rated item).

## 5. Targeting rules (no accidental animal slaughter)

Notoriety comes from `mobile.Notoriety` (`API.Notoriety.*`).

| Notoriety | Rule |
|---|---|
| Murderer (red), Criminal, Enemy (orange) | always a target |
| Gray | only if it is **attacking the player or a companion**, or its name is on the **hunt list** |
| Innocent (blue), Ally (green), Invulnerable | never |
| Own pets, companions, party | never, whatever their notoriety |

"Attacking the player" is decided client-side, since the API has no "who hit me": a gray counts as attacking when it is
in war mode (`InWarMode`) within 2 tiles of the player or a companion **and** the player's or that companion's hits
dropped in the last 3 s, or the player attacked it themselves (`API.LastTargetSerial`, Assist mode consent). The hunt
list is case-insensitive name matching (whole name or a word of it: "ettin" hits "an ettin"), edited in the gump, kept
per character, for monster hunts and culling quests.

"Own pets and companions" is the union of: serials the player added with the gump's **Add companion** target (the
squire, the evo pet, a tamed pet), `API.GetAllFriends()`, `API.GetPartyMemberSerials()`, and any mobile the client
flags renamable (`mobile.IsRenamable`: TazUO's own "own followers" test, `NameOverHeadManager.cs:203`).

Selection: stick to the current target until it is dead or gone. If something else starts attacking the player (or a
companion) mid-fight, re-pick by the setting: **nearest** or **lowest HP**. Candidates come from
`API.GetAllMobiles(distance=..., notoriety=[...])`, filtered through the rules above, `API.IgnoreObject` for things
that stay out of reach.

## 6. Survival

| Rule | Setting (default) | Call |
|---|---|---|
| Bandage self | under `bandageAt` % (70) or poisoned | `API.BandageSelf()`; one cooldown bar ("Bandaging") sized from Dex: `11 - Dex/20` s self, min 1 (the stock formula), overridable |
| Heal potion | under `healPotionAt` % (45), not while a heal potion cooldown runs (10 s) | `API.UseType(0x0F0C, container=API.Backpack)` |
| Cure potion | poisoned and under `curePotionAt` % (90), or poisoned with no bandage out | `API.UseType(0x0F07, ...)` |
| Refresh potion | optional, under `refreshAt` % stamina (0 = off) | `API.UseType(0x0F0B, ...)` |
| Companion care | a companion under `companionHealAt` % (60): bandage it (`UseType` bandage, `WaitForTarget`, `Target(pet)`), walking to within 2 tiles first | per companion cooldown |
| All guard me | once when the player drops under `guardAt` % (50), again after 20 s | `API.Msg("all guard me")` |
| Panic | hotkey, or automatic under `panicAt` % (0 = off) | stop attacking, war mode off, heal, then recall or run (section 3) |

Potion graphics are the stock ones (heal 0x0F0C, cure 0x0F07, refresh 0x0F0B); bandage 0x0E21. Out of bandages or
potions is said once (SysMsg) and the rule is skipped until the pack changes.

## 7. Melee module and the stance hooks

The melee module is the first **combat module**. A module is a Python object with these methods, all optional:

```
name                      "melee"
wants(target) -> bool     could this module fight this target now (melee: always)
on_engage(target)         called once when a target is chosen
on_tick(target, ctx)      every tick while engaged; ctx has hits%, mana, stamina, distance, settings
on_disengage()            target died or was dropped
on_low_hp()               HP crossed the heal threshold while engaged
```

Melee's `on_tick`: step to the target if not adjacent (AFK), `API.Attack(target)` to re-assert, and specials:
toggle the **primary** or **secondary** weapon ability (`API.ToggleAbility("primary"|"secondary")`, checked with
`PrimaryAbilityActive()`/`SecondaryAbilityActive()`) when mana is at or above the setting, the special's own cooldown
(setting, default 3 s) has passed, and the chosen special is enabled; "which special" is a setting (primary, secondary,
alternate, none). The names come from `API.CurrentAbilityNames()` for the gump.

**Stances** layer on top of a combat module: a stance is an object with `on_tick(target, ctx)` and `on_engage` that
the core calls *after* the module's. Bushido (Lightning Strike, Confidence, Evasion), Chivalry (Consecrate Weapon,
Enemy of One, Divine Fury, Close Wounds as a heal) and Necromancy (Curse Weapon, Vampiric Embrace) are each a stance in
a later phase, registered in a list in `SL_Combat_Core` (`STANCES`). Phase 1 ships the list empty and one example
stance in comments. Toggle moves are read with `API.IsSpellActive(name)` so a stance never double-casts.

## 8. The item rater (loot helper)

### 8.1 On and off, and what it looks at

The loot helper is a toggle independent of combat. TazUO autoloot takes the basics (gold, regs, what the player's
autoloot list says); the rater only evaluates **magic items**: anything whose tooltip has a property line the table
knows. Sources: items new in the backpack since the last pass (`API.ItemsInContainer(API.Backpack)` diffed each
Loot state and on the **Rate backpack** button), and, when autoloot is off, the corpse's contents after `UseObject`.

Properties are read from the tooltip: `item.NameAndProps(True)` (one string, newline separated; `wait=True` requests
the OPL when the client lacks it). The first line is the name; each other line is matched against the table.

### 8.2 The property table (data-driven)

One entry per property, in `SL_Combat_Rater.PROPERTIES`; adding a shard property is one line:

```
("Hit Chance Increase", r"^hit chance increase (\d+)%", 45, "HitChanceIncrease", 45),
#  display name           tooltip line regex             item cap  player attribute   player cap
```

- *item cap* is the Artificers' catalogue `MaxVanilla` (the Full tier) so a value is scored as a fraction of what one
  item can carry (`ArtificersImbueGump.cs` catalogue rows).
- *player attribute* names the `API.Player` field that holds the character's current total (`HitChanceIncrease`,
  `DefenseChanceIncrease`, `SwingSpeedIncrease`, `LowerManaCost`, `FasterCasting`, ... all present on `ApiPlayer`),
  or `None` for a property with no character-wide total.
- *player cap* is the character-wide cap (HCI 45, DCI 45, SSI 60, DI 100, LMC 40, LRC 100, FC 2 (4 for a
  Necromancer, the Suggest step notes it), FCR 6, resists from `API.Player.MaxFireResistance` and the others, which
  the client already knows per character).

The shard's custom properties are in the same table with their own regexes: `Bountiful`, `Mastercraft`, `Prospector`,
`Butcher's Eye`, `Fortune's Favor`, `Echo of the Loop`, `Time Slip`, `Shatter`, `Bond`, `Spell Leech`, `Renowned`, all
shown by the server as `<Name> <value>%` (`ImbueCustomStore`, cliloc 1049644). Skill bonuses (`+15 swordsmanship`)
match one entry with the skill name captured; slayers match one entry each for single and super slayers. Properties
the server adds later (loot box luck, gathering, monster parts) are one more line each.

### 8.3 Scoring

A **profile** is a dict of `{property display name: weight}` plus an optional cap override per property. For each
matched property with value `v`, item cap `c`, weight `w`:

```
share     = min(v, c) / c                       how much of one item's worth it carries
headroom  = 1.0                                  if the property has no player cap
          = clamp((playerCap - playerTotal) / c, 0.15, 1.0)   otherwise
points    = w * share * headroom
```

So a property the character already has at or near cap counts for at most 15 % of its weight (never zero: the item
may replace the piece that provides it). The item's **score** is the sum, and the **reason** is the top three
contributors by points, written as "HCI 15 (+6.2), SSI 20 (+4.0), DI 30 (+2.1)".

Properties with a weight of zero are ignored; a weight can be negative (a profile that dislikes Mage Weapon on a
warrior's sword).

### 8.4 Compare mode

Toggle. Off: the score stands alone. On: the item's **slot** comes from `item.GetItemData().Layer` (the tiledata
layer: 1 one-handed, 2 two-handed, 3 shoes, 4 pants, 5 shirt, 6 helmet, 7 gloves, 8 ring, 9 talisman, 10 neck, 11
hair, 12 waist, 13 inner torso, 14 bracelet, 17 middle torso, 18 earrings, 19 arms, 20 cloak, 22 outer torso, 23 outer
legs, 24 inner legs); the equipped piece there is `API.FindLayer(name)` and is scored with the same profile with the
headroom computed **as if that piece were off** (its own contribution added back to the room). The gump shows
`+12.4 upgrade` or `-3.1 downgrade` per slot, and an item that beats the equipped piece lands in **Upgrade**.

### 8.5 Tiers and actions

| Tier | Rule (first that matches) | Action |
|---|---|---|
| **Upgrade** | compare on and the item scores above the equipped piece by at least `upgradeMargin` (2.0) | move to the Keep bag, say so |
| **Keep** | score at or above `keepAt` (profile value, melee starter 12) | Keep bag |
| **Unravel** | at least one property the character **can imbue** (section 8.6) | Unravel bag |
| **Sell** | any matched property at all | Sell bag |
| **Junk** | nothing the table knows | left where it is (never dropped by the script) |

A later tier the feature queue names, **Requisition** (F-47), goes between Upgrade and Keep when the requisitions
board exists: a property pattern the board asks for.

Auto-sort is a toggle; the bags are targeted once in Settings (`API.RequestTarget`) and kept per character; a missing
bag means the item stays in the pack and the result line says "no Keep bag set". Moves use `API.QueueMoveItem`.

### 8.6 Unravel and the Artificers' Order rank

On this shard unravelling is not OSI's residue, essence and relic: the Artificers' table **extracts a property** into an
`Essence of <Property>` or **fully disenchants** (shards plus a chance at each property's essence)
(`ArtificersImbueGump.cs:1267-1341`, `PropertyEssence.cs`). An essence is only useful to someone who can **imbue that
property**, and that is what rank gates: a property is learned at Basic at its ladder rank (the rank's formula book),
Refined a rank later, Full two later (`ImbuingTable.DefaultLadder`, `docs/artificers-imbuing-design.md`); the 140+
path grants others by account. So the rater does not need the rank number alone, it needs **the list of properties the
account knows**, and the rank is the headline.

The best way for the client to learn that was weighed (the prompt's question):

- *Tooltip:* nothing on the player or their items carries the rank. No.
- *Gump:* `[guild` opens the Guild Directory with "Rank: ..." per joined guild, paginated eight rows a page; the
  Artificers' Guildmaster gump shows rank and standing but needs the NPC. Readable with `API.GetGumpContents`, but
  neither lists known properties, and the row-to-label pairing is layout guesswork. No.
- *Command:* one player command that prints the rank and the known list in plain lines the script reads from the
  journal (`API.GetJournalEntries(seconds, "$^\[Artificer\]")`). **Chosen.** It is also useful to a player typing it.

`[artificerrank` (ModernUO, `server/customizations/Imbuing/ArtificerRankCommand.cs`, a Player command declared
`[ShardCommand(CommandCategory.Player)]`) prints:

```
[Artificer] rank 2 of 5 (Journeyman), standing 1,200, 31 properties known
[Artificer] Basic: Balanced, Bonus Dexterity, ...
[Artificer] Refined: Cold Resist Bonus, ...
[Artificer] Full: Luck, ...
[Artificer] end
```

Lines are at most 180 characters; a tier that needs more repeats its `[Artificer] <Tier>:` line. A character that is
not a member still gets the free properties at Basic, because that is what the account can imbue. The script sends the
command on **Refresh rank** (and once per session when the cache is older than a day), parses, caches the result in a
persistent var with the time, and the Unravel tier uses the known list. Test shard only until Chase promotes it, with
a fact seen failing first (`server/tests/Misc/ArtificerRankCommandVerification.cs`).

### 8.7 The results gump

Scrollable list, newest first: item picture, name, score, tier (coloured), the reason, and for compare mode the
slot delta. Buttons: Rate backpack, Sort to bags, Clear, Refresh rank. A row's tooltip is the item's own tooltip
(`SetEntityTooltip(serial)`).

## 9. Profiles and Suggest

Profiles are named weight tables kept per character in the settings JSON; the gump's profile editor lists every table
property with a weight box and a cap box, Save as, Delete, and **Suggest**.

Shipped: **Melee starter**: HCI 10, DCI 8, SSI 8, DI 8, Hit Life Leech 6, Hit Stamina Leech 4, Hit Mana Leech 3,
Hit Lower Defense 4, Hit Lower Attack 3, resists 3 each, Strength 3, Dexterity 3, Hit Point Increase 3, Hit Points
Regen 2, Stamina Regen 3, Luck 2, Enhance Potions 2, LMC 2, Mage Weapon -5, the hit spells 2 each, slayers 4 (single)
and 6 (super), Self Repair 1, Durability 1, custom gathering properties 0, Bond 3, Time Slip 4, Shatter 4.

**Suggest** reads `API.GetSkill(name).Value` for the combat skills and `API.Player.*` totals and writes a profile with
an explanation, one plain line per decision, for example:

- "Hit Chance is 25 of 45: Hit Chance weight raised to 14."
- "Swing Speed is at cap (60): weight dropped to 1."
- "Chivalry 80: Lower Mana Cost and Faster Casting weights raised; Faster Casting cap 2 (4 with Necromancy)."
- "No Magery: Spell Damage, Faster Cast Recovery and Lower Reagent Cost set to 0."
- "Fire resist 70 of 70: fire resist weight dropped to 1."
- "Healing 60 and Anatomy 60: Enhance Potions kept low; bandage-based healing favours Dexterity and Hit Points Regen."

The player can Accept (saves as "Suggested <date>" and selects it) or edit the boxes first.

## 10. Later phases (design only, not built by P145)

Each is a combat module or a stance (section 7) plus settings and a gump page, in a prompt of its own.

- **Archer module:** `wants(target)` true when a ranged weapon is equipped (`API.FindLayer("TwoHanded")` graphic in the
  bow table); keeps `range` tiles (kite step away in AFK when the target closes, pathfind back when it flees), checks
  ammo (`API.FindType` arrows 0x0F3F or bolts 0x1BFB by weapon type), restocks from a bag or stops with a warning,
  specials as melee (Moving Shot and Armor Ignore are the usual pair).
- **Mage module:** a spell rotation by mana band (full: Flamestrike or Energy Bolt; mid: Lightning; low: melee or
  wand), `API.CastSpell` then `API.PreTarget(target, "harmful")`, `API.Player.IsCasting`/`IsRecovering` gates, Magic
  Reflect and Protection as buffs by `API.BuffExists`, Greater Heal and Cure as **survival** actions the survival
  module calls when the mage module is active, meditation in Recover.
- **Tamer module:** pet commands (`all kill` plus `API.Target(target)`, `all follow me`, `all guard me`), pet healing
  as the companion-care rule with Veterinary bandages and Greater Heal, pet stay-close logic in AFK, a pet-dead
  panic (stop, run or recall, never leave a bonded pet behind without saying so).
- **Stance modules:** Bushido (Confidence under threshold, Lightning Strike when mana allows and no special is up,
  Evasion on heavy incoming damage, Honor as a virtue on engage), Chivalry (Consecrate Weapon on engage, Enemy of One
  against a single target, Divine Fury when stamina is low, Close Wounds as a survival heal, Remove Curse), Necromancy
  (Curse Weapon on engage, Vampiric Embrace toggled at start if chosen, Evil Omen before a hit spell). Each is a list
  entry in `STANCES` with its own settings block and gump page.
- **Skill training mode:** fight with a chosen skill to push gains: the module forces a weapon or spell that uses that
  skill, picks targets by the skill's difficulty band (the hunt list can be seeded by level), watches
  `API.GetSkill(name).Value` and stops at a target value; also an AFK "train in place" against a chosen spawn.
- **Looter integration:** the shared vars let a dedicated looter script run beside this one; the rater exposes
  `rate_item(serial)` for it.

## 11. What the server never does

The script never asks the server for anything beyond `[artificerrank`. No new properties, no extra packets, nothing
that changes play for a character without the script. The command is readable by any player and changes nothing.

## 12. Open questions for Chase (none blocking)

1. Whether `SL_Combat_*` as seven top-level modules is acceptable until P144's publisher learns one subfolder (section 2).
2. The default hotkeys (section 3), chosen to avoid TazUO's own F-key macros; change any in Settings.
3. The melee starter weights (section 9) are a first guess for a swordsman with Healing; tune in play.
