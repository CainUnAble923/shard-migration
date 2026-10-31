# cc-P741 (P733s Clear733.py): close the windows the login opens, so the shot shows the isle.
# (paperdoll, TazUO's page, the backpack: last first) and the server's (patch notes, achievements), so the shot shows the isle.
import API

API.Pause(5)
for _ in range(3):
    for i in range(6):
        API.CloseGump()
        API.Pause(0.3)
    for g in API.GetAllGumps():
        try:
            g.Dispose()
        except Exception:
            pass
    API.Pause(2)
