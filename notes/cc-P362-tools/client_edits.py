"""cc-P362: the TazUO source edits for patch 0005 (UI skins), applied to a worktree that already has 0001-0004.
    python -P client_edits.py <TazUO worktree>
Writes SlSkins.cs from SlSkins.cs.template and skintable.cs.txt (both beside this script). Each edit's old text must
occur exactly once. ASCII only."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
W = sys.argv[1]

EDITS = {
    "src/ClassicUO.Assets/ExternalImageLoader.cs": [
        ("""            // Shattered Legacy (cc-P111): a run-time override, read from where it is (never copied into ExternalImages).
            if (!gump_overridePaths.TryGetValue(graphic, out string fullImagePath) &&
                !gump_availableFilePaths.TryGetValue(graphic, out fullImagePath))
                return new GumpInfo();
""",
         """            // Shattered Legacy (cc-P111): a run-time override, read from where it is (never copied into ExternalImages).
            // cc-P362: then a skin's remap, then the ID's own PNG (ResolveGumpPath).
            string fullImagePath = ResolveGumpPath(graphic);
            if (fullImagePath == null)
                return new GumpInfo();
"""),
        ("""        public ArtInfo LoadArtTexture(uint graphic)
        {
            if (!art_availableFilePaths.TryGetValue(graphic, out string fullImagePath))
                return new ArtInfo();
""",
         """        public ArtInfo LoadArtTexture(uint graphic)
        {
            // Shattered Legacy (cc-P362): a skin's remap first, then the ID's own PNG (ResolveArtPath).
            string fullImagePath = ResolveArtPath(graphic);
            if (fullImagePath == null)
                return new ArtInfo();
"""),
        ("""        public void Load(string uoDirectory = null)
        {
            exePath = AppContext.BaseDirectory;
            _uoDirectory = uoDirectory;

            string gumpPath = Path.Combine(exePath, IMAGES_FOLDER, GUMP_EXTERNAL_FOLDER);
""",
         """        public void Load(string uoDirectory = null)
        {
            exePath = AppContext.BaseDirectory;
            _uoDirectory = uoDirectory;
            ScanImages(Path.Combine(exePath, IMAGES_FOLDER));
        }

        // Shattered Legacy (cc-P362): Load's folder scan on its own, so a test can scan a folder of its own.
        public void ScanImages(string imagesRoot)
        {
            string gumpPath = Path.Combine(imagesRoot, GUMP_EXTERNAL_FOLDER);
"""),
        ("""            string artPath = Path.Combine(exePath, IMAGES_FOLDER, ART_EXTERNAL_FOLDER);
""",
         """            string artPath = Path.Combine(imagesRoot, ART_EXTERNAL_FOLDER);
"""),
        ("""        public string GetGumpOverride(uint graphic) => gump_overridePaths.TryGetValue(graphic, out string p) ? p : null;
""",
         """        public string GetGumpOverride(uint graphic) => gump_overridePaths.TryGetValue(graphic, out string p) ? p : null;

        // Shattered Legacy (cc-P362): UI skins. A stock gump (or art index) is drawn from the PNG of another ID, the
        // skin's own, which the package ships under a new ID. Only while a player has picked that skin; the stock ID's
        // own file is never touched. Each set replaces the whole remap and returns every ID whose source changed, its
        // cached pixels dropped, so the caller redraws exactly those.
        private readonly Dictionary<uint, uint> gump_skinRemap = new Dictionary<uint, uint>();
        private readonly Dictionary<uint, uint> art_skinRemap = new Dictionary<uint, uint>();

        public List<uint> SetGumpRemap(IReadOnlyDictionary<uint, uint> remap) => SetRemap(gump_skinRemap, remap, gump_textureCache);

        public List<uint> SetArtRemap(IReadOnlyDictionary<uint, uint> remap) => SetRemap(art_skinRemap, remap, art_textureCache);

        private static List<uint> SetRemap(Dictionary<uint, uint> current, IReadOnlyDictionary<uint, uint> next,
            Dictionary<uint, (uint[] pixels, int width, int height)> cache)
        {
            var changed = new List<uint>();
            foreach (KeyValuePair<uint, uint> old in current)
                if (next == null || !next.TryGetValue(old.Key, out uint now) || now != old.Value)
                    changed.Add(old.Key);
            if (next != null)
                foreach (KeyValuePair<uint, uint> now in next)
                    if (!current.ContainsKey(now.Key))
                        changed.Add(now.Key);
            current.Clear();
            if (next != null)
                foreach (KeyValuePair<uint, uint> now in next)
                    current[now.Key] = now.Value;
            foreach (uint id in changed)
                cache.Remove(id);
            return changed;
        }

        /// <summary>The file a gump is drawn from: the cc-P111 override, a skin's remap (when the skin's file is
        /// there), the ID's own PNG; null for the client's own gump.</summary>
        public string ResolveGumpPath(uint graphic)
        {
            if (gump_overridePaths.TryGetValue(graphic, out string p))
                return p;
            if (gump_skinRemap.TryGetValue(graphic, out uint to) && gump_availableFilePaths.TryGetValue(to, out p))
                return p;
            return gump_availableFilePaths.TryGetValue(graphic, out p) ? p : null;
        }

        /// <summary>The file an art index (item ID + 0x4000) is drawn from: a skin's remap, the ID's own PNG; null for
        /// the client's own art.</summary>
        public string ResolveArtPath(uint graphic)
        {
            if (art_skinRemap.TryGetValue(graphic, out uint to) && art_availableFilePaths.TryGetValue(to, out string p))
                return p;
            return art_availableFilePaths.TryGetValue(graphic, out p) ? p : null;
        }

        public string GetGumpFilePath(uint graphic) => gump_availableFilePaths.TryGetValue(graphic, out string p) ? p : null;

        public string GetArtFilePath(uint graphic) => art_availableFilePaths.TryGetValue(graphic, out string p) ? p : null;
"""),
    ],
    "src/ClassicUO.Renderer/Arts/Art.cs": [
        ("""        public ref readonly SpriteInfo GetLand(uint idx)
""",
         """        // Shattered Legacy (cc-P362): forget one art index's sprite (item ID + 0x4000), so the next draw loads it again
        // (a UI skin was picked or dropped). Its old atlas space is not reclaimed: a few small scrolls per switch.
        public void Invalidate(uint idx)
        {
            if (idx < _spriteInfos.Length)
                _spriteInfos[idx] = default;
        }

        public ref readonly SpriteInfo GetLand(uint idx)
"""),
    ],
    "src/ClassicUO.Client/Configuration/Profile.cs": [
        ("""        public bool WorldMapShowFog { get; set => SetProperty(ref field, value); } = true; // Shattered Legacy patch (cc-P240)
""",
         """        public bool WorldMapShowFog { get; set => SetProperty(ref field, value); } = true; // Shattered Legacy patch (cc-P240)
        public string SlSkins { get; set => SetProperty(ref field, value); } = string.Empty; // Shattered Legacy patch (cc-P362): UI skins, "kind=key;..."
"""),
    ],
    "src/ClassicUO.Client/Game/World.cs": [
        ("""                SeasonFilter.MigrateLegacySqlSettings();
            }
""",
         """                SeasonFilter.MigrateLegacySqlSettings();
            }

            SlSkins.Apply(); // Shattered Legacy patch (cc-P362): this profile's UI skins
"""),
    ],
    "src/ClassicUO.Client/Game/UI/MyraWindows/Options/Tabs/InterfaceTab.cs": [
        ("""                ContainersTab.GetContent,
                new SearchMetadata(TazLang.Get("mog_buttoncontainers"))
            )
""",
         """                ContainersTab.GetContent,
                new SearchMetadata(TazLang.Get("mog_buttoncontainers"))
            )
            .AddTab(
                "Appearance", // Shattered Legacy patch (cc-P362): UI skins
                AppearanceTab.GetContent,
                new SearchMetadata("Appearance", ["skin", "appearance", "backpack", "bag", "chest", "crate", "scroll", "shattered legacy"])
            )
"""),
    ],
}


def edit(rel, pairs):
    path = os.path.join(W, rel)
    with open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    crlf = "\r\n" in text
    if crlf:
        text = text.replace("\r\n", "\n")
    for old, new in pairs:
        n = text.count(old)
        if n != 1:
            sys.exit("%s: found %d times: %r" % (rel, n, old[:70]))
        text = text.replace(old, new)
    if crlf:
        text = text.replace("\n", "\r\n")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print("edited", rel)


for rel, pairs in EDITS.items():
    edit(rel, pairs)

with open(os.path.join(HERE, "SlSkins.cs.template"), encoding="utf-8") as f:
    tpl = f.read()
with open(os.path.join(HERE, "skintable.cs.txt"), encoding="utf-8") as f:
    table = f.read().rstrip("\n")
out = os.path.join(W, "src", "ClassicUO.Client", "Game", "Managers", "SlSkins.cs")
with open(out, "w", encoding="utf-8", newline="\n") as f:
    f.write(tpl.replace("/*TABLE*/", table))
print("wrote", out)
