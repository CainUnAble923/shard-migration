"""cc-P707 run 4: the heal step, when a bandage finds nobody hurt. A trainee's hits come back by themselves within the
bandage's delay, so the bandage ended on a full patient (pinned's "veil of death" cliloc) and the trainee had to know to
ask Wren again. TutorialFarm.Unhurt: on step 3 it gives the scratch there and then and says to bandage again.

    python -P edit_unhurt.py <code repo>
"""
import os
import sys

repo = sys.argv[1]
path = os.path.join(repo, 'server', 'customizations', 'Tutorial', 'TutorialFarm.cs')
text = open(path, 'rb').read().decode('utf-8')
nl = '\r\n' if '\r\n' in text else '\n'


def sub(old, new):
    global text
    old, new = old.replace('\n', nl), new.replace('\n', nl)
    assert text.count(old) == 1, old[:70]
    text = text.replace(old, new)


sub('''        public const string NoMoreBandagesLine =''',
    '''        // cc-P707 run 4: said when a bandage on the heal step finds nobody hurt (the trainee's hits came back by themselves).
        public const string ScratchAgainLine = "A rat nipped your ankle in the rows. Double-click a bandage again, then click yourself to treat it.";
        public const string NoMoreBandagesLine =''')

sub('''            SureHeal = (healer, _) => healer is PlayerMobile pm && StepOf(pm) == 3; // cc-P707
        }''', '''            SureHeal = (healer, _) => healer is PlayerMobile pm && StepOf(pm) == 3; // cc-P707
            Unhurt = OnUnhurt; // cc-P707 run 4
        }''')

sub('''        public static Func<Mobile, Mobile, bool>? SureHeal { get; set; }
''', '''        public static Func<Mobile, Mobile, bool>? SureHeal { get; set; }

        /// <summary>
        /// cc-P707 run 4: asked by Bandage-tutorial-real-heal.patch when a bandage finds its patient unhurt, as it begins
        /// ("That being is not damaged!") or as it ends (the hits came back meanwhile). True when the farm handled it
        /// instead: the trainee got a scratch and was told to bandage again, and pinned's message and the Placebo
        /// achievement are skipped.
        /// </summary>
        public static Func<Mobile, Mobile, bool>? Unhurt { get; set; }
''')

sub('''        public static bool OnHealed(PlayerMobile pm)''', '''        // Step 3, a bandage on an unhurt patient: the trainee or one of their pets. Scratch refuses while anyone is hurt.
        public static bool OnUnhurt(Mobile healer, Mobile patient)
        {
            if (healer is not PlayerMobile pm || StepOf(pm) != 3 ||
                patient != pm && (patient as BaseCreature)?.ControlMaster != pm || !Scratch(pm))
            {
                return false;
            }

            pm.SendMessage(ScratchAgainLine);
            return true;
        }

        public static bool OnHealed(PlayerMobile pm)''')

open(path, 'wb').write(text.encode('utf-8'))
print('edited', path)
