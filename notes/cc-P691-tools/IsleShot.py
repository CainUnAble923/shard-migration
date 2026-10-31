# cc-P720: a still shot's helper, run by TazUO in the world: closes the windows the login opens (patch notes,
# paperdoll and the like, last first) so the shot shows the isle.
import API

API.Pause(5)
for i in range(6):
    API.CloseGump()
    API.Pause(0.3)
