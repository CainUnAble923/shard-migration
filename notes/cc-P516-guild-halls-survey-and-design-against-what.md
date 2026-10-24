# P516: guild halls survey and design audit

October 24, 2026. Completed report: [Guild hall design compared with main](cc-P516-guild-halls-design-vs-build.md). This file supplies the outer task's requested notes path; the linked report supplies the prompt's requested deliverable path.

The report covers every guild's placement evidence, physical size, decor assignment, entrance and tower status, and remaining work with rough effort sizes. It distinguishes main's placement code and P281's removed private proof world from unverified current placement on shared test or live.

Main implements the halls listed in the report except Maritime. Only Smiths, Artificers, and Alembic receive P265 decor groups. No hall assigns a P265 tower. P459 already contains Chase's decision to make all tower types walkable, but this main still creates fixed wall items at their apparent doors. Maritime's Sea Market map check, Alembic's omitted lab groups, League officer identity, and the old Royal City post remain explicit gaps.

Validation: P281's generator verification passed, the real decor template rows match generated C#, and the existing offline map checker passed every implemented hall. No new tests or runtime checks were added. No code, docs-directory files, world data, or services changed. No commits, branch changes, deployments, or Haven connections occurred.

Progress dry run completed with exit 0 using these work-copy paths. Its incidental progress.json rewrite was restored byte for byte. Only the two P516 notes files are deliverables.

P516 DONE
