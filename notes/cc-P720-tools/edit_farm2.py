"""cc-P720 item 6: TutorialFarm.cs. The farmhouse's brass sign (the cottage multi's own) is named, so a click shows it."""
import sys

p = sys.argv[1] + '/server/customizations/Tutorial/TutorialFarm.cs'
s = open(p, encoding='utf-8').read()


def rep(old, new):
    global s
    assert s.count(old) == 1, (old[:80], s.count(old))
    s = s.replace(old, new)


rep('''        public const string GateSignpostName = "Farm signpost: Wren the Farmhand at the gate";
''', '''        public const string GateSignpostName = "Farm signpost: Wren the Farmhand at the gate";

        // cc-P720 item 6: the farmhouse's own sign (the cottage multi's brass sign, on its hanger by the steps)
        public const int HouseSignId = 0x0BD2;
        public const string HouseSignName = "Wren's farmhouse";
''')
rep('''                    c.Name = TutorialFarm.GateSignpostName; // cc-P718
                }
''', '''                    c.Name = TutorialFarm.GateSignpostName; // cc-P718
                }
                else if (art == TutorialFarm.HouseSignId)
                {
                    c.Name = TutorialFarm.HouseSignName; // cc-P720
                }
''')
open(p, 'w', encoding='utf-8', newline='').write(s)
print('edited', p)
