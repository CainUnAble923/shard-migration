#!/usr/bin/env python3
"""Static estimate of BaseInstrument.GetBaseDifficulty for every concrete BaseCreature subclass.

Sources: pinned ModernUO UOContent (whole tree, location column says where) and the shard's
customizations. Expansion EJ: Core.LBR, Core.AOS, Core.SE all true -> hits * 1.6, SetHits not
rescaled, final cap 160.

Formula (pinned BaseInstrument.cs:250-306):
  val = HitsMax*1.6 + StamMax + ManaMax + SkillsTotal(fixed point)/10
  if val > 700: val = 700 + int((val-700)*3/11)
  +100 mage AI with Magery base > 5 ; +100 FireBreath-type ability ; +100 PoisonImmune != null
  +100 VampireBat ; + (HitPoison.Level+1)*20
  val /= 10 ; paragon +40 ; cap 160 (SE)
Range midpoints are used for every Set* call.
"""
import csv, os, re, statistics, sys
from collections import defaultdict

PINNED = r"D:\UO\ModernUO-pinned\Projects\UOContent"
CUSTOM = r"D:\ShatteredLegacy\server\customizations"
OUT = os.path.dirname(os.path.abspath(__file__))

POISON_LEVEL = {"Lesser": 0, "Regular": 1, "Greater": 2, "Deadly": 3, "Lethal": 4,
                "Parasitic": 2, "DarkGlow": 2}  # last two: not in pinned; guessed if seen

def strip_code(src):
    out, i, n = [], 0, len(src)
    while i < n:
        c = src[i]
        if src.startswith("//", i):
            j = src.find("\n", i); i = n if j < 0 else j
        elif src.startswith("/*", i):
            j = src.find("*/", i + 2); i = n if j < 0 else j + 2
        elif c == '"' or (c in "@$" and i + 1 < n and src[i + 1] == '"') or src.startswith('$@"', i) or src.startswith('@$"', i):
            # string literal; blank its content
            k = i
            verbatim = False
            while src[k] != '"':
                if src[k] == '@': verbatim = True
                k += 1
            k += 1
            while k < n:
                if verbatim and src[k] == '"' and k + 1 < n and src[k + 1] == '"': k += 2; continue
                if not verbatim and src[k] == '\\': k += 2; continue
                if src[k] == '"': break
                k += 1
            out.append('""'); i = k + 1
        elif c == "'":
            k = i + 1
            while k < n and src[k] != "'":
                k += 2 if src[k] == '\\' else 1
            out.append("' '"); i = k + 1
        else:
            out.append(c); i += 1
    return "".join(out)

def match_brace(s, i):
    depth = 0
    for k in range(i, len(s)):
        if s[k] == '{': depth += 1
        elif s[k] == '}':
            depth -= 1
            if depth == 0: return k
    return len(s) - 1

CLASS_RE = re.compile(r"((?:\b(?:public|private|protected|internal|abstract|sealed|static|partial|new)\s+)*)class\s+(\w+)\s*(?:<[^>{]*>)?\s*(?::\s*([^{]+?))?\s*(?:where[^{]*)?\{")

classes = {}  # key (src,name) -> dict

def scan(root, tag):
    for dp, dn, fn in os.walk(root):
        for f in fn:
            if not f.endswith(".cs"): continue
            p = os.path.join(dp, f)
            try:
                raw = open(p, encoding="utf-8-sig", errors="replace").read()
            except Exception:
                continue
            s = strip_code(raw)
            for m in CLASS_RE.finditer(s):
                mods, name, bases = m.group(1), m.group(2), m.group(3)
                ob = m.end() - 1
                cb = match_brace(s, ob)
                body = s[ob + 1:cb]
                base = None
                if bases:
                    b0 = bases.split(",")[0].strip()
                    b0 = re.sub(r"<.*", "", b0).split(".")[-1].strip()
                    base = b0
                key = (tag, name)
                if key in classes:  # partial split across files: merge
                    classes[key]["body"] += "\n" + body
                    classes[key]["base"] = classes[key]["base"] or base
                    classes[key]["abstract"] |= "abstract" in mods
                    continue
                classes[key] = dict(name=name, base=base, body=body, file=os.path.relpath(p, root),
                                    tag=tag, abstract="abstract" in mods, static="static" in mods)

scan(PINNED, "pinned")
scan(CUSTOM, "custom")

by_name = defaultdict(list)
for k, v in classes.items(): by_name[v["name"]].append(k)

def resolve(key, basename):
    if basename is None: return None
    cands = by_name.get(basename, [])
    if not cands: return None
    for c in cands:
        if c[0] == key[0]: return c
    return cands[0]

def ancestry(key):
    chain, seen = [key], {key}
    while True:
        cur = classes[chain[-1]]
        b = cur["base"]
        if b == "BaseCreature": chain.append("BaseCreature"); return chain
        nk = resolve(chain[-1], b)
        if nk is None or nk in seen: return None
        chain.append(nk); seen.add(nk)

def strip_nested(body):
    # remove nested class/struct/record bodies so their members do not leak in
    out, i = [], 0
    for m in re.finditer(r"\b(?:class|struct|record|interface)\s+\w+[^{;]*\{", body):
        if m.start() < i: continue
        out.append(body[i:m.start()])
        i = match_brace(body, m.end() - 1) + 1
    out.append(body[i:])
    return "".join(out)

def num(expr):
    e = expr.strip()
    # EJ: every Core.X era flag is true, take the true branch
    m = re.fullmatch(r"\(?\s*Core\.\w+\s*\?\s*([^:]+):\s*(.+?)\)?", e)
    if m: e = m.group(1)
    e = re.sub(r"\bscalar\b", "1.0", e)  # Golem(bool summoned=false, double scalar=1.0)
    e = re.sub(r"(?<=\d)[fFdDmM]\b", "", e)
    e = re.sub(r"\(\s*(?:int|double|float)\s*\)", "", e)
    if not re.fullmatch(r"[\d\.\s\+\-\*/\(\)]+", e): raise ValueError(expr)
    return float(eval(e))

def split_args(a):
    parts, depth, cur = [], 0, ""
    for ch in a:
        if ch == "(": depth += 1
        elif ch == ")": depth -= 1
        if ch == "," and depth == 0: parts.append(cur); cur = ""
        else: cur += ch
    parts.append(cur)
    return [p.strip() for p in parts]

def find_calls(text, fname):
    res = []
    for m in re.finditer(r"\b" + fname + r"\s*\(", text):
        k, depth = m.end() - 1, 0
        for j in range(k, len(text)):
            if text[j] == "(": depth += 1
            elif text[j] == ")":
                depth -= 1
                if depth == 0: res.append((m.start(), text[k + 1:j])); break
    return res

def ctor_of(cls):
    body = strip_nested(cls["body"])
    name = cls["name"]
    ctors = []
    for m in re.finditer(r"(\[Constructible[^\]]*\]\s*)?(?:public|protected|private|internal)?\s*\b" + name + r"\s*\(([^)]*)\)\s*(?::\s*(base|this)\s*\()?", body):
        # must be a ctor: preceded by modifier or newline, followed by '{' or ':'
        pre = body[max(0, m.start() - 12):m.start()]
        if re.search(r"\bnew\s*$", pre): continue
        k = m.end()
        chain_args = ""
        if m.group(3):
            depth, j = 1, k
            while j < len(body) and depth:
                if body[j] == "(": depth += 1
                elif body[j] == ")": depth -= 1
                j += 1
            chain_args = body[k:j - 1]; k = j
        rest = body[k:].lstrip()
        if not rest.startswith("{"):
            if rest.startswith("=>"): continue
            continue
        ob = body.index("{", k)
        cb = match_brace(body, ob)
        ctors.append(dict(constructible=bool(m.group(1)), params=m.group(2).strip(), kind=m.group(3),
                          chain=chain_args, body=body[ob + 1:cb]))
    if not ctors: return None, body
    def score(c):
        return (c["constructible"], len(re.findall(r"\bSet(?:Str|Hits|Skill)\b", c["body"])), c["params"] == "")
    best = max(ctors, key=score)
    # follow this(...) chain within the class
    text = best["body"]
    if best["kind"] == "this":
        others = [c for c in ctors if c is not best]
        if others:
            o = max(others, key=lambda c: len(re.findall(r"\bSet", c["body"])))
            text = o["body"] + "\n" + text
            best = dict(best, chain=o["chain"] + " " + best["chain"], kind=o["kind"])
    return dict(best, text=text), body

def prop_expr(body, prop):
    m = re.search(r"\boverride\s+Poison\s+" + prop + r"\b\s*(=>\s*([^;]+);|\{(.*?)\})", body, re.S)
    if not m: return None
    return m.group(2) or m.group(3) or ""

def poison_level_of(expr):
    toks = re.findall(r"Poison\.(\w+)", expr)
    lv = [POISON_LEVEL[t] for t in toks if t in POISON_LEVEL]
    if not lv:
        if "null" in expr: return None
        return "?"
    return sum(lv) / len(lv)

BREATH_TYPES = {"FireBreath", "ChaosBreath", "ColdBreath"}
# any class deriving (transitively) from FireBreath also has AbilityType FireBreath
changed = True
while changed:
    changed = False
    for k, v in classes.items():
        if v["base"] in BREATH_TYPES and v["name"] not in BREATH_TYPES:
            BREATH_TYPES.add(v["name"]); changed = True

def has_breath(body):
    m = re.search(r"GetMonsterAbilities\s*\(\s*\)", body)
    if not m: return None
    # abilities may be in a static field; look at the whole class body for breath references
    for t in BREATH_TYPES:
        if re.search(r"MonsterAbilities\." + t + r"\b|new\s+" + t + r"\s*\(", body):
            return True
    return False

def resolve_stats(key, memo={}):
    if key == "BaseCreature":
        return dict(str=None, dex=None, int=None, hits=None, stam=None, mana=None, skills={}, ai=None,
                    pimm=None, hitp=None, breath=False, notes=[], ok=True, aiparam=False, dmg=None,
                    BardImmune=False, Unprovokable=False, Uncalmable=False, AreaPeaceImmune=False)
    if key in memo: return memo[key]
    cls = classes[key]
    parent = resolve(key, cls["base"]) if cls["base"] != "BaseCreature" else "BaseCreature"
    st = dict(resolve_stats(parent))
    st["skills"] = dict(st["skills"]); st["notes"] = list(st["notes"])
    ctor, body = ctor_of(cls)
    text = ctor["text"] if ctor else ""
    if ctor:
        m = re.search(r"AIType\.(AI_\w+)", ctor["chain"])
        if m: st["ai"] = m.group(1); st["aiparam"] = False
        elif re.search(r"\bai\w*\b", ctor["chain"], re.I) and st["ai"] is None:
            st["aiparam"] = True
        for m in re.finditer(r"\bAI\s*=\s*AIType\.(AI_\w+)", text): st["ai"] = m.group(1)
    def setstat(fn, field):
        calls = find_calls(text, fn)
        if not calls: return
        if len(calls) > 1: st["notes"].append(f"{fn}x{len(calls)}(last used)")
        a = split_args(calls[-1][1])
        try:
            vals = [num(x) for x in a]
            st[field] = sum(vals) / len(vals)
        except ValueError:
            st["notes"].append(f"{fn} unparsed:{calls[-1][1][:40]}"); st["ok"] = False
    setstat("SetStr", "str"); setstat("SetDex", "dex"); setstat("SetInt", "int")
    setstat("SetHits", "hits"); setstat("SetStam", "stam"); setstat("SetMana", "mana")
    for _, a in find_calls(text, "InitStats"):
        try:
            s, d, i = [num(x) for x in split_args(a)]
            st["str"], st["dex"], st["int"] = s, d, i
        except Exception:
            st["notes"].append("InitStats unparsed"); st["ok"] = False
    for _, a in find_calls(text, "SetSkill"):
        p = split_args(a)
        m = re.match(r"SkillName\.(\w+)", p[0])
        if not m:
            st["notes"].append("SetSkill dynamic"); continue
        try:
            vals = [num(x) for x in p[1:]]
            if len(vals) == 2:
                lo, hi = int(vals[0] * 10), int(vals[1] * 10)
                st["skills"][m.group(1)] = (lo + hi) / 2
            else:
                st["skills"][m.group(1)] = int(vals[0] * 10)
        except ValueError:
            st["notes"].append(f"SetSkill {m.group(1)} unparsed"); st["ok"] = False
    for m in re.finditer(r"Skills(?:\[SkillName\.(\w+)\]|\.(\w+))\.Base\s*=\s*([^;]+);", text):
        sk = m.group(1) or m.group(2)
        try: st["skills"][sk] = int(num(m.group(3)) * 10)
        except ValueError: st["notes"].append(f"Skills.{sk}.Base unparsed")
    if re.search(r"Skills\.Length|Skills\[i\]", text): st["notes"].append("skill loop (not counted)")
    for _, a in find_calls(text, "SetDamage"):
        try:
            v = [num(x) for x in split_args(a)]
            st["dmg"] = sum(v) / len(v)
        except ValueError:
            pass
    for flag in ("BardImmune", "Unprovokable", "Uncalmable", "AreaPeaceImmune"):
        m = re.search(r"override\s+bool\s+" + flag + r"\s*=>\s*(\w+)", body)
        if m: st[flag] = (m.group(1) == "true")
    pe = prop_expr(body, "PoisonImmune")
    if pe is not None:
        st["pimm"] = poison_level_of(pe)
    he = prop_expr(body, "HitPoison")
    if he is not None:
        st["hitp"] = poison_level_of(he)
    hb = has_breath(body)
    if hb is not None: st["breath"] = hb
    memo[key] = st
    return st

def difficulty(st, name, chain_names):
    s = st["str"] or 0; d = st["dex"] or 0; i = st["int"] or 0
    hits = st["hits"] if st["hits"] else s
    stam = st["stam"] if st["stam"] else d
    mana = st["mana"] if st["mana"] else i
    skt = sum(st["skills"].values())  # fixed point
    val = hits * 1.6 + stam + mana + skt / 10.0
    raw = val
    if val > 700: val = 700 + int((val - 700) * (3.0 / 11))
    mage = st["ai"] == "AI_Mage" and st["skills"].get("Magery", 0) > 50
    if mage: val += 100
    if st["breath"]: val += 100
    pimm = st["pimm"] is not None
    if pimm: val += 100
    if name in ("VampireBat", "VampireBatFamiliar") or "VampireBat" in chain_names: val += 100
    hp = st["hitp"]
    hplev = (hp + 1) if isinstance(hp, (int, float)) else (1 if hp == "?" else 0)
    val += hplev * 20
    val /= 10
    uncapped = val
    capped = min(val, 160.0)
    para = min(val + 40, 160.0)
    return dict(hits=hits, stam=stam, mana=mana, skilltotal=skt / 10, raw=raw, mage=mage, breath=st["breath"],
                pimm=pimm, hitplev=hplev, uncapped=uncapped, diff=capped, paragon=para)

rows, fails = [], []
for key, cls in classes.items():
    if cls["abstract"] or cls["static"]: continue
    chain = ancestry(key)
    if not chain: continue
    try:
        st = resolve_stats(key)
    except Exception as e:
        fails.append((key, f"exception {e}")); continue
    names = [classes[c]["name"] for c in chain[1:-1]]
    if st["str"] is None and st["hits"] is None:
        fails.append((key, "no SetStr/SetHits/InitStats found (stats set elsewhere)")); continue
    if not st["ok"]:
        fails.append((key, ";".join(st["notes"]))); continue
    r = difficulty(st, cls["name"], names)
    loc = cls["file"].replace("\\", "/")
    if cls["tag"] == "pinned":
        if loc.startswith("Mobiles/Monsters"): cat = "monster"
        elif loc.startswith("Mobiles/Animals"): cat = "animal"
        elif re.match(r"Mobiles/(Townfolk|Vendors|Guards|Healers|Hireables)", loc): cat = "npc"
        elif loc.startswith("Mobiles/Special"): cat = "special"
        elif loc.startswith("Mobiles/Familiars"): cat = "familiar"
        else: cat = "other"
    else:
        cat = "custom"
    sk = st["skills"]
    wres = max(sk.get(k, 0) for k in ("Wrestling", "Swords", "Macing", "Fencing", "Archery")) / 10
    tac = sk.get("Tactics", 0) / 10; ana = sk.get("Anatomy", 0) / 10; strv = st["str"] or 0
    def gb(v, sc, th, off): return (v * sc + (off if v >= th else 0)) / 100
    bonus = gb(strv, .3, 100, 5) + gb(ana, .5, 100, 5) + gb(tac, .625, 100, 6.25)
    dmg = (st["dmg"] or 0) * (1 + bonus)
    hit0 = max(0.02, (wres + 20) * 100 / (2 * 320 * 100))
    hit45 = max(0.02, (wres + 20) * 100 / (2 * 320 * 145))
    combat = dict(atkskill=wres, dmgbase=st["dmg"] or 0, dmghit=dmg, dmg70=int(dmg * 0.30), hit_vs300=hit0, hit_vs300dci45=hit45,
                  bardimmune=st["BardImmune"], unprovokable=st["Unprovokable"], uncalmable=st["Uncalmable"])
    rows.append(dict(source=cls["tag"], **combat, category=cat, name=cls["name"], parent=cls["base"], file=loc,
                     ai=st["ai"] or ("param" if st["aiparam"] else ""),
                     str=st["str"], dex=st["dex"], int=st["int"], **r, notes=";".join(st["notes"])))

rows.sort(key=lambda r: (-r["uncapped"], r["name"]))
with open(os.path.join(OUT, "s5-creature-difficulty.csv"), "w", newline="", encoding="ascii", errors="replace") as fh:
    cols = ["name", "source", "category", "parent", "file", "ai", "str", "dex", "int", "hits", "stam", "mana",
            "skilltotal", "raw", "mage", "breath", "pimm", "hitplev", "uncapped", "diff", "paragon", "atkskill", "dmgbase", "dmghit", "dmg70", "hit_vs300", "hit_vs300dci45",
            "bardimmune", "unprovokable", "uncalmable", "notes"]
    w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
    w.writeheader()
    for r in rows:
        r2 = {k: (round(v, 2) if isinstance(v, float) else v) for k, v in r.items()}
        w.writerow(r2)
with open(os.path.join(OUT, "s5-parse-failures.txt"), "w", encoding="ascii", errors="replace") as fh:
    for k, why in sorted(fails):
        fh.write(f"{k[0]}\t{k[1]}\t{classes[k]['file']}\t{why}\n")

def summary(sel, label):
    v = sorted(r["uncapped"] for r in sel)
    if not v: return
    q = statistics.quantiles(v, n=4)
    print(f"== {label}: n={len(v)} min={v[0]:.1f} q1={q[0]:.1f} median={statistics.median(v):.1f} q3={q[2]:.1f} max={v[-1]:.1f}")
    print(f"   capped at 160: {sum(1 for x in v if x >= 160)}  >=120: {sum(1 for x in v if x>=120)}  >=100: {sum(1 for x in v if x>=100)}")
    b = defaultdict(int)
    for x in v: b[min(int(x // 20) * 20, 200)] += 1
    for k in sorted(b): print(f"   {k:>3}-{k+19 if k<200 else '+'}: {b[k]}")

print("classes scanned:", len(classes), " computed:", len(rows), " failures:", len(fails))
summary(rows, "all")
summary([r for r in rows if r["category"] in ("monster", "animal", "custom", "special")], "monsters+animals+special+custom")
summary([r for r in rows if r["source"] == "custom"], "custom only")
print("\nTop 30 by uncapped:")
for r in rows[:30]:
    print(f"  {r['name']:<28} {r['source']:<6} {r['uncapped']:7.1f} capped={r['diff']:.1f} hits={r['hits']:.0f} raw={r['raw']:.0f} mage={r['mage']} breath={r['breath']} pimm={r['pimm']} hp={r['hitplev']} atk={r['atkskill']:.0f} dmg={r['dmgbase']:.0f}->{r['dmghit']:.0f}/{r['dmg70']} hit={r['hit_vs300']:.2f}/{r['hit_vs300dci45']:.2f} BI={r['bardimmune']}")
idx = {r["name"]: r for r in rows}
print("\nSanity:")
for n in ["Rat", "GiantRat", "Orc", "OrcishLord", "Troll", "Ogre", "Daemon", "Dragon", "GreaterDragon", "AncientWyrm",
          "Balron", "Harrower", "SerpentineDragon", "ShadowWyrm", "WhiteWyrm", "Lich", "AncientLich", "StygianDragon",
          "Medusa", "Semidar", "Barracoon", "ChaosDragoon", "DreadSpider", "VampireBat", "Wyvern", "Leviathan"]:
    if n in idx: r = idx[n]; print(f"  {n:<18} {r['uncapped']:7.1f} (capped {r['diff']:.1f}) {r['notes']}")
    else: print(f"  {n:<18} not computed")
