"""cc-P177: notes/art/guild-menus/index.html from the survey rows and the mockups."""
import html, json, os
OUT = r'D:\UO\shard-migration\notes\art\guild-menus'
rows = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'today-survey.json')))
SRC = {
    'GuildDirectory': ('Guild Directory ([guild, the board)', 'ClusterFGuildSystem.cs:879'),
    'HallPage_tailoring': ("Hall page: every guild without its own menu (Tailors' Circle here)", 'ClusterFGuildSystem.cs:1052'),
    'HallPage_thieves': ("Hall page: Thieves' Den", 'ClusterFGuildSystem.cs:1052'),
    'HallPage_alembic': ('Hall page: Order of the Alembic', 'ClusterFGuildSystem.cs:1052'),
    'GuildWelcome': ('New Haven welcome', 'ClusterFGuildStarterPath.cs:795'),
    'StarterItems_tailoring': ('Starter items (any guild)', 'ClusterFGuildStarterPath.cs:845'),
    'Smith_Guildmaster': ('Society of Smiths guildmaster', 'SmithGuildmasterGump.cs:53'),
    'Smith_SealsInfo': ('What are Smithing Seals?', 'SmithGuildmasterGump.cs:371'),
    'Smith_SealCatalog': ('Smith Seal catalog', 'SmithSealCatalogGump.cs:138'),
    'Smith_Commission': ('Smith commissions', 'SmithCommissionGump.cs:40'),
    'Smith_BulkOrderChoice': ('Smith bulk order choice', 'SmithBulkOrderChoiceGump.cs:41'),
    'Smith_GuildBook': ('Smithing Guild Book (remote book)', 'SmithGuildBook.cs:162'),
    'Smith_HammerRestore': ('Hammer of Hephaestus restore and upgrade', 'HammerOfHephaestus.cs:1118'),
    'Smith_HammerFamiliarity': ('Hammer of Hephaestus familiarity', 'HammerOfHephaestus.cs:965'),
    'Mining_Liaison': ("Miners' Compact liaison, main", 'MinersCompactLiaisonGump.cs:102'),
    'Mining_Dashboard': ("Miners' Compact member dashboard", 'MinersCompactLiaisonGump.cs:102'),
    'Mining_Restoration': ("Miners' Compact restoration (nothing to restore)", 'MinersCompactLiaisonGump.cs:102'),
    'Mining_ProspectorsLogbook': ("Prospector's Logbook (ore log book)", 'ProspectorsLogbookGump.cs:70'),
    'Mining_SurveyArchivist': ('Survey Archivist', 'SurveyArchivistGump.cs:66'),
    'Mining_JacobsT2': ("Jacob's Pickaxe T2 upgrade (T3 to T5 the same)", 'JacobsReinforcedPickaxe.cs:223'),
    'Artificers_Guildmaster': ("Artificers' Order guildmaster", 'ArtificersGuildmasterGump.cs:33'),
    'Artificers_Dashboard': ("Artificers' member dashboard", 'ArtificersGuildmasterGump.cs:33'),
    'Artificers_Imbue': ('Imbuing table', 'ArtificersImbueGump.cs:878'),
    'Artificers_Mastery': ('Essence Satchel mastery', 'ArtificersSatchel.cs:173'),
    'Artificers_WorkOrders': ('Artificer work orders', 'ArtificerWorkOrderSystem.cs:532'),
    'Artificers_FormulaShop': ('Formula book shop', 'Imbuing/ImbueFormulaBooks.cs:176'),
    'Artificers_Knowledge': ('Imbue knowledge', 'Imbuing/ImbueFormulaBooks.cs:241'),
    'Foresters_Guildmaster': ("Foresters' Union guildmaster", 'ForestersGuildmasterGump.cs:34'),
    'Foresters_Dashboard': ("Foresters' member dashboard", 'ForestersGuildmasterGump.cs:34'),
    'Foresters_Logbook': ("Forester's Logbook (log book)", 'ForestersLogbookGump.cs:85'),
    'Outriders_Guildmaster': ("Rangers' League (Outriders) guildmaster", 'OutridersGuildmasterGump.cs:34'),
    'Outriders_Dashboard': ('Outriders member dashboard', 'OutridersGuildmasterGump.cs:34'),
    'Custodians_Warden': ('Sanitation Warden (Custodians)', 'SanitationWardenGump.cs:47'),
    'Custodians_CleanUpStore': ('Clean Up Britannia store (cliloc names not drawn here)', 'Services/CleanUpBritannia/CleanUpBritanniaRewards.cs:308'),
    'Contracts_Ledger_smithing': ('Guild Contract Ledger (any guild)', 'GuildContractLedgerGump.cs:45'),
    'MuleExchange': ('Civic Mule Exchange', 'CrossGuildExchangeGump.cs:31'),
    'RecipeShop_tailoring': ('Guild recipe shop (any craft guild)', 'Engines/Craft/GuildRecipeShopGump.cs:130'),
    'Schematics_smithing': ('Mule module schematics (any guild)', 'Mobiles/Mule/MuleModuleGumps.cs:575'),
    'League_Registrar': ('League Registrar, main', 'LeagueRegistrarGump.cs:52'),
    'League_Rank': ('League Registrar, Rank (shown to a non-member)', 'LeagueRegistrarGump.cs:52'),
}
MOCK = [
    ('Smiths_Overview', 'Society of Smiths: Overview. The rank ladder (reached ranks met, the rest gray) and the next rank as requirement lines.'),
    ('Smiths_SealCatalog', 'Society of Smiths: Seal Catalog, page 1 of 3. Price green when you can pay, red when not; the buy arrow gray with no button when you cannot.'),
    ('Miners_Restoration', "Miners' Compact: Restoration. cc-P169's requirement lines, summary and Restore (grayed out: one line not met)."),
    ('Artificers_WorkOrders', "Artificers' Order: Work Orders, page 1 of 2. Action rows with a note, and fields."),
    ('Custodians_Rewards', 'The Custodians: the Clean Up store on the template, page 1 of 4. No crest yet: the placeholder (frame and a broom).'),
    ('League_Rank', "The League: the Registrar's Rank page. The League fits the same base (cc-P179)."),
    ('SmithsBook_Repair', "A guild book (cc-P178): the Society of Smiths' tier 1, remote repair, and what later tiers unlock by rank."),
]
e = html.escape
h = ['''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Guild Menu Mockups</title><style>
:root{--bg:#f6f4ef;--fg:#222;--muted:#666;--line:#ddd;--card:#fff}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#17171a;--fg:#e8e6e1;--muted:#a09c94;--line:#333;--card:#202024}}
:root[data-theme="dark"]{--bg:#17171a;--fg:#e8e6e1;--muted:#a09c94;--line:#333;--card:#202024}
body{background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,sans-serif;margin:0;padding:16px}
main{max-width:1240px;margin:auto}h1{margin:.2em 0}
.q{background:var(--card);border:2px solid #c90;padding:12px 16px;border-radius:8px;font-size:17px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}
.wide{grid-template-columns:repeat(auto-fill,minmax(min(520px,100%),1fr))}
figure{margin:0;background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px}
figure img{width:100%;height:auto;image-rendering:pixelated}figcaption{color:var(--muted);font-size:13px}
table{border-collapse:collapse;width:100%;font-size:12px;display:block;overflow-x:auto}
td,th{border:1px solid var(--line);padding:3px 6px;text-align:left;vertical-align:top}th{background:var(--card)}
code{font-size:12px}
</style></head><body><main>
<h1>Guild menus: one look (cc-P177)</h1>
<p>Mockups of the proposed shared guild menu, <code>GuildMenuGump</code> (<code>server\\customizations\\GuildMenuGump.cs</code>), drawn from the gump entries the server builds, with EA's gump and item art, unifont1 glyphs and hues.mul. The striped backdrop shows the window is opaque. No menu uses the template yet.</p>
<p class="q"><b>For Chase:</b> Approve this look, or say what to change.</p>
<h2>The template: four guilds, the League and a guild book</h2><div class="grid wide">''']
for n, cap in MOCK:
    h.append(f'<figure><img src="mockup-{n}.png" alt="{e(n)}"><figcaption>{e(cap)}</figcaption></figure>')
h.append('''</div><h2>Every guild's crest and accent</h2>
<p>Fourteen guilds use the client's gold guild medallions (5545 to 5592). The Custodians and the Keepers draw a placeholder. The Artificers, the Alembic and the League use stand-ins. <a href="art-requests.md">art-requests.md</a> asks the art lane for those five.</p>
<figure><img src="crests.png" alt="crests" style="max-width:820px"><figcaption>Each crest beside the guild name in its accent hue, on the menu's panel.</figcaption></figure>
<figure style="margin-top:12px"><img src="stock-medallions.png" alt="stock medallions" style="max-width:880px"><figcaption>The stock medallion set, 5545 to 5592, at 2x.</figcaption></figure>
<h2>Survey: today's guild menus</h2>
<p>Every guild menu as a Journeyman member sees it (dumped by <code>GuildMenuTemplateVerification.DumpsTodaysGuildMenus</code>). They all share the 9270 frame and the 9304 rules. They differ in size, in a see-through or solid inside, in header layout, in heading hue (1153 white, or 1154, which TazUO draws green), in button art (4005, 4011, 4014, 4017 and 4023 in different roles) and in how they show requirements.</p>
<table><tr><th>Menu</th><th>Source (server\\customizations)</th><th>Size</th><th>Inside</th><th>Buttons</th><th>Label hues</th><th>HTML colours</th><th>cc-P169 lines</th></tr>''')
for r in rows:
    title, src = SRC.get(r['name'], (r['name'], ''))
    h.append('<tr><td><a href="survey/today-%s.png">%s</a></td><td><code>%s</code></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
        e(r['name']), e(title), e(src), r['size'] if r['size'] != '0x0' else 'images', e(r['inside']),
        ', '.join(map(str, r['buttons'])), ', '.join(map(str, r['label_hues'])), ', '.join(r['html_colours']),
        'yes' if r['p169'] else 'no'))
h.append('</table><h2>Survey renders</h2><div class="grid">')
for r in rows:
    title, src = SRC.get(r['name'], (r['name'], ''))
    h.append(f'<figure><img loading="lazy" src="survey/today-{e(r["name"])}.png" alt="{e(r["name"])}"><figcaption>{e(title)}<br><code>{e(src)}</code></figcaption></figure>')
h.append('</div></main></body></html>\n')
open(os.path.join(OUT, 'index.html'), 'w', encoding='ascii', errors='xmlcharrefreplace').write('\n'.join(h))
print('ok', len(rows), len([r for r in rows if r['name'] not in SRC]))
