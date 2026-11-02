"""cc-P773: one mutant per shard rule, each undoing one piece of PlayTest/PlayTestTasks.cs in a copy of the code copy's
customizations PlayTest folder. Writes <out>/<name>/PlayTest/ for probe773.sh (SRC773=<out>/<name>).
Usage: python -P mutate773.py <code copy customizations> <out folder>"""
import pathlib
import shutil
import sys

src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
F = "PlayTest/PlayTestTasks.cs"
MUTANTS = {
    # 1 and 2: anyone is a tester
    "anyone": ("return testers?.FirstOrDefault(t => string.Equals(t.Account, account, StringComparison.OrdinalIgnoreCase));",
               "return testers == null ? null : new PlayTester { Account = account };"),
    # 1: a pulled-back task still shows
    "showpulled": ('string.Equals(t.Account, account, StringComparison.OrdinalIgnoreCase) && t.Status == "open" &&',
                   'string.Equals(t.Account, account, StringComparison.OrdinalIgnoreCase) &&'),
    # 3: a broken tester list throws
    "throws": ('        catch (JsonException e)\n        {\n            error = $"{TestersFileName} is not valid JSON: {e.Message}";',
               '        catch (InvalidOperationException e)\n        {\n            error = $"{TestersFileName} is not valid JSON: {e.Message}";'),
    # 4: a button writes nothing
    "noappend": ('            File.AppendAllText(ReportsPath, line + "\\n", new UTF8Encoding(false));\n', ""),
    # 4: an IP address in the line
    "ip": ('            w.WriteString("version", version ?? "");\n',
           '            w.WriteString("version", version ?? "");\n            w.WriteString("ip", "127.0.0.1");\n'),
    # 4: the problem buttons take no words
    "nowords": ('            if (button != "worked" && text.Length == 0)\n', '            if (false)\n'),
    # 5: "tasks" said aloud does nothing
    "nospeech": ("            ShowTasks(pm, false); // only a tester is answered: anyone may say the word\n", ""),
    # 6: showing the tasks does not remember them (the login line repeats)
    "noseen": ("                acct.SetTag(SeenTag, newest);\n", ""),
    # 7: a Pass button
    "pass": ('public static readonly string[] Buttons = { "worked", "wrong", "couldnt", "report" };',
             'public static readonly string[] Buttons = { "worked", "wrong", "couldnt", "report", "pass" };'),
}
for name, (old, new) in MUTANTS.items():
    dst = out / name
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src / "PlayTest", dst / "PlayTest")
    p = dst / F
    text = p.read_text(encoding="utf-8")
    if text.count(old) != 1:
        sys.exit("%s: anchor found %d times" % (name, text.count(old)))
    p.write_text(text.replace(old, new), encoding="utf-8", newline="")
    print(name)
