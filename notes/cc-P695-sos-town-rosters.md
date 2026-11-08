# P695: people for the SoS towns and keeps

October 27, 2026. Draft rosters for P682, the S10 placement work. Data and notes only.

Place names and locations are credited to **Zigholtul**, creator of Siege of Sosaria Trammel Map 3.0. The author supplied names and map data, not these inhabitants or their stories. P672 supplies its draft cast and hooks. All other new people, civic roles and alignments here are Shattered Legacy proposals. Elara Voss is an existing shard NPC.

## Deliverables and scope

[rosters.json](cc-P695-tools/rosters.json) contains 52 roster entries: 34 new settlement or inhabited-landmark proposals and 18 stock settlement service reconciliations. Its 84 named entries each have a one-line character and occupy an explicit counted slot. The per-place lists below are the coverage list for those counts. The JSON also preserves every matched author go-menu point, the original Trammel region rectangles, source line references, proposed staffing totals, and all 16 selected P672 dungeon handoffs.

The six priority new towns are Valunstead, Hammerhill, Kameron Kove, Elmhaven, Kettleburg and Fort Yondall. Each has a proposed bank, healer, Blacksmith and Provisioner. Elandrim Nur Shaz, Seraphim Peak, Skaddria Naddheim and Viligant Valley receive the same service floor, conditional on a building survey. Sea Market and the proposed unguarded Plunderers Peak market also have that floor. This is a staffing draft, not approval of their alignment, architecture, guards or travel routes.

Rebuilt stock towns are included so S9 and S10 have one service handoff. Their numbers are minimum targets to reconcile against retained people, not replacement populations or instructions to add another set. Jhelom, Papua and Serpent's Hold had no rebuilt go-menu spots in P669's town summary; they are retained comparison cases. Heartwood is an existing enclave and also stays a retention case. Existing specialty vendors, quests, named staff and valid spawners remain S9's responsibility.

## How P682 should use the data

1. Survey each settlement's actual buildings and public paths. Choose counters from forge, anvil, loom, oven and other trade fittings. The station labels describe what to look for; no interior has been verified here. A landmark coordinate, region go point or bounding-box midpoint is never an approved spawn tile. The JSON stores exclusive rectangle edges and keeps the actual rectangle list for irregular sites.
2. Work independently on Trammel and Felucca. Counts mean concurrent people per settlement per facet. Mirrored cast names do not share serials, quest progress, crime records or travel permissions. S3 and S13 own each facet's law and jurisdiction. New regions and routes must be qualified before publishing service access.
3. Reconcile S7 and S9 first. Fill only service shortfalls, use owned stable placement slots, and keep service NPCs within their buildings. Do not place a second Elsie Crow or a second Elara Voss. Do not rename an existing authored stock NPC to make room for a proposed name.
4. Count each person once. Vendor, bank, healer, guard, resident and hostile slots are separate categories. A named vendor already occupies its vendor slot. A named healer already occupies its healer slot. Guards do not include hired enemies or rescued soldiers. A JSON population total is a sum of proposed slots, not a measured spawn density.
5. Place safe service shells only where the phase and survey allow. A renamed service NPC does not implement a quest. Non-vendor residents and quest actors with a null type require later actor implementation. Exact dialogue, rewards, persistence and objectives are outside this task. Keep notice boards for unopened content inactive or clearly future work.
6. Reconcile the draft guard headcounts with P608 before implementation. They allocate staffing, not a new law mode. Its physical guards are not implemented in the source inspected here. Keep existing lawful enforcement until a jurisdiction qualifies. Never use WarriorGuard or ArcherGuard as decorative townsfolk, a dungeon enemy, or a paid guard. Friendly fort sentries do not authorize guard zones over quest fights. A safe outer shelter and a hostile yard require separate geometry and law; otherwise hold the placement.
7. S14 fences and S18 dungeon seals take priority. Glimmerwood and Echoback actors wait for their applicable S19 access work. Public notices can live in an open town without granting entry. Extra author moongates remain decor unless the travel work enables them. No candidate facet route, loop reward, new companion, evo stage or special crafting material is granted by this roster.

Bank and healer yes/no values below describe planned local services. No means no local slot, not a verified route to another service. Keeps, watchposts, ruins and hostile encounter sites are not treated as full civilian towns for S10's bank-and-healer requirement. Standard Healer retains its criminal and murderer refusal rules; adding it does not promise resurrection for every visitor. No extra EvilHealer is proposed without a separate service-policy review.

## New settlements and inhabited landmarks

### 01. Valunstead

**Role:** Walled northern market and winter relief depot, with a keep that protects deliveries.

**Source anchor:** Trammel / Towns / Valunstead / Bank at (484, 434, 15); Trammel region Valunstead, x [201, 669), y [149, 520), TownRegion; Regions.xml:1484.

**Vendors:** Provisioner x2, Blacksmith x1, Tailor x1, Carpenter x1, Baker x1, InnKeeper x1, Alchemist x1, Bowyer x1, AnimalTrainer x1. **Bank:** Yes, Banker x2. **Healer:** Yes, Healer x2.

**Guards:** 8 proposed slots; friendly garrison; jurisdiction to be reviewed by S3/S13. **Other residents:** relief clerk x1, household workers x3.

**Named people:**

- **Ada Fenwick**, League relief clerk: She checks every delivery signature before calling a household supplied. Slot: `resident.relief clerk.1`. Origin: P672-01.
- **Bram Tully**, smith: He repairs cart fittings before polishing a soldier's sword. Slot: `vendor.Blacksmith.1`. Origin: P695 proposal.
- **Mabel Quinn**, banker: She remembers depositors by the work they do. Slot: `bank.1`. Origin: P695 proposal.

**P672 ties:**

- **P672-01**, Valunstead: The Second Delivery. Giver: Ada Fenwick. The Second Delivery begins at the storehouse. Only characters past Chapter 1 receive the optional exchange about remembered returns.

**Placement and phase:** S10. Find the storehouse near the bank, then distribute shops inside the walls. Reserve a public path past the moat and keep; the moongate is outside the region search box.

### 02. Hammerhill

**Role:** A working trade town where pump repairs and clean water matter as much as metalwork.

**Source anchor:** Trammel / Towns / Hammerhill / Bank at (1530, 994, 5); Trammel region Hammerhill, x [1481, 1622), y [959, 1068), TownRegion; Regions.xml:1178.

**Vendors:** Blacksmith x2, Provisioner x1, Tinker x1, Alchemist x1, Tailor x1, InnKeeper x1, Baker x1. **Bank:** Yes, Banker x1. **Healer:** Yes, Healer x1.

**Guards:** 6 proposed slots; friendly garrison; jurisdiction to be reviewed by S3/S13. **Other residents:** drain tender x1, cleanup crew x2.

**Named people:**

- **Elsie Crow**, drain tender: She can tell which pump failed by the sound at the street grate. Slot: `resident.drain tender.1`. Origin: P672-26.
- **Walter Kells**, tinker: He labels every replacement part so a novice can fit it. Slot: `vendor.Tinker.1`. Origin: P695 proposal.
- **Ruth Larkin**, healer: She keeps wash water and drinking water on separate shelves. Slot: `healer.1`. Origin: P695 proposal.

**P672 ties:**

- **P672-26**, Hammerhill Sewers: What the Water Carries. Giver: Elsie Crow. What the Water Carries starts above the sewer entrance. Keep civic cleanup progression separate from League repair delivery.

**Placement and phase:** S10. Use the author bank as a search anchor. Put Elsie and her crew on the surface, never at the underground sewer level or the moongate's negative Z.

### 03. Kameron Kove

**Role:** A coastal outfitting town supplying sailors, fishers and overland travelers.

**Source anchor:** Trammel / Towns / Kameron Kove / Bank at (1297, 2470, 0); Trammel region Kameron Kove, x [1200, 1341), y [2391, 2558), TownRegion; Regions.xml:1234.

**Vendors:** Provisioner x1, Blacksmith x1, Shipwright x1, Fisherman x1, Carpenter x1, Tailor x1, InnKeeper x1, Alchemist x1. **Bank:** Yes, Banker x1. **Healer:** Yes, Healer x1.

**Guards:** 6 proposed slots; friendly garrison; jurisdiction to be reviewed by S3/S13. **Other residents:** dock clerk x1, dockhands x2.

**Named people:**

- **Lena Brackett**, dock clerk: She records cargo before asking where its captain has been. Slot: `resident.dock clerk.1`. Origin: P695 proposal.
- **Owen Bale**, shipwright: He trusts a repaired hull more than a painted promise. Slot: `vendor.Shipwright.1`. Origin: P695 proposal.
- **Hazel Finch**, innkeeper: She always keeps a dry blanket behind the counter. Slot: `vendor.InnKeeper.1`. Origin: P695 proposal.

**P672 ties:**

- **P672-12**, Ivanguard Manor: The Guest Who Was Never Paid. Notice: Lena Brackett. Post the contract-recovery notice for Lysa Trent at Ivanguard Manor; Lysa remains there.
- **P672-11**, Camp Ironfang: Leave the Cages Open. Notice: Lena Brackett. Post June Mercer's animal rescue notice; June remains at Camp Ironfang.

**Placement and phase:** S10. Survey the actual shore for the dock and shipwright. The moongate lies outside the town region search box and is decor until S4 travel policy enables it.

### 04. Elmhaven

**Role:** A southern woodland market supplying foresters and relief crews.

**Source anchor:** Trammel region Elmhaven, x [1891, 2049), y [3135, 3263), TownRegion; Regions.xml:1168.

**Vendors:** Provisioner x1, Blacksmith x1, Carpenter x1, Bowyer x1, Tailor x1, Farmer x1, InnKeeper x1, Alchemist x1. **Bank:** Yes, Banker x1. **Healer:** Yes, Healer x1.

**Guards:** 6 proposed slots; friendly garrison; jurisdiction to be reviewed by S3/S13. **Other residents:** grove liaison x1, woodland households x2.

**Named people:**

- **Etta Marsh**, grove liaison: She copies survey tags onto paper so nobody needs to strip a living tree. Slot: `resident.grove liaison.1`. Origin: P695 proposal.
- **Caleb Winn**, carpenter: He makes braces sturdy enough to lend twice. Slot: `vendor.Carpenter.1`. Origin: P695 proposal.
- **Nora Hale**, banker: She keeps the pay packets of absent crews sealed. Slot: `bank.1`. Origin: P695 proposal.

**P672 ties:**

- **P672-14**, Glimmerwood: What the Grove Remembers. Notice: Etta Marsh. Post Mara Wren's grove notice here while Glimmerwood is fenced; no grove access or Ter Mur permission is granted.
- **P672-20**, Black Widow Pit: The Silk Account. Notice: Etta Marsh. Post Delia Moss's rescue request only when S18 opens Black Widow Pit.

**Placement and phase:** S10. Region-only location. Survey buildings before choosing counters. Keep all services outside S14 Glimmerwood fences; a notice may advertise future work without an active objective.

### 05. Kettleburg

**Role:** A western provision market and repair stop for long journeys south.

**Source anchor:** Trammel region Kettleburg, x [427, 733), y [2316, 2618), TownRegion; Regions.xml:1240.

**Vendors:** Provisioner x1, Blacksmith x1, Cook x1, Farmer x1, Tailor x1, Tinker x1, InnKeeper x1, AnimalTrainer x1. **Bank:** Yes, Banker x1. **Healer:** Yes, Healer x1.

**Guards:** 6 proposed slots; friendly garrison; jurisdiction to be reviewed by S3/S13. **Other residents:** trail clerk x1, carters x2.

**Named people:**

- **Doris Field**, trail clerk: She writes the return route before the departure time. Slot: `resident.trail clerk.1`. Origin: P695 proposal.
- **Samuel Cobb**, cook: He stretches a kettle of stew without shorting the last traveler. Slot: `vendor.Cook.1`. Origin: P695 proposal.
- **Martha Reed**, animal trainer: She checks a pack animal's hooves before weighing its load. Slot: `vendor.AnimalTrainer.1`. Origin: P695 proposal.

**P672 ties:**

- **P672-21**, Bleak Wind Tunnels: A Lamp for the Return. Notice: Doris Field. Record interest in Hollis Beck's return-lamp expedition; activate only after S18 opens Bleak Wind Tunnels.

**Placement and phase:** S10. Use the author's Kettleburg go point only to begin the survey. Keep its service circuit distinct from nearby Skara Brae.

### 06. Fort Yondall

**Role:** A small northeastern resupply post with civilian services for its garrison and passing expeditions.

**Source anchor:** Trammel region Fort Yondall, x [3366, 3413), y [308, 406), TownRegion; Regions.xml:1172.

**Vendors:** Provisioner x1, Blacksmith x1, Bowyer x1, Cook x1. **Bank:** Yes, Banker x1. **Healer:** Yes, Healer x1.

**Guards:** 4 proposed slots; friendly fort-town; public services required, jurisdiction to be reviewed by S3/S13. **Other residents:** expedition clerk x1, porters x1.

**Named people:**

- **Edith Rowe**, expedition clerk: She will not sign a departure sheet without a named return contact. Slot: `resident.expedition clerk.1`. Origin: P695 proposal.
- **Gordon Ash**, quartermaster: He measures every ration against the days of the return march. Slot: `vendor.Provisioner.1`. Origin: P695 proposal.
- **Celia Hart**, healer: She asks the whole patrol about an injury before treating its captain. Slot: `healer.1`. Origin: P695 proposal.

**P672 ties:**

- **P672-23**, Fortress Calcifina: An Answer in Stone. Notice: Edith Rowe. Collect inquiries for Arda Quill's Calcifina expedition. Arda remains its dungeon actor and no Ter Mur route opens here.

**Placement and phase:** S10. Use the separate author rectangles, not the full bounding box. Fit bank and healer into a public service room rather than enlarging the fort.

### 07. Elandrim Nur Shaz

**Role:** A compact scholarly retreat and supply stop in Yew forest, proposed without assigning a race or an author history.

**Source anchor:** Trammel region Elandrim Nur Shaz, x [860, 920), y [987, 1052), TownRegion; Regions.xml:1164.

**Vendors:** Provisioner x1, Blacksmith x1, Scribe x1, Alchemist x1. **Bank:** Yes, Banker x1. **Healer:** Yes, Healer x1.

**Guards:** 2 proposed slots; friendly garrison; jurisdiction to be reviewed by S3/S13. **Other residents:** archive attendant x1.

**Named people:**

- **Miriam Clay**, archive attendant: She labels uncertain translations as uncertain. Slot: `resident.archive attendant.1`. Origin: P695 proposal.
- **Felix Shaw**, scribe: He leaves room in the margin for the next witness. Slot: `vendor.Scribe.1`. Origin: P695 proposal.

**P672 ties:**

- **P672-13**, Mistveil Ruins: The Survey in the Fog. Notice: Miriam Clay. Hold Brin Alder's survey notice; the actual giver remains at Mistveil Ruins.

**Placement and phase:** S10 after building survey. Region-only site immediately north of Whitestone's area. Verify distinct buildings, height and access before staffing; do not merge the two names or infer elven inhabitants from the name.

### 08. Seraphim Peak

**Role:** A proposed highland shelter for overland survey crews and travelers.

**Source anchor:** Trammel region Seraphim Peak, x [4593, 4804), y [1699, 1810), TownRegion; Regions.xml:1401.

**Vendors:** Provisioner x1, Blacksmith x1, Mapmaker x1, InnKeeper x1. **Bank:** Yes, Banker x1. **Healer:** Yes, Healer x1.

**Guards:** 4 proposed slots; friendly garrison; jurisdiction to be reviewed by S3/S13. **Other residents:** route recorder x1.

**Named people:**

- **Harriet Vale**, route recorder: She dates every correction to the mountain chart. Slot: `resident.route recorder.1`. Origin: P695 proposal.
- **Peter Hall**, innkeeper: He holds a room for the last person on the trail list. Slot: `vendor.InnKeeper.1`. Origin: P695 proposal.

**P672 ties:**

No assigned P672 seed. Do not invent a numbered quest or give a nearby dungeon's actor a second home.

**Placement and phase:** S10 after building survey. Region-only site. Its proposed friendly alignment and public counters require inspection of the individual rectangles and actual buildings.

### 09. Skaddria Naddheim

**Role:** A proposed southern craft enclave trading repairs, cloth and ordinary supplies.

**Source anchor:** Trammel region Skaddria Naddheim, x [1442, 1582), y [2926, 3037), TownRegion; Regions.xml:1425.

**Vendors:** Provisioner x1, Blacksmith x1, Tailor x1, Carpenter x1. **Bank:** Yes, Banker x1. **Healer:** Yes, Healer x1.

**Guards:** 4 proposed slots; friendly garrison; jurisdiction to be reviewed by S3/S13. **Other residents:** work steward x1.

**Named people:**

- **Agnes Bell**, work steward: She posts the agreed wage where every worker can read it. Slot: `resident.work steward.1`. Origin: P695 proposal.
- **Martin Pike**, tailor: He keeps the owner's name sewn inside every repair. Slot: `vendor.Tailor.1`. Origin: P695 proposal.

**P672 ties:**

- **P672-12**, Ivanguard Manor: The Guest Who Was Never Paid. Notice: Agnes Bell. Receive inquiries about Lysa Trent's unpaid household; keep the manor quest and rescued guard there.

**Placement and phase:** S10 after building survey. Preserve the author's spelling. Inspect the site rather than treating the name as a race, faction or a story clue.

### 10. Viligant Valley

**Role:** A proposed eastern valley resupply community for carters and prospectors.

**Source anchor:** Trammel region Viligant Valley, x [4835, 5018), y [1910, 2012), TownRegion; Regions.xml:1520.

**Vendors:** Provisioner x1, Blacksmith x1, Tinker x1, Farmer x1. **Bank:** Yes, Banker x1. **Healer:** Yes, Healer x1.

**Guards:** 4 proposed slots; friendly garrison; jurisdiction to be reviewed by S3/S13. **Other residents:** caravan recorder x1.

**Named people:**

- **Violet Shaw**, caravan recorder: She writes down who is missing before totaling a convoy's losses. Slot: `resident.caravan recorder.1`. Origin: P695 proposal.
- **Alfred Moss**, tinker: He would rather mend a dependable tool than sell a fragile novelty. Slot: `vendor.Tinker.1`. Origin: P695 proposal.

**P672 ties:**

No assigned P672 seed. Do not invent a numbered quest or give a nearby dungeon's actor a second home.

**Placement and phase:** S10 after building survey. Keep the author's spelling Viligant. Region-only bounds do not prove the buildings, road or safe approach.

### 11. Plunderers Peak

**Role:** A proposed rough trading refuge, not a source of legal immunity or a second Buccaneer's Den quest system.

**Source anchor:** Trammel region Plunderers Peak, x [3939, 4074), y [1544, 1710), TownRegion; Regions.xml:1349.

**Vendors:** Provisioner x1, Blacksmith x1, InnKeeper x1. **Bank:** Yes, Banker x1. **Healer:** Yes, Healer x1.

**Guards:** 0 proposed slots; proposed unguarded market; no law guards, subject to S3/S13 review. **Other residents:** cargo broker x1, sailors x2.

**Named people:**

- **Greta Cole**, cargo broker: She insists every disputed crate still has a living owner. Slot: `resident.cargo broker.1`. Origin: P695 proposal.
- **Edwin Rusk**, banker: He counts the deposit without promising protection outside the door. Slot: `bank.1`. Origin: P695 proposal.

**P672 ties:**

No assigned P672 seed. Do not invent a numbered quest or give a nearby dungeon's actor a second home.

**Placement and phase:** S10 after building and law review. Author TownRegion does not establish narrative alignment. Banking and healer access require a neutral public approach; do not silently enable author guard law.

### 12. Red Baron Stronghold

**Role:** A proposed armed toll stronghold, held out of civilian town provisioning.

**Source anchor:** Trammel region Red Baron Stronghold, x [4067, 4174), y [1173, 1283), TownRegion; Regions.xml:1361.

**Vendors:** None. **Bank:** No. **Healer:** No.

**Guards:** 0 proposed slots; no public law guards; hostile sentries are encounter actors. **Other residents:** captive tally clerk x1.

**Encounter occupants:** commander x1, hired sentries x4. Deferred combat actors with no selected concrete type.

**Named people:**

- **Roland Voss**, proposed commander: He calls every toll voluntary while keeping the gate shut. Slot: `enemy.commander.1`. Origin: P695 proposal.
- **Penny Dorr**, captive tally clerk: She keeps a second list of the people allowed to leave. Slot: `resident.captive tally clerk.1`. Origin: P695 proposal.

**P672 ties:**

No assigned P672 seed. Do not invent a numbered quest or give a nearby dungeon's actor a second home.

**Placement and phase:** later encounter spec. Region-only and alignment unverified. Do not activate enemies or place a bank inside the stronghold on the strength of its name.

### 13. Sea Market

**Role:** A neutral dock market for ordinary boat provisions, charts and fishing supplies.

**Source anchor:** Trammel region Sea Market, x [4529, 4574), y [2296, 2408), TownRegion; Regions.xml:1397.

**Vendors:** Provisioner x1, Blacksmith x1, Fisherman x1, Shipwright x1, Mapmaker x1, InnKeeper x1. **Bank:** Yes, Banker x1. **Healer:** Yes, Healer x1.

**Guards:** 2 proposed slots; friendly garrison; jurisdiction to be reviewed by S3/S13. **Other residents:** harbor clerk x1, dockhands x2.

**Named people:**

- **Clara Wynn**, harbor clerk: She records a passenger's destination in their own words. Slot: `resident.harbor clerk.1`. Origin: P695 proposal.
- **Hugh Porter**, fisherman: He sells a sound line before boasting about a catch. Slot: `vendor.Fisherman.1`. Origin: P695 proposal.

**P672 ties:**

- **P672-16**, Skypoint Islands: The Ship That Cannot Leave. Notice: Clara Wynn. Refer sailors to Anwen Dale's Skypoint expedition after its landing is qualified; no public Ilshenar passage starts here.

**Placement and phase:** S10 after S9 reconciliation. Use the author go point as a dock landmark, not an NPC tile. S9 must reconcile any retained Sea Market special NPCs; do not add galleons, cannon services or special fish turn-ins.

### 14. Fort Whitestone

**Role:** A relief post for injured scouts and overdue patrols.

**Source anchor:** Trammel / Areas of Interest / Yew Forest / Fort Whitestone at (890, 1055, 32).

**Vendors:** Provisioner x1, Blacksmith x1, Cook x1. **Bank:** No. **Healer:** Yes, Healer x1.

**Guards:** 4 proposed slots; friendly garrison staffing only; S3/S13 must approve jurisdiction. **Other residents:** recovering scouts x2.

**Named people:**

- **Hester Vale**, quartermaster: She lays one more place at supper than the fort can account for. Slot: `vendor.Provisioner.1`. Origin: P672-02.
- **Lydia Marsh**, healer: She treats a tired scout before asking for the patrol report. Slot: `healer.1`. Origin: P695 proposal.

**P672 ties:**

- **P672-02**, Fort Whitestone: A Place at the Table. Giver: Hester Vale. A Place at the Table recovers the patrol roll and the surviving scout. Preserve the same scene for solo players.

**Placement and phase:** S10. Use 890,1055,32 as an exterior survey anchor; check upper floors and public access. Keep relief services available before and after the rescue.

### 15. Fort Viridian

**Role:** A forest boundary and trail survey post.

**Source anchor:** Trammel / Areas of Interest / Yew Forest / Fort Viridian at (1015, 1003, 0).

**Vendors:** Provisioner x1, Bowyer x1, Carpenter x1. **Bank:** No. **Healer:** Yes, Healer x1.

**Guards:** 4 proposed slots; friendly garrison staffing only; S3/S13 must approve jurisdiction. **Other residents:** forester x1, survey crew x2.

**Named people:**

- **Nessa Holt**, forester: She checks a boundary mark against the living tree before trusting a seal. Slot: `resident.forester.1`. Origin: P672-04.
- **Francis Dell**, bowyer: He keeps old bows serviceable for the next trail watch. Slot: `vendor.Bowyer.1`. Origin: P695 proposal.

**P672 ties:**

- **P672-04**, Fort Viridian: The Boundary Trees. Giver: Nessa Holt. The Boundary Trees identifies forged marks. Nessa is a local forester, not a copy of Cedric Rowanwood or a new guildmaster.

**Placement and phase:** S10. Place the field desk within the fort and the survey crew outside its narrow service circuit. Do not extend guard coverage over forged-mark objectives.

### 16. Khalahandra Keep

**Role:** An oath-bound garrison whose supply route has been exploited.

**Source anchor:** Trammel / Areas of Interest / Khalahandra Keep / Entrance at (2505, 1707, 50); Trammel region Khalahandra Keep, x [2314, 2606), y [1501, 1743), untyped; Regions.xml:2534.

**Vendors:** Provisioner x1, Blacksmith x1, Cook x1. **Bank:** No. **Healer:** Yes, Healer x1.

**Guards:** 6 proposed slots; friendly garrison staffing only; S3/S13 must approve jurisdiction. **Other residents:** garrison captain x1, supply porters x2.

**Named people:**

- **Della Marr**, garrison captain: She keeps her earlier reports even when a paymaster calls them inconvenient. Slot: `resident.garrison captain.1`. Origin: P672-03.
- **Morris Grey**, quartermaster: He breaks a crate's seal only in front of its receiver. Slot: `vendor.Provisioner.1`. Origin: P695 proposal.

**P672 ties:**

- **P672-03**, Khalahandra Keep: The Unpaid Watch. Giver: Della Marr. The Unpaid Watch recovers the false paymaster's book and escorts supplies. A later-loop acknowledgment never repeats first-completion rewards.

**Placement and phase:** S10. Keep public infirmary and supply counter on a verified route from the high entrance at 2505,1707,50. Do not put guards on escort ambush ground.

### 17. Fort Stormhammer

**Role:** A repair and training post that values maintained equipment.

**Source anchor:** Trammel / Areas of Interest / Britain Forest - North / Fort Stormhammer at (1490, 1323, 2).

**Vendors:** Blacksmith x1, Armorer x1, Provisioner x1, Cook x1. **Bank:** No. **Healer:** Yes, Healer x1.

**Guards:** 4 proposed slots; friendly garrison staffing only; S3/S13 must approve jurisdiction. **Other residents:** recruits x2.

**Named people:**

- **Tobin Rell**, armorer and smith: He keeps repairing a recruit's shield until the maker can be paid. Slot: `vendor.Blacksmith.1`. Origin: P672-05.
- **Eleanor Beck**, quartermaster: She signs equipment back in with its repairs recorded. Slot: `vendor.Provisioner.1`. Origin: P695 proposal.

**P672 ties:**

- **P672-05**, Fort Stormhammer: A Shield Worth Keeping. Giver: Tobin Rell. A Shield Worth Keeping starts at the smith's bench; ordinary combat XP applies only to already eligible sealed gear.

**Placement and phase:** S10. Survey the nearby Sentinels Military Base entrance separately. The fort's staff must not auto-open or populate that S18 dungeon.

### 18. Castle Dunbain

**Role:** A relief counting house with a corrupt steward and a clerk seeking evidence.

**Source anchor:** Trammel / Areas of Interest / Britain Forest - North / Castle Dunbain at (1333, 1377, 0).

**Vendors:** None. **Bank:** No. **Healer:** No.

**Guards:** 0 proposed slots; no public law guards. **Other residents:** accounts clerk x1, household workers x2.

**Encounter occupants:** steward x1, hired guards x4. Deferred combat actors with no selected concrete type.

**Named people:**

- **Iris Dane**, accounts clerk: She needs a real ledger before she will accuse a superior. Slot: `resident.accounts clerk.1`. Origin: P672-06.
- **Corin Pell**, corrupt steward: He balances the books by erasing the people waiting for supplies. Slot: `enemy.steward.1`. Origin: P672-06.

**P672 ties:**

- **P672-06**, Castle Dunbain: The Open Ledger. Giver: Iris Dane. The Open Ledger offers a work-order route and a guarded service route without mandatory theft or guild membership.

**Placement and phase:** later P672 encounter build. Place Iris at a reachable service entrance for the quest build. No public bank, invulnerable combat guards or shop in the evidence rooms.

### 19. Fort Silverblood

**Role:** A field infirmary containing a local poisoned-water outbreak.

**Source anchor:** Trammel / Areas of Interest / Britain Forest - South / Fort Silverblood at (1561, 2652, -5).

**Vendors:** Provisioner x1, Alchemist x1, Cook x1. **Bank:** No. **Healer:** Yes, Healer x1.

**Guards:** 4 proposed slots; friendly garrison staffing only; S3/S13 must approve jurisdiction. **Other residents:** patients x2, field assistant x1.

**Named people:**

- **Maeve Sutter**, healer: She keeps the suspect water barrels sealed until their origin is clear. Slot: `healer.1`. Origin: P672-07.
- **Arthur Bell**, field assistant: He explains each sample step before handing over a clean vial. Slot: `resident.field assistant.1`. Origin: P695 proposal.

**P672 ties:**

- **P672-07**, Fort Silverblood: The Last Clean Bandage. Giver: Maeve Sutter. The Last Clean Bandage investigates the shipment. The assistant covers missing specialties; the cure is local to this outbreak.

**Placement and phase:** S10. The author fort anchor lies near Agurast Ascension's surface entrance. Separate infirmary doors from sealed dungeon access and keep patients out of guard combat.

### 20. Tigerclaw Fortress

**Role:** A school shelter whose hired commander abuses its pupils' banner.

**Source anchor:** Trammel / Areas of Interest / Covetous Forest / Tigerclaw Fortress at (2595, 1085, 8).

**Vendors:** Provisioner x1, Blacksmith x1. **Bank:** No. **Healer:** Yes, Healer x1.

**Guards:** 2 proposed slots; friendly garrison staffing only; S3/S13 must approve jurisdiction. **Other residents:** instructor x1, displaced pupils x3.

**Encounter occupants:** hired commander x1, toll enforcers x3. Deferred combat actors with no selected concrete type.

**Named people:**

- **Renna Ward**, instructor: She keeps the pupils' charter ready for the day it can be read in the yard. Slot: `resident.instructor.1`. Origin: P672-09.
- **Edgar Moss**, relief healer: He treats pupils in the outer shelter while the yard remains disputed. Slot: `healer.1`. Origin: P695 proposal.

**P672 ties:**

- **P672-09**, Tigerclaw Fortress: The Borrowed Banner. Giver: Renna Ward. The Borrowed Banner recovers the charter and Tokuno clue. Both ordinary combat and optional dojo paths remain viable.

**Placement and phase:** later P672 encounter build. Friendly staff and two sentries belong only in a verified outer shelter. Hostile commander and yard stay outside its guard jurisdiction. If there is no separated shelter, hold the whole arrangement for encounter design.

### 21. Red Dagger Keep

**Role:** A smuggling hold exploiting families with counterfeit passage papers.

**Source anchor:** Trammel region Red Dagger Keep, x [4406, 4693), y [1944, 2203), TownRegion; Regions.xml:1374.

**Vendors:** None. **Bank:** No. **Healer:** No.

**Guards:** 0 proposed slots; no public law guards. **Other residents:** stranded passenger contact x1, stranded families x3.

**Encounter occupants:** smuggler x1, hired guards x4. Deferred combat actors with no selected concrete type.

**Named people:**

- **Vera Flint**, smuggler: She sells the same false assurance with every passage paper. Slot: `enemy.smuggler.1`. Origin: P672-08.
- **Alice Dorr**, stranded passenger contact: She memorizes the other passengers' names when their papers disappear. Slot: `resident.stranded passenger contact.1`. Origin: P695 proposal.

**P672 ties:**

- **P672-08**, Red Dagger Keep: A Forged Passage. Request contact: Alice Dorr. A Forged Passage uses Vera as antagonist. Alice is a proposed approach contact, not a P672-approved giver. Recover the list and refer onward to Ghuul Sanctuary without granting Malas access.

**Placement and phase:** later P672 encounter build. No author entrance point is supplied. Survey rectangles before choosing an exterior contact or relief boat. Never spawn at a computed box center.

### 22. Brit Forest Guard Barracks

**Role:** A small road patrol rest and ration station.

**Source anchor:** Trammel / Areas of Interest / Britain Forest - South / Brit Forest Guard Barracks at (1670, 2476, 10).

**Vendors:** Provisioner x1, Cook x1. **Bank:** No. **Healer:** Yes, Healer x1.

**Guards:** 4 proposed slots; friendly garrison staffing only; S3/S13 must approve jurisdiction. **Other residents:** watch recorder x1.

**Named people:**

- **Mildred Hale**, watch recorder: She keeps the sign-in sheet open until the last patrol returns. Slot: `resident.watch recorder.1`. Origin: P695 proposal.

**P672 ties:**

- **P672-11**, Camp Ironfang: Leave the Cages Open. Notice: Mildred Hale. Post June Mercer's rescue request without sending lawful patrols into Camp Ironfang's fight.

**Placement and phase:** S10. Use the author barracks anchor; reserve services for travelers and a separate watch room.

### 23. Brit Forest Guardpost

**Role:** A road watch with basic supplies and directions back to town.

**Source anchor:** Trammel / Areas of Interest / Britain Forest - South / Brit Forest Guardpost at (1426, 2104, 6).

**Vendors:** Provisioner x1. **Bank:** No. **Healer:** No.

**Guards:** 2 proposed slots; friendly garrison staffing only; S3/S13 must approve jurisdiction. **Other residents:** post clerk x1.

**Named people:**

- **Leonard Shaw**, post clerk: He gives directions using bridges and houses instead of compass bearings. Slot: `resident.post clerk.1`. Origin: P695 proposal.

**P672 ties:**

No assigned P672 seed. Do not invent a numbered quest or give a nearby dungeon's actor a second home.

**Placement and phase:** S10. A post, not a full town. Keep watch footprints small; nearest town service route still needs S15 verification.

### 24. Yew Forest Guardpost

**Role:** A forest road watch sharing reports with the nearby relief forts.

**Source anchor:** Trammel / Areas of Interest / Yew Forest / Yew Forest Guardpost at (1047, 1080, 0).

**Vendors:** Provisioner x1. **Bank:** No. **Healer:** No.

**Guards:** 2 proposed slots; friendly garrison staffing only; S3/S13 must approve jurisdiction. **Other residents:** post clerk x1.

**Named people:**

- **Dorothy Winn**, post clerk: She writes down a missing scout's last certain sighting. Slot: `resident.post clerk.1`. Origin: P695 proposal.

**P672 ties:**

- **P672-02**, Fort Whitestone: A Place at the Table. Notice: Dorothy Winn. Direct patrol inquiries to Hester Vale at Whitestone.
- **P672-04**, Fort Viridian: The Boundary Trees. Notice: Dorothy Winn. Direct boundary disputes to Nessa Holt at Viridian.

**Placement and phase:** S10. Do not merge this post with Viridian or Whitestone because their anchors are close.

### 25. Camp Ironfang

**Role:** A poacher camp with a proposed rescue contact outside its pens.

**Source anchor:** Trammel / Areas of Interest / Britain Forest - South / Camp Ironfang at (1699, 2363, 5).

**Vendors:** None. **Bank:** No. **Healer:** No.

**Guards:** 0 proposed slots; no public law guards. **Other residents:** stablehand x1, rescued handlers x2.

**Encounter occupants:** poacher leader x1, poachers x3. Deferred combat actors with no selected concrete type.

**Named people:**

- **June Mercer**, stablehand: She knows which pack animals will follow a quiet voice out of the pens. Slot: `resident.stablehand.1`. Origin: P672-11.
- **Garrick Venn**, poacher leader: He calls stolen tack battlefield salvage. Slot: `enemy.poacher leader.1`. Origin: P672-11.

**P672 ties:**

- **P672-11**, Camp Ironfang: Leave the Cages Open. Giver: June Mercer. Leave the Cages Open frees animals. No evo stage, replacement starter or Bond Trial completion is awarded.

**Placement and phase:** later P672 encounter build. Keep June at a safe approach in the later encounter build; recovery animals are encounter data outside this human roster.

### 26. Ivanguard Manor

**Role:** An unpaid household and a contracted guard trying to leave service.

**Source anchor:** Trammel / Areas of Interest / Britain Forest - South / Ivanguard Manor at (1773, 2683, 0).

**Vendors:** None. **Bank:** No. **Healer:** No.

**Guards:** 0 proposed slots; no public law guards. **Other residents:** housekeeper x1, household workers x2, unpaid traveling guard x1.

**Encounter occupants:** hired enforcers x3. Deferred combat actors with no selected concrete type.

**Named people:**

- **Lysa Trent**, housekeeper: She keeps a copy of every wage promise the owner forgets. Slot: `resident.housekeeper.1`. Origin: P672-12.
- **Bernard Hale**, unpaid traveling guard: He wants his signed terms honored before he accepts another post. Slot: `resident.unpaid traveling guard.1`. Origin: P695 proposal.

**P672 ties:**

- **P672-12**, Ivanguard Manor: The Guest Who Was Never Paid. Giver: Lysa Trent. The Guest Who Was Never Paid recovers equipment and escorts workers. The traveling guard is not a forced companion reward.

**Placement and phase:** later P672 encounter build. The rescued guard is a resident quest actor, never a public law guard. Keep hired enforcers separate from household escorts.

### 27. Camp Bloodwater Basin

**Role:** A proposed jungle survey camp supplied from the settled south.

**Source anchor:** Trammel / Areas of Interest / Trinsic Jungle / Camp Bloodwater Basin at (1802, 3379, 0).

**Vendors:** Provisioner x1. **Bank:** No. **Healer:** Yes, Healer x1.

**Guards:** 2 proposed slots; friendly garrison staffing only; S3/S13 must approve jurisdiction. **Other residents:** camp recorder x1, survey crew x2.

**Named people:**

- **Florence Wren**, camp recorder: She marks the safe drinking water before drawing the rest of camp. Slot: `resident.camp recorder.1`. Origin: P695 proposal.

**P672 ties:**

No assigned P672 seed. Do not invent a numbered quest or give a nearby dungeon's actor a second home.

**Placement and phase:** S10 after building survey. P672 gives no seed here. Alignment is a new proposal; confirm camp structures and dry standing space before placing a friendly supply shelter.

### 28. Chapel of Saint Lucia

**Role:** A quiet roadside infirmary and shelter for travelers.

**Source anchor:** Trammel / Areas of Interest / Trinsic Jungle / Chapel of Saint Lucia at (1714, 3173, 11).

**Vendors:** None. **Bank:** No. **Healer:** Yes, Healer x1.

**Guards:** 0 proposed slots; no public law guards. **Other residents:** chapel keeper x1, shelter guests x1.

**Named people:**

- **Joan Mercer**, chapel keeper: She leaves a lamp for anyone returning after dark. Slot: `resident.chapel keeper.1`. Origin: P695 proposal.
- **Paul Rell**, healer: He begins every treatment by finding clean water. Slot: `healer.1`. Origin: P695 proposal.

**P672 ties:**

- **P672-07**, Fort Silverblood: The Last Clean Bandage. Notice: Joan Mercer. Relay Maeve Sutter's water warning; the outbreak and its giver remain at Fort Silverblood.

**Placement and phase:** S10. No bank or invented religious rewards. Use stock furnishings after an interior survey.

### 29. Dhampire Ruins

**Role:** A temporary records shelter among damaged burial walls.

**Source anchor:** Trammel / Areas of Interest / Britain Forest - South / Dhampire Ruins at (1469, 2515, 14).

**Vendors:** None. **Bank:** No. **Healer:** No.

**Guards:** 0 proposed slots; no public law guards. **Other residents:** mortuary clerk x1, record helpers x1.

**Named people:**

- **Oren Pike**, mortuary clerk: He writes each recovered name as carefully as a family would. Slot: `resident.mortuary clerk.1`. Origin: P672-10.

**P672 ties:**

- **P672-10**, Dhampire Ruins: Names Beneath the Ash. Giver: Oren Pike. Names Beneath the Ash restores the register for Ghuul Sanctuary. No sword piece or Chapter 3 rescue is attached.

**Placement and phase:** later P672 encounter build. Ruin, not a serviced town. Place the shelter clear of grave-robbing encounter paths.

### 30. Mistveil Ruins

**Role:** A surveyor's hiding place at an old crossing survey.

**Source anchor:** Trammel / Areas of Interest / Yew Forest / Mistveil Ruins at (1177, 792, 0).

**Vendors:** None. **Bank:** No. **Healer:** No.

**Guards:** 0 proposed slots; no public law guards. **Other residents:** surveyor x1.

**Named people:**

- **Brin Alder**, surveyor: He would rather admit a missing measurement than draw a false road. Slot: `resident.surveyor.1`. Origin: P672-13.

**P672 ties:**

- **P672-13**, Mistveil Ruins: The Survey in the Fog. Giver: Brin Alder. The Survey in the Fog points to Ellis Ward in Azurite Caverns, then Anwen Dale at Skypoint. It grants no Ilshenar permission by itself.

**Placement and phase:** later P672 encounter build. Use a later safe approach actor; no generic shop or law guard among the scavengers.

### 31. Glimmerwood

**Role:** A grove ledger and tree-survey camp for an eventual expedition.

**Source anchor:** Trammel / Areas of Interest / Glimmerwood / East at (2834, 3488, 6); Trammel region Glimmerwood, x [2125, 2863), y [3077, 3689), untyped; Regions.xml:2252.

**Vendors:** None. **Bank:** No. **Healer:** No.

**Guards:** 0 proposed slots; no public law guards. **Other residents:** grove keeper x1, survey crew x2.

**Named people:**

- **Mara Wren**, grove keeper: She records which trees survive before calculating the lost timber. Slot: `resident.grove keeper.1`. Origin: P672-14.

**P672 ties:**

- **P672-14**, Glimmerwood: What the Grove Remembers. Giver: Mara Wren. What the Grove Remembers supplies the rubbing for Fortress Calcifina, never a Ter Mur unlock or the League Setting.

**Placement and phase:** S19 after affected fences lift. The Glimmerwood west landmark is outside the summarized region bounding box. Retain both facts; S3/S15 must resolve access. While S14 fences apply, Elmhaven has only a notice and no live grove objectives.

### 32. Dragonstorm Isle

**Role:** A threatened landing with survivors awaiting the next relief crew.

**Source anchor:** Trammel / Areas of Interest / Dragonstorm Island / Moongate at (3186, 3884, 17); Trammel region Dragonstorm Isle, x [3119, 3260), y [3716, 3914), untyped; Regions.xml:2554.

**Vendors:** Provisioner x1. **Bank:** No. **Healer:** Yes, Healer x1.

**Guards:** 2 proposed slots; friendly garrison staffing only; S3/S13 must approve jurisdiction. **Other residents:** harbor keeper x1, shipwreck survivors x3.

**Named people:**

- **Selda Rook**, harbor keeper: She checks the brood tally before allowing another relief landing. Slot: `resident.harbor keeper.1`. Origin: P672-15.
- **Emma Dale**, relief healer: She keeps dry bandages packed for a sudden evacuation. Slot: `healer.1`. Origin: P695 proposal.

**P672 ties:**

- **P672-15**, Dragonstorm Isle: Before the Next Landing. Giver: Selda Rook. Before the Next Landing introduces the Dragons Den expedition, not a working moongate. Selda is distinct from Haven's Rook.

**Placement and phase:** later P672 encounter build. Use only a verified landing shelter for services; drakes and eggs belong to encounter design. The visible gate stays decor unless separately enabled.

### 33. Skypoint Islands

**Role:** A relief ship's staging point for a proposed controlled crossing.

**Source anchor:** Trammel / Areas of Interest / Skypoint Islands / Ship at (4357, 2349, 20); Trammel region Skypoint Islands, x [4334, 4416), y [2288, 2433), untyped; Regions.xml:2538.

**Vendors:** Provisioner x1, Tinker x1. **Bank:** No. **Healer:** Yes, Healer x1.

**Guards:** 2 proposed slots; friendly garrison staffing only; S3/S13 must approve jurisdiction. **Other residents:** pilot x1, relief crew x2.

**Named people:**

- **Anwen Dale**, pilot: She will not call a crossing safe until she has plotted the return. Slot: `resident.pilot.1`. Origin: P672-16.
- **George Flint**, tinker: He checks every compass bearing twice on a moving deck. Slot: `vendor.Tinker.1`. Origin: P695 proposal.

**P672 ties:**

- **P672-16**, Skypoint Islands: The Ship That Cannot Leave. Giver: Anwen Dale. The Ship That Cannot Leave needs Brin's survey and Ellis's repaired instrument. Any Ilshenar permission is a later approved permanent character flag.

**Placement and phase:** later P672 travel build. The ship go point at Z20 is a landmark. Confirm its deck, shore access, ghost route and services separately before opening a camp.

### 34. Echoback Estuary campsite

**Role:** A future estuary survey shelter, withheld while unfinished land is fenced.

**Source anchor:** Trammel / Areas of Interest / Echoback Estuary / Campsite at (4454, 2586, 5); Trammel region Echoback Estuary, x [4424, 4626), y [2513, 2743), untyped; Regions.xml:2546.

**Vendors:** None. **Bank:** No. **Healer:** No.

**Guards:** 0 proposed slots; no public law guards. **Other residents:** survey keeper x1.

**Named people:**

- **Olive Ward**, survey keeper: She refuses to publish a landing she has not walked herself. Slot: `resident.survey keeper.1`. Origin: P695 proposal.

**P672 ties:**

No assigned P672 seed. Do not invent a numbered quest or give a nearby dungeon's actor a second home.

**Placement and phase:** S19 after fence and access review. No active roster while S14 fences apply. The author campsite is a future survey anchor only.

## Stock and rebuilt settlements: reconcile, then fill gaps

All entries in this table have planned bank and healer access. Numbers apply only after comparing retained S9 staff, or S7 staff in Haven. Additional stock specialists are outside the floor and must not be removed. Guard numbers are future staffing targets, with no patrol activation here. One proposed name may label an otherwise unclaimed matching provisioner slot; Elara is the existing registrar and is never an added copy.

| Settlement | Role | Minimum vendor slots | Bankers / healers | Future guard slots | Named person and character | P672 notices |
| --- | --- | --- | --- | --- | --- | --- |
| Britain | A rebuilt civic capital and major market. | Provisioner x2, Blacksmith x2, Tailor x1, Carpenter x1, Baker x1, Alchemist x1, InnKeeper x1, AnimalTrainer x1 | 2 / 2 | 8 | Constance Webb, provisioner: She keeps relief orders separate from the castle's purchases. | P672-06, P672-17, P672-25, P672-31, P672-32 |
| Buccaneers Den | A rebuilt pirate port with services and no law guard response. | Provisioner x1, Blacksmith x1, Tailor x1, Carpenter x1, InnKeeper x1, Shipwright x1 | 1 / 1 | 0 | Percy Dunn, provisioner: He prices a crate by its contents rather than its flag. | P672-08 |
| Cove | A compact walled market and road-service town. | Provisioner x1, Blacksmith x1, InnKeeper x1 | 1 / 1 | 4 | Beatrice Webb, provisioner: She checks the gate notice before promising a delivery date. | P672-09 |
| Delucia | A rebuilt Lost Lands frontier supply town. | Provisioner x1, Blacksmith x1, Tailor x1, Mage x1, InnKeeper x1, AnimalTrainer x1 | 1 / 1 | 4 | Thomas Dale, provisioner: He packs a spare strap with every long-trail order. | None |
| Haven | The author's rebuilt Haven becomes New Haven, the start town and service hub. | Provisioner x1, Blacksmith x1, Tailor x1, Carpenter x1, Fisherman x1, Shipwright x1, InnKeeper x1, AnimalTrainer x1 | 1 / 2 | 8 | Elara Voss, League Registrar: She helps new citizens find their first useful guild contact. | P672-27 |
| Jhelom | An island service town supporting martial training and sea travel. | Provisioner x1, Blacksmith x1, Armorer x1, InnKeeper x1, Shipwright x1 | 1 / 1 | 6 | Rose Tully, provisioner: She puts practical supplies ahead of arena souvenirs. | None |
| Magincia | A rebuilt merchant island with public civic and dock services. | Provisioner x1, Blacksmith x1, Tailor x1, InnKeeper x1, Shipwright x1 | 1 / 1 | 6 | Philip Marsh, provisioner: He writes each delivery destination plainly on the bill. | P672-16 |
| Minoc | A rebuilt mining and metalwork market. | Provisioner x1, Blacksmith x2, Tinker x1, Carpenter x1, InnKeeper x1 | 1 / 1 | 6 | Winifred Cobb, provisioner: She keeps a lamp and a meal ready for delayed miners. | P672-19, P672-31 |
| Moonglow | A rebuilt scholarly port and reagent market. | Provisioner x1, Blacksmith x1, Mage x1, Alchemist x1, Scribe x1, InnKeeper x1, Shipwright x1 | 1 / 1 | 6 | Cecil Larkin, provisioner: He wraps fragile instruments as carefully as fresh bread. | P672-13, P672-19, P672-16 |
| Nujel'm | A desert-side court and shipping market. | Provisioner x1, Blacksmith x1, Alchemist x1, InnKeeper x1, Shipwright x1 | 1 / 1 | 6 | Margaret Dunn, provisioner: She fills the water jars before counting the coin. | P672-18 |
| Papua | A Lost Lands river market whose usable shops should be retained. | Provisioner x1, Blacksmith x1, Carpenter x1, Mage x1, InnKeeper x1, AnimalTrainer x1 | 1 / 1 | 4 | Victor Field, provisioner: He keeps a dry shelf for travelers' maps. | None |
| Serpents Hold | An island garrison town and southern sailing base. | Provisioner x1, Blacksmith x1, Armorer x1, Bowyer x1, InnKeeper x1, Shipwright x1 | 1 / 1 | 6 | Florence Bale, provisioner: She asks for a return date before packing another expedition. | P672-15 |
| Skara Brae | A rebuilt western craft and ferry town. | Provisioner x1, Blacksmith x1, Bowyer x1, Carpenter x1, Tailor x1, InnKeeper x1, AnimalTrainer x1 | 1 / 1 | 6 | Gilbert Clay, provisioner: He labels island and mainland deliveries on different shelves. | P672-21 |
| Trinsic | A rebuilt southern port with craft and caravan services. | Provisioner x1, Blacksmith x1, Armorer x1, Tailor x1, InnKeeper x1, Shipwright x1 | 1 / 1 | 8 | Louisa Beck, provisioner: She checks a caravan's supplies before praising its banner. | P672-07, P672-12, P672-14, P672-20 |
| Vesper | A rebuilt island-chain trade center with specialist shops. | Provisioner x1, Blacksmith x1, Tailor x1, Carpenter x1, Tinker x1, Alchemist x1, InnKeeper x1, Shipwright x1 | 1 / 1 | 8 | Frederick Rowe, provisioner: He remembers which bridges a loaded cart can cross. | P672-09, P672-29 |
| Wind | A mountain mage settlement with its existing access conditions. | Provisioner x1, Blacksmith x1, Mage x1, Alchemist x1, Scribe x1 | 1 / 1 | 4 | Daisy Grey, provisioner: She gives practical directions before discussing magical theory. | P672-13 |
| Yew | A rebuilt woodland court and craft center supplying neighboring relief forts. | Provisioner x1, Blacksmith x1, Carpenter x1, Bowyer x1, Tailor x1, InnKeeper x1, AnimalTrainer x1 | 1 / 1 | 6 | Henry Quinn, provisioner: He keeps a public copy of the forest supply list. | P672-02, P672-04, P672-13 |
| Heartwood | An existing elven enclave retained under its own access and service rules. | Provisioner x1, Blacksmith x1, Bowyer x1, Carpenter x1, Tailor x1 | 1 / 1 | 4 | Cora Bell, provisioner: She matches visiting work crews to the supplies they can actually carry. | None |

Stock placement notes and author anchors:

- **Britain** (S9 and S5): Keep Lord British Castle and Blackthorn Castle as nested Britain staffing allocations, not extra towns. Do not confuse Blackthorn Castle with the disabled EA dungeon. Source: Trammel / Towns / Britain / Artists' Guild at (1445, 1671, 10); Trammel region Britain, x [1356, 1786), y [1408, 1798), TownRegion; Regions.xml:1083.
- **Buccaneers Den** (S9 and S5): Match Buccaneer's Den in Regions.xml. Keep the Den unguarded on both facets; healer is stock Healer with its normal eligibility, not immunity for criminals. Source: Trammel / Towns / Buccaneers Den / Bank at (2731, 2193, 0); Trammel region Buccaneer's Den, x [2562, 2890), y [1915, 2289), TownRegion; Regions.xml:1130.
- **Cove** (S9 and S5): Keep the source Cove Trammel observe-only guard pilot scoped here. A roster count neither enables P608 nor qualifies a physical patrol. Source: Trammel / Towns / Cove / Bank of Cove at (2233, 1198, 0); Trammel region Cove, x [2198, 2311), y [1031, 1256), TownRegion; Regions.xml:1143.
- **Delucia** (S9 and S5): Verify each rebuilt shop against author landmarks; do not assume the old stable and supply depot tiles remain usable. Source: Trammel / Towns / Delucia / Center at (5228, 3978, 37); Trammel region Delucia, x [5125, 5313), y [3932, 4084), TownRegion; Regions.xml:1152.
- **Haven** (S7 with S9 reconciliation): Retain Rook, Elara, all existing guild staff, trainers and service NPCs under S7. No new registrar copies. Rootdeep's cellar hatch stays separate from Haven Catacombs. Source: Trammel / Towns / Haven / Anchors Aweigh at (3635, 2641, 0); Trammel region Haven, x [3313, 3820), y [2345, 3097), NoHousingRegion; Regions.xml:1183.
- **Jhelom** (S9 retention and survey): P669's assessment lists no rebuilt go-menu spots here. Retain working stock staff instead of manufacturing a rebuild. Source: Trammel / Towns / Jhelom / Cemetery at (1296, 3719, 0).
- **Magincia** (S9 and S5): Author town name is Magincia; bank is Bank of New Magincia. Do not create a second New Magincia town or extra broker subsystem. Source: Trammel / Towns / Magincia / Bank of New Magincia at (3730, 2161, 20); Trammel region Magincia, x [3523, 3815), y [2026, 2303), TownRegion; Regions.xml:1245.
- **Minoc** (S9 and S5): Keep mining camp services in distinct retained slots, with public paths through the rebuilt bridge area. Source: Trammel / Towns / Minoc / Bank of Minoc at (2504, 562, 0); Trammel region Minoc, x [2389, 2634), y [343, 691), TownRegion; Regions.xml:1271.
- **Moonglow** (S9 and S5): The new desert landmass changes approaches. Survey the docks, zoo and telescope paths without assuming old island access. Source: Trammel / Towns / Moonglow / Cemetery at (4546, 1338, 8); Trammel region Moonglow, x [4367, 4509), y [1015, 1195), TownRegion; Regions.xml:1294.
- **Nujel'm** (S9 and S5): Use author Nujelm bank and docks landmarks. The large places.csv desert box is a geography warning, not a town boundary. Source: Trammel / Towns / Nujel'm / Bank of Nujelm at (3770, 1315, 0); Trammel region Nujel'm, x [3480, 3806), y [1032, 1428), TownRegion; Regions.xml:1311.
- **Papua** (S9 retention and survey): P669's assessment lists touched and stock go-menu spots, with no rebuilt spots. Preserve valid stock service density. Source: Trammel / Towns / Papua / Center at (5730, 3208, -4); Trammel region Papua, x [5639, 5851), y [3095, 3318), TownRegion; Regions.xml:1340.
- **Serpents Hold** (S9 retention and survey): Match Serpent's Hold in Regions.xml. No new or rebuilt go-menu spots in P669's town summary; inspect touched services and retain the rest. Source: Trammel / Towns / Serpents Hold / Bank at (2892, 3475, 15); Trammel region Serpent's Hold, x [2859, 3085), y [3324, 3639), TownRegion; Regions.xml:1409.
- **Skara Brae** (S9 and S5): Keep the two docks distinct and services separate from Kettleburg. Verify the ferry or foot route rather than assuming it survived. Source: Trammel / Towns / Skara Brae / Bank of Skara Brae at (597, 2153, 0); Trammel region Skara Brae, x [513, 921), y [2043, 2435), TownRegion; Regions.xml:1432.
- **Trinsic** (S9 and S5): Survey moved gates and bank access. Do not extend town guard law into nearby forts, jungle quests or fenced Glimmerwood. Source: Trammel / Towns / Trinsic / Bank of Britannia: Trinisic Branch at (1821, 2822, 0); Trammel region Trinsic, x [1796, 2166), y [2635, 2927), TownRegion; Regions.xml:1460.
- **Vesper** (S9 and S5): Reconcile island-specific stock specialists before applying any floor; a single town target must not erase the author's distributed shops. Source: Trammel / Towns / Vesper / Outer Perimeters / Cemetery at (2786, 867, 0); Trammel region Vesper, x [2813, 3051), y [576, 1011), TownRegion; Regions.xml:1489.
- **Wind** (S9 retention and local rework): Preserve existing Wind entry rules and residents. A service target does not open its entrance to every character. Source: Trammel / Towns / Wind / Caves at (5166, 244, 15); Trammel region Wind, x [5132, 5366), y [3, 204), TownRegion; Regions.xml:1525.
- **Yew** (S9 and S5): Keep Empath Abbey, courts and Heartwood's entrance as separate retained service areas. No automatic guard jurisdiction over outlying ruins or forts. Source: Trammel / Towns / Yew / Cemetery at (724, 1138, 0); Trammel region Yew, x [92, 720), y [656, 1286), TownRegion; Regions.xml:1550.
- **Heartwood** (S9 retention only): Named primary author region, outside the ordinary town go-menu list. Preserve existing authored elf vendors and stock quests. Proposed ordinary service types are floors only, not permission to replace specialty actors. Source: Trammel region Heartwood, x [6911, 7168), y [255, 512), TownRegion; Regions.xml:1204.

## P672 dungeon actor handoff

These are source seed contacts, not additional settlement slots. S18 and the later quest builds own them. Every original seed number is covered either by a local actor above, a notice, or this handoff. Keep P672's story, build alternatives and reward limits. No route bypasses League chapter prerequisites, replaces a sword piece or reveals later chapters early.

| Seed | Location and hook | Seed contact | Placement boundary |
| --- | --- | --- | --- |
| P672-17 | Agurast Ascension: One More Flight | Sella Vane | S18 owns the dungeon actor and encounter. Town contacts are notices only; no duplicate giver. |
| P672-18 | Amul Seketsi Royal Tomb: The Wrong Heir | Edda Marlow | S18 owns the dungeon actor and encounter. Town contacts are notices only; no duplicate giver. |
| P672-19 | Azurite Caverns: The Needle Under Stone | Ellis Ward | S18 owns the dungeon actor and encounter. Town contacts are notices only; no duplicate giver. |
| P672-20 | Black Widow Pit: The Silk Account | Delia Moss | S18 owns the dungeon actor and encounter. Town contacts are notices only; no duplicate giver. |
| P672-21 | Bleak Wind Tunnels: A Lamp for the Return | Hollis Beck | S18 owns the dungeon actor and encounter. Town contacts are notices only; no duplicate giver. |
| P672-22 | Dragons Den: The Stolen Brood | Varric Pell | Varric Pell is the antagonist, not a public quest giver. Selda Rook at Dragonstorm supplies the existing chain contact. |
| P672-23 | Fortress Calcifina: An Answer in Stone | Arda Quill | S18 owns the dungeon actor and encounter. Town contacts are notices only; no duplicate giver. |
| P672-24 | Fungully Grotto: The Sample That Breathes | Mina Bell | S18 owns the dungeon actor and encounter. Town contacts are notices only; no duplicate giver. |
| P672-25 | Ghuul Sanctuary: Room for the Names | Rowan Pike | S18 owns the dungeon actor and encounter. Town contacts are notices only; no duplicate giver. |
| P672-26 | Hammerhill Sewers: What the Water Carries | Elsie Crow | Elsie Crow is in the Hammerhill surface roster. S18 owns only her dungeon crew and objectives; do not add a second Elsie. |
| P672-27 | Haven Catacombs: The Unclaimed Tool Roll | Cora Venn | S18 owns the dungeon actor and encounter. Town contacts are notices only; no duplicate giver. |
| P672-28 | Mongbat Hideout: A Coat Full of Receipts | Nellie Hart | S18 owns the dungeon actor and encounter. Town contacts are notices only; no duplicate giver. |
| P672-29 | Oboru Burial Ground: The Song Left Unfinished | Iona Bell | S18 owns the dungeon actor and encounter. Town contacts are notices only; no duplicate giver. |
| P672-30 | Passage of Lost Souls: The Road Home | Tess Marlow | S18 owns the dungeon actor and encounter. Town contacts are notices only; no duplicate giver. |
| P672-31 | Stone Burrow Mines: The Weight of the Claim | Amos Flint | S18 owns the dungeon actor and encounter. Town contacts are notices only; no duplicate giver. |
| P672-32 | Whispering Hollow: The Answering Voice | Fenna Reed | S18 owns the dungeon actor and encounter. Town contacts are notices only; no duplicate giver. |

## Named places held outside active civic staffing

**Retained nested Britain sites**: Lord British Castle, Blackthorn Castle. Preserve existing occupants under S9. These are not new Dunbain or Stormhammer settlements. No extra civilian service or garrison totals are added here.

**Hostile or creature sites, S9 or later encounter work**: Yew Fort of the Damned, Yew-Britain Brigand Camp, Harpy Campgrounds, Cove Orc Fort, Yew Orc Fort, Delucia Orc Fort. No public vendors, bank, healer or law guard roster. No invented friendly town conversion. Humanoid combat and wildlife composition are outside this civic roster.

**Named landmark only**: Cherrygrove Bliss. No author evidence of a settlement; hold any inhabitants pending building survey.

**S14 fenced land or nonsettlement**: Darkfathom Hollow, Dunbarrow Fissure, Poultry Paradise, northeast snow isles, bare land east of Haven. No active civilian population proposal. S19 determines if usable settlements exist.

**Held, legacy Sosaria region set only**: Death Gulch, Death Gulch Inn, Devil Guard, Devil Guard Inn, the town of Moon, the town of Grey, Grey Inn, the town of West Montor, West Montor Inn, the town of East Montor, East Montor Inn, the town of Fawn, Fawn Inn, the town of Yew, Yew Inn, the town of Britain, Britain Inn, Pirate Isle, Vinterdale Isle, the Iceclad Fisherman's Village, Fisherman's Inn, the Mountain Crest Village, Mountain Crest Inn, the Shingorr Village, Shingorr Inn, Unknown Land, Inn, the town of Renika, Renika Inn, a Cathedral, Ambrosia, a Ababdoned Town, Dawn, the town of Dawn, Dawn Inn, Etherial Plane, the etherial town of Dawn, Etherial Inn, the Dark Tower, a Mountain Stronghold, an Old Fortress, Tarnithok Fortress. The author-spots reference warns this set may be leftovers. Do not create residents or treat these boxes as authoritative Trammel towns.

The second Sosaria region set is deliberately not merged into Trammel. This holds places such as Dawn and the Iceclad Fisherman's Village without claiming they are finished SoS settlements. Dungeon forts such as Fortress Calcifina and Sentinels Military Base are S18 encounters, not more civilian towns. Cemeteries, shrines, camps of nonhuman enemies and geographical features get no invented civilian population here.

## Source evidence and limits

Read both work-copy AGENTS.md files, the direction decision and task list before drafting. Sources used:

- [Author-spots reference](sos-map-author-spots.md), plus the original [locations XML](sos-author-data/locations-trammel.xml) and [regions XML](sos-author-data/Regions.xml). Every roster matches a Trammel name or go-menu entry. The JSON publishes the matched point list and original rectangles beside each roster.
- [P608 physical guard design](cc-P608-guards-patrol-design.md) for the distinction between staffing a post and implementing patrol enforcement.
- [P672 quest seeds](cc-P672-sos-quest-seeds.md). The draft preserves its original named residents, separates opponents from givers, and leaves dungeon contacts in their authored locations.
- [P669 places.csv](cc-P669-tools/out/places.csv). It samples New Haven, New Magincia, Britain, the Nujel'm/desert landmass, gates and several dungeon/void areas. It does not supply plots or dry-area denominators for the new towns. In particular the approximate New Haven box crosses the wider relocation area, and the broad Nujel'm rectangle includes much more than its town. The row-name list is copied into the JSON for audit.
- [P669 assessment](cc-P669-sos-trammel-assessment.md) for rebuilt-town context; [P673 swap plan](cc-P673-sos-swap-plan.md) and the current task prompt for replacement of Trammel and Felucca. Earlier added-facet wording in SOURCE.txt and P672 is historical context, not the current placement target.
- Canonical shard files: `server/customizations/ClusterFNewHavenServicesSeeder.cs` (existing healer reconciliation); `LeagueRegistrar.cs:23,39-41` (Elara and New Haven-specific behavior); `ForestersGuildmaster.cs:19,22-24` (Cedric and existing guildmaster behavior); `ClusterFGuardWitness.cs:1-32,130-134` (observe-only Cove Trammel pilot). No existing registrar or guildmaster is reused as a different town's draft actor.

Pinned ModernUO source was verified at `d4531cd94b739613155225c234900de9f47d2c88`. In the following table, `U/` means `D:/UO/ModernUO-pinned/Projects/UOContent/`. The JSON records declaration and constructor lines for every file listed here. Twenty concrete vendor and service types are selected; the additional files document behavior or alternatives rather than extra roster slots.

| Type | Source file and declaration line | Use |
| --- | --- | --- |
| Alchemist | U/Mobiles/Vendors/NPC/Alchemist.cs:8 | Selected existing service type; keep its normal conditional stock behavior. |
| AnimalTrainer | U/Mobiles/Vendors/NPC/AnimalTrainer.cs:13 | Selected existing service type; keep its normal conditional stock behavior. |
| ArcherGuard | U/Mobiles/Guards/ArcherGuard.cs:7 | Behavior reference only; no slots of this type selected. |
| Armorer | U/Mobiles/Vendors/NPC/Armorer.cs:8 | Selected existing service type; keep its normal conditional stock behavior. |
| Baker | U/Mobiles/Vendors/NPC/Baker.cs:7 | Selected existing service type; keep its normal conditional stock behavior. |
| Banker | U/Mobiles/Townfolk/Banker.cs:13 | Selected existing service type; keep its normal conditional stock behavior. |
| BaseEscortable | U/Mobiles/Townfolk/BaseEscortable.cs:21 | Behavior reference only; no slots of this type selected. |
| BaseGuard | U/Mobiles/Guards/BaseGuard.cs:11 | Behavior reference only; no slots of this type selected. |
| Blacksmith | U/Mobiles/Vendors/NPC/Blacksmith.cs:10 | Selected existing service type; keep its normal conditional stock behavior. |
| Bowyer | U/Mobiles/Vendors/NPC/Bowyer.cs:9 | Selected existing service type; keep its normal conditional stock behavior. |
| Carpenter | U/Mobiles/Vendors/NPC/Carpenter.cs:8 | Selected existing service type; keep its normal conditional stock behavior. |
| Cook | U/Mobiles/Vendors/NPC/Cook.cs:8 | Selected existing service type; keep its normal conditional stock behavior. |
| EvilHealer | U/Mobiles/Healers/EvilHealer.cs:6 | Behavior reference only; no slots of this type selected. |
| Farmer | U/Mobiles/Vendors/NPC/Farmer.cs:8 | Selected existing service type; keep its normal conditional stock behavior. |
| Fisherman | U/Mobiles/Vendors/NPC/Fisherman.cs:8 | Selected existing service type; keep its normal conditional stock behavior. |
| HarborMaster | U/Mobiles/Townfolk/HarborMaster.cs:7 | Behavior reference only; no slots of this type selected. |
| Healer | U/Mobiles/Healers/Healer.cs:6 | Selected existing service type; keep its normal conditional stock behavior. |
| InnKeeper | U/Mobiles/Vendors/NPC/InnKeeper.cs:7 | Selected existing service type; keep its normal conditional stock behavior. |
| Mage | U/Mobiles/Vendors/NPC/Mage.cs:8 | Selected existing service type; keep its normal conditional stock behavior. |
| Mapmaker | U/Mobiles/Vendors/NPC/Mapmaker.cs:7 | Selected existing service type; keep its normal conditional stock behavior. |
| Peasant | U/Mobiles/Townfolk/Peasant.cs:7 | Behavior reference only; no slots of this type selected. |
| Provisioner | U/Mobiles/Vendors/NPC/Provisioner.cs:7 | Selected existing service type; keep its normal conditional stock behavior. |
| Scribe | U/Mobiles/Vendors/NPC/Scribe.cs:9 | Selected existing service type; keep its normal conditional stock behavior. |
| Shipwright | U/Mobiles/Vendors/NPC/Shipwright.cs:8 | Selected existing service type; keep its normal conditional stock behavior. |
| Tailor | U/Mobiles/Vendors/NPC/Tailor.cs:9 | Selected existing service type; keep its normal conditional stock behavior. |
| Tinker | U/Mobiles/Vendors/NPC/Tinker.cs:7 | Selected existing service type; keep its normal conditional stock behavior. |
| WanderingHealer | U/Mobiles/Healers/WanderingHealer.cs:7 | Behavior reference only; no slots of this type selected. |
| WarriorGuard | U/Mobiles/Guards/WarriorGuard.cs:7 | Behavior reference only; no slots of this type selected. |

Behavior read directly: Banker derives from BaseVendor and supplies banking behavior. Healer derives from BaseHealer, has shop stock and checks resurrection eligibility; EvilHealer and WanderingHealer have different behavior and are not substitutes chosen by this draft. AnimalTrainer already owns stabling behavior, while `server/customizations/Services/Pet Training/AnimalTrainer.PetTraining.cs` adds pet-training integration; a stable job title alone is not that service. Shipwright and Mapmaker are existing trades; no galleon or facet-travel feature is implied. HarborMaster is a non-vendor BaseCreature, not a ready-made quest system, so Selda and Anwen remain proposed actors.

BaseGuard.cs:77-95,222-335 and WarriorGuard.cs:95-174 show why normal law guards cannot stand in for a physical garrison or hired opponent. Peasant.cs:7 and BaseEscortable.cs:21,199 show why an inert resident needs a deliberate actor choice rather than a generic Peasant spawn. Concrete class existence is source-verified; it is not a build or a runtime placement test.

Unverified: all stand tiles and Z values, building interiors, service-room capacity, dry-tile area, stock-comparable density, doors, ghost approaches, road and boat access, loaded maps, live law, safe separation of hostile and friendly areas, quest implementation, encounter balance, patrol performance, rewards, training windows and persistence. S10 must measure population per 100 dry tiles after selecting real placement polygons and reconciling stock. The approximate CSV boxes cannot supply that proof. Region-only civic roles remain proposals until the survey confirms their buildings.

## Completion review

Completed the draft rosters and reviewed the data against the author XML, P672 and the source type files. Document and data checks passed: 52 distinct location entries, 84 unique named slots with no double counting, 20 selected concrete service types, and all 32 P672 seed references accounted for. All primary Trammel TownRegion names have either a roster or an explicit retained-site disposition. Every recorded go-menu coordinate and region rectangle agrees with the source XML. Population sums, named-slot references, quest contacts and the civilian town service floors agree. All local Markdown links resolve; both files have no em dashes or trailing whitespace and are below 5 MB. Windows PowerShell 5.1.26100.9711 parsed the JSON successfully. No new test files or runtime tests were added; lane tests are none. These were source, data and document checks, not a build or playtest.

Only `notes/cc-P695-tools/rosters.json` and this note were added. The code work copy is clean. No code, docs/ files, map data, live configuration or services were changed. No Haven connection, build, deployment, commit, merge, push or branch change. No new art is required. Stop-request checks between steps found no request before completion.

P682 / S10 still owns real building surveys, placements, per-facet reconciliation, density and runtime proofs. Quest actors, physical guard implementation, encounter openings and fenced-land access remain with their owning build prompts; the draft is complete within P695's data-and-notes scope.

P695 DONE
