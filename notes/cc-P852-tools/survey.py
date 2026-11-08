import os, re, struct, sys, json

CODE = "D:/UO/third-party/code"
CD = "D:/UO/tool-trials/client-data-copy"
FOLDERS = """blue-couches grey-fireplaces diesel-lamps-pillars drafted-lamps-jackolanterns milva-dragon-lantern milva-stained-glass-lamp milva-tall-lamps lagatha-beer-bar lagatha-desks-benches lagatha-kitchens-bbq lagatha-new-kitchen lagatha-pianos lagatha-holiday-fireplace lagatha-holiday-table lagatha-holiday-table-ns lagatha-campfire-witches lagatha-dancing-fire manwitch-brass-orrery manwitch-buffet-table manwitch-formal-dining manwitch-hammock manwitch-water-wheel medusa-fountains celestial-fairy-tree celestial-holiday-dining celestial-christmas-train candyapple-christmas-tree candyapple-xmas-deco milva-bank-christmas-1 milva-bank-christmas-2 milva-snowglobe xl-christmas-sleigh winter-snow-trees halloween-deco-items olorin-halloween-bank-topper spider-webs deceit-brazier hopers2-world-tree olorin-autumn-trees olorin-boulders-cairns olorin-cloud-ship olorin-feasting-tables olorin-fortune-teller-wagon olorin-gargish-light-posts olorin-grandfather-clock olorin-hunters-camp olorin-hunters-wagon olorin-inn-stable olorin-large-icebergs olorin-large-marketplace olorin-paddle-boat olorin-pond-bridge olorin-rose-garden olorin-sarcophagus-set olorin-scaffold-set olorin-temple-of-the-dragon smithy-townhouse house-boat-addon prebuilt-houses-12-custom prebuilt-houses-custom-structures prebuilt-houses-original arena-addon wedding-arches wedding-venue variable-carpet""".split()

# art index: static i at entry 0x4000+i, 12 bytes each
idx = open(CD + "/artidx.mul", "rb").read()
nidx = len(idx) // 12
def art_exists(i):
    e = 0x4000 + i
    if e >= nidx: return None
    off, ln, _ = struct.unpack_from("<iii", idx, e * 12)
    return off != -1 and ln > 0

td = open(CD + "/tiledata.mul", "rb").read()
LAND = 512 * (4 + 32 * 30)
ITEMREC = 41
GROUP = 4 + 32 * ITEMREC
nitems = (len(td) - LAND) // GROUP * 32
def td_name(i):
    if i >= nitems: return None
    g, r = divmod(i, 32)
    o = LAND + g * GROUP + 4 + r * ITEMREC
    nm = td[o + 21:o + 41].split(b"\0")[0]
    return nm.decode("latin-1")

PAT = [
    re.compile(r"AddComplexComponent\s*\(\s*\(?\s*BaseAddon\s*\)?\s*this\s*,\s*(0x[0-9A-Fa-f]+|\d+)"),
    re.compile(r"AddComplexComponent\s*\(\s*this\s*,\s*(0x[0-9A-Fa-f]+|\d+)"),
    re.compile(r"new\s+AddonComponent\s*\(\s*(0x[0-9A-Fa-f]+|\d+)"),
    re.compile(r"new\s+LocalizedAddonComponent\s*\(\s*(0x[0-9A-Fa-f]+|\d+)"),
    re.compile(r"new\s+Static\s*\(\s*(0x[0-9A-Fa-f]+|\d+)"),
    re.compile(r"\bbase\s*\(\s*(0x[0-9A-Fa-f]+)\s*\)"),
    re.compile(r"ItemID\s*=\s*(0x[0-9A-Fa-f]+|\d+)"),
]
TABLE = re.compile(r"\{\s*(\d+)\s*,\s*-?\d+\s*,\s*-?\d+\s*,\s*-?\d+\s*\}")  # {id,x,y,z} array tables
FLAGS = {
    "xmlspawner": re.compile(r"XmlSpawner|XmlAttach|XmlDialog", re.I),
    "powerscroll": re.compile(r"PowerScroll|StatCapScroll|SkillScroll", re.I),
    "bless": re.compile(r"BlessDeed|LootType\s*=\s*LootType\.Blessed|ItemBlessed", re.I),
    "skillbonus": re.compile(r"SkillBonuses|AddSkillMod|StatMod|RawStr\s*\+|SkillMod\(", re.I),
    "attrs": re.compile(r"Attributes\.(RegenHits|BonusStr|BonusDex|BonusInt|SpellDamage|WeaponDamage|Luck)", re.I),
    "timer": re.compile(r"\bTimer\b"),
    "gump": re.compile(r"\bGump\b"),
    "basehouse": re.compile(r"BaseHouse|HouseFoundation|MultiComponentList", re.I),
    "ondblclick": re.compile(r"OnDoubleClick"),
    "spawn": re.compile(r"BaseCreature|Spawner", re.I),
    "gold": re.compile(r"\bGold\b|Banker\.Withdraw|ConsumeTotal", re.I),
    "core_replace": re.compile(r"class\s+(PlayerMobile|BaseCreature|BaseHouse|BaseAddon|BaseWeapon|BaseArmor)\b"),
}
SERRE = re.compile(r"override\s+void\s+Serialize")
CLS = re.compile(r"public\s+(?:partial\s+)?class\s+(\w+)\s*:\s*(\w+)")

out = {}
for f in FOLDERS:
    p = os.path.join(CODE, f)
    r = {"exists": os.path.isdir(p)}
    if not r["exists"]:
        out[f] = r; continue
    src = ""
    sp = os.path.join(p, "SOURCE.txt")
    if os.path.exists(sp):
        src = open(sp, encoding="utf-8-sig", errors="replace").read()
    r["source"] = src
    cs, other, zips = [], [], []
    for root, ds, fs in os.walk(p):
        for n in fs:
            full = os.path.join(root, n)
            rel = os.path.relpath(full, p).replace("\\", "/")
            if rel.startswith("_zips/"): zips.append(rel[6:]); continue
            if n.lower().endswith(".cs"): cs.append(rel)
            elif n != "SOURCE.txt": other.append(rel)
    r["cs"], r["other"], r["zips"] = cs, other, zips
    ids = {}
    lines = ser = 0
    flags = {}
    classes = []
    for c in cs:
        t = open(os.path.join(p, c), encoding="utf-8", errors="replace").read()
        lines += t.count("\n") + 1
        ser += len(SERRE.findall(t))
        for k, rx in FLAGS.items():
            n = len(rx.findall(t))
            if n: flags[k] = flags.get(k, 0) + n
        classes += [f"{a}:{b}" for a, b in CLS.findall(t)]
        found = []
        for rx in PAT:
            found += rx.findall(t)
        found += TABLE.findall(t)
        for v in found:
            i = int(v, 16) if v.lower().startswith("0x") else int(v)
            if 0 < i < 0x10000:
                ids[i] = ids.get(i, 0) + 1
    r["lines"], r["ser"], r["flags"], r["classes"] = lines, ser, flags, classes
    missing, beyond = [], []
    for i in sorted(ids):
        e = art_exists(i)
        if e is None: beyond.append(i)
        elif not e: missing.append(i)
    r["nids"] = len(ids)
    r["maxid"] = max(ids) if ids else 0
    r["missing"] = [hex(i) for i in missing]
    r["beyond"] = [hex(i) for i in beyond]
    # top names
    names = {}
    for i, n in ids.items():
        nm = td_name(i) or "?"
        names[nm] = names.get(nm, 0) + n
    r["names"] = sorted(names.items(), key=lambda kv: -kv[1])[:12]
    r["hi"] = sum(1 for i in ids if i >= 0x4000)
    out[f] = r

json.dump(out, open(sys.argv[1], "w"), indent=1)
print("art entries", nidx - 0x4000, "tiledata items", nitems)
for f, r in out.items():
    if not r["exists"]:
        print(f, "MISSING FOLDER"); continue
    print(f"{f}: cs={len(r['cs'])} lines={r['lines']} ser={r['ser']} ids={r['nids']} max={hex(r['maxid'])} hi={r['hi']} missing={r['missing'][:6]} beyond={r['beyond'][:4]} other={len(r['other'])} zips={r['zips']} flags={r['flags']}")
