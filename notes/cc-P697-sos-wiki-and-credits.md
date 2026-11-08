# P697: Sosaria wiki pages and credits for S16

October 27, 2026. Draft text only, prepared in the Verite-tower work copies.

## Deliverables

- [World map](wiki-drafts/world-map.md): the planned Trammel and Felucca geography, regional landmarks, changed New Haven and Rootdeep directions, travel limits, and planned surface and dungeon closures.
- [New towns and keeps](wiki-drafts/towns-new.md): short entries for the new towns and named settlements, rebuilt Haven, and fort landmarks. References distinguish mapped landmarks from verified services. Quest hooks are explicitly proposals.
- [Credit text](wiki-drafts/credits-sosaria.md): copy for in-game credits, the package README, and wiki, plus S16 handoff text for the player changelog, in-game patch notes, converted data headers, and vendor SOURCE.txt.

These are drafts for the new world, not a claim that the swap has shipped. No code, package files, source data, published wiki, or migration docs/ files were changed.

## Evidence and editorial choices

Read both work-copy AGENTS.md files, the migration direction decision and task list, and the requested sources:

- [Author-spots reference](sos-map-author-spots.md).
- [P672 quest seeds](cc-P672-sos-quest-seeds.md).
- [P673 swap plan](cc-P673-sos-swap-plan.md), including its credit section and S14, S16, S18, and S19 boundaries.
- [Author-data SOURCE.txt](sos-author-data/SOURCE.txt).

Also consulted [P669's assessment](cc-P669-sos-trammel-assessment.md) for the map-change descriptions, the raw [location list](sos-author-data/locations-trammel.xml), and the raw [regions](sos-author-data/Regions.xml). Parsed the XML to inspect the Trammel town names and additional named town regions. Existing wiki dungeon wording was read for context, not treated as evidence that the new map is live.

SOURCE.txt still records the October 12 added-facet proposal. P673 records Chase's later October 26 decision to replace both Trammel and Felucca geography. The drafts follow that replacement decision and explain the older source note without rewriting it. P673's later stock-art assessment is kept separate from the optional redrawn-art package.

The author's Trammel regions supply additional settlement names without stories. They receive modest location entries, not invented factions or service rosters. The separate Sosaria region set is excluded because the author-spots reference warns that it may belong to another project. Fortress Calcifina is identified as a custom dungeon rather than a town. The fort list also includes the author's Yew Fort of the Damned landmark without asserting that it is open.

Credit names Zigholtul and Siege of Sosaria Trammel Map 3.0. Map names are attributed to him; added shard stories and characters are identified as ours. The recorded reuse invitation is not relabeled as a named license. Credit snippets use release wording inside a clearly marked future-release handoff. The wiki overview itself uses planned wording.

## S16 handoff

Place the credit snippets when the swap ships. The package README destination is player-package/payload/README.txt under "What is in here." Keep the map line beside, but distinct from, the optional redrawn-art credit. The vendor SOURCE.txt needs the actual terms-check date and the changes that really ship. No terms-check date is invented here.

S16 also owns the changelog, in-game patch notes, converted region and decoration headers, and wiki publication. The fidelity-register row remains for the overseer in migration docs/fidelity-principle.md. This task supplies credit copy and records that placement work; it does not make those release changes.

Older wiki drafts such as dungeons.md and the Haven guides describe the previous map's ruined-bank route. This task leaves them untouched. At publication, reconcile their directions with the verified cellar-hatch placement and the final New Haven route. The new pages explicitly identify the changed route and avoid linking players to obsolete entrance directions.

Before publication, reconcile the drafts against the implemented town services, moongate list, closure boundaries, opened dungeons, and swap play-through. P673 still presents choices about Blackthorn and closures, so the copy identifies them as planned or proposed rather than independently approving them. P672's NPCs and facet routes remain proposals.

## Verification and limits

All coordinate triples and region ranges in towns-new.md matched the author-spots reference. The raw XML corroborates the town names, mapped landmarks, and additional Trammel town-region names used for those entries. Local Markdown link targets resolve. Document review found no em dashes or trailing whitespace. Each new file is below 5 MB.

Unverified: actual map geometry and walkability, exact entrances and safe landing tiles, active services and guards, runtime facet rules and travel permissions, closure behavior, completed swap tasks, live deployment status, and current upstream reuse terms. P697 did not revisit the author's web page. Its URL, version dates, and quotation are copied from the supplied local source record. No new art is needed for these prose drafts.

Lane tests are none. No tests or gates were added, and no build or runtime tests were run for this prose-only change. Document checks were run from Windows PowerShell 5.1.26100.9711. Both work copies were clean at the start. Final changes are confined to the deliverables listed above and this note; the code work copy remains clean.

Ran python tools/progress.py --dry-run with SL_SHARD and SL_MIGRATE pointing at these work copies; exit 0. The tool's build() writes tools/progress.json before checking the dry-run flag, so its original bytes were preserved and restored with byte equality confirmed. No generated progress change remains.

No Haven connection, deployment, commit, merge, push, or branch switch. Stop-request checks between steps found no P697 stop request.

P697 DONE
