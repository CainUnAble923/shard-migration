# cc-P794: one mutant per rule of the reward routes, each undoing that rule, for the red-first check.
# Usage: python -P mutate794routes.py <server/customizations> <out folder>
# Each mutant folder holds all three route files, one of them changed.
import shutil
import sys
from pathlib import Path

src = Path(sys.argv[1])
out = Path(sys.argv[2])

FILES = {
    "EtherealLooks.cs": src / "Mobiles" / "Mounts" / "EtherealLooks.cs",
    "ClusterFAchievements.cs": src / "ClusterFAchievements.cs",
    "LeagueShop.cs": src / "LeagueShop" / "LeagueShop.cs",
}
LOOKS, ACH, SHOP = FILES

# name: (file, old, new): the old text must occur exactly once.
MUTANTS = {
    # No shop rows at all.
    "norows": (SHOP, "        .. EtherealLooks.ShopRows()", ""),
    # A wrong price.
    "wrongprice": (LOOKS, '"Mount: ethereal peacock", 1500)', '"Mount: ethereal peacock", 1400)'),
    # The row is not kind Mount, so a box can draw it.
    "boxable": (LOOKS, "ap, renown, LeagueShopKind.Mount,", "ap, renown, LeagueShopKind.Decor,"),
    # A row hands over the wrong look.
    "wrongrow": (LOOKS, '("tiger", typeof(EtherealTiger),', '("tiger", typeof(EtherealLightTiger),'),
    # The prices ignore the settings.
    "apfixed": (LOOKS, "Math.Max(0, ServerConfiguration.GetOrUpdateSetting(ShopApSetting, DefaultShopAp))", "DefaultShopAp"),
    "renownfixed": (LOOKS, "Math.Max(0, ServerConfiguration.GetOrUpdateSetting(RenownSettingPrefix + look.Key, look.Renown))", "look.Renown"),
    # Nothing marks a payment, so every login pays again.
    "nomark": (LOOKS, "            ClusterFAchievementSystem.AddToCounter(acct.Username, paid, 1);\n", ""),
    # The mark is not read.
    "noread": (LOOKS, " ||\n                ClusterFAchievementSystem.GetCounter(acct.Username, paid) > 0", ""),
    # It pays whether or not it was earned.
    "unearned": (LOOKS, "!ClusterFAchievementSystem.HasEarned(acct, achievement) ||\n", "false ||\n"),
    # No hand-over at login, so a past earner is never paid.
    "nologin": (ACH, "        Server.Mobiles.EtherealLooks.PayOwed(pm);\n", ""),
    # No payment at the moment of earning.
    "nograntpay": (ACH, "                Server.Mobiles.EtherealLooks.PayOwed(online);\n", "                _ = online;\n"),
    # The ordinary reward pays too, so an online earner gets two.
    "double": (ACH, "            if (Server.Mobiles.EtherealLooks.PaysOnce(type)) continue; // cc-P794: TryGrant and the login pay these\n", ""),
    # An achievement names no look.
    "noreward": (ACH, "            rewardItems:     new[] { typeof(Server.Mobiles.EtherealBoura) }, // cc-P794: an ethereal look (EtherealLooks.PayOwed)\n", ""),
}

texts = {name: path.read_bytes().decode("utf-8") for name, path in FILES.items()}

if out.exists():
    shutil.rmtree(out)


def write(folder, changed=None, text=None):
    folder.mkdir(parents=True)
    for name, body in texts.items():
        (folder / name).write_bytes((text if name == changed else body).encode("utf-8"))


write(out / "_base")
for mutant, (name, old, new) in MUTANTS.items():
    body = texts[name]
    if "\r\n" in body:
        old = old.replace("\n", "\r\n")
        new = new.replace("\n", "\r\n")
    assert body.count(old) == 1, (mutant, body.count(old))
    write(out / mutant, name, body.replace(old, new))
print(len(MUTANTS), "mutants in", out)
