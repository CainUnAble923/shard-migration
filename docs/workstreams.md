# Workstreams

The migration splits into five streams. Three can run in parallel once Core is standing.
This replaces the strictly sequential phase list in `migration-plan.md` as the day-to-day
structure; the phases remain useful as gates.

**The thing to internalise: ServUO's content is not work.** It ships in the box. High Seas,
Time of Legends, Endless Journey, the revamped dungeons, seasonal events, Skill Masteries,
all of it is already written and maintained. We enable and tune it. Every stream below is
about *our* side of the line.

---

## 1. Core / platform
**Owner: Codex.** Blocks everything.

- Stock ServUO `pub57` built and running from `ServUO-work`
- `Config/Expansion.cfg` set to `EJ`; `Config/DataPath.cfg` pointed at client files
- Runtime decision: Windows or Mono. Benchmark a full world save at real size.
- Docker: new Dockerfile and `apply-patches.sh` targeting the ServUO tree
- `AutoRestart.cfg`, autosave interval, off-box `Saves/` rotation
- The pristine `ServUO-pub57` reference stays frozen and untouched

**Done when:** stock ServUO boots, `[CreateWorld]` populates all six facets, and a full save
completes in an acceptable time under the chosen runtime.

## 2. Customizations
**Owner: Claude drafts, Codex builds.** The bulk of the project.

Our 111 scripts and 17 patches rewritten for ServUO. Triaged in `port-triage.md`:
82 trivial, 25 mechanical, 3 repetitive, 1 genuinely hard. No Core bucket.

- Prerequisite: `server/customizations` compiles standalone against pinned ModernUO, so we
  are porting from a known-good baseline. Codex has recovered the three missing pieces.
- Order: the repetitive trio (68 near-identical types, one pattern), then the 82 trivial in
  batches, then the 25 mechanical, then the five upstream replacements last as ServUO patches.
- Five files collide with existing ServUO scripts and must become patches, not additive
  files: `CharacterCreation`, `CraftItem`, `HammerOfHephaestus`, `Meditation`, `RegenRates`.

**Done when:** all 111 build clean against ServUO and the shard runs with our systems intact.

## 3. Data and identity
**Owner: Claude writes the converters, Codex runs them.**

- **Accounts — bridgeable.** Exporter emits ServUO-shaped `accounts.xml` with hyphenated
  SHA512 hashes. Tooling exists in `tools/modernuo/`.
- **Spawn placement — bridgeable.** `[ExportSpawners]` JSON converted to ServUO XmlSpawner
  XML. Tool and tests exist in `tools/`; validated against stock data, not yet against ours.
- **The world — not bridgeable.** Fresh world plus a compensation pass: bank checks against
  house value, skill restoration, rare-item audit. Announce before cutover.

**TIME-BOXED:** switch ModernUO to SHA2 hashing **now**, while the old shard still takes
logins. The window closes at cutover and cannot be reopened.

**Done when:** accounts import and a real player password authenticates on ServUO.

## 4. Content enablement and tuning
**Owner: Chase decides, Codex configures.** Cheap. This is the payoff.

Not porting. Choosing what is on.

- Expansion level, and per-system toggles in `Config/` (Factions, VvV, City Loyalty,
  Shadowguard, seasonal events, Champions, Honesty, Vet Rewards)
- Spawner engine choice per region. Three ship: stock `Spawner`, XmlSpawner2, `ChampionSpawn`.
  One per region or you get silent double spawn.
- `Config/XmlSpawner2.cfg` features are all defaulted off; enable deliberately
- Spawn edits go through `SpawnerPersistence.cs` with a version bump so they replay
- **Custom facets are available.** ServUO allocates 256 map slots and ClassicUO reads well
  past index 5; Immortal Realms runs `map0`-`map21` in production. Pin the client version
  before cutting any map.

**Done when:** the shard's content set is a deliberate list rather than whatever defaulted on.

## 5. Verification and cutover
**Owner: Codex runs it, Chase decides the date.** The gate.

- Fresh world, `[CreateWorld]`, converted spawners imported, density spot-checked
- Accounts imported; test one that logged in since the SHA2 switch and one that has not, to
  size the reset list
- Three save/restart cycles. Gate is **zero deserialization errors**, not "mostly clean"
- Several clients at once, exercising every rewritten system
- ModernUO kept cold-bootable for at least a week after

---

## Parallelism

Core blocks everything. Once it stands, Customizations, Data and Content run in parallel.
Verification is last and gates the cutover.

The SHA2 switch in stream 3 is independent of all of it and should happen today.
