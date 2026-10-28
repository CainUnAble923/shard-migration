"""cc-P717 red run: a copy of the customizations probe.sh mounts (Tutorial/, CharacterCreation.cs, ClusterFDevTools.cs)
with one new behaviour put back to the old one, behind the new API so the new facts compile.
Usage: python -I mutate.py <src customizations dir> <dest dir> <mutant>"""
import os, shutil, sys

src, dest, name = sys.argv[1], sys.argv[2], sys.argv[3]

if os.path.exists(dest):
    shutil.rmtree(dest)
os.makedirs(dest)
shutil.copytree(os.path.join(src, "Tutorial"), os.path.join(dest, "Tutorial"))
for f in ("CharacterCreation.cs", "ClusterFDevTools.cs"):
    shutil.copy(os.path.join(src, f), os.path.join(dest, f))


def edit(path, old, new):
    p = os.path.join(dest, path)
    s = open(p, encoding="utf-8").read()
    assert s.count(old) == 1, (path, old[:60], s.count(old))
    open(p, "w", encoding="utf-8", newline="\n").write(s.replace(old, new))


START = "Tutorial/TutorialStart.cs"

if name == "nolock":  # P663: New Haven always offered, a New Haven pick skips
    edit(START, "ClusterFAccountPersistence.Get(account)?.HasFlag(HavenUnlockedFlag) == true;", "true;")
elif name == "forced":  # the list shows it locked, but a New Haven pick is still honoured
    edit(START, "        if (c == Choice.Haven && pm.Account is IAccount acct && !IsHavenUnlocked(acct))",
         "        if (false && c == Choice.Haven && pm.Account is IAccount acct && !IsHavenUnlocked(acct))")
elif name == "hidden":  # the locked list drops New Haven instead of showing it locked
    edit(START, "        cities[1] = new CityInfo(LockedHavenCity,", "        return [cities[0]];\n        cities[1] = new CityInfo(LockedHavenCity,")
elif name == "nostaff":  # staff get the locked list too
    edit(START, "account.AccessLevel >= AccessLevel.GameMaster || ", "")
elif name == "deleted":  # the unlock belongs to the character who earned it
    edit(START, "ClusterFAccountPersistence.Get(account)?.HasFlag(HavenUnlockedFlag) == true;",
         "ClusterFAccountPersistence.Get(account) is { } d && d.HasFlag(HavenUnlockedFlag) && "
         "World.FindMobile((Serial)d.Tutorial.CharacterSerial) is { Deleted: false };")
elif name == "nounlock":  # graduation and the skip set no flag
    edit(START, "ClusterFAccountPersistence.GetOrCreate(account).SetFlag(HavenUnlockedFlag);", "ClusterFAccountPersistence.GetOrCreate(account);")
elif name == "norelock":  # the reset keeps the unlock
    edit("ClusterFDevTools.cs", "            data.Flags.Clear();", "            data.Flags.RemoveWhere(f => f != Server.Tutorial.TutorialStart.HavenUnlockedFlag);")
elif name == "legacy":  # the first design: a finished record counts as unlocked too, which the reset cannot clear
    edit(START, "ClusterFAccountPersistence.Get(account)?.HasFlag(HavenUnlockedFlag) == true;",
         "ClusterFAccountPersistence.Get(account) is { } d && "
         "(d.HasFlag(HavenUnlockedFlag) || d.Tutorial.State is TutorialState.Graduated or TutorialState.Skipped || d.Tutorial.WasSkipped);")
elif name == "shared":  # every account gets the one shared list (pinned AccountHandler)
    edit("CharacterCreation.cs", "Server.Tutorial.ClusterFTutorial.Enabled ? Server.Tutorial.TutorialStart.Cities(account) : GetStartingCities();",
         "GetStartingCities();")
else:
    raise SystemExit("unknown mutant " + name)
