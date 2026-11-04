# cc-P793: the one-off edits to existing files, each refused unless its old text occurs exactly once; then the shard
# data row and ShrinkTable-shard-rows.patch made with diff -u against pinned. python -P apply_edits.py
import os
import subprocess
import tempfile
from pathlib import Path

CODE = Path("D:/UO/golems/Iron/ShatteredLegacy")
PINNED = "D:/UO/ModernUO-pinned"


def edit(rel, old, new):
    p = CODE / rel
    s = p.read_bytes().decode("utf-8")
    assert s.count(old) == 1, rel
    p.write_bytes(s.replace(old, new).encode("utf-8"))


edit(
    "server/customizations/Mobiles/Evo/ShardBodyTypes.cs",
    """(cc-P365: the evo dog's top stage (kr-wolf; actions 0-10 and 12))")\n""",
    """(cc-P365: the evo dog's top stage (kr-wolf; actions 0-10 and 12))"),
            // cc-P793: the client's Bird_Peacock_Mount. bodyTable.cfg has no row for it (Empty); mobtypes.txt says ANIMAL.
            (1440, BodyType.Animal, "peacock (cc-P793: the tamable mount)")\n""",
)
edit(
    "server/customizations/Services/Pet Training/PetTrainingHelper.cs",
    """        new("Phoenix", Class.MagicalAndClawed,""",
    """        new("Peacock", Class.Clawed, MagicalAbility.StandardClawedOrTailed, SpecialAbilityClawed, WepAbility1, AreaEffectNone, 1, 3), // cc-P793: the ostards' row
        new("Phoenix", Class.MagicalAndClawed,""",
)
edit(
    "docker/uo/Dockerfile",
    "COPY server/data/treasure.cfg /build/modernuo/Distribution/Data/treasure.cfg\n",
    """COPY server/data/treasure.cfg /build/modernuo/Distribution/Data/treasure.cfg
# cc-P793: the shard's rows on top of pinned's shrink.json (a body's figurine), read by ShrinkTable-shard-rows.patch.
COPY server/data/shrink.json /build/modernuo/Distribution/Data/ShatteredLegacy/shrink.json\n""",
)
edit(
    "docker/uo/apply-patches.sh",
    'apply_patch "$PATCHES/Beekeeper-beekeeping.patch"\n',
    """apply_patch "$PATCHES/Beekeeper-beekeeping.patch"

# cc-P793: Data/ShatteredLegacy/shrink.json adds rows to pinned's Data/shrink.json (Distribution/Data stays pinned), so a body
# pinned has no figurine for gets one wherever pinned looks one up (the leash, Tracking, a pet's trade). ShrinkTable keeps its
# table private and sized to the file, so writing into it from outside would mean rebuilding it by reflection. Made with
# diff -u against pinned; pinned by PeacockVerification.
apply_patch "$PATCHES/ShrinkTable-shard-rows.patch"\n""",
)

(CODE / "server/data/shrink.json").write_bytes(b'{\n  "0x05a0": "0xA0C0"\n}\n')

REL = "Projects/UOContent/Misc/ShrinkTable.cs"
src = subprocess.run(["git", "-C", PINNED, "show", "HEAD:" + REL], capture_output=True, check=True).stdout.decode("utf-8")
OLD = """                throw new JsonException($"Failed to deserialize {path}.");
            }

            var length = 0;
"""
NEW = """                throw new JsonException($"Failed to deserialize {path}.");
            }

            // cc-P793: the shard's rows, on top of pinned's.
            var shardPath = "Data/ShatteredLegacy/shrink.json";
            var shardRows = JsonConfig.Deserialize<Dictionary<string, string>>(shardPath);
            if (shardRows == null)
            {
                throw new JsonException($"Failed to deserialize {shardPath}.");
            }

            foreach (var (body, item) in shardRows)
            {
                table[body] = item;
            }

            var length = 0;
"""
assert src.count(OLD) == 1
with tempfile.TemporaryDirectory() as w:
    for side, text in (("a", src), ("b", src.replace(OLD, NEW))):
        f = Path(w) / side / REL
        f.parent.mkdir(parents=True)
        f.write_bytes(text.encode("utf-8"))
    d = subprocess.run(["diff", "-u", "a/" + REL, "b/" + REL], cwd=w, capture_output=True).stdout.decode("utf-8")
    lines = d.split("\n")
    lines[0] = lines[0].split("\t")[0]
    lines[1] = lines[1].split("\t")[0]
    out = "\n".join(lines)
    (CODE / "server/patches/ShrinkTable-shard-rows.patch").write_bytes(out.encode("utf-8"))
    r = subprocess.run(["patch", "-p1", "--fuzz=0", "--dry-run", "-i", str(CODE / "server/patches/ShrinkTable-shard-rows.patch")], cwd=os.path.join(w, "a"), capture_output=True, text=True)
    print(r.stdout, r.stderr, r.returncode)
