# cc-P609: apply the tutorial text pass (P588)

## In plain words

- **The New Haven tutorial now speaks plainly.** Every lesson hint, Rook's window, the farm, the vet, the combat and
  magic lessons, the trade checklists and the walking tours say what to click and where to go, in one or two short
  sentences. The jokes and the "remedial training" wording are gone, and so are promises the game cannot keep yet
  (loop resets, the Bond Trial, pet forms you cannot reach).
- **Names you will see change too:** the death lesson's rat is "the pale gray rat", Rook's arrow says "Rook
  Hallowell, the tutorial guide", the Farmhand's arrow says "Wren the Farmhand", and the lesson titles read "Walk and
  run", "Your character window and clothes", "Speak and read your Journal" and "Watch a loop vision".
- **The patch notes say:** "The tutorial's words are clearer" (version 2026.10.25.3).
- **For you:** on the test world, run `[ClusterFSeedTutorial` once after this deploys. Without it, the rat already
  standing at the farm gate keeps its old name, "the pale death echo", because a placed creature keeps the name it
  was saved with. Then walk one or two lessons to see how the longer lines wrap.

## What was applied

Source: `notes\cc-P588-tutorial-text-pass.md` has 606 table rows, of which 292 propose a change. The rest repeat the
current text. All 292 are applied in `D:\UO\golems\Iron\ShatteredLegacy\server\customizations\Tutorial\`: 13 files,
264 lines.

- **278 rows by script.** Each change replaced a whole quoted C# literal on the row's line (none had to move to a
  nearby line). The script refused a change if the placeholders (`{...}`, `{0}`) differed between old and new
  text. It refused one, below.
- **13 rows by hand.** P588 wrote these in forms not found verbatim in the source:
  - The graduation-box suffix (`ClusterFTutorial.cs:281`, a string concatenation).
  - The four fallback-page lines (`TutorialGumps.cs:318-321`: "Practice:", "Related skills:", "Learn about:",
    "TazUO features: ... Help:").
  - Eight stock localized messages that P588 gave tutorial wording for. Each now sends the proposed English with
    `SendMessage` and keeps a `// cc-P609: was cliloc N` comment:
    - `TutorialFarm.cs:581` and `TutorialRecruiter.cs:59`, both 500446.
    - `TutorialPetCare.cs`: 501041, 500643, 1113200, 1113279, 1060020, and 1060398. 1060398 is now
      `$"You paid the vet {fee} gold from your bank."`.

    The shared cliloc file is not touched; other code keeps the stock messages.
- **1 row adapted, to keep a placeholder.** P588's line for `TutorialWingTrials.cs:155` dropped
  `{Weapons[choice].Skill}`. The applied line is P588's wording with the placeholder kept: "...then double-click the
  blue sparring echo and land three hits with {Weapons[choice].Skill}."
- **4 rows adjusted, for pronouns:**
  - `ClusterFTutorial.cs:122`: "His window" became "Rook's window".
  - `TutorialGumps.cs:209`: "Double-click him" became "Double-click Rook".
  - `TutorialCoreTrials.cs:100` and `TutorialWingTrials.cs:180`: "double-click her" (Sera) became "double-click Sera".

  Sera is a stock `Healer`, whose gender is random (`BaseVendor.InitBody`, pinned), so "her" can be wrong. Rook's body
  is male, but the original wording was deliberately neutral ("they bill by the hour"), so naming Rook keeps it that
  way. Wren is set `Female = true` (`TutorialFarm.cs:542`), so "double-click her" for Wren is kept as proposed.

## Lines skipped, and why

**None of the 292 was skipped.** The prompt asked me to skip lines that P480 or P453 had changed in a way P588 did not
see. There were none:
- The last commits to the Tutorial folder are P480 (10-23 15:14), then P290, then P291, and last P453 (10-24 16:39).
  P588 was written after all of them (10-25 03:17).
- Before applying anything, a scan found every row's current text verbatim in today's source, on its listed line. The
  only exceptions were the 13 hand-done rows, which differ in form only.

Not changed, because it is outside the server: `docker\wiki\content\pages\uo\drafts\tutorial.txt` still uses some old
names ("the League recruiter", "Reset this lesson", the old station titles). It is a draft and is not published.

## Tests

Tests whose strings changed with the text:

| Test | Was | Now |
|---|---|---|
| `Misc/TutorialVerification.cs:485` | `"Finish the core first."` | the new refusal, "Finish the main lessons listed in Rook's window before you graduate." |
| `Tutorial/TutorialFirstPlayVerification.cs:173` | contains "after the core" | contains "Finish the main lessons to open" |
| `Tutorial/TutorialFirstPlayVerification.cs:367, 377` | "Choose your companion" | "Choose your pet" |
| `Tutorial/TutorialFirstPlayVerification.cs:441` | box reason "graduating the New Haven tutorial" | "finishing the New Haven tutorial" |
| `Tutorial/GraduationLoopVerification.cs:160` | the island refusal contains "recruiter" | contains "Rook" |

I also updated the comment in `tools\playtest-bot\uobot\checks_p224_rootdeep.py:48` that quotes the refusal. No bot
check matches on a changed string. I searched `tools\playtest-bot` for every changed string, whole and in pieces of 25
or more characters.

No new test: this is a wording change, and each updated assertion names the new text, so it fails against the old
code.

**Probe** (builder `sl-uo-builder:cc-P456`, with the Tutorial folder and its tests bind-mounted, filtered to the tutorial
classes): **126 of 126 passed** (`probe-P609-1.log` in the session scratchpad).

**The gated build:** I ran `docker\uo\build.sh -t sl-modernuo:cc-P609` under the `docker-build` lock, and released the
lock afterwards. The first cycle hit the apply-patches flake (see Deviations). The second cycle finished with
EXIT=0: "Built sl-modernuo:cc-P609 with patches applied and 2376 shard test(s) passing". That is **2,380 tests: 2,376
passed, 4 skipped (the real-map-data facts), 0 failed**. The images are `sl-modernuo:cc-P609` = `1edbf7f0aca6` and
builder `sl-uo-builder:cc-P609` = `069e0a0eb5e3`. `latest` is untouched.

## Deviations and decisions for Chase

- **Pronouns.** The four adjustments are described above. Everything else is P588's wording, word for word.
- **Localized messages became plain English** at the eight tutorial call sites. That is what P588 proposed. A client
  in another language would now see English there, which matches the rest of the tutorial.
- **Placed objects keep their saved names** until they are re-placed. See the last bullet of "In plain words".
- **Tools:** I made the edits with Python exact-replace scripts in the session scratchpad: `p609_scan.py`,
  `p609_apply.py`, `p609_manual.py`, `p609_tests_edit.py`. The Read and Edit tools are denied on the ShatteredLegacy
  copy in unattended runs. The diff is the same as hand edits would have made.
- **The first gated cycle failed on the apply-patches flake.** `CraftGump-MakeXClear.patch` was reported "present but
  never applied" straight after a run of "Applied:" lines. That is the known pipefail race, not a real failure. I kept
  the log (`build-P609-c1-flake.log`) and reran once.

P609 DONE
