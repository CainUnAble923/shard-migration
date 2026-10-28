def edit(p, pairs):
    s = open(p, encoding="utf-8").read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old[:60], s.count(old))
        s = s.replace(old, new)
    open(p, "w", encoding="utf-8", newline="").write(s)


C = "D:/UO/golems/Iron/ShatteredLegacy/server/customizations/Tutorial/TutorialFarm.cs"
T = "D:/UO/golems/Iron/ShatteredLegacy/server/tests/Tutorial/TutorialIsleBandageWaitVerification.cs"
edit(C, [
("""            BandageSeconds = IsleSeconds; // cc-P721""", """            BandageSeconds = IsleSeconds; // cc-P721
            // cc-P721: pinned's Trammel rules refuse a player's beneficial act on an uncontrolled creature ("Players
            // cannot heal uncontrolled mobiles", Notoriety.Mobile_AllowBeneficial), the isle uses Trammel's rules, and
            // Pip is one: the bandage was refused (the P721 bot run). Pip alone is let through; everything else is pinned's.
            var inner = Mobile.AllowBeneficialHandler;
            Mobile.AllowBeneficialHandler = (from, target) => AllowBeneficial(from, target, inner);"""),
("""        /// <summary>A trainee on the Wakening Isle (or a copy of it).</summary>""", """        /// <summary>cc-P721: Pip may be bandaged; every other beneficial act is <paramref name="inner"/>'s (pinned's) to judge.</summary>
        public static bool AllowBeneficial(Mobile from, Mobile target, AllowBeneficialHandler? inner) =>
            target is TutorialWoundedHelper || (inner?.Invoke(from, target) ?? true);

        /// <summary>A trainee on the Wakening Isle (or a copy of it).</summary>"""),
])
edit(T, [
("""        Assert.True(p.Pm.CanBeBeneficial(pip, false, true)); // a bandage may be used on him (P721 bot run: it was refused)""",
 """        // A bandage may be used on him: pinned's Trammel rule refuses an uncontrolled creature (the P721 bot run's
        // "You cannot perform beneficial acts on your target"), and the farm lets Pip, and only Pip, through.
        Assert.False(Notoriety.Mobile_AllowBeneficial(p.Pm, pip));
        Assert.True(TutorialFarm.AllowBeneficial(p.Pm, pip, Notoriety.Mobile_AllowBeneficial));
        var rat = p.Add(new FarmRat());
        rat.MoveToWorld(pip.Location, pip.Map);
        Assert.False(TutorialFarm.AllowBeneficial(p.Pm, rat, Notoriety.Mobile_AllowBeneficial));"""),
])
print("ok")
