# cc-P844 (P823 s Clear823.py, P817 s Clear817.py, P741's, P733's): close the windows the login opens (paperdoll, TazUO's Version History,
# the backpack, the server's patch notes and achievements), so the shot shows the isle. P817's outside shot kept the
# paperdoll and Version History: they can open after the first pass, so this keeps closing for about 30 s.
import API

API.Pause(4)
for _ in range(10):
    for i in range(6):
        API.CloseGump()
        API.Pause(0.2)
    for g in API.GetAllGumps():
        try:
            g.Dispose()
        except Exception:
            pass
    API.Pause(1.5)
