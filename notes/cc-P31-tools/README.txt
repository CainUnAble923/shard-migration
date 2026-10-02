cc-P31 tools and their outputs. Read-only unless marked WRITES.

office_z.py          Part A 1 and 2: notes/cc-P19-tools/office_z.py, unchanged but for a header line, run against the
                     14-component design/registrar-office/layout.json. Output: office_z.out.txt.
gen_office_layout.py WRITES: successor of notes/cc-P19-tools/gen_office_layout.py. Writes
                     server/customizations/ClusterFRegistrarOfficeLayout.cs and
                     server/tests/Misc/RegistrarOfficeLayoutDesignCopy.cs from layout.json (same form as P19's), and
                     server/tests/Misc/RegistrarOfficeLayoutP19Copy.cs from design/registrar-office/cleanup/layout_p19.json
                     (the P19-world fixture for the replace facts). Re-run after any change to layout.json.
breaks.py            WRITES: the red-run breaks (A, B, C) and "restore", which puts byte copies back and checks SHA-256
                     and that no P31-BREAK marker is left. A also writes git HEAD's (P19's) generated files back.
