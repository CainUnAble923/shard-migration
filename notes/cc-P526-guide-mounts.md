# P526: mounts guide sources and open questions

The [player guide draft](wiki-drafts/mounts.md) covers ordinary mounts, P277's red riding dragon, P365's reward mounts, veteran figurines, and related mule and boss rewards.

Full source paths, line evidence, roster, and verification are in [the P526 lane notes](cc-P526-guide-mounts-and-reward-mounts.md). That longer filename is the Golem's designated notes artifact; this file satisfies the task body's shorter filename too.

Primary evidence: canonical `server/customizations/Mobiles/Mounts/RideableDragons.cs`, `RewardMounts.cs`, `RewardMountStatuette.cs`, `ClusterFAchievements.cs`, `LeagueShop/LeagueShop.cs`, and `LootBoxes/`, checked against pinned ModernUO commit `d4531cd94b739613155225c234900de9f47d2c88` for stock mounts, spawn definitions, riding rules, and veteran rewards. Implementation context: [P277](cc-P277-rideable-red-dragon.md) and [P365](cc-P365-reward-mounts-and-evo-stages.md).

Open publication questions: running build and package availability; final P365 routes, prices, and stats; a player source for high-tier Tamer boxes; the previously reported Boss box award failure; rewards for accounts that already earned the achievements; the dragon's future player route; live wild spawns, encounter access, faction vendors, and veteran settings. These are recorded without blocking a labeled draft or changing code.

Documentation review complete: source roster coverage, relative links, plain American English, no em dashes, whitespace, size, and repository scope checked. No tests or code build required for this task.

P526 DONE
