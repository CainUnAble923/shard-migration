> **OBSOLETE.** Written for a migrate-to-ServUO plan that was not taken. The shard stays on
> ModernUO and ports ServUO content in; see `direction-decision.md`. Measurements here remain
> accurate and are cited elsewhere; the plans do not apply.

# Migration plan: ModernUO to ServUO pub57

Origin: **ModernUO** (`main`). Target: **ServUO `pub57`**, expansion **EJ**.
Scope: full post-ML world including naval combat and Eodon.

See `direction-decision.md` for why this direction and not the reverse.

## URGENT, time-boxed: switch ModernUO to SHA2 now

ModernUO defaults `accountSecurity.encryptionAlgorithm` to **Argon2**, which is one-way and
unreadable by ServUO. Left alone, every player needs a password reset at cutover.

ModernUO also ships a `SHA2` algorithm its own source comments mark *"ServUO compatibility"*,
and it rehashes a stored password to the current algorithm on successful login. Set the
algorithm to SHA2 **while ModernUO is still live** and returning players silently convert
their own hashes over the following weeks.

Both engines hash `username + password` as ASCII, truncated at 256 chars, through SHA512, so
the digests are byte-identical. Only the string format differs:

- ServUO: `BitConverter.ToString` output, hyphenated hex (`A1-B2-C3`)
- ModernUO: `ToHexString` output, unseparated hex (`A1B2C3`)

Conversion is inserting a hyphen every two characters. **This window closes when the old
shard stops taking logins.** You cannot recover a plaintext password from an Argon2 hash.

## Phase 0 - Freeze and inventory (this week)

- Flip ModernUO to SHA2. Everything else here can wait a day; this cannot.
- Tag the repo and cold-copy the whole shard directory. Config, `Distribution/Data`,
  client data path, all of it.
- **Count custom files under `Projects/UOContent`.** That number, not any judgment about
  ServUO, is the schedule for this project.
- Sort them into **Content** (items, mobiles, quests, gumps), **Systems** (own persistence
  or timers), **Core** (anything under `Projects/Server`). Core is the expensive bucket.
- Record the client version served. Phase 4 depends on it.

## Phase 1 - Stock ServUO beside the live shard (no conversion)

- Clone `pub57`. Build with `_winrelease.bat` on Windows, or `dotnet build` then
  `mono ServUO.exe` elsewhere.
- Point `Config/DataPath.cfg` at a **copy** of the client files. Set `Config/Expansion.cfg`
  to EJ.
- Run `[CreateWorld]`, walk all six facets, confirm stock spawn XML populated.
- **Freeze this install and never edit it.** It is the reference shard and the diff baseline
  for the whole project.

## Phase 2 - Rewrite the custom scripts (the bulk)

Same C#, different idioms. This is a rewrite with a good reference implementation, not a port.

- **Persistence.** Every `[SerializationGenerator(n)]` partial class becomes a normal class
  with hand-written `Serialize(GenericWriter)` / `Deserialize(GenericReader)` and a version
  int. Each `[SerializableField(n)]` becomes a property written and read in a fixed order you
  now maintain by hand. Generated JSON migration files have no counterpart and are discarded.
- **Serial is a different type.** MUO's `Serial` is a readonly struct over `uint`; ServUO's is
  signed. Arithmetic, comparisons against `-1`, and raw serial serialization need checking,
  not find-and-replace.
- **Networking.** MUO deleted `Packet` / `PacketWriter` / `PacketReader`, which ServUO still
  uses. Custom packets get rewritten against the older API.
- **Smaller drift.** Lambda timers back to callback timers. Some ServUO collections are still
  ArrayList-era. `IEntity` parameters may be `object parent`.

Order: Content, then Systems, then Core. Build after each script. One commit per system.
Before rewriting a Core change, check whether ServUO already exposes the hook, since many MUO
Core edits exist only because MUO removed something ServUO still has.

## Phase 3 - Move what can move (two bridges, one wall)

**Accounts - bridgeable.** ServUO reads `Accounts/accounts.xml`, taking the SHA512 hash from
a `newSecureCryptPassword` node. MUO reads that legacy XML but saves accounts through binary
entity persistence, so write a small MUO exporter that walks accounts and emits ServUO-shaped
XML, hyphenating hashes on the way out. An afternoon. Preserves usernames, access levels and
(given Phase 0) passwords.

**Spawn placement - bridgeable.** `[ExportSpawners]` writes every spawner to JSON via
`SpawnerJsonSerializer`. Write a JSON to ServUO XmlSpawner XML converter. Do this **before**
hand-placing anything in ServUO.

**The world - not bridgeable.** Characters, items, houses. Different serialization model,
different Serial width, different type names. No converter. Writing one is where migrations
die. Plan a fresh world plus a compensation pass: bank checks against house value, skill
restoration, rare-item audit. Announce before cutover. Accounts surviving makes the
conversation much easier.

## Phase 4 - Spawns and maps (the reason for the move)

- **One primary spawner engine per region.** Stock `Spawner` for plain placement, XmlSpawner2
  where conditions, quest logic or attachments are needed. Three engines are available now
  versus MUO's one, and mixing them inside a region is the standard route to silent double
  spawn.
- Enable XmlSpawner2 features deliberately in `Config/XmlSpawner2.cfg`. Sockets, points and
  factions all ship defaulted off.
- Put spawn edits through `Scripts/Misc/SpawnerPersistence.cs` with a version bump rather than
  hand-placing in game. Hand placement does not survive a world rebuild; versioned persistence
  replays. Closest analogue to the JSON workflow we are used to.
- **Custom facets are a real option.** ServUO allocates 256 map slots and ClassicUO reads map
  indices well past 5. See `client-analysis.md`: Immortal Realms runs `map0.mul` through
  `map21.mul` in production. The 0-5 ceiling is an official-client limit.
- Tooling: CentrED / CentrED+ to edit, UOFiddler for UOP to MUL, UOLandscaper or Dragon for
  terrain from a heightmap. Most of it is fragile past client 7.0.59. **Pin the client version
  first**, then build maps against it.

## Phase 5 - Runtime and hosting

- ServUO targets `net48` on every branch. Choose Windows or Mono deliberately.
- **Benchmark a full world save at real target size.** Coming from MUO's fast save path, this
  is the metric most likely to disappoint. Measure while changing hosts is still cheap.
- Set autosave interval, configure `AutoRestart.cfg`, get off-box rotation of `Saves/` running
  before any player connects.

## Phase 6 - Verify, then cut over

- Fresh world, `[CreateWorld]`, import converted spawners, spot-check density against the
  Phase 1 reference shard.
- Import converted accounts. Confirm a real player password authenticates. Test one account
  that logged in **since** the SHA2 switch and one that has not, to size the reset list.
- Save and restart three times. The gate is **zero deserialization errors in the console**,
  not "mostly clean". One warning is a corrupt system not yet found.
- Several clients at once, exercising every rewritten system, especially timer-serialized ones.
- Only then point players at it. Keep ModernUO cold-bootable for at least a week.

## Risks

| Risk | Likelihood | Response |
|---|---|---|
| Argon2 strands every password | Certain if not acted on | Switch MUO to SHA2 this week |
| World data does not carry over | Certain | Fresh world + compensation pass |
| Rewrite scope larger than estimated | High | Count custom files in Phase 0 before committing to a date |
| Map tooling breaks on modern client | High if cutting maps | Pin client version in Phase 0 |
| Save times regress under Mono | Medium | Benchmark in Phase 5 at real world size |
| Double spawn from mixed engines | Medium | One engine per region, audit in Phase 6 |

## Known-not-verified

- Per-branch last-commit dates for ServUO (GitHub API rate-limited during research).
- Whether `p58-wip` moves off net48 in any project file other than `Server.csproj`.
- ModernUO's actual post-SA content coverage beyond the file counts in `direction-decision.md`.
