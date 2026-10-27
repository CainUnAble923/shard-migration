"""cc-P666: edits to the code copy's Tutorial files (Read is denied on the code copy in unattended runs)."""
import shutil
import sys

ROOT = 'D:/UO/golems/Iron/ShatteredLegacy/server/customizations/Tutorial/'
HERE = sys.argv[1]


def edit(name, pairs):
    p = ROOT + name
    t = open(p, 'rb').read().decode('utf-8')
    crlf = '\r\n' in t
    t = t.replace('\r\n', '\n')
    for old, new in pairs:
        assert t.count(old) == 1, (name, old[:80], t.count(old))
        t = t.replace(old, new)
    if crlf:
        t = t.replace('\n', '\r\n')
    open(p, 'wb').write(t.encode('utf-8'))


shutil.copyfile(HERE + '/TutorialPetCare.cs', ROOT + 'TutorialPetCare.cs')

edit('TutorialFarm.cs', [
    ('        public const string DoneLine = "You finished the farm lessons. If your bonded pet dies, bring its ghost to Tobin the vet beside me.";\n',
     '        public const string DoneLine = "You finished the farm lessons. If your bonded pet dies, bring its ghost to Tobin the vet beside me. While you are Young, he brings it back free.";\n'),
    ('''        public const string GhostPetLine = "Your pet has died. Wait for its body to disappear, then bring its ghost to Tobin the vet beside me.";
        public const string GhostPetNoVetLine = "Your pet has died. Wait for its body to disappear, then bring its ghost to the vet by the New Haven stables.";
''',
     '''        public const string GhostPetLine = "Your pet has died. Wait for its body to disappear, then bring its ghost to Tobin the vet beside me.";
        public const string GhostPetNoVetLine = "Your pet has died. Wait for its body to disappear, then bring its ghost to any town's vet.";
        // cc-P666: a Young owner's pet on the isle comes back at Tobin at once, free and whole (TutorialPetCare.IsleCare).
        public const string GhostPetYoungLine = "Your pet has died. Bring its ghost to Tobin the vet beside me. While you are Young, he brings it back free, with everything it carried.";
        // cc-P666: Sera, the healer at the shrine, points pet ghosts to Tobin too.
        public const string HealerGhostPetLine = "I heal people, not pets. Wait for your pet's body to disappear, then bring its ghost to Tobin the vet at the farm gate.";
        public const string HealerGhostPetYoungLine = "I heal people, not pets. Bring your pet's ghost to Tobin the vet at the farm gate. While you are Young, he brings it back free.";
'''),
    ('''        /// <summary>Says the dead pet line to its owner, unless said to them within the cooldown. True when it spoke.</summary>
        public static bool NoticeGhostPet(Mobile hand, BaseCreature pet)
''',
     '''        /// <summary>The dead pet line for this speaker (Wren, or Sera the healer) and this pet.</summary>
        public static string GhostPetLineFor(Mobile speaker, BaseCreature pet)
        {
            if (FindVet() == null)
            {
                return GhostPetNoVetLine;
            }

            var young = FoldMaps.IsFold(pet.Map) && pet.ControlMaster is PlayerMobile { Young: true };
            return speaker is TutorialHealer
                ? young ? HealerGhostPetYoungLine : HealerGhostPetLine
                : young ? GhostPetYoungLine : GhostPetLine;
        }

        /// <summary>Says the dead pet line to its owner, unless said to them within the cooldown. True when it spoke.</summary>
        public static bool NoticeGhostPet(Mobile hand, BaseCreature pet)
'''),
    ('            hand.SayTo(owner, FindVet() != null ? GhostPetLine : GhostPetNoVetLine);\n',
     '            hand.SayTo(owner, GhostPetLineFor(hand, pet));\n'),
    ('''            TutorialCoreTrials.FarmFinished(pm);
            return true;
''',
     '''            TutorialCoreTrials.FarmFinished(pm);
            ClusterFTutorial.SystemLine(pm, TutorialPetCare.FarmPetLessonLine); // cc-P666: the farm's pet lesson line
            return true;
'''),
])

edit('TutorialCorePlacement.cs', [
    ('''    public TutorialHealer() { Name = "Sera"; Title = "the tutorial healer"; CantWalk = true; }
''',
     '''    public TutorialHealer() { Name = "Sera"; Title = "the tutorial healer"; CantWalk = true; }
    // cc-P666: a dead bonded pet stepping near her gets the line pointing to Tobin (the Farmhand's cooldown, shared).
    public override void OnMovement(Mobile m, Point3D oldLocation)
    {
        base.OnMovement(m, oldLocation);
        if (m is BaseCreature { IsDeadBondedPet: true } pet && InRange(pet, 4)) { TutorialFarm.NoticeGhostPet(this, pet); }
    }
'''),
])
print('ok')
