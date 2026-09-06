# P1 / CC1 — runtime validation of the port recipe and the five repaired patches

Date: 2026-09-06. Agent: Claude Code. Pinned ModernUO `7c9215d97`.
Corrections landed in `notes/port-recipe.md`. This file is the evidence and the method.

Nothing was deployed. The live `sl-modernuo` container was never started and is still
`Exited` exactly as found. All testing ran in a throwaway container `sl-modernuo-p1` on
**127.0.0.1 only**, with a scratch `Saves/` under the session temp directory, a copy of the
Configuration, and no `ddns-updater`. The container and its 5 GB builder image were removed
afterwards.

## What was done

1. Ported `PlagueRat.cs` from ServUO `Mobiles/Normal` into
   `server/customizations/Mobiles/Normal/PlagueRat.cs`.
2. Full `docker build` from pinned upstream: all 9 patches applied, zero compiler errors.
3. Ran it, logged in with ClassicUO, spawned the creature, read its live properties.
4. Saved, restarted the server, confirmed it reloaded identically.
5. Exercised three of the five F3-repaired patches at runtime.

## Result: the port

| Check | Result |
|---|---|
| Builds | Yes. Zero errors. `Structured customizations installed: 1 file(s).` |
| Spawns | Yes. `[add PlagueRat` -> `1 object generated in 0.00 seconds` |
| Correct identity | `a Clan Ribbon Plague Rat`, Body `0xD7`, Hue `1710` |
| Survives save/reload | Yes, both instances, all properties identical |
| Needs a migration JSON | No |
| Needs an `apply-patches.sh` change | No |

Live property read after the restart, both rats (`[2]` = two matching instances):

```
Serial : 0x00000051
Name : 'a Clan Ribbon Plague Rat' [2]
RangePerception : 16 [0x10] [2]
ActiveSpeed : 0.25 [2]
PassiveSpeed : 0.5 [2]
Hue : 1710 [0x6AE] [2]
Body : 0xD7 [2]
Serial : 0x0000005F
```

Both draft "fidelity traps" were wrong; the corrected versions with source citations are in
`notes/port-recipe.md`. Short form:

- **Range perception was backwards.** ServUO's constructor rewrites `10` to `16`
  (`OldRangePerception` -> `DefaultRangePerception`, `BaseCreature.cs:2353-2377`), so ServUO
  already runs at ModernUO's default. The draft's "RIGHT" example would have narrowed perception
  from 16 to 10 across 476 of ~493 creatures.
- **Speeds: ServUO ignores its own constructor arguments.** `SpeedInfo.UseNewSpeeds` is hardcoded
  `true`; speed is derived from Dex and recomputed on `SetDex`. Dropping the two arguments is
  right, but the resulting ModernUO value (Medium, 0.25/0.5) is not what ServUO runs (0.664/1.328
  for this creature). This needs a shard-wide decision — Q-008.

## Result: the five repaired patches

F3 left all five compiling-but-untested. Three are now exercised at runtime; two are not.

| Patch | Runtime status |
|---|---|
| `Bandage-pet-mimic-targeting.patch` | **VERIFIED working** |
| `BaseWeapon-talisman-durability.patch` | **VERIFIED working** |
| `CraftGumpItem-MakeX.patch` | **VERIFIED working, but with a cosmetic defect — see below** |
| `CraftGump-MakeXClear.patch` | Partially observed, not isolated. See below. |
| `AOS-pet-mimic-attribute-aggregation.patch` | **Not exercised.** Needs a mimic with real
  `AosAttributes` and a stat that reads through `AOS.GetValue`. Out of scope for one session. |

### Bandage a PetMimic — works

Used a clean bandage on a `PetMimic` at 40/100:

```
Your pet mimic absorbs the bandage, recovering 5 health. (45/100)
```

Tooltip afterwards: `A Pet Mimic / Blessed / Weight: 1 Stone / Health: 51 / 100`
(the extra points are `ApplyPendingRegen`, which `TryFeed` runs before healing).

+5 matches `clusterf.petMimic.bandageHeal: 5`. Without the patch this would have been
`Bandages can not be used on that.` (cliloc 500970). `PetMimic.TryFeed` is reachable.

### Talisman durability — works

A `PetMimic` was equipped (confirmed `Layer : Talisman`, `Parent : 0x00000050 'Ratcatcher'`) at
`CurrentHP : 100`. The character then fought spawned PlagueRats for several minutes. Afterwards:

```
Parent : 0x00000050 'Ratcatcher'
CurrentHP : 45 [0x2D]
```

100 -> 45 across combat, at `clusterf.petMimic.decayHPPerHit: 1` per hit. The talisman slot is
receiving `IWearableDurability.OnHit` from `BaseWeapon.AbsorbDamage`, which is exactly what the
patch adds and what `PetMimic.cs:376`'s comment already assumed.

### MAKE X — works, and the overlap question is answered

**No overlap.** The three controls render as a clean row: BACK button + label, MAKE X button +
label, MAKE NOW button + label. Nothing collides visually and nothing steals clicks — MAKE X was
clicked and responded.

Geometry, for the record:

| Control | Gump x | Extent |
|---|---|---|
| BACK button (art 4014) | 15 | ~15-44 |
| BACK label, `AddHtmlLocalized(50, 390, **150**, 18, 1044150)` | 50 | box 50-200 |
| MAKE X button (art 4005) | 140 | ~140-169 |
| MAKE X label, `AddLabel(175, 390, ...)` | 175 | ~175-220 |
| MAKE NOW button (art 4005) | 270 | ~270-299 |
| MAKE NOW label, `AddHtmlLocalized(305, 390, 150, 18, 1044151)` | 305 | box 305-455 |

The MAKE X button at 140 *does* sit inside the BACK label's declared 150-pixel HTML box
(50-200). It does not matter in practice: the localized "BACK" string is short and left-aligned,
and a background-less `AddHtmlLocalized` region paints nothing and takes no mouse input. Worth
knowing if anyone ever widens that label or gives it a background.

Functionally end-to-end:

- MAKE X opened `CraftCountGump` — "Make How Many?", with 5 / 10 / 20 / 50 / 100, a Custom field
  and CANCEL.
- Chose 5 scissors: iron went 200 -> 190 (5 x 2 ingots) and NOTICES read `You create the item.`
- Chose 50: iron kept dropping, 190 -> 98 over the run. The repeat loop works.

**Defect found: the MAKE X label is effectively invisible.** BACK and MAKE NOW render in normal
light text; MAKE X renders near-black on the dark gump and cannot be read.

Cause is a constant mix-up in the patch. `CraftGumpItem.cs` defines two different things:

```csharp
private const int LabelHue        = 0x480;   // :11  a UO hue, for AddLabel
private const int LabelColor      = 0x7FFF;  // :14  an RGB555 colour, for AddHtmlLocalized
private const int GreyLabelColor  = 0x3DEF;  // :17
```

The patch calls `builder.AddLabel(175, 390, LabelColor, "MAKE X")` (and `GreyLabelColor` in the
greyed-out branch). `AddLabel` takes a **hue**, not an HTML colour. `0x7FFF` is 32767, far outside
the client's hue table, so the text renders unhued/black. Upstream shows the correct pairing two
lines further down — `supportsEx ? LabelColor : RedLabelColor, supportsEx ? LabelHue : RedLabelHue`
(`:124-125`) — the API distinguishes them deliberately.

**Fix:** use `LabelHue` in the enabled branch. The greyed branch needs a grey *hue*;
`CraftGumpItem` does not define one, so pick a grey hue (`0x3B2` is the usual choice) rather than
reusing `GreyLabelColor`. Not applied here — it is a change to a patch, and P1's remit was to
exercise the patches, not revise them. One-line change, worth doing before anyone sees this gump.

### MAKE X clear — observed, not isolated

While a 50-item repeat was in flight (iron dropping steadily), the tinkering gump was reopened
and a single item clicked. Iron stopped dropping and stayed at 98 across the following 25 seconds,
where an uninterrupted repeat would have consumed roughly 30 more ingots. That is consistent with
`CraftGump-MakeXClear.patch` zeroing `RepeatCount`, but the manual craft itself did not visibly
consume ingots, so the click may simply have missed a gump that had been re-sent underneath it.
**Treat as not proven.** A clean re-test wants a long repeat and a confirmed single craft.

## Three obstacles worth writing down

Anyone standing up a local client against a throwaway build will hit all three.

### 1. The relay address

ModernUO's `ServerList` hands the client an address to reconnect to for the game server. With
`serverListing.address` set (the shard config has `192.168.1.58`) that value is used
**unconditionally**, including for loopback clients (`ServerList.cs:91-93`), and the port is
whatever port the client connected to. A container published only on `127.0.0.1` therefore
authenticates fine and then fails with `Connection lost: Connection Refused`.

Fix for a local run: set `serverListing.address` to `127.0.0.1` in the scratch Configuration copy,
and have the container listen on the same port it is published on (edit `listeners`), so the relay
port matches too.

### 2. New accounts cannot log in under SHA2 — a real ModernUO bug

`docker/uo/entrypoint.sh` forces `accountSecurity.encryptionAlgorithm=SHA2` on every start, for
ServUO bridging. Under SHA2, **a freshly created account can never authenticate.**

`Account.SetPassword` picks the phrase to hash from `_passwordAlgorithm` — the account's *existing*
algorithm — and only then stamps the new one:

```csharp
var phrase = _passwordAlgorithm is PasswordProtectionAlgorithm.SHA1 or PasswordProtectionAlgorithm.SHA2
    ? $"{_username}{plainPassword}"
    : plainPassword;

Password = AccountSecurity.CurrentPasswordProtection.EncryptPassword(phrase);
PasswordAlgorithm = AccountSecurity.CurrentAlgorithm;
```

For a brand-new account `_passwordAlgorithm` is the enum default `None`, so the stored hash is
`SHA512(password)` — but `PasswordAlgorithm` is then set to `SHA2`, and `CheckPassword` hashes
`SHA512(username + password)`. They never match.

Confirmed both ways: the stored hash for account `p1admin` was exactly
`SHA512("p1testpass")`, a packet capture proved the client transmitted `p1admin` / `p1testpass`
correctly, and login still failed. Rewriting the stored hash to `SHA512("p1adminp1testpass")` in
`Saves/Accounts/Accounts.bin` made login succeed immediately.

This affects the **live shard**: `accountHandler.enableAutoAccountCreation` is `True` and the
entrypoint forces SHA2, so any player creating a new account gets in once (auto-creation logs you
straight in) and is locked out on every later attempt. Existing accounts are unaffected — the bug
is only in the first `SetPassword` on a new account. Recorded as evidence on Q-007; this is Chase's call, not
mine, and it is not a migration issue.

### 3. Staff are invisible to creature AI

`BaseAI.AcquireFocusMob` only targets mobiles with `AccessLevel == AccessLevel.Player`
(`BaseAI.cs:450`), and staff characters are created `Blessed`. Forcing `Combatant` via
`[global set combatant ... ` does not stick — the AI clears it on its next think.

For the durability test the character had to be `[self set blessed false` **and**
`[self set accesslevel player`. Note that the second is one-way: `AccessLevel` is stored per
mobile and is not re-read from the account on login. The way back is to create a *second*
character on the same account — `CharacterCreation.cs:203` copies `args.Account.AccessLevel`, and
the account is still Owner. Do that rather than stranding yourself.

Also: a character logged out in the wild holds its slot for several minutes, so a second character
on the same account cannot log in immediately. Restarting the container releases it.

## Useful commands

`[global get ... where <Type>` is the single biggest time saver — it reads every instance without
requiring you to click a wandering creature, which otherwise eats most of the session:

```
[global get name rangeperception activespeed passivespeed currentspeed dex where PlagueRat
[global get parent currenthp layer where PetMimic
[global set currenthp 40 where PetMimic
[global bringtopack where TinkerTools
```

`[props <serial>` also works without a target if you already have the serial.

## Not verified

- `AOS-pet-mimic-attribute-aggregation.patch` at runtime.
- `CraftGump-MakeXClear.patch` in isolation.
- The second argument to `[SerializationGenerator(0, false)]`. The attribute is in the
  `ModernUO.Serialization` NuGet package, not the source tree; all 2921 in-tree usages pass
  `false`.
- Anything about `Serial` arithmetic, `[SerializableField]`, or the ModernUO string idioms —
  PlagueRat exercises none of them.
- The MAKE X label hue fix. Diagnosed, not applied.
