"""cc-P682: the red run's mutated copy of the spawn set, for tools/tests/test_sos_new_spawns.py.

    python -P mutate.py <scratch folder>      then SL_SHARD_REPO=<scratch folder> python tools/tests/test_sos_new_spawns.py

Copies the code copy's regions file and spawn set into <scratch folder>/server/data and breaks four facts' worth of it:
Hammerhill's Trammel banker removed (fact 2), a wild spawner moved into Valunstead's bank square (facts 1 or 3), a
held Dragon added to a wild spawner (fact 3), a keep garrison post dropped (fact 4).
"""
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402

dst = sys.argv[1]
src = os.path.join(common.SHARD, "server", "data")
os.makedirs(os.path.join(dst, "server", "data"), exist_ok=True)
shutil.copy(os.path.join(src, "regions-trammel.json"), os.path.join(dst, "server", "data"))
sp = os.path.join(dst, "server", "data", "Spawns")
shutil.rmtree(sp, ignore_errors=True)
shutil.copytree(os.path.join(src, "Spawns"), sp)
sos = os.path.join(sp, "sos")


def rw(rel, fn):
    p = os.path.join(sos, rel)
    d = json.load(open(p))
    d = fn(d)
    json.dump(d, open(p, "w"), indent=2)


rw("towns/Hammerhill.json", lambda d: [r for r in d if not (r["map"] == "Trammel" and r["entries"][0]["name"] == "Banker")])


def wild(d):
    d[0]["location"] = [484, 434, 15]
    d[1]["entries"].append({"name": "Dragon", "maxCount": 1, "probability": 100})
    return d


rw("wild/Islands.json", wild)
rw("keeps/FortWhitestone.json", lambda d: d[1:])
print("mutated copy at", dst)
