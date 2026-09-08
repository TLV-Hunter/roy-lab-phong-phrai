# RLS AI STUDIO — CURRENT STATE
Updated: 2026-09-08 08:42 Asia/Bangkok

## PUBLICATION TRUTH
Published so far:
- RLS-001 Still — PUBLISHED
- RLS-001 Reel — PUBLISHED

Not confirmed published:
- RLS-002 Still — NOT CONFIRMED POSTED
- RLS-002 Reel — NOT PUBLISHED
- RLS-003 Still — NOT CONFIRMED POSTED
- RLS-003 Reel — NOT PUBLISHED

Do not mark RLS-002, RLS-003, or later episodes as published unless TalentVee confirms publication or the publishing system verifies it.

## OFFICIAL DAILY PUBLISHING QUEUE V1
Locked daily rule from 2026-09-08:
- 10:00 Asia/Bangkok — MASTER STILL
- 20:00 Asia/Bangkok — FINAL REEL
- STARTER FRAME is production-only and must not be posted.
- If Final Reel is not QA PASS by publish time, do not post a failed asset; finish/repair that Reel first.
- Do not skip episode order merely to fill a slot.

Official queue:
- Sep08 — RLS-002 — It was already in the frame.
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

Final Reel production:
- RLS-002 — FINAL QA PASS / READY / 1080×1920
- RLS-003 — FINAL QA PASS / READY / 1080×1920
- Mainline Final Reels ready: 2/24
- RLS-004 onward still requires actual generation, raw QA, final edit/QA, and upload.

## RLS-002 FINAL
Title: “It was already in the frame.”
- Final edit: QA PASS
- Dola AI removed by crop/reframe
- CAMERA 07 / 02:17:43 AM continuity preserved
- Resolution: 1080×1920, 24fps
- Drive ID: 1NHs7X2HU6RwzNI0FnLZfbAYyA4Gl1nML
- Website: wired to RLS-002 Reel slot
- Publication: NOT PUBLISHED

## RLS-003 FINAL
Title: “This boulder was not here yesterday.”
- Final edit: QA PASS
- Dola AI removed by crop/reframe
- CREEK CROSSING / 02:37 AM preserved
- Resolution: 1080×1920, 24fps
- Drive ID: 1FHJ4hhqnS4CKt56CGie-isGnfbFqHSLv
- Website: wired to RLS-003 Reel slot
- Reel copy QA: PENDING
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

Daily queue commit:
- fe9beb3fd61d2329f7a1872b9958480e428fe019

Current daily queue UX:
- Large TODAY / NEXT hero.
- Large fixed 10:00 MASTER STILL and 20:00 FINAL REEL blocks.
- Full Sep08–Oct01 episode queue.
- Current Bangkok date is highlighted automatically.
- Clear warning that Starter Frame is not a publishing asset.
- Publication plan is visually separate from actual publication truth.
- Built as a separate page so existing DESK/CHECKLIST/CALENDAR/BATCH QA/STRATEGY/PERFORMANCE behavior is not modified.

RLS Reel data:
colossus/rls-content.json

Latest Reel data commit:
- 1de448d43d649c896cf2d73f4b6a111c3a471f67

Latest DESK truthful-resolution UI commit:
- 279c767e6b62dc216e2aea93b65fd69b17c34e56

Current DESK behavior:
- RLS-002 and RLS-003 Reel slots use Drive final-video URLs.
- Reel label reads actual resolution when supplied, e.g. REEL • FINAL 1080×1920.
- Reel buttons use OPEN FINAL REEL / DOWNLOAD FINAL rather than falsely claiming 4K.
- Master Still and Starter Frame 4K behavior remains unchanged.
- CHECKLIST / CALENDAR / BATCH QA / STRATEGY / PERFORMANCE / PUBLISHER preserved.

## TOOL REALITY
Current editing environment check:
- Real-ESRGAN / realesrgan-ncnn-vulkan: NOT VERIFIED / NOT INSTALLED in this runtime
- Do not call simple resize true 4K.
- Current RLS-002 and RLS-003 finals are truthfully labeled 1080×1920.

## EXACT NEXT ACTION
1. Today Sep08: publish RLS-002 Master Still at 10:00 Asia/Bangkok if still not published.
2. Publish RLS-002 Final Reel at 20:00 only after publication copy is confirmed QA PASS.
3. Continue Final Reel production from RLS-004 using locked Starter + Prompt → Raw QA → repair if needed → final edit/audio → final QA → upload.
4. Keep publication truth unchanged until actual posting is confirmed.
