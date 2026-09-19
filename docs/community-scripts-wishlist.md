# Community scripts wishlist

**Pinned 2026-09-07 at Chase's request.** Source: the ModernUO Discord `#🔧・scripts` forum
channel (`/channels/751317910504603701/1022600946653597696`). Captured here because Discord
posts are not durable and a channel is not a backlog.

## This is a separate lane, deliberately

Everything here is **custom content, not ported OSI content.** It does not go in the CC or S
task numbering, it does not count toward expansion coverage, and it never blocks or interleaves
with the port backlog. It is its own list with its own rules.

**The tradeoff, stated once so nobody has to rediscover it.** The reason this project exists in
its current shape is Chase's own: *"by including as much up to date content players will be able
to find information outside custom wiki for most of the content."* Nothing in this file is on any
wiki. OSI has no CloneTrap, no MagnetTrap, and its paragons do not gain levels over real time.
So each item taken from this list is **deliberate documentation debt**: a thing only a Shattered
Legacy wiki could ever explain, on a shard that already carries a hundred-odd undocumented custom
scripts.

That is a legitimate choice and it is Chase's to make. A shard for family and possibly a school
has reasons to want fun over faithfulness, and "a trap that spawns an evil clone of you" is a
better story for a twelve-year-old than an accurate drop rate. The point of writing it down is
that the cost stays visible and bounded rather than leaking into the fidelity accounting.

**So: anything adopted from here goes on the shard-wiki list at the same time.** If we run it, we
document it. That is the whole deal.

## Rules for this lane

1. **Resolve licensing before porting any of it.** ServUO has a known license. A `.cs` posted in
   a Discord forum by a community member does not. Ask the author, or find a stated license, or
   reimplement from the described behaviour rather than copying the file. Unresolved licence
   means it does not land in the repo.
2. **Treat every one as a design description, not a file to copy.** Quality is unverified and
   this project has already found that six of its own eight patches were never valid diffs.
   Reimplement against pinned ModernUO with the recipe and the standards we use everywhere else.
3. **They target ModernUO, but not necessarily our commit.** Verify against `7c9215d97`.
4. **Anything that patches a base class** follows `docs/subsystem-policy.md`: argued in `notes/`
   first, and a failing patch beats copied upstream logic.
5. **Anything player-facing ships with a shard-wiki entry.** See above.
6. **Never let one of these into a content task.** One task, one lane.

## The list, as of 2026-09-07

All by "Expa" unless noted. All posts were over 30 days old when captured, dated January to May
2026. **This capture may be incomplete** - the forum was read from one screen and not paged to
the end. Re-read the channel before treating it as the full list.

| Item | What it does | Note |
|---|---|---|
| `[gmtool` command | GM tooling. Posted by **Rik**, the only non-Expa post, and the only thread with real discussion (6 replies) | **The most interesting one.** A GM tool is not player-facing, so it carries no wiki debt at all. Worth reading first |
| Time Item Manager | items with an expiry timer, `[SetTemp` / `[UnsetTemp` | Infrastructure rather than content, so low wiki debt. Its instructions edit `BaseArmor.GetProperties` directly, which for us is a patch under rule 4 |
| Lockpick / RemoveTrap Training Box | chest auto-adjusts difficulty to the player's skill, auto-relocks, trap respawns | OSI has lockpickable training chests; the auto-adjust is the custom part. Closest thing here to standard |
| Noob Dummy | interactive combat training dummy | OSI has training dummies; this one is custom |
| Auto Bandage | `bas` self-bandages to full, `bat` bandages a target, stops on death or interruption | Quality-of-life. Meaningful gameplay change: removes the bandage-timing skill |
| Aging Paragon System | paragons gain levels 1-10 over hours of real time, stat and resist bonuses, hue change, `[Lv: X]` name prefix, JSON config, six GM commands | Entirely invented. The largest and most complex item here |
| Set of traps | CloneTrap spawns a hostile copy of the player; CurseTrap makes an item immovable; LandMobTrap spawns skeletons; MagnetTrap forces players to drop metal items; ItemSealingTrap locks items in a chest needing a scroll | Entirely invented. Likely the most fun for a young audience, and the most wiki debt |
| LoginStats | announces arrivals and departures, shows total playtime, grants 10s invulnerability and invisibility on login | The invulnerability window is a real gameplay rule, not cosmetic |

## Chase's own ideas, uncosted

**Drop them here the moment they are said, in one line, even half-formed.** An idea that only
exists in a chat is gone at the next compaction. Costing can wait; capture cannot.

The move from here to the costed section below is research: what does pinned ModernUO already
ship, what would it cost, what does it deviate from, and what wiki debt does it carry. That
research has already changed what an idea *was* once: the quest board arrived as a convenience
and turned out to be the thing that makes 26 quests reachable at all under our skill-gain rate.

| Idea | Said | Status |
|---|---|---|
| _(none open)_ | | |

## Chase's own ideas, costed

Not from the Discord. These are ours, and they carry the same wiki debt as anything else in this
lane.

### The New Haven quest board — costed 2026-09-19, ready to build

**The idea (Chase):** a stone or bulletin board in New Haven where a new player can pick up the
New Haven training quests from one place, instead of walking the town finding trainers before
their skills pass 50.

**This is not a convenience on our shard. It is what makes the content reachable at all.**

Pinned ModernUO ships **26 New Haven skill-training quests**
(`Engines/ML Quests/Definitions/NewHavenSkillTraining.cs`), each one
`GainSkillObjective(skill, 500, useReal: true, accelerate: true)` — "raise this skill to 50.0",
with the New Haven gain bonus. `GainSkillObjective.CanOffer` refuses the moment the skill reaches
the threshold, with cliloc 1077772, *"I cannot teach you, for you know all I can teach!"* Past
50, that quest is gone permanently.

**We run `ClusterFSkillGain` at 3 attempts and 5x gain.** So the window between the starting value
and the lockout is minutes of play, not days. Whatever a new player does not claim early, they
lose forever. On stock rates a player has time to wander and find trainers; on ours they do not.

**Cost: one file, roughly 80 lines, no patch.**

- Stock ModernUO already ships `Engines/ML Quests/Items/QuestGiverItem.cs`, an abstract `Item`
  implementing `IQuestGiver` that routes `OnDoubleClick` into the normal offer flow. The board is
  a subclass of it, registered as the quester for the 26 quests.
- Because it uses the stock path, the **real offer gump with the real quest text** appears.
  Quests already held or completed are filtered by the existing system, not by us.
- **One override needed:** `QuestGiverItem.OnDoubleClick` requires `IsChildOf(from.Backpack)`. A
  fixed board in the world is not in a backpack, so our subclass relaxes that check. Small
  override in our own file, not a patch.
- Plus a placement line, the same shape as the Fountain of Fortune placement (Q-021).

**Place it where new characters arrive**, not decoratively in the square. The value is in being
double-clickable in the first minute, before anything has been used enough to gain.

**Leave `MLQuestSystem.MaxConcurrentQuests = 10` alone.** Verified 2026-09-19 that we have not
touched it and have no quest patches at all. Raising it changes every quest in the game, not just
New Haven, and the cap is not what costs us the content — the gain rate is. Skills only rise from
use and nobody exercises 26 at once, so the real loop is: take ten matching what you are about to
do, push them to 50, turn them in, take ten more. Revisit only if that proves annoying in play.

**One trap worth putting on the board's own text.** These quests pass `useReal: true`, so
`CanOffer` tests `skill.Fixed`, the **effective** value including item bonuses, not the base. A
new player who equips something with a skill bonus can be pushed over 50 on paper and lose the
quest while their base skill is still far below it. Claim the quests before gearing up.

**Starting skills are 30** (`Distribution/Data/Professions/SA/Prof.txt`), so nothing is locked at
character creation. All 26 are takeable by a brand-new character.

**Wiki debt:** real. A player who looks up New Haven training will not find a quest board
anywhere. It needs a shard-wiki entry saying it exists, that it gives the standard quests, and
that the 50-point lockout is OSI behaviour rather than ours.

**Status:** costed, not scheduled. Small enough to slot in whenever Chase wants a break from
dungeon porting.

## Suggested order, if these get picked up

1. **`[gmtool`** - no wiki debt, helps administer the shard, and it is the one with discussion.
2. **Time Item Manager** - infrastructure, useful for events, low debt.
3. **The traps and the Aging Paragon System** - the actual fun, and the actual cost. Worth doing
   deliberately as a themed batch with its own wiki page rather than one at a time.
4. **Auto Bandage and LoginStats** last, or not at all. Both change combat or safety rules rather
   than adding content, which is the kind of change hardest to explain to a player who read a
   wiki somewhere else.

Nothing here is scheduled. It sits until Chase says otherwise.

**The New Haven quest board is the exception in spirit**: it is costed, it is ours rather than
someone's Discord post, so it carries no licensing question, and it fixes a problem our own
skill-gain rate created. If anything in this lane gets built first, it should be that.
