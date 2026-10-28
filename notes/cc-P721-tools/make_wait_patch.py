"""cc-P721: writes server/patches/Bandage-tutorial-wait-lines.patch from the Bandage.cs the build has after every other
Bandage patch (taken from sl-uo-builder:cc-P717), with diff -u, so it applies at --fuzz=0 after Bandage-asclepius-bonus.
Three hooks into TutorialFarm: the delay (BandageSeconds), the start (BandageBegun) and a failed roll (BandageFumbled)."""
import os, subprocess, sys

S = os.path.dirname(os.path.abspath(__file__))
rel = "Projects/UOContent/Items/Skill Items/Misc/Bandage.cs"
a = os.path.join(S, "bd", "a", rel)
b = os.path.join(S, "bd", "b", rel)
os.makedirs(os.path.dirname(b), exist_ok=True)
s = open(a, encoding="utf-8", newline="").read()


def rep(old, new):
    global s
    assert s.count(old) == 1, old[:60]
    s = s.replace(old, new)


rep("""            else
            {
                healerNumber = 500968; // You apply the bandages, but they barely help.
                playSound = false;
            }""", """            else
            {
                healerNumber = 500968; // You apply the bandages, but they barely help.
                playSound = false;
                // Shattered Legacy (cc-P721): on the Wakening Isle a trainee is told plainly that the roll failed.
                Server.Tutorial.TutorialFarm.BandageFumbled?.Invoke(Healer, Patient);
            }""")
rep("""            context?.StopHeal();
            seconds *= 1000;""", """            context?.StopHeal();
            // Shattered Legacy (cc-P721): a trainee on the Wakening Isle bandages themselves faster (TutorialFarm).
            seconds = Server.Tutorial.TutorialFarm.BandageSeconds?.Invoke(healer, patient, seconds) ?? seconds;
            seconds *= 1000;""")
rep("""            healer.SendLocalizedMessage(500956); // You begin applying the bandages.
            return context;""", """            healer.SendLocalizedMessage(500956); // You begin applying the bandages.
            // Shattered Legacy (cc-P721): on the Wakening Isle, how long to wait, and a cue over the trainee's head.
            Server.Tutorial.TutorialFarm.BandageBegun?.Invoke(healer, patient, seconds / 1000);
            return context;""")
open(b, "w", encoding="utf-8", newline="").write(s)
os.chdir(os.path.join(S, "bd"))
out = subprocess.run(["diff", "-u", "a/" + rel, "b/" + rel], capture_output=True, text=True).stdout
lines = out.split("\n")
lines[0] = '--- "a/' + rel + '"'
lines[1] = '+++ "b/' + rel + '"'
open(sys.argv[1], "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print("ok", len(lines))
