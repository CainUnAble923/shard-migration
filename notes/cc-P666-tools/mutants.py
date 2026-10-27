"""cc-P666 red run: the stubbed old Tutorial folder (red-old) and the two mutants of the new TutorialPetCare.cs.
Run from the scratchpad that holds orig-Tutorial (a copy of Tutorial before the change); see probe.sh."""
import shutil
import sys

s = sys.argv[1]


def edit(p, pairs):
    t = open(p, 'rb').read().decode('utf-8'); crlf = '\r\n' in t; t = t.replace('\r\n', '\n')
    for o, n in pairs:
        assert t.count(o) == 1, (p, o); t = t.replace(o, n)
    if crlf: t = t.replace('\n', '\r\n')
    open(p, 'wb').write(t.encode('utf-8'))


shutil.rmtree(s + '/red-old', ignore_errors=True)
shutil.copytree(s + '/orig-Tutorial', s + '/red-old')
edit(s + '/red-old/TutorialPetCare.cs', [('        public const string IfYourPetDiesLine =',
    '        // cc-P666 red-run stubs\n        public const string IsleRevivedLine = "Your pet is alive again, with everything it carried.";\n        public const string FarmPetLessonLine = "If your pet dies, bring its ghost to a vet. stub";\n\n        public const string IfYourPetDiesLine =')])
edit(s + '/red-old/TutorialFarm.cs', [('        private static readonly Dictionary<Serial, DateTime> _ghostPetSaid = new();\n',
    '        private static readonly Dictionary<Serial, DateTime> _ghostPetSaid = new();\n        // cc-P666 red-run stubs: today\'s choice of line, for every speaker.\n        public const string GhostPetYoungLine = "stub young";\n        public const string HealerGhostPetLine = "stub healer";\n        public const string HealerGhostPetYoungLine = "stub healer young Tobin";\n        public static string GhostPetLineFor(Mobile speaker, BaseCreature pet) => FindVet() != null ? GhostPetLine : GhostPetNoVetLine;\n')])
for name, old, new in [('everywhere', 'FoldMaps.IsFold(vet.Map) && pet.Map == vet.Map', 'pet.Map == vet.Map'),
                       ('anyowner', 'pet.ControlMaster is PlayerMobile { Young: true }', 'pet.ControlMaster is PlayerMobile')]:
    d = s + '/m-' + name; shutil.rmtree(d, ignore_errors=True)
    shutil.copytree('D:/UO/golems/Iron/ShatteredLegacy/server/customizations/Tutorial', d)
    edit(d + '/TutorialPetCare.cs', [(old, new)])
print('ok')
