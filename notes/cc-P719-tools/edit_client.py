"""cc-P719: author client patch 0009 in the p719 worktree (0001 to 0008 applied and staged)."""
import sys, os
W = sys.argv[1]

def edit(rel, old, new):
    p = os.path.join(W, rel)
    with open(p, 'rb') as f:
        data = f.read()
    crlf = b'\r\n' in data
    t = data.decode('utf-8').replace('\r\n', '\n')
    assert t.count(old) == 1, (rel, t.count(old))
    t = t.replace(old, new)
    if crlf:
        t = t.replace('\n', '\r\n')
    with open(p, 'wb') as f:
        f.write(t.encode('utf-8'))
    print(rel, 'crlf' if crlf else 'lf')

edit('src/ClassicUO.Client/Configuration/Profile.cs',
     "        public bool SlRedrawnArt { get; set => SetProperty(ref field, value); } // Shattered Legacy patch (cc-P670): redrawn world art, off by default\n",
     "        public bool SlRedrawnArt { get; set => SetProperty(ref field, value); } // Shattered Legacy patch (cc-P670): redrawn world art, off by default\n"
     "        public bool SlOpenPaperdollAtLogin { get; set => SetProperty(ref field, value); } = true; // Shattered Legacy patch (cc-P719): ask for the own paperdoll at login; the launcher's default.json turns it off for new characters\n")

edit('src/ClassicUO.Client/Network/PacketHandlers/LoginComplete.cs',
     "            ObjectActionQueue.Instance.Enqueue(ObjectActionQueueItem.DoubleClick(world.Player | 0x8000_0000), ActionPriority.UseItem);\n",
     "            // Shattered Legacy patch (cc-P719): a profile can start without the paperdoll; one saved open still comes back with the gumps below.\n"
     "            if (ProfileManager.CurrentProfile.SlOpenPaperdollAtLogin)\n"
     "                ObjectActionQueue.Instance.Enqueue(ObjectActionQueueItem.DoubleClick(world.Player | 0x8000_0000), ActionPriority.UseItem);\n")
