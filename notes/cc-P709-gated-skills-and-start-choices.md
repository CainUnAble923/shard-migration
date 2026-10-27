# P709: learning Chivalry and Necromancy, and choosing starting skills

October 27, 2026. Design for Chase's answers and later build prompts. No code changes.

Start players with a few understandable ways to play. Let them discover the more specialized skills through teachers in the world. Chivalry and Necromancy each need a short quest before that character can train or use the skill. A book alone should not open either school.

Recommend earning each permission once per character and keeping it through every reset. A character can learn both. Chivalry's dependence on karma and Necromancy's karma loss provide a natural tradeoff without forcing a permanent class choice. Neither quest raises a skill or its cap. The reward is permission to begin, the necessary book, and a clear next step.

For creation, recommend four beginner templates plus a shorter custom skill list. Choosing a template and choosing Tutorial Island or New Haven are separate choices. Skipping the tutorial gives no school permission. The quests, names, amounts, and restrictions proposed below await Chase's answers. His request to gate Chivalry and Necromancy is the settled scope; this note does not decide additional gates.

## What already exists

Paths marked `C/` are relative to the code work copy's `server/customizations/`. `U/` means `D:/UO/ModernUO-pinned/Projects/UOContent/`, inspected at pinned commit `d4531cd94b739613155225c234900de9f47d2c88`. Source reading establishes behavior in the tree, not deployment or a successful client run.

| Topic | Source evidence and design consequence |
| --- | --- |
| Starting skills and professions | `C/CharacterCreation.cs:19` contains the broad starting list, including both schools. `:242` uses the server profession's skills when a profession is selected. `:425` validates custom allocations, rejects an individual value above 50, checks duplicates, and accepts totals of 100 or 120. Both the profession and custom routes need the new policy. |
| Stock Paladin and Necromancer | Pinned `Distribution/Data/Professions/SA/Prof.txt` defines Paladin as Chivalry, Tactics, Focus, and Swordsmanship at 30 each; Necromancer as Necromancy, Spirit Speak, Swordsmanship, and Meditation at 30 each. `C/CharacterCreation.cs:497` gives profession equipment separately from skill assignment, including a Necromancer book at `:551` and Book of Chivalry at `:589`. Merely removing two skills from the custom list leaves profession and equipment problems. |
| Where professions come from | `U/Misc/ProfessionInfo.cs:52` reads a found `prof.txt`, otherwise the expansion's distribution copy. Server definitions and the player's creation display must agree. The effective installed client profession file and skill picker were not inspected in a running client. |
| Caps today | `C/ClusterFSkillCaps.cs:11` defaults to 200. Its player application at `:176` sets every individual cap, including on login/load. Setting a locked school's cap to zero once would not survive that policy. Use a saved permission and enforcement, not a one-time cap edit. Running settings are unverified. |
| F-12 target | [Levels and loops](f12-levels-loops-caps.md) specifies maximum 50 at creation, 100 after the first reset, then +5 to 200 at loop 21. Every skill remains learnable on one character. `C/Tutorial/ClusterFLoops.cs:31` contains that ladder, but `:40` is still an empty reset integration method. A saved loop counter is not real current-level progression. |
| Later school training | [October 5 decisions](f12-decisions-2026-10-05.md) require a Training Ward or special quest content beyond stock casting ceilings. [P535](cc-P535-skills-design-vs-build.md) distinguishes that unfinished work from the gain machinery already built. P709's permission to start at zero is a separate gate. It does not supply training to 200 or reopen the rejected blanket school gain extension. |
| Chivalry mechanics | `U/Spells/Chivalry/PaladinSpell.cs:25` checks tithing and mana; `:136` includes karma and Chivalry in power. `U/Gumps/TithingGump.cs` consumes backpack gold and adds the same number of tithing points. `U/Items/Skill Items/Magical/BookOfChivalry.cs` defaults to all ten abilities. Keep those mechanics. |
| Necromancy mechanics | `U/Spells/Necromancy/NecromancerSpell.cs:22` computes negative karma awards, including the Increased Karma Loss attribute. Its damage skill is Spirit Speak. There is no negative-karma admission requirement in that school base. Do not describe negative karma as necessary to start learning. |
| A school already has permission | `U/Spells/Spellweaving/ArcanistSpell.cs:58` checks the character's ML quest context. `U/Engines/ML Quests/Definitions/Spellweaving.cs` contains its quest definitions. Retain this existing gate rather than inventing a second Spellweaving license. |
| Tutorial route and loans | [P663](cc-P663-tutorial-moves-to-isle.md) moves the main lessons to the Wakening Isle; Rook's optional lessons remain in New Haven. `C/Tutorial/TutorialWingTrials.cs:266` and `:275` lend Necromancy and Chivalry skill, with tithing at `:272`. Those lessons need an explicit change when gates ship. |

Read [skills design](skills-design.md), its magic decisions, P535, the revised F-12 notes, [P289](cc-P289-tutorial-core-trials.md), [P480](cc-P480-tutorial-first-play-fixes.md), [P481](cc-P481-new-player-start-area-design.md), P663, and [P702's newcomer text review](cc-P702-tutorial-new-player-text.md). `docs/skills-design.md` is absent in this work copy; the design is in `notes/`.

The League continuity comes from the drafts for [P593](cc-P593-league-chapter-2-draft.md), [P601](cc-P601-league-chapter-3-draft.md), [P616](cc-P616-league-chapter-4-draft.md), and [P621](cc-P621-league-chapter-5-draft.md). Side quests below reveal no feeding sword, trapped expedition, Unbound, empty-world vision, or Mend/Sunder answer. They grant no blade piece, League promotion waiver, or facet permission.

## Which skills should have a gate

An introduction to a demanding tradition is a good quest. Having a narrow use or a difficult interface alone is a weaker reason to prohibit a skill entirely. Keep ordinary supporting skills available: Spirit Speak, Healing, Tactics, Focus, Hiding, and Forensics do not become gated because a school uses them.

| Skill | Does the same reasoning fit? | Recommendation for Chase |
| --- | --- | --- |
| Chivalry | Yes. Service, tithing, and karma need context before the player receives a complete ability book. | Gate as requested, using the service quest below. |
| Necromancy | Yes. The player should understand the dead, reagents, Spirit Speak, and karma consequences. | Gate as requested, using the mortuary quest below. |
| Bushido | Yes. A short initiation can teach stance and defense through the Twin Paths Dojo. | Favor a later, separate initiation, but build only the two requested gates first. No exclusive choice between Bushido and Ninjitsu. |
| Ninjitsu | Yes. Its forms, concealment, and tools suit a practical dojo initiation. | Favor a separate later initiation, offered beside Bushido. Do not require learning Bushido first. |
| Spellweaving | Yes, and stock already does this. | Keep the existing arcanist quest and permission. A new-map referral or access repair may be needed, not a replacement requirement. |
| Mysticism | Somewhat. An Arcane Society teacher would help, but this alone does not justify another mandatory chain. | Leave trainable from zero; offer a later introduction. Reconsider a hard gate only with its own quest design. |
| Imbuing | Somewhat. Artificers' instruction suits the craft, but the shard already has an Imbuing rework and guild route. | No additional zero-skill gate in this batch. Keep the separate mastery/rework decision. Removing it from creation does not prohibit world training. |
| Throwing | Weakly. It is a racial weapon skill, not a learned magical tradition. | No quest gate. Keep it as a gargoyle's starting alternative to Archery and retain racial equipment rules. |

Exclusion from the creation list and a world gate are different policies. Under this recommendation Bushido, Ninjitsu, Mysticism, and Imbuing are learned later but remain usable and trainable without a new P709 permission. Existing requirements still apply, including Spellweaving's quest.

## Shared rule for the two new permissions

Save `Chivalry learned` and `Necromancy learned` separately for each character, along with resumable quest steps. Account storage may carry that data if keyed to character identity; it must not turn completion into an account-wide entitlement. The tutorial's account-level completion state is not a substitute.

Before completion, the character has zero trained skill and cannot use that school's spells or gain its points. Owning a book, acquiring tithing points, wearing skill bonuses, having favorable stats or racial benefits, or borrowing a tutorial skill does not authorize use. A refusal says which teacher to visit. Supporting skills continue to work normally.

At the final conversation, the player accepts the school's terms and the server saves permission. **The trained skill stays at 0.0. Its cap is the character's normal skill cap.** No free 30 or 50 skill points, special 100 cap, or cap increase is included. A character with permission can practice, pay a trainer, or use otherwise legal training items. At zero, a beginner spell may fail; the teacher explains practice and offers ordinary paid training after completion.

With completed F-12, that cap is 50 in loop 0, 100 in loop 1, then the corrected +5 ladder. A character doing the quest after tutorial graduation would normally already have the loop-1 maximum of 100. If built before F-12, the gate uses the existing configured cap, whose source default is 200. It must not pretend to enforce the future ladder. Recommend allowing that independent build, with no hard current-level requirement until real levels exist.

Permission is permanent through death, logout, restart, skill decay or reduction, soulstone storage, guild departure, karma change, and Keeper or Breaker resets. A reset may lower skill under F-12's chosen retention rules, but never makes the player repeat the initiation. Both permissions can coexist. Neither removes race restrictions, spell requirements, total caps, reagent costs, or later mastery requirements. Receiving another player's heal or other legal spell effect does not require initiation and grants no permission; this gate controls the character's own learning and use.

Recommend per-character completion because each character makes the pledge and receives the lesson. Account-wide completion saves alternate-character travel but makes every later character a trained initiate without doing it. If Chase chooses account-wide instead, the builder must change quest credit and reward claims together; permission and repeatable kits cannot be mixed casually.

## Chivalry quest: A Place on the Watch

**Giver:** proposed Sister Aveline Hart, a Chivalry instructor helping the Healers' Covenant at Fort Whitestone. A Warriors' Brotherhood contact and Rook both offer the same referral; League membership is optional.

**Place:** Fort Whitestone, author anchor **890,1055,32**, on Siege of Sosaria's Trammel map. Use the relief post and a nearby road approach, not a remote dungeon or another facet. The position comes from [Zigholtul's named spots](sos-map-author-spots.md); it is not an approved NPC spawn tile. Credit Zigholtul for map names and locations. Sister Aveline, the quest, and its events are our proposals.

**Pacing:** tune for current level **20-40**, solo, about **25-35 minutes of quest activity**, with travel extra and unmeasured. These are encounter targets, not mandatory level checks or measured completion times. The route must remain approachable with starter equipment and ordinary combat or a pet. No Chivalry, positive-karma threshold, League rank, guild membership, or loop milestone is required to accept.

1. **Find who needs relief.** Aveline shows an incomplete watch list and three medical bundles. Speak to the quartermaster and match the bundles to the named scouts. The journal records the names and next destination. This can sit beside P672's Hester Vale rescue seed without requiring that separate quest or paying its rewards.
2. **Keep the road open.** Carry the marked supplies to a waiting patrol outside the fort and help one injured scout reach the relief post. Clear a short encounter with scavengers blocking the approach. Ordinary weapons, Magery, or a pet work. Healing can add an optional treatment, but a supplied field orderly covers treatment for other builds. Do not require casting a locked spell to qualify.
3. **Understand the cost.** At a verified nearby ankh, Aveline explains that tithing converts gold into a supply spent by Chivalry abilities. Tithe **100 gold** through the normal shrine interaction. This consumes the player's gold and grants 100 ordinary tithing points. Record the actual transaction after this step is active; existing balance alone is not proof. Supply delivery itself grants no free gold, free karma, or infinitely refillable tithe loan. A penniless player can pause and earn ordinary gold, then return.
4. **Take the watch.** Back at Aveline, review: service earned the teaching; tithing supplies abilities; karma affects their strength. Confirm to learn Chivalry. Save the permission and mark the quest complete once. Give the Book of Chivalry, then offer optional Close Wounds practice on an injured training volunteer. Practice comes after unlocking and is not another required stage. Failure to cast does not undo completion.

**Starting supplies:** one normal Book of Chivalry, with its stock ten abilities. The 100 points from the player's own tithe remain available; there is no second free grant. Chivalry uses mana and tithing rather than a Necromancy reagent bag. Aveline explains how to buy a replacement book and where to tithe again. A replacement is an ordinary purchase, not a repeat quest payout. Do not change stock book trade or loot rules merely to make a gate work.

**Karma and virtues:** teach Compassion through helping someone and Honesty through delivering what was entrusted. These are story themes, not automatic Virtue-system points, a new meter, or a formal virtue-rank requirement. Accept any karma. Higher karma helps Chivalry power under existing formulas; tithing does not buy karma. Learning Necromancy later does not revoke permission. Its casting can lower karma and weaken Chivalry's karma-sensitive effects, which the player must hear before deciding.

Suggested Aveline lines:

> A book gives you the words. Bringing those people home is why I will teach you to use them.

> Tithing turns your gold into points these abilities spend. Karma affects their strength. You can learn other arts, but their consequences follow you here too.

**League and guild fit:** the League directory points to the fort as useful local service. The Brotherhood supplies the watch referral; the Covenant hosts relief work. Do not force the player to join either, spend League currency, or complete Bronze's story trial. No new guild subsystem is needed.

## Necromancy quest: Names for the Last Door

**Giver:** existing **Warden Morrow** of the Keepers of the Last Door, with proposed field clerk **Oren Pike** at Dhampire Ruins as the local quest contact. Morrow refers and closes the lesson; Oren handles field steps. `C/ClusterFStarterGuildmasters.cs:90` names Morrow. P672 already proposes Oren as the mortuary clerk, so reuse him rather than adding a conflicting second occupant.

**Place:** Dhampire Ruins, author anchor **1469,2515,14**, and its safe outer burial work area. No trip to Malas or Ghuul Sanctuary is required. P672's deeper nameplate investigation is level 60-80 and can remain a later follow-up. This initiation needs its own clearly marked **25-45** outer route with no mandatory passage through that harder encounter. A builder must verify that separation on the actual map before using the site.

**Pacing:** solo, about **30-40 minutes of quest activity**, with travel extra and unmeasured. Level band is a tuning target. No negative-karma threshold, Necromancy, Spirit Speak, Keepers membership, or League chapter is required to begin. Provide readable evidence for players who have no forensic or spirit skills.

1. **Learn the duty.** Morrow sends the player to Oren with a copied burial register. Oren explains that stolen nameplates are being sold as relics. The first task is to identify people, not demonstrate death magic. The journal records a local route and three missing entries.
2. **Recover the names.** Search three marked outer work sites and recover the corresponding plates from the quest scavengers or their guarded caches. Match them to the register. Forensics or Spirit Speak adds optional details, but the inscriptions and Oren's records provide every required answer. No stealing from players, killing innocents, or rare random drop is required.
3. **Stop the binding.** Expose a small local collector who is holding one unnamed shade to guard a cache. Break the collector's focus by following Oren's written instructions, then subdue its ordinary quest guardian. The shade identifies its plate and is laid to rest. This is a local burial abuse, with no Doom company, feeding sword, or explanation of Britannia's loop. Necromancy remains locked throughout the objective.
4. **Accept the art's cost.** Return the register to Morrow. Show a plain warning about karma loss and its effect on Chivalry. The player may accept now or leave the completed investigation pending. Confirming saves Necromancy permission once, then supplies the beginner book and reagents. Optional Curse Weapon practice follows, using an ordinary weapon and the character's real newly permitted skill. Do not require the spell to complete the gate.

**Starting supplies:** a Necromancer spellbook containing **Curse Weapon and Evil Omen**, plus **10 each of Pig Iron, Bat Wings, Grave Dust, Daemon Blood, and Nox Crystals**, once per character. Curse Weapon can be attempted from zero and uses Pig Iron (`U/Spells/Necromancy/CurseWeapon.cs:25`). Evil Omen requires 20 skill and uses Bat Wing and Nox Crystal (`EvilOmen.cs:28`). Explain that an ability appearing in a book does not mean the player can cast it successfully yet. Spirit Speak improves associated effects and remains independently trainable.

Morrow points to an ordinary reagent seller and spell-scroll sources for further learning. The builder must verify a reachable stock book/scroll seller and a zero-to-next-spell training route on the new world before calling the reward usable. Lost books can be replaced through normal paid sources. This small kit is help starting, not a full spell collection or a recurring reagent source. Keep normal trading rules; permission stays on the character if the book changes hands.

**Karma and virtues:** no evil-character pledge and no forced karma reduction at acceptance. Necromancy casting carries the existing negative karma awards. Explain this before the final confirmation and before optional practice. Do not require a fixed negative total to cast, set karma to a negative number, or require sacrificing an innocent. Permission survives later positive karma. Respectful handling of the dead is this guild's teaching, not a claim that casting has no consequences.

Suggested Morrow lines:

> Find their names before you ask anything of their dead.

> These spells lower your karma. If you also practice Chivalry, that can weaken its effects. You may learn both, but I will not hide the cost from you.

**League and guild fit:** registration and the directory provide a lead, but the quest is open to nonmembers. Keepers membership and this permission remain separate. `C/ClusterFGuildSystem.cs:268` currently allows joining through Necromancy 30 or ten Grave Dust. Do not put initiation behind that membership check: needing Necromancy to earn Necromancy would be circular. Joining by tribute alone must not unlock casting either. Existing guild starter kits must respect permission while retaining their ordinary membership function.

## Character creation proposal

Offer plain descriptions before asking the player to understand a skill list. These are starter packages, not permanent classes. Each modern template allocates **120 skill points as four skills at 30**. That fits the current per-skill creation maximum. Proposed stats total 90 and fit today's 10-60 bounds. Keep race-appropriate clothing, weapons, ammunition, tools, and ordinary beginner supplies.

| Template | Player description | Starting skills, each 30 | Strength / Dexterity / Intelligence |
| --- | --- | --- | --- |
| Fighter | Fight up close and treat your wounds with bandages. | Swordsmanship, Tactics, Anatomy, Healing | 45 / 35 / 10 |
| Archer | Fight from a distance and treat your wounds. | Archery, Tactics, Anatomy, Healing | 45 / 35 / 10 |
| Mage | Cast basic spells and recover mana, the energy spells spend. | Magery, Evaluating Intelligence, Meditation, Wrestling | 25 / 20 / 45 |
| Maker | Mine metal and make equipment and tools. You can learn fighting too. | Mining, Blacksmithy, Tinkering, Tailoring | 60 / 15 / 15 |

For gargoyles, replace Archer with **Thrower**, using Throwing instead of Archery and a legal racial weapon. Keep the same point budget and the rest of the skills. Do not offer an unusable bow template or quietly change the race. Fighter weapons and every kit also follow current race rules.

Keep **Choose my own skills** as a secondary option. Its entire starting whitelist is:

- Weapons: Swordsmanship, Macing, Fencing, Archery, Throwing, Wrestling, subject to race restrictions.
- Combat support: Tactics, Anatomy, Parrying, Healing.
- Basic magic: Magery, Evaluating Intelligence, Meditation.
- Gathering and making: Mining, Lumberjacking, Fishing, Blacksmithy, Tailoring, Tinkering, Carpentry.
- Exploration: Hiding, Tracking.

All modern allocations total 120, use at most the packet's supported four slots, and place no more than 50 in one skill. Explain complementary choices with examples. For a legacy creation route that supplies only 100 points, retain a legal 100-point custom allocation from the same whitelist and the existing 80-stat budget; do not award an extra 20 afterward. A client that cannot display the approved choices needs an explicit supported fallback before release.

Everything outside this list starts at zero. Ordinary trainers, vendors, guilds, and optional lessons introduce it in the world. Only Chivalry and Necromancy get new mandatory permissions in this batch. Do not make a paid guild join a blanket requirement for other skills. A player who chose Maker can later learn magic, animals, music, or either gated school.

### Paladin, Necromancer, and other stock professions

Recommend **removing Paladin and Necromancer from creation**. Keep those names in world teaching and suggested later builds. Once a character earns a school, the teacher can describe a Paladin or Necromancer skill plan, but this is advice, not a second creation transaction, a free point allocation, or an exclusive class. Renaming Paladin to Fighter while leaving its Chivalry allocation underneath would still bypass the rule.

Replace the stock menu as a whole with the beginner templates. Stock Warrior and Mage closely match Fighter and Mage; Maker uses stock Blacksmith's skill allocation. Stock Samurai and Ninja are also removed from creation under the shortened-list proposal, even if Chase does not approve future world gates for their skills. The custom route cannot select excluded skills. Focus and Spirit Speak remain freely learnable later.

The builder must update the supported client display, its profession definitions, and server validation together. Do not assume the server can hide the client's picker by changing a whitelist. Ensure server profession IDs resolve to the new allocations, and validate resolved profession skills as well as custom packet skills before assigning any stats, points, or kit. A stale Paladin, Necromancer, Samurai, or Ninja request must produce clear recovery instructions and another supported selection, without consuming a character slot or leaving a zero-skill character. No silent fallback to Alchemy or an unexplained remap.

UI feasibility is unverified. Before the creation build prompt is finalized, inspect the shipped TazUO picker and package's effective `prof.txt`/descriptions, including custom-skill filtering and legacy packets. If restricting that display needs client work, scope it explicitly and ship the server guard with it. A server-only denial of visible choices is not a finished beginner experience. Neither this design nor a later build should change expansion/race flags just to hide a school.

### Fit with the tutorial

Keep P663's destination choice: **Tutorial Island** by default and **New Haven** to skip. The beginner template determines initial skills and kit. The destination determines the tutorial route and existing eligibility handling. Neither grants a school permission. Finishing the main lessons, graduating, skipping, choosing a companion, or entering remedial training does not unlock either school. Preserve the current first-loop/skip behavior without treating it as an initiation.

Follow P480 and P702: use short sentences, explain a term before expecting an action, keep the exact skill/spell name visible, and tell the player what to click. Tamsin teaches the main lessons on the Wakening Isle. Rook in New Haven offers the world leads after graduation or a skip. Haven Island and the Wakening Isle must not be described as the same place. Map travel to these quests still respects the tutorial's existing island exit rules.

Suggested creation text:

> These choices give you starting skills and supplies. They do not choose a permanent class. You can learn other skills in the world. Chivalry and Necromancy each begin with a teacher's quest.

Suggested Rook lead, available to graduates and skippers:

> To learn Chivalry, speak with Sister Aveline at Fort Whitestone. To learn Necromancy, ask Warden Morrow of the Keepers of the Last Door. Each teacher gives you a quest before you can train or cast that school's spells. You can learn both.

After permission:

> You can now train Chivalry. Your skill starts at zero. Practice or pay a trainer to improve it. The quest did not raise your skill cap. Your book's abilities use mana and tithing points.

Use equivalent Necromancy wording explaining reagents, Spirit Speak, and karma. The quest journal gives one next task, a teacher name, and a tested direction arrow. Spell instructions say to double-click the book, double-click the named spell, and click its target when asked. Explain that a failed attempt does not mean the permission was lost.

**Optional school lessons need a change.** Recommend replacing the pre-unlock Chivalry and Necromancy casting trials with a short teacher demonstration and referral. Give no school skill mod, tithing loan, real player cast, or permanent quest credit during that preview. The NPC can demonstrate with existing effects. Mark only an introduction as viewed; keep the actual casting lesson visibly waiting for initiation. After permission, the optional practice trial may run under the existing loan cleanup rules. Main graduation must continue without either optional school lesson. Remedial training and repeated previews never unlock a school or refill its quest kit.

Spellweaving's introduction should still describe its real arcanist quest. Verify the new map's route to the stock quest contacts before publishing directions; today's Heartwood advice is not proof that those contacts will remain reachable after the map swap.

## Existing characters and abuse cases

The task's planning assumption is a **fresh playable world at the map swap**, so no ordinary characters are expected to need a skill migration. This is a new-map launch assumption, not a move away from ModernUO or a claim that existing saves or accounts have been inspected. Persistent accounts and old tutorial flags are a separate launch concern. A fresh map does not by itself prove character records were removed.

Recommend no grandfathering of school access for fresh-launch characters. Staff test characters should use an explicit, logged test grant, not positive skill as an implicit permission. If Chase retains playable characters with trained schools, stop the *rollout* for an explicit keep/reset/grandfather policy and an inventory before applying restrictions; do not silently erase their skills or rewrite saves. That possible rollout decision does not block this design.

| Attempt or failure | Required behavior in a later build |
| --- | --- |
| Normal gain or a macro before permission | Deny the school action and school gain before any ordinary, repeated, accelerated, or echoed gain attempt. Give a restrained teacher hint, not a message every macro tick. Do not bank deferred gains or new skill peaks for later. Ordinary legal training after initiation follows the shard's existing rules. |
| NPC training, guild reward, consumable point grant | Refuse a locked school's point assignment before charging gold, spending currency, or consuming the item. Joining the Keepers or receiving a guild kit is not initiation. Preserve unrelated rewards. |
| Transcendence, Alacrity, power scrolls | Transcendence cannot add locked points. Alacrity cannot create permission or make a denied attempt gain. An individual school power scroll cannot unlock it; reject while locked before consumption. Future F-12 level-cap scrolls keep their own progression function and grant neither school permission. |
| Soulstones and similar transfers | Do not allow stored points to enter a locked character, even from an initiated character on the same account. Deny before emptying a stone or lowering another skill. Once permitted, normal cap/lock rules still apply. Storage never transfers the quest flag. |
| Books, loose spell scrolls, hotkeys, saved macros, equipment spells | Check school permission at actual use, not only when opening a book. Cover client cast requests, direct spell creation paths, and any item route that invokes these school spells. A book, reagent bag, tithing balance, scroll, racial benefit, skill bonus, transformation, or tutorial loan never substitutes for permission. Skill bonuses may remain on equipment, but grant no locked-school action or gain. Unrelated item effects are not newly prohibited just for looking magical. |
| Party help and shared targets | Friends may help fight. Each eligible character must accept, perform the recorded objectives, and confirm personally. Shared kills need the quest's normal participation rule; standing nearby, receiving a traded plate, or another member's final conversation gives no automatic completion. No forced solo instance is required by this design. |
| Quest items and repeated turn-ins | Record character-owned objective credit; duplicates, dropped items, relogging, abandoned quests, and repeatedly clicking caches cannot manufacture a completed step or extra reward. Quest props cannot be sold as a recurring income source. Books and normal reagents retain ordinary item rules. |
| Reward failure or disconnect | Save completion independently from a pending one-time supply claim. No room means the teacher holds delivery pending and tells the player to make room. Reconnect or repeated confirmation must not duplicate permission rewards. A later build must define and test crash-safe delivery and retry, including a failure between item creation and marking the claim delivered. |
| Death, abandon, reset, deletion | Keep completed permission and claim state through death and resets. In-progress field steps resume safely or can restart without paying kits. Character deletion deletes that character's entitlement; a new character does the quest. Keeping the modest consumables tradable accepts some deletion farming cost, not an unlimited repeat reward on one character. No gold, AP, or rare sellable item is granted here. |

There are real assignment routes to cover. Pinned `U/Items/Special/SoulStone.cs:736` assigns Base directly; `U/Items/Special/Special Scrolls/ScrollofTranscendence.cs` also writes Base. The shard's gain wrappers and cap application are not sufficient by themselves. An implementer must inventory trainer, reward, transfer, test-tool, and direct assignment paths before choosing shared hooks. Avoid a design that only checks a zero cap or a book possession flag.

## Build handoff after Chase answers

These are proposed work packages, not permission to change code in P709.

1. **School permissions and enforcement.** Implement durable per-character permissions, pending reward claims, denial messages, and the gain/use/transfer policy. Inventory canonical customizations and pinned entry points first. Argue alternatives in notes before any targeted upstream patch. Extend the existing layered customization/patch system; no engine fork. Include the tutorial preview adjustment in this package so the new gate does not strand optional trials.
2. **The two quests and world access.** Verify new-map approach paths, a usable tithe site, safe NPC tiles, vendors, and the low-level outer Dhampire route. Seed idempotently with existing art. Add resumable objectives and personal credit, rewards, paid replacement sources, and tested referrals. Do not gate public facets or League story trials as a side effect. The gating feature should ship only when both teachers and full quest routes are reachable.
3. **Creation and teaching text.** Inspect the actual supported client flow, then change its display/package and the server together. Cover stock profession requests, custom allocations, all supported races' weapon choices, destination choice, skip/remedial, and full backpacks. Update the tutorial and player guide when the feature exists. Preview labels must describe a viewed introduction separately from learned-school status.

Build acceptance must include new tests seen failing against pre-change behavior, then passing, followed by `docker/uo/build.sh`. Require real flows for both school unlocks, locked book/scroll/hotkey casts, gear/loan bonuses, trainer payment, direct point consumables, soulstones, restart/reset persistence, and interrupted reward delivery. Cover a pre-gate optional preview, post-gate casting practice, and graduation without either school. Include an ungated-skill and nonplayer regression case so a player gate does not break ordinary NPC casting or other skills.

Creation needs crafted invalid packets as well as the supported client's screen: old profession IDs, excluded custom skills, race-incompatible weapons, duplicate skills, over-budget allocations, and unsupported legacy requests. Verify clear recovery without character-slot loss. Play both creation destinations and both quests on a throwaway loopback-only world, including two players helping one another. Validate actual beginner spell access and restocking, not just completion flags. Chase alone decides deployment.

This design needs no new art. Reuse current NPC bodies, books, reagents, plates, shrines, and effects. Quest NPCs, objective coordinates, time estimates, balance, client filtering, reward transaction implementation, and new-map travel remain unverified. No tests or build were run for this prose-only task; lane tests are none.

## For Chase

Each item is a real design choice. Recommended answers are proposals, not recorded decisions.

| Decision | Recommended answer |
| --- | --- |
| What else gets a new gate now? | Chivalry and Necromancy only. Keep stock Spellweaving; favor later Bushido/Ninjitsu initiations. Leave Mysticism, Imbuing, and Throwing without a new gate. |
| Character or account completion? | Per character, once, permanent through resets. Both schools may be learned on the same character. |
| What does initiation grant? | Permission at 0.0 skill, normal cap, book and the modest specified supplies. No free skill points or cap increase. |
| When should it happen? | Early world play, Chivalry tuned for 20-40 and Necromancy for 25-45. These are soft bands, with no hard level or League-rank gate. Allow implementation before full F-12 using the existing cap policy. |
| Which places and stories? | Fort Whitestone's relief watch and Dhampire's outer burial work. Keep both independent of P672's harder follow-ups and all League chapters. Verify the beginner routes before building encounters. |
| Require good/evil alignment or a virtue rank? | No. Teach service and respectful burial; preserve normal karma effects. No karma reset, forced evil act, virtue-point grant, or permanent exclusion. |
| How much starter help? | Chivalry: stock full book and 100 points from the player's own 100-gold tithe. Necromancy: Curse Weapon/Evil Omen book and ten of each standard Necromancy reagent, once. Paid replacements and later ordinary training. |
| How narrow is creation? | Four 120-point templates and the published shorter custom list. Thrower replaces Archer for gargoyles. Retain a legal 100-point legacy custom route only where the client needs it. |
| What happens to Paladin/Necromancer and Samurai/Ninja? | Remove them from creation. Offer world learning and later build advice; no free profession respec after a gate. Ship matching client and server changes. |
| Can an uninitiated character try a school in the tutorial? | NPC demonstration and referral only. Real optional casting practice opens after initiation. Graduation and skip grant neither school. |
| Fresh-launch policy and one-time supplies? | Assume no playable characters to migrate as the task states; verify that before rollout. No automatic grandfathering. Accept ordinary trading of the small kit rather than adding new bound versions of stock items. |

## Work record and review

Read both work-copy AGENTS files first, followed by the governing index, direction record, task guidance, and the design inputs linked above. Used canonical customizations and pinned ModernUO, not the stale `server/uo/` tree. No Haven connection, deployment, code/configuration change, migration `docs/` edit, commit, merge, push, or branch switch. No tests or persistent test gates were added.

Reviewed the proposal against every requested topic: the additional-school recommendations, both quest routes, zero-skill access and caps, supplies, karma, guilds, character/account scope, creation templates and custom list, stock professions, tutorial and skip, fresh-launch assumptions, and bypass cases. The For Chase table gives a recommended answer for each open design choice. No answer was invented or requested as a blocker for this design task.

Document checks ran under Windows PowerShell 5.1.26100.9711 with local Python. Relative Markdown links and explicit C/U source references resolve; cited line numbers are in bounds. Checked table rows, absence of em dashes, trailing whitespace, and file size below 5 MB. These were editorial checks, not new automated tests. Client flow, world placements, live settings, and runtime behavior remain unverified as stated above.

Ran `tools/progress.py --dry-run` successfully with `SL_SHARD` and `SL_MIGRATE` set to these work copies and the read-only ServUO reference as `SL_SERVUO`. Suppressed its known incidental `tools/progress.json` write in memory for this invocation only; no reporter source or generated file changed. No inventory total from that reporter is used as proof of game behavior.

Final scope review found the code work copy clean and only this new notes file in the migration work copy. `git diff --check` passed in both. The P709 stop-request file was absent at the checks between work steps and at final review. Completion is marked only after that review.

P709 DONE
