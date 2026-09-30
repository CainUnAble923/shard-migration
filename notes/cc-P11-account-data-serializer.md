# cc-P11: D40, the serializer failure that stopped the live shard

Brief: `cc-P11` (pasted). Nothing is committed, deployed or restarted. The live container and its `y/n/a` prompt were
not touched. The only things run against Docker's live state were `docker inspect sl-modernuo` and
`docker image ls/inspect`, all read-only. Changes in `D:\ShatteredLegacy`'s working tree:

- `server/customizations/WoodDiscoveryEntry.cs`: the read constructor branches on version.
- `server/tests/Misc/AccountDataSerializerVerification.cs`: new, three facts.

## 0. Answer

**It is a version skew, not an asymmetry in current code.** It runs backwards, though: the save was written by a
**newer** `WoodDiscoveryEntry` (v1) than the one now reading it (v0), and the v0 reader read its version number and
ignored it. The brief's hypothesis, that an earlier collection misaligned the stream and `WoodDiscoveryEntry` was only
the messenger, is **refuted by measurement**: every collection before `WoodDiscoveries` is byte-aligned (§2).
`WoodDiscoveryEntry` is the culprit.

- The current code writes what it reads. A full round trip with every collection non-empty passes on the
  **unchanged** code (§3, red run). A fresh world would not hit this.
- It is **D29 happening.** The world was last written by the 2026-06-29 container. At 14:16 `sl-modernuo` was
  recreated on `uo-modernuo:latest`, which is `bc04a35bf344`, built 2026-09-06 from canonical `server/customizations`.
  That is the untested image D29 warned "bring it back up on `uo-modernuo`" would start.
- **Fixed** with a version branch, which reads v1 and collapses it to v0. Nothing is lost for this world (§4).
  Green 261/261, image `sl-modernuo:latest` built. **Not deployed.**

**Chase: answering `y` at the prompt deletes the whole `ClusterFAccountPersistence` item, not one wood entry.** That item
holds all 7 accounts' progression: renown, guild rep, currency, restoration registry, work orders, ore discoveries,
commissions and exploration. Only `CainUnAble` has wood entries, but a `y` loses everyone's data.

## 1. Where v1 came from

| Image | What it is | `WoodLocationRecord` in `UOContent.dll` |
|---|---|---|
| `f390c877f0b7` `sl-modernuo:rollback-live-20260927` | DLL dated 2026-06-29 17:34 | **1** (present) |
| `bc04a35bf344` `uo-modernuo:latest`, built 2026-09-06 | **what `sl-modernuo` runs since 14:16** (`docker inspect`: created 19:16:00Z) | 0 |
| `a63b135a5a90` `sl-modernuo:setcomplete` (09-26) | | 0 |
| `e1cc98812f16` `sl-modernuo:latest` (P10's 16:37 build) | | 0 |

Checked with a throwaway `docker run --rm --network none --entrypoint sh <image> -c 'grep -c WoodLocationRecord …'`
on each. None of these is the live container.

The source of v1 is the stale build tree: `server/uo/modernuo/Projects/UOContent/Misc/WoodDiscoveryEntry.cs`,
mtime 2026-06-29. It is **v1**, with a `WoodLocationRecord` list (facet, region, Point3D, DateTime, amount) in place of
`FirstFound`, and its v0 to v1 migration synthesises a `("Unknown", "Unknown", Point3D.Zero, firstFound, TotalChopped)`
location. **That is exactly what is in the save** (§2). Canonical `server/customizations/WoodDiscoveryEntry.cs` has one
commit, `9f5dc21` (2026-05-31, the import), and is v0. The Jun 29 grove-tracking feature never reached canonical.
`git log --all` finds no other version, and no other tree under `D:\UO` or `D:\ShatteredLegacy` defines the class.

**Only this serializer regressed.** I diffed every `Misc/*.cs` in that build tree against canonical (`diff -w
--strip-trailing-cr`). Five files differ in substance: `WoodDiscoveryEntry.cs` (137 lines),
`ForestersLogbookGump.cs` (37), `ClusterFLumberjackingExtension.cs` (17), `OutridersGuildmaster.cs` (2) and
`ResourceInfo.cs` (2). The first three are the Jun 29 feature, and only the first has a serializer. Every other file
with a serializer is identical ignoring whitespace: `ClusterFAccountData`, `OreDiscoveryEntry`,
`ClusterFWorkOrderSystem`, `ClusterFBulletin`, `ClusterFAchievements`, `ForestersLogbook` and the satchels.
**Not checked:** files outside `Misc/`, and whether the Jun 29 image's ModernUO core was the pinned `7c9215d97`.

## 2. The measurement: the stream, byte by byte

Read-only from `D:\ShatteredLegacy\server\lib\uo\modernuo\Saves\Items\` (all 20 save files are dated 13:50:00):

- `Items.idx` is v3 with 192,177 entries. Serial `0x40128E03` is at `Items.bin` position 7,776,186, length **656,288**.
- I decoded that blob with a Python mirror of the C# readers, printing offsets. The script is
  `notes/cc-P11-decode-account-blob.py`. `ClusterFAccountPersistence` starts at byte 13 with version 0 and 7 accounts,
  and every account is `ClusterFAccountData` v13.

**Decoded with the current (v0) wood reader:**

```
OK   acct#0 'Aetherion'       32-131283   ore2 sc3 sl1 chunks1 (6 bitarrays) ec0 wood0
OK   acct#1 'Cain'            131289-131438
OK   acct#2 'whoartthoudiddy' 131455-131537
FAIL acct#3 'CainUnAble' from 131549: IMPOSSIBLE TICKS 7950268418068840449 (0x6e55070100000001) at offset 265433
```

`CainUnAble` reads cleanly through all earlier collections: rep 6, currency 6, registry 2, joined 6, flags 4, flag
values 2, work orders 5 active and 20 completed, ore 7, commissions 3, chunks with 6 bit arrays, and creatures 14
ending at `Brigand`. Then the wood count is 4 and the first entry is:

```
01000000  01 0B "RegularWood"  F4000000 (244)  01000000 (Reported)  01000000 (1 location)
01 07 "Unknown"  01 07 "Unknown"  00*12 (0,0,0)  FC10F673E4BBDE08 (2026-05-27 11:38:20Z)  F4000000 (244)
```

The v0 reader reads `01000000 01 07 55 6E 6B 6E` ("1 location" plus the start of "Unknown") as ticks. Those are the
impossible ticks above, and the live exception.

**Decoded with a v1 wood reader: all 7 accounts, ending at byte 656,288 of 656,288.** Every length matches, which is
the check ModernUO's loader makes (`GenericEntityPersistence.cs`, "Serialized object was N bytes").

All four wood entries (RegularWood 244, OakWood 101, AshWood 20, YewWood 10) have exactly one location, the
synthesised `Unknown / (0,0,0)` one. Each carries the original FirstFound (2026-05-27 and 05-28) and amount =
TotalChopped. **The v1 data holds nothing that v0 cannot, so collapsing it loses nothing in this world.**

Answers to brief §2:
1. `ClusterFAccountData` writes a version (13) and branches on it. `WoodDiscoveryEntry` wrote one (0) and **did not**
   branch. `var version = r.ReadInt();` was never read again. That is the latent defect that turned a skew into a crash.
2. No earlier collection changed shape. Every file has one commit, `9f5dc21`, and the bytes agree.
3. The read goes wrong at object offset 265,433, inside the first wood entry of account #3.

## 3. The test, red then green

`server/tests/Misc/AccountDataSerializerVerification.cs`, namespace `ShatteredLegacy.Tests`:

| Fact | Old code | New code |
|---|---|---|
| `AnAccountWithEveryCollectionNonEmptySurvivesAWriteAndARead`: every collection non-empty, including 2 wood entries with a real `FirstFound`, exploration on 2 of 6 facets, and an artificer order. Asserts every field, ticks for every DateTime, null facets stay null, every bit, and **bytes read == bytes written** | **PASS** (proves the current code is symmetric) | PASS |
| `TheWoodDiscoveriesThatStoppedTheLiveShardReadBackToTheLastByte`: the exact 276 live bytes (object bytes 265,404 to 265,679, wood names, counts and timestamps only, no account data), read to the last byte, FirstFound ticks as in the save, then written as v0 and read again | **FAIL**: `ArgumentOutOfRangeException: Ticks must be between…` at `IGenericReader.ReadDateTime` from `WoodDiscoveryEntry..ctor`, **the live stack** | PASS |
| `AWoodDiscoveryEntryOfAnUnknownVersionFailsLoudly`: version 2 throws `InvalidDataException` naming the version | FAIL: nothing thrown | PASS |

Runs via `docker/uo/build.sh`: red was `--tests-only`, 259/261 passing. Green was the full build, **261/261**, then
`Built sl-modernuo:latest with patches applied and 261 shard test(s) passing`.

**The round trip catches the failure the brief was worried about.** I removed `w.Write(Reported)` from
`OreLocationRecord.Serialize`, which is an earlier collection changing shape with no version bump. The round trip went
**red** on the length assertion (expected 956). I then restored the file and checked its sha256 was identical, and
reran `--tests-only` so `sl-uo-builder:latest` does not hold the mutant.

About `FirstFound` being get-only (brief §3): the read constructor assigns it directly. That is legal for a get-only
auto-property and symmetric with the writer. It was never the drift. The drift was a second, different writer.

## 4. The fix

`WoodDiscoveryEntry(IGenericReader)` now branches on the version:

- **v0** reads as before.
- **v1** reads the location list and sets `FirstFound` to the earliest location's time, or `DateTime.MinValue` if the
  list is empty, which is what v1's own `FirstFound` getter returned.
- **Any other version throws `InvalidDataException`.** That is loud on purpose: it is the same prompt, but with a message
  that says what is wrong.

The writer **stays v0**, so the rollback image's reader (whose v0 branch reads this layout) can still load a world
saved by the fixed build. The doc comment records v1's layout and says never to reuse 1. No catch was widened.

## 5. What this does not establish (unverified)

- **Whether the whole 13:50 save loads on the fixed image.** The loader stops at the first failure, so nothing after
  `0x40128E03` has been tried. Everything in that world was written by the Jun 29 build and is now read by a Sep build
  with ~250 more files (D25). Serializer drift in other `Misc/` files is excluded (§1). Core ModernUO and non-`Misc`
  paths are not. **The decisive check is to load a copy of the live `Saves/` on the fixed image, away from live**,
  before anyone points live at it.
- Why the 14:16 start came up on `uo-modernuo` is not established here. `notes/shard-console.md` and D37 cover the
  13:50 stop. The mechanism D29 describes (compose recreating the container) fits, but I did not verify it.

## 6. Decisions that are Chase's

1. **The live shard.** Do not answer `y` (§0). The candidate is to deploy an image with this fix, after the load check
   in §5. The other way back is the rollback image `f390c877`, which reads this save as it is; D29 records it as the
   last copy of the build that wrote the world.
2. **The Jun 29 grove-tracking feature** (three files in the stale build tree) is missing from canonical. Players had
   it live, and this fix drops it silently. Porting it forward would mean making canonical write v1, which is safe now
   that the reader understands v1. It is a content decision, so I did not make it.
3. **D40's row in `docs/bug-list.md`.** I did not edit `docs/`. Proposed text: cause = D29 realised, WoodDiscoveryEntry v1
   (Jun 29 build) read by v0 canonical, which ignored its version; fix = version branch plus a round-trip gate;
   evidence = this note.
