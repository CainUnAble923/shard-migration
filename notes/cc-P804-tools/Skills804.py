# cc-P804: the skills window with the Miscellaneous group open, in TazUO on the private proof shard.
import API
import System
from System.Reflection import Assembly, BindingFlags

LOG = r"D:\UO\golems\Iron\p740-proof\walk.log"
SIG = r"D:\UO\golems\Iron\p740-proof\shots.sig"
F = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static | BindingFlags.Instance


def say(text):
    with open(LOG, "a") as f:
        f.write(text + "\n")


def sig(line):
    with open(SIG, "a") as f:
        f.write(line + "\n")


if API.Player.Name != "Iron Skills":
    API.Stop()
open(LOG, "w").close()
API.Pause(7)
API.Msg("[self set Skills.Herbalism.Base 30")
API.Pause(1.5)
asm = Assembly.GetEntryAssembly()
game = asm.GetType("ClassicUO.Client").GetProperty("Game", F).GetValue(None)
uo = game.GetType().GetProperty("UO", F).GetValue(game)
world = uo.GetType().GetProperty("World", F).GetValue(uo)
actions = asm.GetType("ClassicUO.Game.GameActions").GetMethod("OpenSkills", F)
actions.Invoke(None, System.Array[System.Object]([world]))
API.Pause(3)
ui = asm.GetType("ClassicUO.Game.Managers.UIManager")
gumps = ui.GetProperty("Gumps", F).GetValue(None)
# Rig only, in memory: the window scrolls and clicks do not reach it, so its list is cut to the Miscellaneous group's Herbalism row.
groups = world.GetType().GetProperty("SkillsGroupManager", F).GetValue(world).Groups
for g in groups:
    for i in range(58):
        g.Remove(System.Byte(i))
for g in list(gumps):
    if g.GetType().Name == "StandardSkillsGump":
        g.Dispose()
API.Pause(1.5)
actions.Invoke(None, System.Array[System.Object]([world]))
API.Pause(3)
gumps = ui.GetProperty("Gumps", F).GetValue(None)
for g in list(gumps):
    if g.GetType().Name == "StandardSkillsGump":
        controls = g.GetType().GetField("_skillsControl", F).GetValue(g)
        first = list(controls)[0]
        first.GetType().GetProperty("IsMinimized", F).SetValue(first, False)
        say("opened the first group")
    elif "Bulletin" in g.GetType().Name or g.GetType().Name == "Gump":
        g.Dispose()
for x in API.GetAllGumps():
    try:
        if x.PacketGumpText:
            x.Dispose()
    except Exception:
        pass
API.Pause(3)
sig("SHOT skills-window")
API.Pause(3)
sig("END")
say("done")
