# P638: review of P626, Persuasion stage 1

Reviewed October 26, 2026. Code HEAD: `a3f017e279e29eed0ac12c506ef51e6310291583`. Notes HEAD before this review: `782363353dc7c3e394b61925f34878f7c672f6f5`. Read-only ModernUO HEAD: `d4531cd94b739613155225c234900de9f47d2c88`, matching the shard's pin.

This reviews the stage P626 actually built: identity, charity, and courier practice. The accepted direction is option B as recorded in `cc-P626-build-social-skill.md:3`: audited haggling, modest selling bonuses, standing rather than extra gold or Renown, and earned training. The matching design is `cc-P606-begging-skill-design.md`. Haggling, rumors, requisition terms, calm, client labels, and tutorial relocation are explicitly later stages, so their absence is not a finding against this slice. Chase's answers are assessed as recorded by the builder; the original conversation was not independently inspected.

I read `cc-P626-build-social-skill-codex-review.md` and `cc-P606-begging-skill-design-codex-review.md`. The earlier P626 review already covers stale menu eligibility and banking letters to stockpile assignments. Those findings are not repeated below.

Paths beginning `server/` refer to ShatteredLegacy. Paths beginning `U/` refer to `D:/UO/ModernUO-pinned/`. These are source review findings, supported by reading the implementation and parsing the shipped region and spawn data. They are not claims of reproduction on the running shard.

## Findings

### 1. Medium (P2): unnamed town subregions hide the parent town from courier work

**Location:** `server/customizations/ClusterFPersuasion.cs:392`, with consequences at lines 475-484 and 540 in the same file.

`TownOf` returns the name of the first `TownRegion` in the ancestry, even when that region has no name. Pinned `Region.GetRegion<T>()` returns that first match immediately (`U/Projects/Server/Regions/Region.cs:458`); it does not continue to a named ancestor. `Region.Name` is assigned directly from the constructor argument at line 161.

This occurs in supplied content. Luna has an unnamed `TownRegion` child covering x=986..1003, y=509..529 (`U/Distribution/Data/regions.json:3516`), inside the named Luna town. The bank spawner is at (989, 520, -50), with Banker and Minter entries (`U/Distribution/Data/Spawns/shared/malas/Vendors.json:237`). The location is inside both regions; the child wins. Consequently, those bankers have a null courier town. A novice asking there cannot get a local letter because the issuer town is null. Other banks omit them as destinations. A letter addressed to Luna also fails its recipient check while the banker remains in that subregion.

**Fix:** resolve a stable, named town through the ancestry, skipping unnamed town subregions. Use the same resolution for issuance, candidate selection, rotation, and delivery.

**Missing regression:** put a banker in an unnamed `TownRegion` child of named Luna and complete a real letter through it. The existing `Town` fixture creates only named, parentless regions (`server/tests/Skills/PersuasionVerification.cs:137`), so it cannot expose this case.

### 2. Medium (P2): the board selects banker subclasses that cannot accept its letters

**Location:** `server/customizations/ClusterFPersuasion.cs:493` and `:498`; `server/customizations/ClusterFExchangeLetter.cs:68`.

For non-novice jobs, selection accepts any `v is Banker`, then records `typeof(Banker)` instead of the actual candidate type. Delivery requires exact equality with `m.GetType().FullName`. A Minter or GypsyBanker therefore passes selection but fails delivery.

There is a concrete shipped route: `U/Distribution/Data/Spawns/shared/ilshenar/Vendors.json:481` supplies a GypsyBanker at (1405, 439, 2). That point is inside Alexandretta's Bowl (`U/Distribution/Data/regions.json:3029`, bounds x=1272..1439, y=352..591). `GypsyBanker` derives from `Banker` (`U/Projects/UOContent/Mobiles/Vendors/NPC/GypsyBanker.cs:7`). From a different Ilshenar town, such as Gargoyle City, the board can select that NPC and issue "a banker in Alexandretta's Bowl", but that very NPC cannot receive it. Without an exact Banker in the town, the assignment cannot be completed and keeps the ordinary one-letter gate occupied until the player deletes it or it expires.

**Fix:** make selection and delivery use one recipient contract. Either save the selected concrete type and compare it consistently, or deliberately accept Banker subclasses at delivery with a stable role identifier and suitable eligibility checks. Do not offer a destination whose selected NPC fails `IsRecipient`.

**Missing regression:** issue and deliver a letter where the destination town has only a GypsyBanker or Minter. Existing courier tests instantiate exact Bankers (`server/tests/Skills/PersuasionVerification.cs:370`), masking the mismatch.

### 3. Low (P3): restart forgets the destination used to enforce rotation

**Location:** `server/customizations/ClusterFPersuasion.cs:64`, `:443`, and `:463`.

The only previous-destination record is a static dictionary. Issuance writes it and destination selection reads it; there is no save/load registration or persistent field for it. The letter saves its destination, but a completed letter is deleted, so it cannot restore that history. Following a normal save and restart, the board may immediately assign the same destination again. This falls short of the design's persistent objective/contact behavior and its instruction to avoid immediate repeats (`cc-P606-begging-skill-design.md:157-159`).

This does not establish a replay of a consumed letter. It is a loss of rotation history, separate from the earlier stockpiling finding.

**Fix:** save the last issued destination on persistent character data, or another persistent courier record, and use it after load. Include the destination map if the record spans facets.

**Missing regression:** finish a delivery, save and reload the courier's state, and verify that the next assignment excludes the previous destination. The existing test checks rotation within one process only (`server/tests/Skills/PersuasionVerification.cs:403`).

### 4. Low (P3): pruning the charity ledger allows an old contact to teach again

**Location:** `server/customizations/ClusterFPersuasion.cs:262-268`, enforced by `:353`.

The design permits introductory training once per distinct successful contact until Base 20 (`cc-P606-begging-skill-design.md:140`). The implementation saves only 200 taught contacts and drops the rest. Below Base 20, after receiving aid from more than 200 distinct contacts, an evicted contact becomes eligible to teach again on a later UTC day. Failed gain rolls or locked skill still add contacts to this ledger, so retaining 200 contacts does not imply that the character has already reached 20. This also affects another low-skill character on the same account, since the ledger is shared.

The builder note discloses the 200-entry limit, but the design has no expiry for a contact's introductory practice credit. Actual availability of enough qualifying contacts in the current saved world is unverified; the eviction and renewed eligibility follow directly from `Save`, `Load`, and `day.Taught.Add(key)`.

**Fix:** retain durable credited-contact identities for the life of this introductory allowance. If a bounded representation is necessary, use one that cannot turn a previously credited contact into a fresh contact. Do not silently age practice credits out.

**Missing regression:** credit more than 200 distinct contacts while the character remains below 20, advance the UTC day, and verify that the earliest credited contact cannot teach again, including after save/load.

## Other acceptance coverage and limits

The new behavior is in `server/customizations/ClusterFPersuasion.cs` and `server/customizations/ClusterFExchangeLetter.cs`; its test file is `server/tests/Skills/PersuasionVerification.cs`. Supporting integration reviewed included `ClusterFSkillGain.cs`, the begging-marked FrenchBread wrapper, the hidden refusal achievement registration, pinned skill checks, item/mobile drop handling, account tags, and the region and spawn sources cited above.

The practice helper adds positive Value-minus-Base bonus to both gain-window edges and uses `CheckSkillWornBonusIncluded`. That matches the design and avoids applying the cap compensation twice. The helper routes through the existing gain pipeline. Letter deletion precedes practice, and the saved skill slot remains Begging. Account tags are serialized properties in pinned `Account.cs:76`, and `SetTag` marks the account dirty at line 684. I found no source basis for claiming that all charity allowances reset on restart.

However, P606's acceptance cases are not all demonstrated by this test file. Its player helper fixes Cap at 200 and removes stat/racial offsets, and its final-letter fact exercises Up and Locked only (`PersuasionVerification.cs:152-162`, `:439-453`). Add coverage for representative lower caps, Down lock, Base 199.9 with a positive skill bonus, and one logical SkillUsed event per consumed objective. Add actual serialization round trips for letter owner, recipient, map, difficulty and expiry, and for account-wide daily charity and taught-contact state. The current tests check in-memory fields and manually change the day tag; they do not prove those round trips. These are missing acceptance evidence, not additional proven runtime bugs.

The shipped Tokuno data also exposes a job-pool limitation to track when adding the promised local alternatives. At Base 10 the board switches to difficulty 35, requiring another town on the same facet. The supplied Tokuno TownRegion data has Zento as its named town (`U/Distribution/Data/regions.json:3681`), and its vendor data places the banker there (`U/Distribution/Data/Spawns/shared/tokuno/Vendors.json:646`). With that content alone, a Zento courier must leave the facet to continue. The mathematical tier-window test does not establish destination availability. P626 explicitly assigns local alternatives and broader upper work to stage 5, so this is recorded as remaining content coverage rather than another defect in an allegedly finished stage.

Unverified: current saved-world NPC placement and additions, actual player training pace, client menu and drag/drop appearance, and a real server save/load round trip. The reported P626 gated build and mutation results were read, not rerun. No tests were added or changed, and no build or container operation was needed for this docs-only review.

## Review checks

Read both work copies' AGENTS.md and the required direction/task documents. Checked the stop-request path between review steps. Ran the progress reporter with `--dry-run` against these work copies; it exited successfully but still rewrote `tools/progress.json` before checking the dry-run flag. Restored that generated file to its previously clean HEAD content. Both repositories pass `git diff --check`; this note is plain ASCII with no trailing whitespace and is below 5 MB. No code, `docs/`, accounts, saves, or service inventory was changed. No Haven connection, deployment, commit, merge, push, or branch switch was performed. Shell reads used Windows PowerShell 5.1. Only this review note is the deliverable.

P638 DONE
