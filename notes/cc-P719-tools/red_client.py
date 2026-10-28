"""cc-P719 red run: in the p719 build worktree, undo 0009's code (keep its tests) and leave only a stub property with
TazUO's plain bool default (false). Pass "restore" to put 0009's lines back."""
import sys
BS = chr(92)
W = sys.argv[1]
restore = len(sys.argv) > 2 and sys.argv[2] == "restore"

prof = W + "/src/ClassicUO.Client/Configuration/Profile.cs"
real = "public bool SlOpenPaperdollAtLogin { get; set => SetProperty(ref field, value); } = true;"
stub = "public bool SlOpenPaperdollAtLogin { get; set => SetProperty(ref field, value); } /*P719-RED*/"
login = W + "/src/ClassicUO.Client/Network/PacketHandlers/LoginComplete.cs"
gate = "            if (ProfileManager.CurrentProfile.SlOpenPaperdollAtLogin)\n"
gate_off = "            if (true) // P719-RED\n"

def swap(path, a, b):
    s = open(path, encoding="utf-8", newline="").read()
    assert s.count(a) == 1, (path, a)
    open(path, "w", encoding="utf-8", newline="").write(s.replace(a, b))

if restore:
    swap(prof, stub, real); swap(login, gate_off, gate)
else:
    swap(prof, real, stub); swap(login, gate, gate_off)
print("restored" if restore else "red")
