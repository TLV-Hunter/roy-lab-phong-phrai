# RLS AI STUDIO — CURRENT STATE / RECOVERY CHECKPOINT

Updated: 2026-09-06 01:02 Asia/Bangkok
Status: ACTIVE RECOVERY CHECKPOINT
Owner: TalentVee
Primary repo: `TLV-Hunter/roy-lab-phong-phrai`
Web area: `colossus/`

## 1. GOVERNING DIRECTION

- Project: **RLS AI STUDIO — รอยลับพงไพร**
- International-first reboot. New audience-facing content is English-first.
- Old Thai posts remain unchanged.
- Brand direction: **Hybrid** — easy/viral mystery on the surface, recurring hidden universe underneath.
- Content DNA:
  - RLS — EVIDENCE
  - RLS — ENCOUNTER
  - RLS — ARCHIVE
- Recurring identifiers may include `FIELD LOG`, `FIELD RULE`, `CAMERA 07`, `CASE 001`, `SECTOR H-4`.

## 2. ACTIVE PRODUCTION MODE

**IMAGE-FIRST • REELS HOLD**

User directive: finish the complete image pipeline first. Reel production remains frozen until the image set is complete, QA-passed, stored and represented in the web control system.

Rules:
- 1 image = 1 file.
- Production image target = 30 images total.
- Never expose internal production labels such as Batch/Image # in public-facing artwork.
- Master Still only becomes ready after QA1 PASS + QA2 PASS.
- Starter Frame only becomes ready after Frame QA PASS + Prompt QA PASS.
- Starter Frames are production assets and do not count as public still posts.
- Do not generate Reel video until user explicitly lifts the hold.

## 3. QA MODEL

### QA1 — Growth & Story
Score: STOP 20 / STAY 25 / PAYOFF 20 / SHARE 15 / FOLLOW 10 / ORIGINALITY 10 = 100
- <85 FAIL
- 85–89 REVISE
- 90–94 PASS—TEST
- 95+ HERO CANDIDATE

### QA2 — Visual / Technical / Policy / Monetization
Checks identity, anatomy, scale, perspective, lighting, physics, continuity, artifacts, camera, composition, reveal, sound readiness, originality and policy.
Verdict: PASS / PASS WITH MINOR FIX / REVISE / REJECT-REBUILD.

## 4. IMAGE BATCH STATUS

### BATCH 1 — #01–#10
- **LOCKED**
- 10/10 image assets passed QA.
- Do not regenerate.

### BATCH 2 — #11–#20
- **IN QA**
- Passed/public-ready slots: #11, #13, #16, #19, #20.
- Unresolved correction slots: **#12, #14, #15, #17, #18**.
- These are the FIRST rebuild targets when image generation becomes available again.

### BATCH 3 — #21–#30
- **WAITING**
- Not started.
- #21 Sep25 — It never crossed the trail.
- #22 Sep26 HERO — CASE 001 — The Hollow Trail.
- #23 Sep27 — After CASE 001, we found this.
- #24 Sep28 — No one noticed the second pair of eyes.
- #25 Sep29 — FIELD RULE 02.
- #26 Sep30 FINALE — Camera 07 wasn’t the only one recording.
- #27–#30 = hero backup images around Sep12 / Sep19 / Sep26 / Sep30.

## 5. SEPTEMBER CALENDAR STATE

Default public test time: **21:00 Asia/Bangkok**.
Sep5 launch still used 20:30.

- Sep05 — STILL — QA PASS — **PUBLISHED**
- Sep06 — REEL STARTER — Frame PASS / Prompt PASS — **HOLD**
- Sep07 — STILL — QA PASS — READY
- Sep08 — REEL STARTER — Frame PASS — HOLD
- Sep09 — STILL / ARCHIVE — QA PASS — READY
- Sep10 — REEL STARTER — Frame PASS — HOLD
- Sep11 — STILL — QA PASS — READY
- Sep12 — HERO STARTER — Frame PASS — HOLD
- Sep13 — STILL / ARCHIVE — QA PASS — READY
- Sep14 — REEL STARTER — Frame PASS — HOLD
- Sep15 — STILL FIELD RULE 01 — QA PASS — **SCHEDULED**
- Sep16 — starter concept — REVISE / BLOCKED
- Sep17 — STILL High Gouges — QA PASS — **SCHEDULED**
- Sep18 — starter concept — REBUILD / BLOCKED
- Sep19 — HERO starter — REVISE / BLOCKED
- Sep20 — STILL SECTOR H-4 — QA PASS — READY
- Sep21 — starter concept — REVISE / BLOCKED
- Sep22 — STILL / ARCHIVE RECOVERED NOTE — REVISE / BLOCKED
- Sep23 — REEL STARTER — QA PASS — HOLD
- Sep24 — STILL Warm Bark — QA PASS — **SCHEDULED**
- Sep25–Sep30 — WAITING IMAGE / Reel remains HOLD

## 6. CONFIRMED RLS CONTENT ARCHIVED IN GITHUB WEB DATA

Current data source: `colossus/rls-content.json`
Current plan source: `colossus/rls-plan.json`

Archived/passed records in `rls-content.json`:
- RLS-001 NORTH TRAIL / 02:11 AM — published
- RLS-002 CAMERA 07 — starter frame archived, Frame QA PASS, Prompt QA PASS, Reel HOLD
- RLS-003 HIGH MARKS — ready, archived preview + Drive reference
- RLS-004 FOREST WENT SILENT — starter frame PASS; prompt intentionally withheld until Prompt QA
- RLS-005 FIELD LOG 001 — ready, archived
- RLS-006 FOG MOVED WRONG — starter frame PASS; prompt withheld
- RLS-007 CAMERA 07 MOVED — ready, archived
- RLS-008 1998 MATCH — hero starter PASS; prompt withheld
- RLS-009 SAME MARK / DIFFERENT YEAR — ready, archived
- RLS-010 HEAR IT FIRST — starter PASS; prompt withheld
- RLS-011 FIELD RULE 01 — scheduled, archived preview
- RLS-013 HIGH GOUGES / SCALE — scheduled, archived preview
- RLS-016 SECTOR H-4 — ready, archived preview
- RLS-019 ONLY ONE CAMERA SAW IT — starter archived, Frame QA PASS, prompt withheld
- RLS-020 BARK WAS STILL WARM — scheduled, archived preview

## 7. CONFIRMED DRIVE / METRICOOL STATE

Scheduled through Metricool at 21:00 Asia/Bangkok:
- Sep15 FIELD RULE 01
- Sep17 HIGH GOUGES / SCALE
- Sep24 BARK WAS STILL WARM

Known published launch still:
- Sep05 NORTH TRAIL / 02:11 AM

Do not describe Metricool `firstCommentText` as a pinned comment; it is a first comment.

## 8. WEB / GITHUB DIRECTION

The user does **not** want a separate Airtable-login control surface.
The RLS control should live with the existing Colossus web system in the same GitHub Pages project.

Repository contains Colossus web assets including:
- `colossus/index.html`
- `colossus/plan.html`
- `colossus/content.json`
- `colossus/rls-content.json`
- `colossus/rls-plan.json`
- `colossus/assets/...`

The correct product direction is one hosted GitHub web app / one operational surface, with Colossus and RLS data in the same web project. No extra Airtable login for normal use.

## 9. RECOVERED GITHUB HISTORY — RLS

Important RLS commits recovered from the lost chat period:
- `4d48f33f0dfbcce81e00b9054077cdf5939ada58` — Sync RLS plan to image-first hold only.
- `c78a167ff65da5196c2f493e455f34319894e624` — Archive RLS starter preview only.
- `c968fd99eba2e964e785382369275a9d65fc7151` — Link RLS Camera 07 starter preview only.
- `282f6337488b7fe26962e7869fec68be77d4a2f8` — Archive RLS Batch 1 previews 03–06 only.
- `d1a82674aaad204dec8de4002928a654b377340e` — Archive confirmed RLS previews 07 and 09 only.
- `ad93ac5ad7cbe220b09a2cf96bd1094cc9fa0007` — Archive confirmed RLS stills and starter references only.
- `c876ded362ec095a097a7642c8dd2167c05dfd44` — Archive RLS Batch 2 previews 11 and 13 only.
- `8f06bb15ad08fcc5a99c274ecb2578aed7a3ecea` — Link RLS Batch 2 previews 11 and 13 only.
- `267efe07f63aa94eadd5e63cf928b4bf7d42d1b3` — Archive RLS Batch 2 previews 16, 19, 20 only.
- `93b1b083001c79b649db46fa0a4c9b262a92674f` — Link RLS Batch 2 previews 16, 19, 20 only.

Latest confirmed RLS data timestamp in `rls-content.json`: **2026-09-06T00:35:00+07:00**.

## 10. FIRST WORK WHEN IMAGE LIMIT RETURNS

Rebuild ONLY unresolved Batch 2 slots, in this order:
1. #12 Sep16 — The tree moved twice.
2. #14 Sep18 — It looked small until it stood up.
3. #15 Sep19 HERO — Camera 07 came back online.
4. #17 Sep21 — The same shadow appeared on two cameras.
5. #18 Sep22 — RECOVERED NOTE / one set of tracks going in.

Then:
- QA1 + QA2 each image.
- Lock Batch 2.
- Build Batch 3 #21–#30 as separate 1:1 files.
- QA and archive.
- Keep Reel generation frozen until user lifts IMAGE-FIRST hold.

## 11. IMMEDIATE WEB NEXT ACTION

While image generation is unavailable:
- Finish the hosted GitHub web control, not a separate offline tool.
- Make RLS visible alongside Colossus in the same web experience.
- Use `rls-content.json` + `rls-plan.json` as the RLS sources of truth.
- Expose monthly still/image plan, QA status, previews, captions, first comments, schedule state and Next To Do.
- Never show REVISE / REBUILD assets as READY.
- Keep REELS HOLD obvious in the UI.

This file is the recovery checkpoint to use if the chat disappears again.
