# cc-P707: the vision shot's trigger, run by TazUO itself (Data\lscript.json starts it in the world). The trainee stands at
# the standing stones with the loop lesson next: the first double-click on the blue rune stone starts the lesson, the
# second plays the vision (TutorialCoreTrials.WatchVision), as a player would do it.
import API

API.Pause(6)
stones = API.GetItemsOnGround(5, 0x1F14)
if stones:
    API.SysMsg("IsleVision: rune stone " + hex(stones[0].Serial))
    API.UseObject(stones[0].Serial)
    API.Pause(2.5)
    API.UseObject(stones[0].Serial)
else:
    API.SysMsg("IsleVision: no rune stone within 5 tiles")
