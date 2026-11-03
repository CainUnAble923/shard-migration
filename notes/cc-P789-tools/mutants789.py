# cc-P789: one mutant per new shard fact, written to <out>/m<n>.cs. Usage: python -P mutants789.py <PlayTestTasks.cs> <out>
import os, sys
src, out = sys.argv[1], sys.argv[2]
M = {
    8: ("        if (string.IsNullOrEmpty(s))\n        {\n            return \"\";\n        }\n\n        s = Parenthetical.Replace(s, \"\");",
        "        if (string.IsNullOrEmpty(s) || s.Length > 0)\n        {\n            return s ?? \"\";\n        }\n\n        s = Parenthetical.Replace(s, \"\");"),
    9: ("        if (staff && t.NeedsPlayer == true)", "        if (false && staff && t.NeedsPlayer == true)"),
    10: ("w.WriteBoolean(\"staff\", acct != null && acct.AccessLevel >= AccessLevel.Counselor);", "w.WriteBoolean(\"staff\", false);"),
}
text = open(src, encoding="utf-8", newline="").read()
os.makedirs(out, exist_ok=True)
for n, (old, new) in M.items():
    assert text.count(old) == 1, (n, text.count(old))
    open(os.path.join(out, "m%d.cs" % n), "w", encoding="utf-8", newline="").write(text.replace(old, new))
    print("m%d ready" % n)
