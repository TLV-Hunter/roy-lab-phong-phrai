# RLS AI STUDIO — CURRENT STATE
Updated: 2026-09-08 10:20 Asia/Bangkok

## PUBLICATION TRUTH
Published so far:
- RLS-001 Still — PUBLISHED
- RLS-001 Reel — PUBLISHED
- RLS-002 Still — PUBLISHED / confirmed by TalentVee as posted on Sep07 night

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
- Catch-up rule: if the previous Still is already published but its Reel is pending, close that episode with the Reel before opening the next episode.

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

## ASSET INVENTORY
Mainline Stills:
- 24/24 QA PASS / ready

Starter Frames:
- 24/24 QA PASS / ready
- discarded wrong generations / collages must never be reused

Video Prompts:
- 24/24 QA PASS / LOCK
- Seedance 2.0 Fast oriented
- Audio ON
- continuity protections added

Copy QA:
- September public Still/Reel copy library is QA PASS for all listed RLS episodes.

Final Reel production:
- RLS-002 — FINAL QA PASS / READY / 1080×1920
- RLS-003 — FINAL QA PASS / READY / 1080×1920
- Mainline Final Reels ready: 2/24
- Remaining Final Reels: 22/24, beginning RLS-004 through RLS-026.

## RLS-002 FINAL
Title: “It was already in the frame.”
- Master Still: PUBLISHED Sep07
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
- Reel copy QA: 95/100 PASS
- Publication: NOT PUBLISHED

## METRICOOL — SYNCED TO OFFICIAL QUEUE V1
Verified pending Facebook auto-publish schedules:
- Sep16 10:00 — RLS-011 FIELD RULE 01 — Metricool ID 372486721 / UUID 149216554598286220
- Sep18 10:00 — RLS-013 High Gouges — Metricool ID 372486749 / UUID 1651887173610391708
- Sep25 10:00 — RLS-020 Warm Bark — Metricool ID 372486632 / UUID 624171268109978941

The old Sep15 21:00 / Sep17 21:00 / Sep24 21:00 schedule conflict has been cleared.

## WEBSITE / DATA STATE
Main website:
https://tlv-hunter.github.io/roy-lab-phong-phrai/colossus/

Large daily queue:
https://tlv-hunter.github.io/roy-lab-phong-phrai/colossus/rls-daily-queue.html

Data synchronization completed:
- `colossus/rls-content.json` synchronized to Official Queue V1, RLS-002 Still publication truth, PASS copy state, 20:00 Reel time, catch-up dates, and current Metricool IDs.
- `colossus/rls-plan.json` replaced with canonical Official Daily Publishing Queue V1.
- Main DESK `PUBLISHER` is now campaign-aware:
  - RLS selected → opens `rls-daily-queue.html`
  - COLOSSUS selected → preserves `plan.html`
- Unrelated DESK / CHECKLIST / CALENDAR / BATCH QA / STRATEGY / PERFORMANCE behavior preserved.

Latest synchronization commits:
- rls-content sync: acab0ff6563239f68fc16c30e935629e4d48f753
- rls-plan sync: 172a10f54551758a524cc929c4066f07854e0640
- PUBLISHER campaign routing: e5964be408eb948d7b6a63909aab34a349c04c49
- PUBLISHER HTML-escape QA repair: 728422c824ed008f69e271798bb62ff64eba89cf

## PROJECT SOURCE SYNC
The GitHub Current State is now current.
The copy of `RLS_CURRENT_STATE.md` already uploaded to ChatGPT Project Sources is still the older Sep07 file and cannot be replaced from the GitHub connector.
Replace that Project Source with the latest file exported from this state so new Project chats recover the correct publication truth and queue.

## TOOL REALITY
- Real-ESRGAN / realesrgan-ncnn-vulkan is NOT VERIFIED / NOT INSTALLED in the current editing runtime.
- Do not call simple resize true 4K.
- Current RLS-002 and RLS-003 finals are truthfully labeled 1080×1920.
- True AI 4K remains optional / unfinished and is not a posting blocker.

## REMAINING BACKLOG
1. Publish RLS-002 Final Reel at 20:00 Sep08.
2. Produce the 22 remaining Final Reels RLS-004 through RLS-026.
3. Replace the stale ChatGPT Project Source copy of `RLS_CURRENT_STATE.md` with the latest exported file.
4. Optional: establish and verify a true AI 4K Reel pipeline if 4K Reel delivery becomes mandatory.

## EXACT NEXT ACTION
1. Export this latest `RLS_CURRENT_STATE.md` for ChatGPT Project Source replacement.
2. Sep08 20:00 — publish RLS-002 Final Reel using the QA-PASS copy.
3. Continue batch Final Reel production from RLS-004 onward until the 22-reel backlog is cleared.
4. Resume normal publishing pair with RLS-003 on Sep09: 10:00 Still / 20:00 Reel.
5. Keep publication truth synchronized only with actual confirmed posts.
