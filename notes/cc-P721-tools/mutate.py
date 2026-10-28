"""cc-P721 red run: a copy of the customizations probe.sh mounts (Tutorial/, Fold/, LeagueRegistrar.cs, ClusterFSkillGain.cs)
with the behaviour before P721 put back behind the new API, so the new facts compile.
  old:    every item at once (each new fact must fail for its own reason)
  benef:  pinned's beneficial rule alone (bandages refused on Pip)
  nopace: the isle's gain pace off (P718's, which the Focus and Meditation fact checks)
Usage: python -I mutate.py <src customizations dir> <dest dir> <old|nopace>"""
import os, shutil, sys

src, dest, name = sys.argv[1], sys.argv[2], sys.argv[3]
if os.path.exists(dest):
    shutil.rmtree(dest)
os.makedirs(dest)
for d in ("Tutorial", "Fold"):
    shutil.copytree(os.path.join(src, d), os.path.join(dest, d))
for f in ("LeagueRegistrar.cs", "ClusterFSkillGain.cs"):
    shutil.copy(os.path.join(src, f), os.path.join(dest, f))


def edit(path, old, new):
    p = os.path.join(dest, path)
    s = open(p, encoding="utf-8").read()
    assert s.count(old) == 1, (path, old[:70], s.count(old))
    open(p, "w", encoding="utf-8", newline="\n").write(s.replace(old, new))


F, V = "Tutorial/TutorialFarm.cs", "Tutorial/TutorialVisionScene.cs"
if name == "old":
    # 1. Pinned's delay; no wait or fumble words.
    edit(F, "            healer == patient && IsleTrainee(healer) ? Math.Min(seconds, IsleSelfBandageSeconds) : seconds;", "            seconds;")
    edit(F, 'public const string WaitLine = "A bandage takes a few seconds.', 'public const string WaitLine = "" + "A bandage takes a few seconds.')
    edit(F, 'public const string WaitLine = "" + "A bandage takes a few seconds. You will see \'You begin applying the bandages\': stand still and wait until \'You finish applying the bandages\'. A bandage that heals finishes this step.";',
         'public const string WaitLine = "A bandage that heals finishes this step.";')
    edit(F, 'public const string FumbleLine = "You fumble the bandage. Try again: double-click a bandage, then click your patient.";', 'public const string FumbleLine = "";')
    # 2. A patient who heals by himself; an unhurt trainee gets the old scratch.
    edit(F, "        public override bool CanRegenHits => false;", "")
    edit(F, "            if (FindPip(pm.Map) is { } pip)\n            {\n                pm.SendMessage(PipNotYouLine);", "            if (false && FindPip(pm.Map) is { } pip)\n            {\n                pm.SendMessage(PipNotYouLine);")
    # 3. No words on dying.
    edit("Tutorial/TutorialDeathHelp.cs", "        if (pm.Alive || !TutorialWorld.IsOnIsle(pm)", "        if (true || pm.Alive || !TutorialWorld.IsOnIsle(pm)")
    # 5. The old opening: dim, no braziers, the Stranger already beside the Gem, 45 s.
    edit(V, "    public const int Length = 61;", "    public const int Length = 45;")
    edit(V, "    public const int Lit = 6;", "    public const int Lit = 18;")
    edit(V, "                s.Stranger = Figure(s, TutorialVisionFigure.Stranger(), At(s, 6, -1), Direction.West);", "                s.Stranger = Figure(s, TutorialVisionFigure.Stranger(), At(s, 3, -1), Direction.West);")
    edit(V, "                Place(s, new TutorialVisionProp(BrazierId) { Name = \"a brazier\", Light = LightType.Circle300 }, At(s, 1, -3));\n", "")
    edit(V, "                Place(s, new TutorialVisionProp(BrazierId) { Name = \"a brazier\", Light = LightType.Circle300 }, At(s, 3, -3));\n", "")
    edit(V, "                    var to = At(s, 6 - (s.Second - Beats.Walk + 1), -1);", "                    var to = walker.Location;")
    edit(V, "                if (s.Stranger is { Deleted: false } facer) { facer.Direction = Direction.Up; }", "")
    # 6. No wake-up.
    edit("Tutorial/TutorialStart.cs", "        if (wake)\n        {\n            TutorialWake.Play(pm, FirstLines);", "        if (false)\n        {\n            TutorialWake.Play(pm, FirstLines);")
    # 7. No weapon or war mode, no strike needed.
    edit(F, "            Has(pm, FollowKey) && Has(pm, GuardKey) && Has(pm, WeaponKey) && Has(pm, WarKey);", "            Has(pm, FollowKey) && Has(pm, GuardKey);")
    edit(F, "            if (!_struck.Contains(pm.Serial))\n            {\n                ClusterFTutorial.SystemLine(pm, StrikeLine);", "            if (false)\n            {\n                ClusterFTutorial.SystemLine(pm, StrikeLine);")
    edit(F, "        public override int AosStrengthReq => 10;", "")
elif name == "benef":
    # P721's first Pip: pinned's beneficial rule alone, which refuses a bandage on him (the bot run).
    edit(F, "            target is TutorialWoundedHelper || (inner?.Invoke(from, target) ?? true);", "            inner?.Invoke(from, target) ?? true;")
elif name == "nopace":
    edit("Tutorial/TutorialSkillPace.cs", "        !Applies(m) || !_last.TryGetValue", "        true || !_last.TryGetValue")
else:
    raise SystemExit("unknown mutant " + name)
