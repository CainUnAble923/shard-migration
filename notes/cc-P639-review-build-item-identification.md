# P639: review of P627 item identification

Reviewed October 26, 2026, by the Golem's Codex lane. Documentation only. No code, configuration, saves, or services changed.

## Scope and evidence

Reviewed code HEAD `a3f017e` and notes HEAD `d1196d2`. Read both work copies' AGENTS.md, the direction decision and task list, and:

- `notes/cc-P627-build-item-identification.md`, including its remaining-stage drafts.
- `notes/cc-P627-build-item-identification-codex-review.md`.
- `notes/cc-P607-item-identification-design.md` and its Codex review.
- `server/customizations/ClusterFItemKnowledge.cs`.
- `server/patches/Item-property-list-policy.patch`, `LootPack-unidentified-magic.patch`, `ItemIdentification-item-knowledge.patch`, and `ArmsLore-item-knowledge.patch`.
- `server/tests/Items/ItemKnowledgeVerification.cs` and the patch registration in `docker/uo/apply-patches.sh`.

Traced the affected routes through pinned ModernUO at verified HEAD `d4531cd94b739613155225c234900de9f47d2c88`: `Projects/Server/Items/Item.cs`, `PropertyList/ObjectPropertyList.cs`, `Targeting/Target.cs`, `Serialization/GenericPersistence.cs`, and `Projects/UOContent/Skills/ItemIdentification.cs`, `Skills/ArmsLore.cs`, `Misc/LootPack.cs`, `Items/Weapons/BaseWeapon.cs`, and `Items/Skill Items/Tools/BaseRunicTool.cs`. Also read the shard's existing Appraisal and Arms Lore patches, `BaseRunicTool-no-random-self-repair.patch`, `ClusterFArmsLore.cs`, `Requisitions/RequisitionItems.cs`, and the relevant readers in `ArtificersImbueGump.cs`.

Chase's answers are recorded in P627's opening paragraph: option B, item-wide discoveries, Appraisal for magic, Arms Lore for resists, documented crafts, and existing information preserved. I found no separate answer transcript in the referenced design/review files, so that paragraph is the approval evidence used here.

This review treats P627 as the disabled first stage it actually builds. Jewelry, other reward paths, NPC prices/services, wands, legacy outputs, item gain, hazards, revision invalidation, adoption, and client checks are explicitly deferred in its notes. Their absence is not presented as a new P627 finding. The earlier review's public protection/restriction labels and missing test-shard activation guard are also excluded below.

## New findings

### 1. Medium (P2): completing the tracks bypasses the disclosure catalog

**Location:** `server/customizations/ClusterFItemKnowledge.cs:167`, with the early return at `:399` and the stock-builder fallback in `server/patches/Item-property-list-policy.patch:22`.

**What happens:** `IsConcealed` becomes false as soon as Magic is Values and Arms is Measured. `Render` then returns false, so the core seam invokes the unrestricted virtual property builder. Any line without a catalog owner, including arbitrary derived-item or `Item.ExtraProperties` text, becomes public at that point. It does not matter that no adapter has classified that line.

There is an existing concrete counterexample in the leak fact: `server/tests/Items/ItemKnowledgeVerification.cs:161` adds the unclassified cliloc 1060658 with `Hidden power` and value 42. The fact checks only the concealed state. If that same extra-property handler remains installed while both tracks complete, the fallback sends that line. The separate completion fact at `:213` does not install the handler and instead requires the whole stock tooltip.

**Design difference:** P607 at `:77` requires an explicit owner before a new property becomes visible, and at `:189` keeps unknown derived properties concealed until their adapter is reviewed. P627 describes its catalog as an allowlist, but the completion shortcut gives that protection an expiration condition. This is a disclosure-boundary defect even within stage 1, separate from the acknowledged non-tooltip leaks. It also undermines stage 2's instruction to leave unreviewed extra lines concealed.

**Fix:** continue rendering managed items through the catalog after the supported tracks complete. Release reviewed fields according to their owning track, and keep unclassified fields hidden until explicitly classified or exempted. Restore any approved name through that policy too. Do not use track completion as permission to run an unrestricted builder into the public list.

**Missing regression:** keep the leak fact's extra-property handler active through both discoveries and assert that its unclassified text/value stays absent from the real cached buffer. Check that reviewed magic and arms fields do appear. Add the test red first when implementing the fix.

### 2. Medium (P2): the difficulty reader misses a supported monster-loot enchantment

**Location:** `server/customizations/ClusterFItemKnowledge.cs:499` and `:501`.

**What happens:** difficulty takes both its count and strongest intensity from the imbuing/requisition catalog. That catalog does not contain Use Best Weapon Skill. Pinned `Items/Skill Items/Tools/BaseRunicTool.cs:384` can roll `AosWeaponAttribute.UseBestSkill` on a loot weapon, and P627 explicitly recognizes its tooltip property as Appraisal-owned at `ClusterFItemKnowledge.cs:265`. The shard's runic patch does not remove that roll.

For a normal longsword whose only enchantment is Use Best Weapon Skill, `RequisitionProperties.PropertyCount` delegates to the catalog at `RequisitionItems.cs:205`; `ImbueCatalogue.CountActiveProperties` at `ArtificersImbueGump.cs:799` visits only its own rows. Neither that count nor the intensity loop sees the enchantment. The implemented calculation therefore uses N=0 and I=0, returning the floor D=10. Applying the design's boolean intensity rule gives N=1, I=100, D=90. At skill 60, these produce a values success chance of 100% versus 0%, respectively. These numbers follow the source formulas; they are not a runtime sample or an estimate of drop frequency.

**Design difference:** P607 at `:133` counts distinct enchantments, including boolean ones, and at `:139` expressly says the existing catalogs are useful inputs rather than a universal magic detector. The issue is reader coverage, not the slayer balance concern already recorded by P627.

**Fix:** give the item-knowledge adapters complete readers for the enchantments they disclose, independently of which ones players may imbue. Include Use Best Weapon Skill as one boolean enchantment at full intensity. Audit the other supported weapon and armor properties against those readers before fixing the balance formula.

**Missing regression:** use a pure Use Best Weapon Skill loot weapon to pin its count, intensity, difficulty, and skill-window behavior. The current loot fact at `ItemKnowledgeVerification.cs:378` filters its samples through `PropertyCount > 0`, so it excludes this exact counterexample. Its formula fact at `:310` also checks only the range and downstream formulas, not a representative expected difficulty. Add the regression red first.

### 3. Low (P3): saving omits dead rows but never prunes the live registry

**Location:** `server/customizations/ClusterFItemKnowledge.cs:70`, particularly `:73` through `:89`.

**What happens:** serialization builds a temporary list containing only live items and writes that list. It never removes dead serials from the static `Rows` dictionary. No production delete hook or other removal path exists in this class. A concealed item that decays or is destroyed therefore leaves its row in memory across every save, until a restart. Continued loot generation can accumulate those rows throughout server uptime, and switching the policy still walks their serials at `:156`.

This is narrower than the already deferred serial-reuse/delete-hook work. P627 specifically claims deleted rows are dropped at save; only their serialized copies are dropped. P607 at `:183` separately requires pruning dead rows on save as well as deletion cleanup.

**Fix:** prune dead registry entries on the appropriate world thread at a safe save/lifecycle boundary, or add deletion cleanup plus a reconciliation pass. Avoid introducing dictionary mutation races with persistence serialization.

**Missing regression:** after deleting and saving an item, inspect the live registry before resetting it. The current persistence fact at `ItemKnowledgeVerification.cs:432` deletes an item, saves, clears all rows with `ResetForTests` at `:439`, and checks absence only after deserialization at `:446`. That proves filtering of the save payload but cannot prove live pruning. Add a red-first assertion for the live state when fixing it.

## Verification and limits

These are source-confirmed control-flow and reader-coverage findings in our implementation. No new tests were added or run. Lane tests are none. I did not rerun P627's reported build, create a shard, modify a save, or observe either client. Runtime reproduction, real save/load behavior, client refresh behavior, performance costs, and the actual loot difficulty distribution remain unverified here. The low-severity finding asserts retained dictionary entries, not a measured memory size or a demonstrated serial-reuse exploit.

The progress reporter ran with the work-copy path overrides and `--dry-run`. Its unconditional `tools/progress.json` write was intercepted with a process-local `Path.write_text` mock, and the suppressed write was observed. Its existing review reminders do not change these findings. No progress or decision files were changed.

No Haven connection, deployment, commit, merge, push, branch switch, or code change was made. The generated `server/uo/` tree was not used as source evidence.

Final checks passed: only this note is changed, the code work copy is clean, both Git whitespace checks passed, and the note has no em dashes or trailing whitespace and is below 5 MB. PowerShell verification used Windows PowerShell 5.1.

P639 DONE
