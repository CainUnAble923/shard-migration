"""cc-P680: one copy of pinned Decorate.cs reads our Trammel and Felucca decoration (Data/ShatteredLegacy/Decoration).

    python -P edit_decorate.py <Decorate.cs>
"""
import sys

OLD = '''        public static void Generate(string folder, params Map[] maps)
        {
            if (!Directory.Exists(folder))
'''
NEW = '''        public static void Generate(string folder, params Map[] maps)
        {
            // Shattered Legacy (cc-P680, SoS swap S5): a decoration folder we ship under Data/ShatteredLegacy/Decoration
            // (Britannia, Trammel and Felucca: pinned's cfgs decided for the Siege of Sosaria land, made by
            // shard-migration notes/cc-P680-tools/deco.py) is read in place of pinned's; every other folder is pinned's.
            var shardFolder = folder.Replace("Data/Decoration/", "Data/ShatteredLegacy/Decoration/");
            if (Directory.Exists(shardFolder))
            {
                folder = shardFolder;
            }

            if (!Directory.Exists(folder))
'''


def main():
    p = sys.argv[1]
    t = open(p, encoding='utf-8', newline='').read()
    assert t.count(OLD) == 1
    open(p, 'w', encoding='utf-8', newline='').write(t.replace(OLD, NEW))


if __name__ == '__main__':
    main()
