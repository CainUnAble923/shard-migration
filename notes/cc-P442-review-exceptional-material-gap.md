# P442: review of P228 exceptional material scaling

Reviewed 2026-10-22. Notes only. No code or tests changed.

Read `notes/cc-P228-exceptional-material-gap.md` first. No separate P228 Codex review was found beside it or elsewhere in tracked `notes/` files. The findings below do not repeat its recorded old-item durability limitation, historical bow bonuses, or deliberate extended-wood exclusion.

## Findings

1. **bug | `server/customizations/ClusterFExceptionalMaterial.cs:62`**: Material resists now depend on armor quality, but pinned `Projects/UOContent/Items/Armor/BaseArmor.cs:191` changes quality without calling the wearer's `UpdateResistances()`, so changing an equipped colored piece from regular to exceptional or back leaves cached player resists at the old values until another refresh; `ExceptionalMaterialVerification.cs:478` explicitly refreshes them and hides this case. Patch the quality setter to refresh equipped resists and add an uncapped test that primes the player's resistance cache, changes quality in both directions, and checks the player without a manual refresh.

2. **risk | `server/tests/Items/ExceptionalMaterialVerification.cs:105`**: X1 and X2 assign resource and quality directly, while X6's real runic armor crafts compare only rolled properties, so these assertions do not protect the selected ore, leather, or scale reaching the finished item's scaled reads, or the resulting current and maximum hit points. Add real crafting cases that assert the finished resource, material bonuses, and durability, including the secondary scale selection and an exceptional Dawnstone plate whose material durability rounds from 25 to 38 before the separate exceptional +20.

3. **risk | `server/tests/Items/ExceptionalMaterialVerification.cs:38`**: There is no pre-P228 serialized-item fixture or save/load assertion in this suite, so old-item compatibility and preservation of stored bow properties and durability are unverified by these tests. Load preserved exceptional ore armor, an ore weapon, and an OSI wood bow in a disposable test world, then save and reload them while checking quality, resource, stored durability, stored bow properties, and the new live material reads.

## Checks with no new finding

- No additional material missing from the scaling lookup was found. `ResourceInfo.cs` registers the current metal, leather, scale, and wood ranges, including Dawnstone, Burrowhide, and Rootwood; `ClusterFExceptionalMaterial.Attrs` looks up the item's resource rather than maintaining a second resource list, and `Scaled` copies every current `CraftAttributeInfo` property.
- No wrong-resource read was found in the armor and weapon hooks. Their `Resource` properties expose the same backing resource that the replaced expressions read; pinned `OnCraft` resolves the selected type or the recipe's first resource, and dragon armor uses the secondary scale collection. The crafting coverage concern is finding 2, not a demonstrated resource-selection bug.
- Normal and low quality items return the original attribute object. Positive values round half up, negative penalties stay unchanged, and runic ranges are copied unchanged. The bow snapshot follows base crafting, preserving exceptional damage and the separate extended-wood table.
- No save-format or inheritance change, or specific old-save load failure, was found in P228's helper and patches. Old-save loading remains unverified at runtime; the original note's known behavior differences are not new findings here.

## Evidence and verification limits

Reviewed canonical files:

- `server/customizations/ClusterFExceptionalMaterial.cs`, `ResourceInfo.cs`, and supporting `ClusterFWoodBonuses.cs`.
- `server/patches/BaseArmor-exceptional-material.patch`, `BaseWeapon-exceptional-material.patch`, and `BaseRanged-exceptional-wood.patch`, plus the existing wood hooks and crafting resource flow.
- `server/tests/Items/ExceptionalMaterialVerification.cs`, `ExtendedWoodBonusesVerification.cs`, and the starter-resource material assertions in `StarterResourcesVerification.cs`.
- `docker/uo/apply-patches.sh:779`, `CHANGELOG.md:274`, and `VERSION`.

Verified the read-only `D:/UO/ModernUO-pinned` checkout is at `d4531cd94b739613155225c234900de9f47d2c88`. Read its armor, weapon, and ranged base classes, `Engines/Craft/Core/Enhance.cs`, relevant `CraftItem.cs` and `DefBlacksmithy.cs` resource selection, and the material luck consumers in `Misc/AOS.cs`. Paths in this paragraph are relative to `Projects/UOContent/`.

Finding 1 follows from source: `Projects/Server/Mobiles/Mobile.cs:3109` invalidates the resistance cache, and `:3144` reads that cache. Armor quality only unscales durability, changes the field, marks dirty, and rescales durability; those paths invalidate item properties, not the mobile resistance cache. `Projects/Server/Serialization/ISerializableExtensions.cs:25` makes `MarkDirty` a no-op. Runtime reproduction and client behavior are unverified in this review.

No tests were added or run, and no build was performed, as this task requests review notes only and specifies no lane tests. P228's red and green results remain historical evidence from its implementation note.

Ran `tools/progress.py --dry-run` successfully with both work-copy paths set, under Windows PowerShell 5.1. The reporter writes `tools/progress.json` even in dry-run mode; restored that file byte for byte to preserve this task's notes-only scope. No Haven connection, deployment, commit, merge, push, or branch switch was made.

P442 DONE
