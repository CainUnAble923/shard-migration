# Workstreams

Five streams. This is a long-running effort with no completion date, so these are ongoing
areas of work rather than phases with an end.

**Stream 1 blocks everything. Streams 2-5 then run indefinitely and in parallel.**

---

## 1. Foundation
**Owner: Codex.** Blocks everything else. Finite, and nearly done.

Problems with the shard as it runs today, independent of any content work.

- Recover the three missing pieces so `server/customizations` compiles standalone against
  pinned ModernUO: `CraftContext` members, the eight `ResourceInfo` wood enum members,
  `OutridersGuildmaster`. **Codex has done this; needs committing.**
- **`apply-patches.sh` must fail on a failed patch.** It currently converts failures to
  warnings and exits 0, and seven patches fail. A green build proves nothing until this is
  fixed. Then triage the seven: some may be obsolete.
- Delete the stale `server/customizations/migrations/` subfolder, whose PetMimic v0-v2 JSONs
  diverge from the canonical set in `server/migrations/`.
- Make `RegenRates` routing explicit. It currently works by accident: both it and ModernUO's
  land in `Misc/`, so ours overwrites. The other six replacements are explicitly routed.

**Done when:** a clean Docker build from pinned ModernUO plus only tracked canonical inputs
succeeds, and a failing patch actually fails the build.

## 2. Port pipeline
**Owner: Claude.** Build once, use forever.

The repeatable recipe for bringing one ServUO system across. Getting this right is worth more
than any individual port, because everything downstream runs through it.

- Collision check against pristine ModernUO before any work starts
- Dependency check: does it touch a subsystem ModernUO lacks? If so it belongs to stream 4.
- Serialization conversion: ServUO's hand-written `Serialize`/`Deserialize` with a version int
  becomes ModernUO's `[SerializationGenerator]` partial class with `[SerializableField]`
- `[Constructable]` becomes `[Constructible]`; `Serial` is signed in ServUO, `uint` in ModernUO
- Where the ported file lands, and whether it is additive or a routed replacement
- A worked example, start to finish, that the next twenty ports copy

**Done when:** a documented recipe plus one reference port exists, and the second port is
visibly faster than the first.

## 3. Content backlog
**Owner: Chase prioritises, Claude drafts, Codex builds.** Never empties. That is fine.

The queue, priced in `content-menu.md`. 3,091 candidate files across ServUO, but the order
matters far more than the total.

Best value first, by measured dependency cost:

- **Revamped Dungeons** — 255 files, 28,828 lines, 2% dependency. Places to go and things to
  fight, almost no coupling. The single best value on the list.
- **High Seas cheap half** — ~78 files, ~17,000 lines. Fishing, rare fish, sea creatures,
  food. 0% missing-subsystem dependency.
- **Creatures and NPCs** — 354 files, 0% dependency. Take a handful at a time as needed.
- **Decoration and housing** — Addons, Decorative, New Magincia. 0% dependency, highly visible.
- **Crafting and resources** — Items/Resource, BulkOrders. 0% dependency.
- **High Seas naval half** — ~54 files, ~14,000 lines. Not blocked, but means extending
  ModernUO's `BaseBoat`. Its own mini-project.

**Done when:** never. Pull from it for as long as the shard is being worked on.

## 4. Subsystem builds
**Owner: decide case by case.** Expensive. Only when a wanted piece of content needs one.

ModernUO ships **zero** files for: Skill Masteries, Shadowguard, Myrmidex Invasion, Vendor
Searching, Instanced Peerless. Content resting on these cannot be ported until the subsystem
exists.

This gates Eodon in particular: Shadowguard is 71% dependent and Myrmidex Invasion 83%.
An open question worth answering before committing: how much of the Valley of Eodon separates
from the Myrmidex battle system? Nobody has measured it. If it separates well, Eodon gets a
lot cheaper.

**Done when:** each is built, or explicitly and permanently declined.

## 5. Shard operations
**Owner: Codex, Chase decides deploys.** Continuous.

- Docker build, entrypoint, compose, deployment of each batch of ported content
- Off-box `Saves/` rotation, autosave interval, restart policy
- **Custom facets are available.** ModernUO supports them and ClassicUO reads well past map
  index 5; Immortal Realms runs `map0`-`map21` in production. Pin the client version before
  cutting any map.
- Keep `tools/progress.py` current; run it at the end of every session

**Done when:** never. This is running a shard.

---

## What is explicitly not happening

No migration. No cutover, no fresh world, no compensation pass, no account export, no
password conversion window. The 111 custom scripts are never rewritten. Every port leaves a
working shard.
