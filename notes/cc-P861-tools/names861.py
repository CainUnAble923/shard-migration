"""cc-P861: our extra NPC name lists, read out of Sirenix's expanded names.xml (D:/UO/third-party/code/expanded-names;
reference: only the names are read) into server/data/names-shard.json, in pinned's names.json shape
({"type", "names"}), beside pinned's Data/names.json (never edited).

Two kinds of row:
  - new lists (types pinned has not): elf, gargoyle, druid, paladin (with titles), juka, meer, gladiator (P854's pick);
  - "extend": extra names for a list pinned already has, the author's own "expanded" lists (gargoyle vendor, savage
    rider, golem controller). ShardNames adds only the names pinned's list lacks.
Greek, graveyard, drow and the author's copies of pinned's other lists are left out (P854).

Read by eye (P854 asked): accents (the elf lists') are folded to plain letters, as a
name goes to the client as ASCII; a few entries the author ran together with full stops are split; typos
in the titles and druid names are corrected (FIX), and two gladiator titles unfit for a town NPC and one paladin title
that reads wrong are dropped (DROP).

  python -P names861.py <out names-shard.json>
Prints each list's count and a sample, for the eye check.
"""
import json
import re
import sys
import unicodedata

SRC = r"D:/UO/third-party/code/expanded-names/names.xml"
PINNED = r"D:/UO/ModernUO-pinned/Distribution/Data/names.json"
NEW = {  # our type: the xml's
    "elf male": "Elf Male", "elf female": "Elf Female",
    "gargoyle male": "Gargoyle Male", "gargoyle female": "Gargoyle Female",
    "druid": "Druid", "paladin": "paladin", "paladin title": "paladintitle",
    "juka": "juka", "meer": "meer",
    "gladiator male": "GladiatorMale", "gladiator female": "GladiatorFemale", "gladiator title": "GladiatorTitle",
}
EXTEND = ["gargoyle vendor", "savage rider", "golem controller"]
FIX = {"the Victorius": "the Victorious", "the Stuborn": "the Stubborn", "the Aweful": "the Awful",
       "the Grizley": "the Grizzly", "the Firey": "the Fiery", "the wimpy": "the Wimpy", "the relentless": "the Relentless",
       "the flagellant": "the Flagellant", "Mountiangleam": "Mountaingleam", "Mountianbrook": "Mountainbrook",
       "the Paladin of Clear Judgement": "the Paladin of Clear Judgment",
       "Paladin of Swift Blade": "the Paladin of Swift Blade"}
DROP = {"the Bastard", "the Lecherous", "the Paladin of Fist of Dauros"}


def ascii_name(n):
    n = unicodedata.normalize("NFKD", n)
    return "".join(c for c in n if not unicodedata.combining(c)).encode("ascii", "ignore").decode()


def lists():
    t = open(SRC, encoding="utf-8-sig").read()
    out = {}
    for m in re.finditer(r'<namelist type="([^"]+)">(.*?)</namelist>', t, re.S):
        names = [ascii_name(re.sub(r"\s+", " ", n).strip()) for n in re.split(r"[,.]", m.group(2))]
        names = [FIX.get(n, n) for n in names if n and n not in DROP]
        out[m.group(1)] = names
    return out


def unique(names):
    seen, out = set(), []
    for n in names:
        if n.lower() not in seen:
            seen.add(n.lower())
            out.append(n)
    return out


def main():
    xml = lists()
    pinned = {e["type"].lower(): e["names"] for e in json.load(open(PINNED, encoding="utf-8"))}
    rows = []
    for ours, theirs in NEW.items():
        assert ours not in pinned, ours
        names = unique(xml[theirs] if ours.endswith("title") else [n[0].upper() + n[1:] for n in xml[theirs]])
        rows.append({"type": ours, "mode": "new", "names": names})
    for t in EXTEND:
        have = {n.lower() for n in pinned[t]}
        extra = [n for n in unique(xml[t]) if n.lower() not in have]
        rows.append({"type": t, "mode": "extend", "names": extra})
    doc = {
        "credit": "Sirenix, Custom expanded names.xml 1.1 (servuo.dev, 2014); converted by shard-migration notes/cc-P861-tools/names861.py",
        "lists": rows,
    }
    with open(sys.argv[1], "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
        f.write("\n")
    for r in rows:
        print("%-16s %-6s %4d  %s" % (r["type"], r["mode"], len(r["names"]), r["names"][:10]))


if __name__ == "__main__":
    main()
