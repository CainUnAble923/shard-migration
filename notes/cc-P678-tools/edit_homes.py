r"""cc-P678: write out/homes.csv into the code: ClusterFNewHavenSeeder.Entries, GuildLocations, Appraiser's office post.
    python -P edit_homes.py
"""
import csv, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "D:/UO/golems/Iron/ShatteredLegacy/server/customizations/"
rows = list(csv.DictReader(open(os.path.join(HERE, "out", "homes.csv"))))
seed = {r["name"]: r for r in rows if r["kind"] == "seed"}
office = next(r for r in rows if r["kind"] == "office")
seed["League Registrar"] = office

# 1. the seeder
p = CODE + "ClusterFNewHavenSeeder.cs"
s = open(p, encoding="utf-8").read()
pat = re.compile(r'new(?: SeedEntry)?\("(?P<name>[^"]+)", "(?P<area>[^"]+)", (?P<mid>typeof\([^)]*\), \(\) => new [A-Za-z]+\(\)), '
                 r'(?P<x>\d+), (?P<y>\d+), Direction\.(?P<dir>\w+), (?P<z>-?\d+)\)(?P<was>\.WasAt\([^)]*\))?')
done = set()
def sub(m):
    r = seed.get(m.group("name"))
    if r is None:
        return m.group(0)
    done.add(m.group("name"))
    d = "South"
    return 'new("%s", "%s", %s, %s, %s, Direction.%s, %s)' % (m.group("name"), r["building"], m.group("mid"), r["x"], r["y"], d, r["z"])
s2 = pat.sub(sub, s)
missing = set(seed) - done
if missing:
    raise SystemExit("seeder: not found %s" % missing)
open(p, "w", encoding="utf-8", newline="").write(s2)

# 2. guild posts
p = CODE + "ClusterFGuildStarterPath.cs"
s = open(p, encoding="utf-8").read()
guild = {r["name"]: r for r in rows if r["kind"] in ("guild", "stock", "inst")}
look = {r["name"]: r for r in rows if r["kind"] == "lookout"}
gpat = re.compile(r'new\((?P<key>"[a-z]+"|ClusterFAlembicGuild\.Key), *"(?P<hall>[^"]+)", "New Haven", *(?P<mid>typeof\(\w+\), *GuildLocation\.TrammelIndex), *'
                  r'(?P<x>\d+), (?P<y>\d+), (?P<z>-?\d+), *(?P<seeded>true|false)(?P<rest>[^\n]*)')
gdone = set()
def gsub(m):
    key = m.group("key").strip('"')
    key = "alembic" if key.startswith("ClusterF") else key
    in_lookouts = "ThievesDenLookout" in m.group("mid")
    r = (look if in_lookouts else guild).get(key)
    if r is None:
        return m.group(0)
    gdone.add(("l:" if in_lookouts else "") + key)
    rest = m.group("rest")
    rest = re.sub(r", new Point3D\(\d+, \d+, -?\d+\)", "", rest)        # the artificers' OldTiles: a fresh world has none
    rest = re.sub(r", Direction\.South\)", ")", rest)
    rest = re.sub(r", Direction\.East\)", ")", rest) if in_lookouts else rest
    return 'new(%s, "%s", "New Haven", %s, %s, %s, %s, %s%s' % (m.group("key"), r["building"], m.group("mid"), r["x"], r["y"], r["z"], m.group("seeded"), rest)
s2 = gpat.sub(gsub, s)
print("guild rows changed:", sorted(gdone))
open(p, "w", encoding="utf-8", newline="").write(s2)

# 3. the Appraiser's post in the office
p = CODE + "Requisitions/Appraiser.cs"
s = open(p, encoding="utf-8").read()
a = next(r for r in rows if r["kind"] == "post")
s2, n = re.subn(r'new\("New Haven", "League field office", 1, \d+, \d+, -?\d+, Direction\.(?:West|South), true\)',
                'new("New Haven", "League field office", 1, %s, %s, %s, Direction.South, true)' % (a["x"], a["y"], a["z"]), s)
assert n == 1
open(p, "w", encoding="utf-8", newline="").write(s2)
# 4. the institution seeder: the Sanitation Warden in the League office, the Outriders and Foresters guildmasters
p = CODE + "ClusterFInstitutionSeeder.cs"
s = open(p, encoding="utf-8").read()
for t, key, label in (("SanitationWarden", "custodians", "League field office"),
                      ("OutridersGuildmaster", "rangers", "the farmhouse stables"),
                      ("ForestersGuildmaster", "foresters", "the Woodsman in Haven")):
    r = guild[key]
    s, n = re.subn(r"(typeof\(%s\),\s*\(\) => new %s\(\),\s*)x: \d+, y: \d+, z: -?\d+," % (t, t),
                   r"\g<1>x: %s, y: %s, z: %s," % (r["x"], r["y"], r["z"]), s)
    assert n == 1, t
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
