"""cc-P436 step 2: put every guild and League gump (step 1's table) on GuildStyledGump. Each declaration ": Gump" becomes
": GuildStyledGump"; a file that neither is in Server.Gumps nor uses it gets "using Server.Gumps;". Refuses a class it
does not find exactly once. Prints the list it changed (the list the test pins).
    python -P rebase_gumps.py           apply
    python -P rebase_gumps.py --list    print the classes only
"""
import os
import re
import sys

ROOT = r"D:\UO\golems\Iron\ShatteredLegacy\server\customizations"

# (file, class). Step 1's table, less LeagueShopGump (a scroll of its own: no frame, left alone) and the mule gumps
# beside GuildSchematicsGump (not guild menus).
GUMPS = [
    ("GuildMenuGump.cs", "GuildMenuGump"),
    ("MinersCompactLiaisonGump.cs", "MinersCompactLiaisonGump"),
    ("SmithGuildmasterGump.cs", "SmithGuildmasterGump"),
    ("SmithGuildmasterGump.cs", "SmithSealsInfoGump"),
    ("ForestersGuildmasterGump.cs", "ForestersGuildmasterGump"),
    ("ForestersLogbookGump.cs", "ForestersLogbookGump"),
    ("OutridersGuildmasterGump.cs", "OutridersGuildmasterGump"),
    ("OutridersCrook.cs", "CrookActionsGump"),
    ("ArtificersGuildmasterGump.cs", "ArtificersGuildmasterGump"),
    ("ArtificersImbueGump.cs", "ArtificersImbueGump"),
    ("ArtificersSatchel.cs", "ArtificersMasteryGump"),
    ("ArtificerWorkOrderSystem.cs", "ArtificerWorkOrderGump"),
    ("SanitationWardenGump.cs", "SanitationWardenGump"),
    ("GuildContractLedgerGump.cs", "GuildContractLedgerGump"),
    ("CrossGuildExchangeGump.cs", "CrossGuildExchangeGump"),
    ("SmithBulkOrderChoiceGump.cs", "SmithBulkOrderChoiceGump"),
    ("SmithCommissionGump.cs", "SmithCommissionGump"),
    ("SmithGuildBook.cs", "SmithGuildBookGump"),
    ("SmithSealCatalogGump.cs", "SmithSealCatalogGump"),
    ("ClusterFSmithBODPayout.cs", "SmithTurnInChoiceGump"),
    ("ClusterFSmithBODPayout.cs", "RegularSmithBulkOrderGump"),
    ("ClusterFGuildSystem.cs", "GuildProgressGump"),
    ("ClusterFGuildSystem.cs", "GuildTaskDetailGump"),
    ("ClusterFGuildStarterPath.cs", "GuildWelcomeGump"),
    ("ClusterFGuildStarterPath.cs", "GuildStarterItemsGump"),
    (os.path.join("Engines", "Craft", "GuildRecipeShopGump.cs"), "GuildRecipeShopGump"),
    (os.path.join("Mobiles", "Mule", "MuleModuleGumps.cs"), "GuildSchematicsGump"),
    ("LeagueRegistrarGump.cs", "LeagueRegistrarGump"),
    (os.path.join("LeagueRegister", "LeagueRegisterGump.cs"), "LeagueRegisterGump"),
    (os.path.join("LeagueRegister", "LeagueConsolidation.cs"), "CombinedLogbookGump"),
    (os.path.join("LeagueShop", "LeagueHall.cs"), "LeagueHallFacingGump"),
    (os.path.join("LeagueShop", "LeagueShopGumps.cs"), "LeagueShopConfirmGump"),
    (os.path.join("LeagueShop", "LeagueShopGumps.cs"), "LeagueHallGump"),
    (os.path.join("LeagueShop", "LeagueShopGumps.cs"), "LeagueTitleGump"),
]

if "--list" in sys.argv:
    print("\n".join(c for _, c in GUMPS))
    sys.exit(0)

texts = {}
for f, cls in GUMPS:
    path = os.path.join(ROOT, f)
    t = texts.get(path) or open(path, "rb").read().decode("utf-8")
    pat = re.compile(r"(\bclass %s\s*:\s*)Gump\b" % re.escape(cls))
    n = len(pat.findall(t))
    if n != 1:
        done = len(re.findall(r"\bclass %s\s*:\s*GuildStyledGump\b" % re.escape(cls), t))
        if done == 1:
            texts[path] = t
            continue
        sys.exit("FAIL %s: class %s : Gump found %d times" % (f, cls, n))
    texts[path] = pat.sub(r"\1GuildStyledGump", t)

for path, t in texts.items():
    if not re.search(r"^namespace Server\.Gumps\b", t, re.M) and not re.search(r"^\s*using Server\.Gumps;", t, re.M):
        # after the last top-level using
        usings = list(re.finditer(r"^using [^\n]*;\r?\n", t, re.M))
        nl = "\r\n" if "\r\n" in t else "\n"
        at = usings[-1].end() if usings else 0
        t = t[:at] + "using Server.Gumps;" + nl + t[at:]
    open(path, "wb").write(t.encode("utf-8"))
    print("ok", os.path.relpath(path, ROOT))
print(len(GUMPS), "classes")
