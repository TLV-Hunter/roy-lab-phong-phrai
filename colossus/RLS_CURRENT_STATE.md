# RLS AI STUDIO — CURRENT STATE
Updated: 2026-09-08 09:58 Asia/Bangkok

## PUBLICATION TRUTH
Published so far:
- RLS-001 Still — PUBLISHED
- RLS-001 Reel — PUBLISHED
- RLS-002 Still — PUBLISHED / confirmed by TalentVee as posted last night (Sep07)

Not published:
- RLS-002 Reel — NOT PUBLISHED
- RLS-003 Still — NOT PUBLISHED
- RLS-003 Reel — NOT PUBLISHED

Do not mark RLS-002 Reel, RLS-003, or later episodes as published unless TalentVee confirms publication or the publishing system verifies it.

## OFFICIAL DAILY PUBLISHING QUEUE V1
Locked daily rule:
- 10:00 Asia/Bangkok — MASTER STILL
- 20:00 Asia/Bangkok — FINAL REEL
- STARTER FRAME is production-only and must not be posted.
- If Final Reel is not QA PASS by publish time, do not post a failed asset; finish/repair that Reel first.
- Do not skip episode order merely to fill a slot.

Current catch-up state:
- Sep07 — RLS-002 Master Still — PUBLISHED
- Sep08 — RLS-002 Final Reel — NEXT TO PUBLISH at 20:00
- Sep09 — RLS-003 — resume normal pair: 10:00 Still / 20:00 Reel

Official queue after catch-up:
- Sep09 — RLS-003 — This boulder was not here yesterday.
- Sep10 — RLS-004 — The forest went silent first.
- Sep11 — RLS-005 — Both sides of the bridge failed at the same height.
- Sep12 — RLS-006 — The fog moved upstream.
- Sep13 — RLS-007 — Camera 07 was found 28 feet above the trail.
- Sep14 — RLS-008 — Tonight’s footage matches a file from 1998.
- Sep15 — RLS-009 — The 1998 map shows a river where the trail is now.
- Sep16 — RLS-011 — FIELD RULE 01
- Sep17 — RLS-010 — You hear it before you see it.
- Sep18 — RLS-013 — The highest gouge was nearly twelve feet up.
- Sep19 — RLS-012 — The tree moved twice.
- Sep20 — RLS-015 — Camera 07 came back online from above us.
- Sep21 — RLS-016 — The station was abandoned in 2014. The radio answered tonight.
- Sep22 — RLS-014 — It looked small until it stood up.
- Sep23 — RLS-018 — Only one set going in. Nothing came back out.
- Sep24 — RLS-019 — Only one camera saw it.
- Sep25 — RLS-020 — The bark was still warm.
- Sep26 — RLS-017 — Every camera skipped the same 17 minutes.
- Sep27 — RLS-022 — CASE 001 — The Hollow Trail.
- Sep28 — RLS-023 — The missing pack was found twenty feet above the ground.
- Sep29 — RLS-024 — Reflection mismatch.
- Sep30 — RLS-025 — FIELD RULE 02.
- Oct01 — RLS-026 — Camera Network Finale.

## SEPTEMBER ASSET INVENTORY
Mainline Still Sep07–Sep30:
- 24/24 QA PASS / ready

Starter Frames:
- 24/24 have a starter base
- 19 new/rebuilt starters completed
- Set1 10/10 PASS
- Set2 9/9 PASS
- RLS-014 final rebuild: PASS 95 / LOCK
- RLS-018 final rebuild: PASS 95 / LOCK
- discarded wrong generations / collages must never be reused

Video Prompts:
- 24/24 QA PASS / LOCK
- Seedance 2.0 Fast oriented
- Audio ON
- continuity protections added

Copy QA library:
- September public still/reel copy library is QA PASS for all listed RLS episodes.
- RLS-003 Reel copy is 95/100 PASS in `rls-copy-qa.json`; any PENDING label elsewhere is stale data and must be synchronized.

Final Reel production:
- RLS-002 — FINAL QA PASS / READY / 1080×1920
- RLS-003 — FINAL QA PASS / READY / 1080×1920
- Mainline Final Reels ready: 2/24
- Remaining Final Reels: 22/24, beginning RLS-004 through RLS-026.

## RLS-002 FINAL
Title: “It was already in the frame.”
- Master Still publication: PUBLISHED Sep07 (exact posting time not recorded)
- Final Reel: QA PASS / READY
- Dola AI removed by crop/reframe
- CAMERA 07 / 02:17:43 AM continuity preserved
- Resolution: 1080×1920, 24fps
- Drive ID: 1NHs7X2HU6RwzNI0FnLZfbAYyA4Gl1nML
- Website: wired to RLS-002 Reel slot
- Reel publication: NOT PUBLISHED

## RLS-003 FINAL
Title: “This boulder was not here yesterday.”
- Final edit: QA PASS
- Dola AI removed by crop/reframe
- CREEK CROSSING / 02:37 AM preserved
- Resolution: 1080×1920, 24fps
- Drive ID: 1FHJ4hhqnS4CKt56CGie-isGnfbFqHSLv
- Website: wired to RLS-003 Reel slot
- Reel copy QA: 95/100 PASS in `rls-copy-qa.json`
- Publication: NOT PUBLISHED

## WEBSITE STATE
Main website:
https://tlv-hunter.github.io/roy-lab-phong-phrai/colossus/

Main DESK file:
colossus/index.html

Large daily queue page:
https://tlv-hunter.github.io/roy-lab-phong-phrai/colossus/rls-daily-queue.html

Daily queue source:
colossus/rls-daily-queue.html

Current daily queue UX:
- Large TODAY / NEXT hero.
- RLS-002 Still visibly marked POSTED / DONE.
- RLS-002 Reel highlighted as next pending publication.
- Normal pair schedule resumes with RLS-003 on Sep09.
- Starter Frame remains production-only.
- Publication status is visually separated from the plan.

RLS Reel data:
colossus/rls-content.json

Current DESK behavior:
- RLS-002 and RLS-003 Reel slots use Drive final-video URLs.
- Reel label reads actual resolution when supplied, e.g. REEL • FINAL 1080×1920.
- Reel buttons use OPEN FINAL REEL / DOWNLOAD FINAL rather than falsely claiming 4K.
- Master Still and Starter Frame 4K behavior remains unchanged.
- CHECKLIST / CALENDAR / BATCH QA / STRATEGY / PERFORMANCE / PUBLISHER preserved.

## LIVE BACKLOG AUDIT — UNFINISHED / NEEDS SYNC
Priority A — publication / schedule:
1. Publish RLS-002 Final Reel at 20:00 Sep08.
2. Metricool still has three old auto-publish schedules that conflict with Official Queue V1:
   - Sep15 21:00 — RLS-011 FIELD RULE 01
   - Sep17 21:00 — RLS-013 High Gouges
   - Sep24 21:00 — RLS-020 Warm Bark
   These must be rescheduled or cancelled before their current trigger dates.

Priority B — production:
3. Produce 22 remaining Final Reels from RLS-004 through RLS-026 using locked Starter + Prompt → Raw QA → repair → final edit/audio → final QA → upload.

Priority C — source-of-truth synchronization:
4. `colossus/rls-content.json` is stale in several fields:
   - RLS-002 Still still says LOCKED instead of PUBLISHED.
   - several copy_qa fields say PENDING although `rls-copy-qa.json` is PASS.
   - Reel `post_time` fields still use historical 18:00 while Official Queue V1 uses 20:00.
   - some episode dates reflect the pre-catch-up queue.
5. The ChatGPT Project Sources copy of `RLS_CURRENT_STATE.md` uploaded on Sep07 is stale and still says RLS-002 was not posted. Replace it with the latest current state after this audit so new Project chats do not recover outdated publication truth.

Priority D — technical / optional quality upgrade:
6. True AI 4K Reel pipeline is not yet verified in the current editing runtime. Real-ESRGAN / realesrgan-ncnn-vulkan is NOT VERIFIED / NOT INSTALLED. Current RLS-002 and RLS-003 finals are truthfully 1080×1920. This is not a posting blocker, but it remains unfinished if true AI-upscaled 4K is a project requirement.

## TOOL REALITY
Current editing environment check:
- Real-ESRGAN / realesrgan-ncnn-vulkan: NOT VERIFIED / NOT INSTALLED in this runtime
- Do not call simple resize true 4K.
- Current RLS-002 and RLS-003 finals are truthfully labeled 1080×1920.

## EXACT NEXT ACTION
1. Synchronize operational data before it causes publishing mistakes: Metricool old schedules + stale `rls-content.json` + stale ChatGPT Project `RLS_CURRENT_STATE.md`.
2. Sep08 20:00 — publish RLS-002 Final Reel using the QA-PASS copy.
3. Continue batch Final Reel production from RLS-004 onward until the 22-reel backlog is cleared.
4. Resume normal publishing pair with RLS-003 on Sep09: 10:00 Still / 20:00 Reel.
5. Keep publication truth synchronized only with actual confirmed posts.
