"""cc-P134: the edits to D:\\UO\\tools\\vseUOAware (a copy of vseUOAware's source). Each is exact and asserted."""
import os

ROOT = r'D:\UO\tools\vseUOAware'
NOTE = '// vseUOAware by ghostbyte420, GPL-3.0. Modified for Shattered Legacy 2026-10-17 (cc-P134): %s\n'


def edit(rel, pairs, note):
    p = os.path.join(ROOT, rel)
    raw = open(p, 'rb').read()
    bom = raw.startswith(b'\xef\xbb\xbf')
    s = raw.decode('utf-8-sig')
    for old, new in pairs:
        n = s.count(old)
        assert n == 1, (rel, old, n)
        s = s.replace(old, new)
    s = NOTE % note + s
    open(p, 'wb').write((b'\xef\xbb\xbf' if bom else b'') + s.encode('utf-8'))
    print('edited', rel)


edit('Program.cs', [("    .WithRequestFilters(f => f.AddCallToolFilter(vseUOAware.RulesGate.Filter()))\n", "")],
     'the vseAgentRules gate (RulesGate.cs and its\n// call filter) is removed; it needed vseAgentRules running and called Process.GetProcessById.')

FOLDER = 'outputFolder confined to ExportPathResolver.Folder (exports\\MapCreator\\<name>).'
for rel, sig, var in [
    ('Services/CommonEdit.cs', 'string outputFolder,', 'outputFolder'),
    ('Services/TerrainEdit.cs', 'string outputFolder, string name, int id,', 'outputFolder'),
    ('Services/TransitionCreate.cs', 'string outputFolder,', 'outputFolder'),
]:
    p = os.path.join(ROOT, rel)
    s = open(p, encoding='utf-8-sig').read()
    i = s.index(sig)
    j = s.index('{', i)
    edit(rel, [(s[i:j + 1], s[i:j + 1] + '\n        %s = ExportPathResolver.Folder(%s, "MapCreator");' % (var, var))], FOLDER)

p = os.path.join(ROOT, 'Services/TransitionRepair.cs')
s = open(p, encoding='utf-8-sig').read()
i = s.index('public static RepairResult Run(')
j = s.index('{', i)
edit('Services/TransitionRepair.cs', [(s[i:j + 1], s[i:j + 1] + '\n        outputFolder = ExportPathResolver.Folder(outputFolder, "MapCreator");')], FOLDER)

p = os.path.join(ROOT, 'Services/TransitionAudit.cs')
s = open(p, encoding='utf-8-sig').read()
i = s.index('public static AuditResult Run(')
j = s.index('{', i)
edit('Services/TransitionAudit.cs', [(s[i:j + 1], s[i:j + 1] + '\n        outputFolder = ExportPathResolver.Folder(outputFolder, "MapCreator");')], FOLDER)

p = os.path.join(ROOT, 'Services/TransitionTemplate.cs')
s = open(p, encoding='utf-8-sig').read()
i = s.index('internal static string Run(')
j = s.index('{', i)
edit('Services/TransitionTemplate.cs', [(s[i:j + 1], s[i:j + 1] + '\n        outputFolderPath = ExportPathResolver.Folder(outputFolderPath, "MapCreator");')], FOLDER)

p = os.path.join(ROOT, 'Services/TransitionTemplatesWays.cs')
s = open(p, encoding='utf-8-sig').read()
pairs = []
for sig in ('internal static string RunTwoWay(', 'internal static string RunThreeWay('):
    i = s.index(sig)
    j = s.index('{', i)
    pairs.append((s[i:j + 1], s[i:j + 1] + '\n        outFolder = ExportPathResolver.Folder(outFolder, "MapCreator");'))
edit('Services/TransitionTemplatesWays.cs', pairs, FOLDER)

edit('Tools/MapExportTools.cs', [(
    '''        string baseDir = Path.Combine(AppContext.BaseDirectory, "uoaExport", "Map");
        if (string.IsNullOrWhiteSpace(requested)) return Path.Combine(baseDir, defaultName);
        return Path.IsPathRooted(requested) ? requested : Path.Combine(baseDir, requested);''',
    '''        return ExportPathResolver.Resolve(requested, defaultName, "Map");''')],
    'ResolveOutput goes through ExportPathResolver\n// (it accepted any rooted path).')

edit('Tools/WaterTools.cs', [(
    '''            string outDir = Path.GetFullPath(outputFolder);''',
    '''            string outDir = ExportPathResolver.Folder(outputFolder, "Water");''')],
    'the CSV folder is confined to\n// ExportPathResolver.Folder (exports\\Water\\<name>).')
