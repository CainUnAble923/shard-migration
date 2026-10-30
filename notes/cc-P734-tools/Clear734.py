# cc-P734 (P724's Clear724.py): closes the server's login windows (patch notes, achievements) so the shot shows the
# build, then stays idle.
import API

for _ in range(4):
    API.Pause(3)
    for g in API.GetAllGumps():
        try:
            g.Dispose()
        except Exception:
            pass
