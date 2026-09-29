# Deploy readiness: what a deploy would land on, measured 2026-09-27

Task C, overnight. Read-only throughout: no container started, stopped or created, nothing under `server/`,
`Saves*/`, `Backups/`, `Archives/`, `Accounts/` or `client-data/` written, no `build.sh`, no commit. The only
Docker commands run were `ps`, `inspect`, `image ls`, `image inspect`, `history`, `info` and `logs`. All times
are CDT unless marked UTC. **Save folder names are UTC** (the live log writes the 08:50 CDT backup as
`2026-09-27-13-50-00`), so `2026-09-28-01-40-00` is 20:40 CDT on the 27th.

---

## 1. Does the no-instance condition still hold?

**On the live world: yes, for all five types.** Zero instances of `SpiritualityHelm`, `ValorGauntlets`,
`BestialKilt`, `VirtuososKilt` or `BestialArms` in the live save, in any of the 20 automatic backups, in any of
the 918 snapshots inside the 57 daily, hourly and monthly archives, or in the 26 saves inside the May
pre-migration tarball. Every snapshot passed its positive control.

**Across every save, strictly: no, for two types.** `Saves-test` holds **one `BestialKilt` and one
`VirtuososKilt`**, created on the test shard at 17:49:04 and 17:49:16 CDT on 09-27 (serials `0x40000321`,
`0x40000322`), which is almost certainly the C.6 client check `notes/armour-set-completion.md` asks for. What that
costs: those two types were born on `BaseSetClothing` and nothing pending moves them, so the instances only matter
if someone later changes either kilt's parent, and even then only for a save the compose file itself calls
throwaway. It is still the rule's letter broken, so it is written here rather than under the table.

**`SpiritualityHelm` and `ValorGauntlets`, the two types the condition actually protects** (they are stock
ModernUO types, so the running image could have created them): zero everywhere, including `Saves-test`.
**`BestialArms` (D28)**: zero everywhere, including `Saves-test`, so D28's fix still has nothing to migrate.

**Two findings from §6 belong on this first screen, because they change the rollback, not the measurement:**

- **The image the live shard is running no longer exists in the image store.** `sl-modernuo` runs
  `sha256:36cc709a…` (container created 2026-06-29); `docker image inspect` on that ID says "No such image", and
  the `uo-modernuo` tag now points to a different image, `bc04a35bf344`, built 2026-09-06 10:45. The running
  container holds the only copy. §4 starts by capturing it, and "bring it back up on `uo-modernuo`" would bring up
  something else. §6.1.
- **Any `docker compose up` in `docker/uo` replaces the live container**, because the running container no longer
  matches the compose file (its `/modernuo-projects` mount differs), and the replacement would use that other
  image. §6.2.

---

## 2. Per type, per save

**Method.** The 09-26 check (`tools/save_instance_check.py`) asked whether each type's name appears in a save's
`SerializedTypes.db`. It read `Saves`, `Saves-test`, every automatic backup, and **only the last two archives of
each kind** (`files[-2:]`), 120 type tables in all. Tonight's check does two things per snapshot:

1. **The same test, so the numbers compare:** is the name in that snapshot's type table?
2. **A count:** parse `Items/Items.idx` and `Mobiles/Mobiles.idx` and count entries by type hash. Each entry is
   `byte 2, ulong typeHash, uint serial, long created, long pos, int length` (idx version 3; written at
   pinned `Server/Serialization/GenericEntityPersistence.cs:100` and `:118`), and the hash resolves through the
   same snapshot's type table.

It reads **every** snapshot of **every** archive, not the last two. The two methods agree on every one of the 938
snapshots: a type is in the type table exactly where it has an instance. That is what the pinned writer implies,
since an entity's type only enters the table through `idx.Write(e.GetType())`
(`Serialization/MemoryMapFileWriter.cs:237-249`), and it is now observed rather than assumed.

**Controls, all 938 plus the 26 in the tarball:** `Server.Items.Dagger` present in the type table and **at least
21 instances** in every snapshot; every idx file exactly `8 + 33 × count` bytes; **zero** idx hashes that failed to
resolve in their own type table; every type table parsed to its last byte.

**Artefacts read:** `Saves` and `Saves-test` (written 20:40 tonight), 20 automatic backups, 30 daily, 24 hourly and 3
monthly archives. Every archive holds several snapshots, and each was counted separately; the row gives the range.

| Save | Snapshots | Snapshot time(s), CDT | Items | Players | Type table: control / hit | SpiritualityHelm | ValorGauntlets | BestialKilt | VirtuososKilt | BestialArms |
|---|---|---|---|---|---|---|---|---|---|---|
| `Saves` (live) | 1 | written 09-27 20:40 | 192,208 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Saves-test` | 1 | written 09-27 20:40 | 724 | 5 | yes / BestialKilt, VirtuososKilt | 0 | 0 | **1** | **1** | 0 |
| `Automatic/2026-09-16-23-00-00` | 1 | 09-16 18:00 | 192,198 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Automatic/2026-09-19-23-55-01` | 1 | 09-19 18:55 | 192,289 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Automatic/2026-09-20-23-55-01` | 1 | 09-20 18:55 | 192,734 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Automatic/2026-09-21-23-55-00` | 1 | 09-21 18:55 | 192,146 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Automatic/2026-09-22-17-35-00` | 1 | 09-22 12:35 | 192,285 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Automatic/2026-09-23-23-55-00` | 1 | 09-23 18:55 | 192,062 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Automatic/2026-09-24-23-55-00` | 1 | 09-24 18:55 | 192,518 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Automatic/2026-09-25-23-55-00` | 1 | 09-25 18:55 | 192,490 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Automatic/2026-09-26-23-55-00` | 1 | 09-26 18:55 | 192,212 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Automatic/2026-09-27-23-55-00` | 1 | 09-27 18:55 | 192,455 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Automatic/2026-09-28-00-55-00` | 1 | 09-27 19:55 | 192,339 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Automatic/2026-09-28-01-00-00` | 1 | 09-27 20:00 | 192,184 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Automatic/2026-09-28-01-05-00` | 1 | 09-27 20:05 | 192,003 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Automatic/2026-09-28-01-10-00` | 1 | 09-27 20:10 | 192,092 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Automatic/2026-09-28-01-15-00` | 1 | 09-27 20:15 | 192,217 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Automatic/2026-09-28-01-20-00` | 1 | 09-27 20:20 | 192,142 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Automatic/2026-09-28-01-25-00` | 1 | 09-27 20:25 | 192,206 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Automatic/2026-09-28-01-30-00` | 1 | 09-27 20:30 | 191,974 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Automatic/2026-09-28-01-35-00` | 1 | 09-27 20:35 | 192,499 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Automatic/2026-09-28-01-40-00` | 1 | 09-27 20:40 | 191,997 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Daily/2026-05-25.tar.zst` | 24 | 05-24 19:55 to 05-25 18:55 | 191,504-192,210 | 5 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Daily/2026-05-26.tar.zst` | 24 | 05-25 19:55 to 05-26 18:55 | 191,343-192,333 | 5 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Daily/2026-05-27.tar.zst` | 22 | 05-26 19:55 to 05-27 18:55 | 191,676-192,582 | 5 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Daily/2026-05-28.tar.zst` | 22 | 05-27 19:55 to 05-28 18:55 | 191,661-192,847 | 5 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Daily/2026-05-29.tar.zst` | 24 | 05-28 19:55 to 05-29 18:55 | 191,804-192,552 | 5 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Daily/2026-05-30.tar.zst` | 18 | 05-29 19:55 to 05-30 13:08 | 191,774-193,229 | 5 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Daily/2026-05-31.tar.zst` | 2 | 05-31 07:55 to 05-31 08:05 | 191,958-192,265 | 5 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Daily/2026-06-01.tar.zst` | 24 | 05-31 19:55 to 06-01 18:55 | 192,005-192,569 | 5 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Daily/2026-06-02.tar.zst` | 20 | 06-01 19:55 to 06-02 14:30 | 191,662-192,533 | 5 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Daily/2026-06-15.tar.zst` | 22 | 06-14 21:55 to 06-15 18:55 | 191,900-192,527 | 5 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Daily/2026-06-16.tar.zst` | 24 | 06-15 19:55 to 06-16 18:55 | 191,951-192,461 | 5 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Daily/2026-06-17.tar.zst` | 24 | 06-16 19:55 to 06-17 18:55 | 191,912-192,416 | 5 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Daily/2026-06-18.tar.zst` | 24 | 06-17 19:55 to 06-18 18:55 | 191,977-192,574 | 5 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Daily/2026-06-19.tar.zst` | 22 | 06-18 19:55 to 06-19 16:35 | 192,086-192,614 | 5 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Daily/2026-06-29.tar.zst` | 8 | 06-29 11:55 to 06-29 18:55 | 192,094-192,977 | 5 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Daily/2026-06-30.tar.zst` | 24 | 06-29 19:55 to 06-30 18:55 | 191,872-192,326 | 5 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Daily/2026-07-01.tar.zst` | 24 | 06-30 19:55 to 07-01 18:55 | 192,141-192,712 | 5 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Daily/2026-07-02.tar.zst` | 24 | 07-01 19:55 to 07-02 18:55 | 192,032-192,663 | 5 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Daily/2026-07-03.tar.zst` | 24 | 07-02 19:55 to 07-03 18:55 | 192,053-192,593 | 5 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Daily/2026-07-04.tar.zst` | 15 | 07-03 19:55 to 07-04 09:10 | 192,122-192,529 | 5 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Daily/2026-09-16.tar.zst` | 2 | 09-16 17:55 to 09-16 18:00 | 192,150-192,198 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Daily/2026-09-19.tar.zst` | 10 | 09-19 09:55 to 09-19 18:55 | 192,089-192,500 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Daily/2026-09-20.tar.zst` | 24 | 09-19 19:55 to 09-20 18:55 | 191,962-192,734 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Daily/2026-09-21.tar.zst` | 24 | 09-20 19:00 to 09-21 18:55 | 191,900-192,500 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Daily/2026-09-22.tar.zst` | 18 | 09-21 19:55 to 09-22 12:35 | 191,871-192,520 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Daily/2026-09-23.tar.zst` | 2 | 09-23 17:55 to 09-23 18:55 | 192,039-192,062 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Daily/2026-09-24.tar.zst` | 24 | 09-23 19:55 to 09-24 18:55 | 192,193-192,703 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Daily/2026-09-25.tar.zst` | 24 | 09-24 19:55 to 09-25 18:55 | 192,203-192,678 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Daily/2026-09-26.tar.zst` | 24 | 09-25 19:55 to 09-26 18:55 | 192,212-192,768 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Daily/2026-09-27.tar.zst` | 24 | 09-26 19:55 to 09-27 18:55 | 191,939-192,618 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Hourly/2026-09-27-01.tar.zst` | 12 | 09-26 20:00 to 09-26 20:55 | 192,012-192,416 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Hourly/2026-09-27-02.tar.zst` | 12 | 09-26 21:00 to 09-26 21:55 | 192,031-192,621 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Hourly/2026-09-27-03.tar.zst` | 12 | 09-26 22:00 to 09-26 22:55 | 191,939-192,508 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Hourly/2026-09-27-04.tar.zst` | 12 | 09-26 23:00 to 09-26 23:55 | 192,052-192,449 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Hourly/2026-09-27-05.tar.zst` | 12 | 09-27 00:00 to 09-27 00:55 | 191,854-192,625 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Hourly/2026-09-27-06.tar.zst` | 12 | 09-27 01:00 to 09-27 01:55 | 191,945-192,672 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Hourly/2026-09-27-07.tar.zst` | 12 | 09-27 02:00 to 09-27 02:55 | 192,000-192,466 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Hourly/2026-09-27-08.tar.zst` | 12 | 09-27 03:00 to 09-27 03:55 | 192,111-192,492 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Hourly/2026-09-27-09.tar.zst` | 12 | 09-27 04:00 to 09-27 04:55 | 192,077-192,483 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Hourly/2026-09-27-10.tar.zst` | 12 | 09-27 05:00 to 09-27 05:55 | 191,969-192,404 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Hourly/2026-09-27-11.tar.zst` | 12 | 09-27 06:00 to 09-27 06:55 | 192,033-192,487 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Hourly/2026-09-27-12.tar.zst` | 12 | 09-27 07:00 to 09-27 07:55 | 192,052-192,520 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Hourly/2026-09-27-13.tar.zst` | 12 | 09-27 08:00 to 09-27 08:55 | 192,115-192,598 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Hourly/2026-09-27-14.tar.zst` | 12 | 09-27 09:00 to 09-27 09:55 | 191,938-192,560 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Hourly/2026-09-27-15.tar.zst` | 12 | 09-27 10:00 to 09-27 10:55 | 191,783-192,433 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Hourly/2026-09-27-16.tar.zst` | 12 | 09-27 11:00 to 09-27 11:55 | 191,886-192,396 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Hourly/2026-09-27-17.tar.zst` | 12 | 09-27 12:00 to 09-27 12:55 | 191,881-192,415 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Hourly/2026-09-27-18.tar.zst` | 12 | 09-27 13:00 to 09-27 13:55 | 192,047-192,716 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Hourly/2026-09-27-19.tar.zst` | 12 | 09-27 14:00 to 09-27 14:55 | 192,057-192,554 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Hourly/2026-09-27-20.tar.zst` | 12 | 09-27 15:00 to 09-27 15:55 | 191,863-192,618 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Hourly/2026-09-27-21.tar.zst` | 12 | 09-27 16:00 to 09-27 16:55 | 191,967-192,322 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Hourly/2026-09-27-22.tar.zst` | 12 | 09-27 17:00 to 09-27 17:55 | 191,838-192,413 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Hourly/2026-09-27-23.tar.zst` | 12 | 09-27 18:00 to 09-27 18:55 | 192,016-192,455 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Hourly/2026-09-28-00.tar.zst` | 12 | 09-27 19:00 to 09-27 19:55 | 191,861-192,404 | 6 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Monthly/2026-05.tar.zst` | 23 | 05-07 18:55 to 05-31 08:05 | 191,396-192,540 | 2/3/4/5 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Monthly/2026-06.tar.zst` | 9 | 06-01 18:55 to 06-30 18:55 | 191,999-192,535 | 5 | yes / none | 0 | 0 | 0 | 0 | 0 |
| `Monthly/2026-07.tar.zst` | 5 | 07-01 18:55 to 07-06 13:25 | 192,105-192,529 | 5 | yes / none | 0 | 0 | 0 | 0 | 0 |
| **All 79 artefacts** | **938** | 05-07 to 09-27 | | | | **0** | **0** | **1** | **1** | **0** |

**Beyond the brief's list:** `D:\ShatteredLegacy\backups\uo-modernuo-premigration-full-20260531T130851Z.tar.gz`
(3.75 GB, 2026-05-31) holds **26 more saves**, 25 automatic backups (05-07 to 05-31 UTC) and a `Saves`. Read the
same way: **zero** of all five types in each, `Dagger` controls 21 to 31. Its two `temp/` folders hold idx files
without a type table (interrupted saves) and were not counted.

**Why these five.** The brief said to derive the list from `notes/armour-set-completion.md`. That task
re-parented exactly two types, `SpiritualityHelm` and `ValorGauntlets`, through
`server/patches/Virtue-stock-pieces-set-carrier.patch` (§A.1.1, §C). It ported two new ones, `BestialKilt` and
`VirtuososKilt`, which were in its own 09-26 check. `BestialArms` is D28. Types re-parented by earlier tasks (S10's
four gargish bases, CC9's `GargishDagger` and the rest) are not in this table. They are covered by §6.4, which
counts instances of **every** type we declare, not only these five, and finds none of those in the live save either.

---

## 3. What the live world contains

From the live `Saves` written 20:40 tonight, cross-checked against the 20:40 automatic backup:

| | Count |
|---|---|
| Accounts | **7** |
| Characters (`PlayerMobile`) | **6** |
| Mobiles, all | 34,986 (NPCs, vendors and creatures, apart from the 6) |
| Items | 192,208 (`Static` 28,531, `Backpack` 24,248, `Gold` 20,498 and `Spawner` 5,284 lead) |
| Distinct types with instances | 1,457 (1,465 in the type table) |
| Oldest save on disk | 2026-05-07 18:55 (`Monthly/2026-05`, first snapshot; the tarball's first is the same save) |
| Oldest entity | created 2026-05-07 08:47:59 |
| Newest save | 2026-09-27 20:40, and it keeps going: the live shard saves every 5 minutes |
| Characters created | 05-07, 05-10, 05-12, 05-14, 05-20, **09-16** |

The live server's own load line agrees: `Loading world done (192181 items, 34986 mobiles)` at its 08:54 restart
this morning.

**Has anyone played since 09-26? No. Nobody has logged into the live shard since 2026-09-16, 17:35 CDT.** Three
independent readings agree:

1. **The account file has not changed in eleven days.** `Accounts/Accounts.bin` is byte-identical (SHA-1 prefix
   `4fdc9558a3fc`) in every snapshot from `2026-09-16-22-55-00` UTC through tonight's live save. A play session
   cannot leave it unchanged, because game time accrues to the account at logout (pinned
   `UOContent/Accounting/Account.cs:784`, into `TotalGameTime`, `[SerializableProperty(12)]`).
2. **The live container's log** (`docker logs sl-modernuo`, which runs back to the container's creation on 06-29)
   has **7** `Valid credentials` lines in total. The last is 2026-09-16 22:35 UTC. That day an account was created
   (17:13 CDT) and its character with it (17:14), which is the sixth character above.
3. **Every character's serialized record has kept the same length** since that 09-16 snapshot.

The only connections since are **five on 09-26 between 18:14 and 18:38 CDT**, each connecting and disconnecting
within the same millisecond, with no credentials sent. That looks like the player package's reachability check,
though that is inferred from the timing and was not verified.

The item count moves by ±400 between snapshots, and that is spawners, not people. In short: 6 characters on 7
accounts, the last one made on 09-16, and nothing played since.

**One correction this implies for D25.** Its row says Chase searched the Add Menu for `gargishwarhammer` on the
live shard on 09-27. The live log has no login on 09-27, so that search was on another shard, most likely the test
shard. D25's conclusion stands, since the type is not in the live image either way. Only the account of where the
search happened is off.

---

## 4. The rollback, as commands. None of these were run.

**Assumed throughout:** Windows PowerShell 5.1 (`;`, never `&&`); Docker Desktop running; paths as measured
tonight; nobody logged in (§3); the compose network `uo_default` still exists, which it does as long as `sl-ddns`
from the same project exists. Nothing here uses `docker compose down`, because the live compose project also owns
`sl-ddns` and `down` would take public DNS updates with it.

**Where things are.** The live shard reads four host paths, all verified with `docker inspect sl-modernuo`:

| Host path | In the container | Why it matters |
|---|---|---|
| `D:\ShatteredLegacy\server\lib\uo\modernuo\Saves` | `/var/lib/uo/modernuo/Saves` | the world, **and the accounts** (`Saves\Accounts`) |
| `D:\ShatteredLegacy\server\uo\modernuo\Configuration` | `/modernuo/Configuration` | live config. **In the gitignored build tree, so no copy exists anywhere else** |
| `D:\ShatteredLegacy\server\lib\uo\modernuo\Backups`, `...\Archives` | same names | written by the server, not read at load |
| `D:\ShatteredLegacy\server\uo\modernuo\Projects\UOContent\Misc` | `/modernuo-projects` (rw) | copied over `/modernuo/Projects` by `entrypoint.sh` at start. **Not** what the compose file says (§6.2) |

### 4.1 Capture the running image. Any time before the deploy; it touches no save.

```powershell
docker inspect sl-modernuo --format "{{.Image}}"
# expect sha256:36cc709a82a67a1bc233e6aa0ce44a1f3991d6277c05f0e6fe18663b524e8dc4
docker commit sl-modernuo sl-modernuo:rollback-live-20260927
docker image inspect sl-modernuo:rollback-live-20260927 --format "{{.Id}} {{.Created}}"
```

`docker commit` pauses the server for a moment by default. It may also **fail**, because the parent image is gone
from the store; whether a containerd-snapshotter commit still works in that state is **unverified**. If it fails,
export the filesystem instead. The rollback in 4.3 supplies the entrypoint itself, so this route needs no
`--change` quoting, which PowerShell 5.1 mangles:

```powershell
docker export sl-modernuo -o D:\ShatteredLegacy\backups\sl-modernuo-rootfs-20260927.tar
docker import D:\ShatteredLegacy\backups\sl-modernuo-rootfs-20260927.tar sl-modernuo:rollback-live-20260927
```

**Until one of these has worked, there is no rollback to the running image.** Only `uo-modernuo:latest`
(`bc04a35bf344`) would be available, and that is a different build (§6.1).

### 4.2 Cold backup of the live save, immediately before the deploy

```powershell
$stamp = Get-Date -Format 'yyyyMMdd-HHmm'
$dst = "D:\ShatteredLegacy\backups\predeploy-$stamp"
New-Item -ItemType Directory -Path $dst | Out-Null

# 1. Nobody online: the most recent Connected/Disconnected line should end "[0 Online]"
docker logs --tail 40 sl-modernuo

# 2. Stop. SIGTERM waits for a save already in flight but does NOT save again (pinned Server/Main.cs:333-348),
#    so the backup is the last 5-minute autosave. With nobody online that loses nothing a player made.
docker stop -t 120 sl-modernuo

# 3. Keep the container's record and its log. The log is the only login history (§3), and it dies with the container.
docker inspect sl-modernuo | Out-File -Encoding utf8 "$dst\sl-modernuo.inspect.json"
cmd /c "docker logs -t sl-modernuo > $dst\sl-modernuo.log 2>&1"

# 4. If 4.1 was not done yet, do it now (a stopped container commits without pausing anything)
docker commit sl-modernuo sl-modernuo:rollback-live-20260927

# 5. Copy the save (accounts included) and the live configuration
robocopy D:\ShatteredLegacy\server\lib\uo\modernuo\Saves "$dst\Saves" /E /COPY:DAT /DCOPY:DAT /R:1 /W:1 /NP
robocopy D:\ShatteredLegacy\server\uo\modernuo\Configuration "$dst\Configuration" /E /COPY:DAT /DCOPY:DAT /R:1 /W:1 /NP
robocopy D:\ShatteredLegacy\server\uo\modernuo\Projects\UOContent\Misc "$dst\Misc" /E /COPY:DAT /R:1 /W:1 /NP
Copy-Item D:\ShatteredLegacy\docker\uo\docker-compose.yml, D:\ShatteredLegacy\docker\uo\entrypoint.sh $dst

# 6. Verify the copy. No output from Compare-Object means identical.
$a = Get-ChildItem D:\ShatteredLegacy\server\lib\uo\modernuo\Saves -Recurse -File | Get-FileHash | ForEach-Object { $_.Hash }
$b = Get-ChildItem "$dst\Saves" -Recurse -File | Get-FileHash | ForEach-Object { $_.Hash }
Compare-Object $a $b
```

`robocopy` exit codes 0 to 7 are success; 8 and above is a failure. The save is about 30 MB, and D: had 390 GB free
tonight. `backups/` is already the gitignored home of the May tarball. `.env` is left out on purpose: it holds the
Cloudflare token and does not change in a deploy.

To take a backup **without** deploying, finish with `docker start sl-modernuo`.

### 4.3 Bring the live shard back up on the old image with that backup

```powershell
$dst = 'D:\ShatteredLegacy\backups\predeploy-YYYYMMDD-HHMM'   # the folder 4.2 made
$stamp2 = Get-Date -Format 'yyyyMMdd-HHmm'

# 1. Stop and remove the NEW container. Keep its log for the post-mortem. Not "compose down" (it takes sl-ddns too).
docker stop -t 120 sl-modernuo
cmd /c "docker logs -t sl-modernuo > $dst\failed-deploy-$stamp2.log 2>&1"
docker rm sl-modernuo

# 2. Set aside what the new image wrote, then restore the save and the configuration exactly.
#    ModernUO adds missing keys to modernuo.json at start (ServerConfiguration.GetOrUpdateSetting), so the new
#    image may have changed the config too. /MIR makes the folder match the backup exactly.
Move-Item D:\ShatteredLegacy\server\lib\uo\modernuo\Saves "D:\ShatteredLegacy\server\lib\uo\modernuo\Saves-failed-$stamp2"
robocopy "$dst\Saves" D:\ShatteredLegacy\server\lib\uo\modernuo\Saves /E /COPY:DAT /DCOPY:DAT /R:1 /W:1 /NP
robocopy "$dst\Configuration" D:\ShatteredLegacy\server\uo\modernuo\Configuration /MIR /COPY:DAT /DCOPY:DAT /R:1 /W:1 /NP

# 3. Start the captured image with the running container's exact settings, as inspected 2026-09-27.
#    One line on purpose. --entrypoint and the ENVs make it work for the "docker import" route too.
docker run -d --name sl-modernuo --restart unless-stopped -t -i --security-opt seccomp=unconfined --network uo_default --network-alias modernuo -p 2593:2593/tcp -p 2593:2593/udp -w /modernuo --entrypoint /entrypoint.sh -e TZ=America/Chicago -e DOTNET_ROOT=/usr/local/dotnet -e DOTNET_RUNNING_IN_CONTAINER=true -e DOTNET_EnableDiagnostics=0 -e PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/dotnet -v D:/ShatteredLegacy/server/uo/modernuo/Projects/UOContent/Misc:/modernuo-projects -v D:/ShatteredLegacy/server/uo/modernuo/Configuration:/modernuo/Configuration -v D:/ShatteredLegacy/server/lib/uo/modernuo/Saves:/var/lib/uo/modernuo/Saves -v D:/ShatteredLegacy/server/lib/uo/modernuo/Backups:/var/lib/uo/modernuo/Backups -v D:/ShatteredLegacy/server/lib/uo/modernuo/Archives:/var/lib/uo/modernuo/Archives -v D:/ShatteredLegacy/client-data/classic-client:/var/lib/uo/client-data/classic-client:ro sl-modernuo:rollback-live-20260927

# 4. Verify it is the old server on the old world
docker logs --tail 80 sl-modernuo
```

**What "back" looks like in that log:** `Loading world done (` about 192,200 items and 34,986 mobiles, then
`ClusterF stat caps applied to 6 loaded player(s): 500 per stat, 1500 total.` and
`Restricting client version to 7.0.114.40 or newer`. The old image prints exactly those lines at every start, and
two of them identify this world.

**What these commands assume and do not cover:**

- **It deliberately avoids `docker compose up`,** because that would build or use `uo-modernuo:latest`, the wrong
  image (§6.2). A container made with `docker run` carries no compose labels, so a later `compose up` stops on the
  name clash instead of silently replacing it. That is the safe failure.
- **Backups and archives the new image wrote stay where they are.** They are not read at load, but they sit in the
  same folders as the old ones. If anyone later restores "the latest automatic backup", check it predates the
  deploy.
- **Anything a player did on the new image is lost by design,** because the restore is a restore.

---

## 5. Q-063: the client data version, stated as a coupling

**What the live shard's data auto-detects as today: 7.0.114.40.** The server has no `clientData.clientVersion`
set, and no CUO `settings.json` in the data folder, so `UOClient.Load` falls to `DetectClassicClient` (pinned
`Server/Client/UOClient.cs:38-42`). That reads the `VS_VERSION_INFO` of
`D:\ShatteredLegacy\client-data\classic-client\client.exe`. Read directly tonight: **7.0.114.40**. The live log
says `Automatically detected client version 7.0.114.40` at every start, the latest at 08:54 this morning.

**What the server enforces: 7.0.114.40 or newer, Kick after 20 s.** Live `modernuo.json` has
`clientVerification.enable` true, `invalidClientResponse` Kick, `kickDelay` 00:00:20, and **no**
`clientVerification.minRequired` or `maxRequired`. With neither set, `ClientVerification.Initialize` makes the
floor whatever was detected (`UOContent/Misc/ClientVerification.cs:54`). **The floor is not configured anywhere.
It is a side effect of which `client.exe` sits in the data folder.** `Configuration-test/modernuo.json` is identical
in all of these keys.

**What the player package enforces: 7.0.114.40, as its own constant.**
`player-package/payload/app/Setup.ps1:30` hard-codes `$minVersion = [version]'7.0.114.40'` and refuses anything
older, with a message telling the player to let EA's launcher finish. That constant is also baked into
`dist/ShatteredLegacy-2026-09-26.zip`, which is the copy family members actually hold.

**What would have to move together if the data went to 7.0.117.0:**

| # | Thing | Moves how |
|---|---|---|
| 1 | `client-data\classic-client` contents | the swap itself. Changes collision (statics, tiledata, map UOPs) **and**, through `client.exe`, the detected version |
| 2 | The server's kick floor | **moves automatically to 7.0.117.0** with the `client.exe` in (1). It moves independently only if `clientVerification.minRequired` is set in `modernuo.json`. That key is read with `GetSetting`, not `GetOrUpdateSetting` (`ClientVerification.cs:34`), so it is never written there by default and has to be added by hand. That is Q-063's "pin it lower for a grace window" lever, and it exists |
| 3 | The package's `$minVersion` | does **not** move by itself. Left at 7.0.114.40, a player on 7.0.114.40 to 7.0.116.x passes setup and is kicked 20 seconds after login. Raising it means rebuilding the package **and** redistributing it, because copies already handed out keep the old constant |
| 4 | The test shard | mounts **the same** `client-data\classic-client` folder read-only (`docker-compose.test.yml`), so live and test change together. Q-063's plan to try 7.0.117.0 "on the test shard first" needs the test compose to mount a **different** folder first. As things stand, swapping the folder for the test swaps it for live |
| 5 | Houses and seeded coordinates in the 1,487 changed blocks | Q-063's own two checks, unchanged by anything here |

**One trap for whoever tests it:** client verification **exempts staff** (`ClientVerification.cs:120` returns early
unless `AccessLevel == Player`). A GM or admin account is never kicked for version, so a staff login cannot show
whether the floor is right. Test with a player account.

**Coupling to the deploy itself: none mechanical.** The client data is a host folder, and every image mounts the
same one. D25 asks that Q-063 be settled before a deploy. That is a sequencing choice, and nothing in either image
forces it.

---

## 6. What makes a deploy riskier than §2 to §5 imply

### 6.1 The running image is gone from the store; only the container holds it

`docker ps` shows `sl-modernuo`'s image as a bare ID, `36cc709a82a6`. `docker image ls -a` has no such image, and
`docker image inspect` on the full digest says "No such image". The container keeps running from its own snapshot
(containerd snapshotter, `docker info`). Its `Config.Image` still reads `uo-modernuo`, which is the string D25
quotes. That tag now resolves to **`uo-modernuo:latest` = `bc04a35bf344`, built 2026-09-06 10:45**, while the
container was created 2026-06-29. **They are not the same image**, and nothing on disk records what `bc04a35`
contains. It was built in the middle of 09-06's direction changes (`uo-modernuo:f1-verify` followed 40 minutes
later).

So:

- "Roll back to `uo-modernuo`" means `bc04a35`, an untested build, against the live save.
- `docker rm sl-modernuo`, `compose up --force-recreate`, or any compose run that decides to recreate destroys the
  only copy of the server the world was saved by.
- §4.1 is the fix. It is cheap and can happen any time. It has **not** been done, and whether `docker commit` works
  here is unverified.

The test shard shows the same thing in miniature: `sl-modernuo-test` runs `2e7dcae65e54`, which is also no longer
tagged, because `sl-modernuo:latest` moved to `2bc0e19c25cd` at 19:32 tonight. That one does no harm on a
throwaway save. It is the same mechanism, though: **retagging an image strands the container running it.**

### 6.2 The live compose file no longer describes the live container, and does not name the new image

`docker/uo/docker-compose.yml`:

- has `build:` and **no `image:`**, so compose names its image `uo-modernuo` (project `uo` + service `modernuo`).
  Nothing in it refers to `sl-modernuo:latest`, the gated image `build.sh` produces. **A deploy is therefore not a
  one-command step:** the file needs an `image: sl-modernuo:latest` line, as `docker-compose.test.yml` has, or the
  new image needs retagging, which strands the old one as in 6.1. And `docker compose up --build` from this file
  would build an image **with no test gate**, which AGENTS.md exists to prevent.
- mounts `server/customizations` read-only at `/modernuo-projects`. The running container has
  `server/uo/modernuo/Projects/UOContent/Misc` there, read-write. The config hash differs (label `e9c28f95…`), so
  **any** `docker compose up -d` in `docker/uo` recreates `sl-modernuo`, even one meant for `sl-ddns`.
- The `/modernuo-projects` copy in `entrypoint.sh` is, I believe, inert for the running server. ModernUO runs
  compiled assemblies, and nothing in the entrypoint compiles. That is **unverified**. The compose comment
  ("synced into the container on each start") suggests someone once expected hot edits to take effect.

### 6.3 Nobody has shown the live save loads under the new image

§2 answers the question it was asked: re-parenting is free for these types because there are no instances. It
says nothing about the **1,457 types that do have instances**, and a deploy re-reads all of them with new
serializers. Checked tonight, from source only:

- **Every type with a live instance resolves by name** in pinned ModernUO or `server/customizations`: 1,457 of
  1,457, zero unresolved, full namespace checked for our own 73. This matters more than it looks, because
  ModernUO **silently skips** an entity whose type it cannot resolve (`GenericEntityPersistence.cs:182`,
  `if (ctor == null) continue;`). A missing type would delete items without an error.
- **Of our own types, 73 have live instances** (34 gargoyle vendor types with 43 instances, `OldHavenMage` ×22,
  `PropertyEssence` ×23, `PetMimic` ×3, the ClusterF persistence singletons, the extended ingots,
  `ReinforcedHammerOfHephaestus`, and the rest). They are declared in 38 files. **35 of those files are unchanged
  in git since the June commit `44db37b`** (`git diff 44db37b HEAD` is empty, and none has uncommitted edits).
  The other 3 did not exist then: two are partial-class additions with no serialized members
  (`EliteNinjaSpawnAlias.cs`, `PlayerMobileSetResistances.cs`), and one is `OutridersGuildmaster.cs`.
- The five full-file replacements in `server/patches/` (`BaseGuildmaster`, whose subclasses account for most of
  the 247 live `*Guildmaster` instances; `BulkMaterialType`; `JacobsPickaxe`; `LargeSmithBOD`; `Mining`) are
  **unchanged in git since `44db37b`**.
  `ResourceInfo.cs` moved to `customizations/` on 09-06. Its `CraftResource` enum is unchanged for every value
  that existed in June, and it gained eight lumber values **after** the last one, so every stored resource number
  keeps its meaning. No patch in `server/patches/` adds a serialized member.

**The gap: the June image was not built from `44db37b`,** or from any commit. `OutridersGuildmaster` has a live
instance, and its file first appears in git at `1f5dd63` ("Recover canonical ModernUO customizations", 09-06). So
the June image had source that git never saw, and "unchanged since `44db37b`" is evidence, not proof, that the new
serializers read what the old ones wrote. **What proves it is loading a copy of the live save under
`sl-modernuo:latest` and comparing the `Loading world done` counts** (192,2xx items, 34,986 mobiles, 7 accounts,
6 characters). That is the rehearsal this task was told not to run, because it needs a container. It is the one
check here that turns "should load" into "loads".

### 6.4 None of our re-parented types exists in the live world

This widens §2 without being asked. Every one of the 1,067 type names declared in `server/customizations` was
counted against the live save, not just the five. The 73 with instances in §6.3 are all ClusterF-era content that
predates the porting work. **None of the S10, CC9, CC4, CC6 or armour-set ports has a live instance**, because the
live image has never contained them (D25). So the re-parenting window is open for all of them at once. It closes
for all of them at once too, on the first play after a deploy.

### 6.5 Smaller things a deploy operator should know

- **Stopping the server does not save** (`Main.cs:333-348`). §4.2 accepts the last autosave. That is right only
  while nobody is online.
- **The live configuration exists in one place.** `server/uo/modernuo/Configuration` is inside the gitignored
  build tree, and ModernUO writes new keys into `modernuo.json` on start. Back it up with the save (§4.2 does).
- **The log that proves nobody has played lives only in the container.** Removing `sl-modernuo` deletes it.
- **Live `serverListing.address` is `192.168.1.58`,** the same LAN address as the test config. Noted, not
  investigated. It is outside this brief, and D8's history suggests it is deliberate for the house LAN.
- **The saves themselves look healthy.** In 938 snapshots from 05-07 to tonight, every idx is the right size,
  every hash resolves, the item count stays within 191,343 to 193,229, and the character count only ever rises. The
  one gap, 2026-07-06 to 2026-09-16, is the server being stopped (the container log is silent across it), not lost
  saves.

---

## What was not verified

- **That the live save loads under the new image** (§6.3). Source-level evidence only.
- **That `docker commit` or `docker export` works** on a container whose image left the store (§4.1).
- **That the `/modernuo-projects` copy is inert** (§6.2).
- **What `uo-modernuo:latest` (`bc04a35`) contains** (§6.1).
- **That the 09-26 connections were the player package** (§3). Inferred from timing.
- None of the §4 commands has been run, in any form, by anyone.

## Reproducing the count

Tonight's parser was a scratch script, not a repo tool (this task writes one file). Its core, enough to reproduce
every number above:

```python
import struct
def types(b):                      # SerializedTypes.db: int version, int count, then (ulong hash, 7-bit-length UTF-8 name)
    v, n = struct.unpack_from('<ii', b, 0); o = 8; db = {}
    for _ in range(n):
        h = struct.unpack_from('<Q', b, o)[0]; o += 8; l = s = 0
        while True:
            c = b[o]; o += 1; l |= (c & 0x7F) << s; s += 7
            if c < 0x80: break
        db[h] = b[o:o + l].decode(); o += l
    return db
def entries(b):                    # Items.idx / Mobiles.idx, version 3: 33-byte entries after an 8-byte header
    v, n = struct.unpack_from('<ii', b, 0); assert v == 3 and len(b) == 8 + 33 * n
    return struct.iter_unpack('<BQIqqi', b[8:])   # flag(2), typeHash, serial, createdTicks, pos, len
```

Archives are `tar.zst`, one folder per snapshot, read with `zstandard` stream decompression. The 09-26 tool,
`tools/save_instance_check.py`, is still correct for what it reads, but **it reads only the last two archives of
each kind**. Anyone re-running it for a deploy decision should widen that.
