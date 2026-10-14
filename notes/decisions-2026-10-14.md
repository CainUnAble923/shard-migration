# Chase's decisions, 2026-10-14 (overseer chat, 05:59 to 06:06)

Answers to the open questions from P80, P89, P90, P91 and P93. Prompts drafted from these cite this file.

## Boot bug and deploys
- D89 (HEAD does not boot, ImbueCatalogue): logged, fix soon. Prompt **P95**, queued behind P94.
- Chase re-ran `Start-TestQueue.ps1` after P90; the Ideas tab is live.

## Shard Console (new requests)
- Controls on the console for the websites: start, stop, redeploy and open for the play-test site, status page,
  public website and wiki.
- **A button or tab to open Nginx Proxy Manager** (NPM) from the console.
- Haven deploys as a console function: a button that runs a named deploy script on Haven over SSH with Chase's key,
  only when he clicks it. CC never holds keys to Haven. (Answer to P89 #8.)

## Haven pages (P89)
1. Shape: yes.
2. Who gets in: Chase and his daughter, both pages, each result marked by who made it.
3. Hostname: `ops.shatteredlegacyuo.com` (Cloudflare Access, email code, 24 h, as recommended).
4. Repo pull on Haven: git-pull container, every 2 minutes.
5. Shard login (H6): **sooner rather than later.** Build it right after the first Haven pages. Separate
   `[webpassword`, never the game password; lockout and rate limits.
6. Game PC stats on Homepage: from the snapshot.
7. Haven containers on Homepage: yes, through a read-only socket proxy.
8. Deploys on Haven: Chase-run, as a one-click console function (above).
9. Stale Homepage and checkout: as recommended (replace that Homepage in H5, leave `~/shattered-legacy` alone, note
   which Homepage is real in `docker\dashboard\README.md`). Explained to Chase 10-14.
10. `dashboard.shatteredlegacyuo.com`: Chase is checking NPM himself; instructions given 10-14.
11. Rename "Migration status" to "Public progress page": yes.

## Overnight bot (P91)
- The rule rewording is fine: the bot gathers evidence, Chase reviews its report and marks every result.
  (Overseer places it in `docs\client-test-queue.md`.)
- Nightly scheduled task: yes, but **only run when there are items it can test**, and **email before the run and
  after**.
- Transcripts: **keep 14 days in the repo, then archive** to iCloud Drive (`D:\Cloud Drives\iCloudDrive`, the Windows
  iCloud sync root; a `Shattered Legacy\bot-runs\` folder there) before deleting from the repo. Reports and results
  stay in the repo forever.
- The 6 eyes-only items: Chase will do them from the play-test page.

## Ideas inbox (P90)
- **Bug reports inbox** on the play-test page, linkable to a play test or new: prompt **P96** (with the reason rule).
- **Declining or deleting an idea requires a reason**, so the reason is never forgotten.

## servuo.dev assessment (P93)
- Go on the draft prompts. Staff tools (Building Duplicator, Visual Builder) now; Animal Lore dashboard and specimen
  rating after the Pet Training port; League hunts after the port.
- Vault Pass: not at this time.
- Virtual storage: not at this time, keep as a possibility.
- Power Hour: **rebuild natively** (after the port). Chase believes the Vita-Nex system breaks the TazUO client on
  Immortal Realms; the rebuild must not do whatever causes that.
- Animal Lore dashboard GPL-3.0 header: fine (explained to Chase 10-14).
- Unzip UORespawn's ModernUO scripts for a closer read: yes.
- Add the assessment copy to the Claude project: yes.

## Tutorial (P80)
1. **Live never existed.** It is never turned on until a 1.0 state. When the tutorial update is pushed, **all
   accounts are wiped** to force the tutorial. No "existing characters" handling is needed.
2. Recruiter: keep Rook Hallowell.
3. The "System:" voice is the Echo.
4. Achievement values: as proposed.
5. Graduation box: as proposed (Explorer's tier 1, Common).
6. TazUO client patch (about 30 lines, whitelisted 0xCE ClientCommand): yes.
7. Loop placeholders: parked with F-12, after the port.
8. Trial order: **hybrid (option C).** The 9-station core stays required and short; after it the Echo guides through
   the wings in F-35's story order as the suggested path, on the farm; any wing can be taken or left.
9. **Combat wing teaches melee and ranged**, both (not a single weapon pick).
10. **Housing wing gives a teeny tiny first home:** an instanced room through an Inn, decoratable, very little space
    and storage. Logged as **F-44** in `docs\feature-queue.md` for the features chat to design.
