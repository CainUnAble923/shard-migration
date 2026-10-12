# Client test queue (fixture: three rows in the real file's shape)

## A. In the UO client

| ID | Status | Check | How | Pass | Source |
|---|---|---|---|---|---|
| T-001 | ⬜ OPEN | **MAKE X label** | Open any craft menu, look at the MAKE X entry | Text is visible | cc6 sheet 1.1 |
| T-009 | ✅ PASS | **Gargoyle starts dressed** | Create a gargoyle | A kilt | D26 |
| T-040 | ❌ FAIL | **Guild Directory and joining** | Board first page, pick a guild, join | Directory lists the guilds | cc-P15 F-9 |

---

## Results

- T-040, 2026-10-01: **FAIL, and it splits in two.** Joining a guild works. (a) **The Guild Directory
  lists the Artificers twice**: **D41**.
- T-009, 2026-09-30: **PASS.** New gargoyle characters start with a kilt.
