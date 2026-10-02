# cc-P29 Part G: watch the two changed tool facts fail for the reason each targets, then pass, without editing
# tools/. Run from anywhere:  python tool_red.py red-satchel | red-twin | green
#   red-satchel  READER_SITES without 'SatchelTypes' (the state before cc-P29)
#   red-twin     the twin sweep's cliloc-only test switched off (labels dropped from the pinned side)
import os, sys, unittest
TOOLS = r'D:/UO/shard-migration/tools'
sys.path.insert(0, TOOLS)
os.chdir(TOOLS)
import content_index as ci
import test_content_index as t

mode = sys.argv[1] if len(sys.argv) > 1 else 'green'
if mode == 'red-satchel':
    ci.READER_SITES.discard('SatchelTypes')
elif mode == 'red-twin':
    real = ci.type_facts

    def no_labels(root):
        facts = real(root)
        return {n: (f, g, None) for n, (f, g, lab) in facts.items()} if os.path.normcase(root) == os.path.normcase(ci.M) else facts

    ci.type_facts = no_labels

names = ['test_twin_sweep_finds_a_pinned_type_under_another_name',
         'test_reach_the_guild_satchel_list_reads_types_and_makes_none']
suite = unittest.TestSuite(t.ContentIndexTest(n) for n in names)
r = unittest.TextTestRunner(verbosity=2).run(suite)
print(mode, 'failures:', len(r.failures), 'errors:', len(r.errors))
