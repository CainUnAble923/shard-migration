r"""cc-P685: writes the shard's server\patches\GenChamps-sos-sites.patch from champs.py's MOVES, against pinned's
GenChamps.cs (diff -u, three lines of context, checked with patch --fuzz=0 by the caller).

    python -P make_patch.py
"""
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import champs  # noqa: E402

REL = "Projects/UOContent/Engines/CannedEvil/GenChamps.cs"
PINNED = os.path.join(r"D:\UO\ModernUO-pinned", REL)
OUT = os.path.join(champs.SHARD, "server", "patches", "GenChamps-sos-sites.patch")
NOTE = ("    // Shattered Legacy (cc-P685, SoS swap S12): on the Siege of Sosaria land LL06, LL07 and LL11 stand on new ground\n"
        "    // (P696's option A), and LL08 keeps its altar with a new eject point; the rest are pinned's. Checked on the map by\n"
        "    // shard-migration notes/cc-P685-tools/champs.py.\n")


def p3(p):
    return f"new Point3D({p[0]}, {p[1]}, {p[2]})"


def main():
    raw = open(PINNED, "rb").read()
    crlf = b"\r\n" in raw
    text = raw.decode("utf-8").replace("\r\n", "\n")
    stock = {i: (c, e) for i, _, _, c, e in champs.STOCK}
    new = text
    for i, (nc, ne) in champs.MOVES.items():
        oc, oe = stock[i]
        old = f"{p3(oc)}, Map.Felucca, {p3(oe)}, Map.Felucca)"
        if new.count(old) != 1:
            sys.exit(f"{i}: {old} found {new.count(old)} times")
        new = new.replace(old, f"{p3(nc)}, Map.Felucca, {p3(ne)}, Map.Felucca)")
    anchor = "    private static readonly ChampionEntry[] LLLocations =\n"
    assert new.count(anchor) == 1
    new = new.replace(anchor, NOTE + anchor)
    with tempfile.TemporaryDirectory() as d:
        for side, body in (("a", text), ("b", new)):
            p = os.path.join(d, side, REL)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            data = body.replace("\n", "\r\n") if crlf else body
            open(p, "w", encoding="utf-8", newline="").write(data)
        r = subprocess.run(["diff", "-u", f"a/{REL}", f"b/{REL}"], cwd=d, capture_output=True)
        if r.returncode != 1:
            sys.exit(r.stderr.decode())
        lines = r.stdout.decode("utf-8").split("\n")
        lines[0], lines[1] = f"--- a/{REL}", f"+++ b/{REL}"
        open(OUT, "w", encoding="utf-8", newline="").write("\n".join(lines))
    print("wrote", OUT, "crlf" if crlf else "lf")


if __name__ == "__main__":
    main()
