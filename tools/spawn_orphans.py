"""Regenerate tools/spawn-orphans.txt: the entry names in pinned ModernUO's own Distribution/Data/Spawns
that no declared type matches, case-insensitively, the way AssemblyHandler.FindTypeByName (ignoreCase = true)
and BaseSpawner.Spawn (EntryFlags.InvalidType, BaseSpawner.cs:1130) see them.

    python tools/spawn_orphans.py            # rewrite tools/spawn-orphans.txt
    python tools/spawn_orphans.py --dry-run  # print only

Declared types are read from the source trees, not from a description of them: every class/struct/enum/interface/
record declaration under D:\\UO\\ModernUO-pinned\\Projects\\{Server,UOContent} plus D:\\ShatteredLegacy\\server\\
customizations, AND every [TypeAlias("...")] string in the same files, because AssemblyHandler.TypeCache registers
alias names in the same lookup FindTypeByName reads (AssemblyHandler.cs:251-263), so a name absent as a declaration
may still resolve (batch 5's GargishClothChest). The match is on the simple type name - for an alias, its last dotted
segment - which is what FindTypeByName resolves a spawn entry with.
Written for CC6 batch 2 (2026-09-19) to replace the by-hand method 391db6c used; it reproduces that file exactly.
Alias registration added for CC6 batch 6 (2026-09-21); measured that day, no alias in either tree covered an orphan,
so it changed nothing until the batch-6 spike added one.
"""

import collections
import datetime
import glob
import json
import os
import re
import sys

PINNED = r"D:\UO\ModernUO-pinned"
SHARD = r"D:\ShatteredLegacy"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "spawn-orphans.txt")

DECL = re.compile(r"\b(?:class|struct|enum|interface|record)\s+([A-Za-z_][A-Za-z0-9_]*)")
# [TypeAlias("Server.Items.A", "Server.Items.B")]: the attribute's params string[] (Attributes.cs:89-94).
ALIAS = re.compile(r"\bTypeAlias\s*\(([^)]*)\)")
ALIAS_STRING = re.compile(r'"([^"]+)"')

HEADER = """# Spawn orphans: names in pinned ModernUO's own Distribution/Data/Spawns that no
# loaded assembly declares or aliases ([TypeAlias]). BaseSpawner flags these
# EntryFlags.InvalidType (BaseSpawner.cs:1130) and a player standing there sees nothing.
#
# Regenerate: python tools/spawn_orphans.py. Matching is CASE-INSENSITIVE on purpose -
# the spawn data mixes PascalCase and lowercase (tanglingroots, gremlin, acidslug,
# bloodworm, rotworm, wolfspider), and AssemblyHandler.FindTypeByName defaults to
# ignoreCase = true, so a case-sensitive match silently under-reports.
#
# {count} remaining as of {date}.
#
"""


def declared_types(roots):
    names = set()
    for root in roots:
        for path in glob.glob(os.path.join(root, "**", "*.cs"), recursive=True):
            with open(path, encoding="utf-8-sig", errors="replace") as f:
                text = f.read()
            for m in DECL.finditer(text):
                names.add(m.group(1).lower())
            for m in ALIAS.finditer(text):
                for full in ALIAS_STRING.findall(m.group(1)):
                    names.add(full.rsplit(".", 1)[-1].lower())  # TypeCache: fullTypeName[(LastIndexOf('.') + 1)..]
    return names


def spawn_entries(spawns_dir):
    """name (first spelling seen, files in sorted order) -> (entry count, set of files)."""
    counts = collections.Counter()
    files = collections.defaultdict(set)
    spelling = {}
    for path in sorted(glob.glob(os.path.join(spawns_dir, "**", "*.json"), recursive=True)):
        rel = os.path.relpath(path, spawns_dir).replace(os.sep, "/")
        with open(path, encoding="utf-8-sig") as f:
            for spawner in json.load(f):
                for entry in spawner.get("entries", []):
                    name = entry["name"]
                    key = name.lower()
                    spelling.setdefault(key, name)
                    counts[key] += 1
                    files[key].add(rel)
    return counts, files, spelling


def render(counts, files, spelling, types, date):
    rows = []
    for key, n in counts.items():
        if key in types:
            continue
        rows.append((-n, key, n, spelling[key], ", ".join(sorted(files[key]))))
    rows.sort()
    out = HEADER.format(count=len(rows), date=date)
    out += "# entries  " + "name".ljust(34) + "spawn files\n"
    for _, _, n, name, flist in rows:
        out += f"{n:9d}  {name:<34}{flist}\n"
    return out


def main(argv):
    dry = "--dry-run" in argv
    date = datetime.date.today().isoformat()
    customizations = os.path.join(SHARD, "server", "customizations")
    for a in argv:
        if a.startswith("--date="):
            date = a[len("--date="):]
        elif a.startswith("--customizations="):  # e.g. a `git archive HEAD` export, to reproduce an older run
            customizations = a[len("--customizations="):]
    types = declared_types([
        os.path.join(PINNED, "Projects", "Server"),
        os.path.join(PINNED, "Projects", "UOContent"),
        customizations,
    ])
    counts, files, spelling = spawn_entries(os.path.join(PINNED, "Distribution", "Data", "Spawns"))
    text = render(counts, files, spelling, types, date)
    if dry:
        sys.stdout.write(text)
    else:
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        print(f"wrote {OUT}: {text.splitlines()[9]}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
