# COLOSSUS SIGNAL — VIDEO EDITING / SHORT FILM ROOM — ALL-IN-ONE V3.0

Updated: 2026-09-11
Status: ACTIVE — GOVERNING EDITING MASTER
Scope: COLOSSUS SIGNAL Reels, cinematic scenes, trailers, short films, MV-style edits, AI-generated/source-derived video post-production.

## 0. Authority / supersession

This file supersedes `COLOSSUS_RETENTION_EDITING_STANDARD_V2.md` for all new editing decisions from this checkpoint forward.

Priority order:
1. Latest explicit user instruction in the current task.
2. Verified episode / source authority and current production state.
3. This V3.0 master.
4. Older Colossus editing standards and historical notes.

Rules:
- Never reset the project.
- Never replace a verified episode identity because of a filename guess.
- Verify visual content before assigning an episode.
- DRAFT / REJECTED / FAILED / CANCELLED material is never authority.
- Preserve layers that already passed QA when repairing one failed layer.
- If the user gives a new explicit instruction, it overrides a conflicting legacy editing rule unless it would break source authority or safety.

## 1. Editing mission

The editor is not a filter stack. The editor must improve story comprehension, emotion, continuity, retention and perceived production value while protecting the identity of the original source.

Global quality hierarchy:
1. Identity / continuity integrity
2. Story clarity / intention
3. Performance / emotional truth
4. Natural motion
5. Pacing / retention
6. Sound and rhythm
7. Scale / composition readability
8. Color / image polish
9. Technical delivery

Never trade continuity for spectacle.
Never add activity only to make a clip feel “busy.”

## 2. Work modes

### A. COLOSSUS REEL / SHORT-FORM SIGNAL
Current default when editing Colossus Facebook Reels.
- Current project minimum final duration: 11 seconds unless the user explicitly overrides.
- Vertical 9:16 unless episode authority says otherwise.
- Viewer-facing text: English only.
- Core story engine: ANOMALY → BEHAVIOR → CONSEQUENCE → INTENT.
- First useful anomaly must already be readable in the opening.
- Monumental, slow, heavy motion remains part of the brand.

### B. SHORT FILM / CINEMATIC SCENE
Use when the user asks for a short film, narrative scene, drama, comedy, horror, action, investigation or cinematic sequence.
- No fixed 11-second rule.
- Cut for scene objective, conflict, turn, reaction and payoff.
- Performance takes priority over arbitrary short-form pacing.
- Protect acting pauses, eye-lines, reaction timing and useful silence.
- Use motivated cuts, not constant cuts.

### C. MV / MUSIC-DRIVEN EDIT
Use for music video, performance montage or rhythm-led film.
- Build a song map first: intro / verse / pre / chorus / bridge / drop / outro.
- Cut by phrase, musical change, vocal emphasis and visual intent; do not cut on every beat by default.
- Lip-sync, performance continuity and musical dynamics are authority.
- Speed ramps, flash frames and strobe-like edits are optional tools, never defaults.

### D. TRAILER / TEASER
- State the promise quickly.
- Escalate information, not just volume.
- Reserve the strongest image or consequence for the final third unless the hook requires an earlier glimpse.
- End with a clean unresolved implication or title beat.

## 3. Mandatory source intake before editing

For every uploaded source:
1. Identify the actual visual content and episode/scene by inspection.
2. Run technical inspection with ffprobe/metadata: duration, resolution, fps, codec, audio streams, SAR/DAR, variable/CFR risk.
3. QA identity / continuity / morphing / face / hands / props / celestial geometry / background drift.
4. Check watermark/logo/text contamination.
5. Check audio: clipping, noise, speech intelligibility, sync, dead air, repeated lines.
6. Classify source:
   - PASS — safe to edit.
   - PASS WITH REPAIR — usable after targeted fix.
   - REJECT — structural failure that editing cannot safely hide.
7. Only PASS/PASS WITH REPAIR proceeds to Final.

If the source fails identity or continuity, do not “polish through” the failure.

## 4. Core editing workflow

### STEP 1 — STORY MAP
Before touching effects, define:
- What must the viewer understand?
- What changes during the clip?
- What is the payoff?
- What should remain unexplained?
- What single emotional state should dominate?

### STEP 2 — SELECT / TRIM
- Remove dead lead-in and dead tail.
- Preserve useful reaction time.
- Remove accidental repeated frames/lines.
- Do not cut breaths or pauses that carry performance.
- For generated clips, cut around morph/artifact spikes if continuity survives.

### STEP 3 — ROUGH CUT
Build the story with only picture and source sound first.
If the sequence is unclear without effects, the edit is not ready for polish.

### STEP 4 — FINE CUT / CONTINUITY
Check:
- match on action
- eye-line
- 180° screen direction
- 30° angle separation where relevant
- prop hand / costume / lighting continuity
- entrance / exit direction
- shot size progression
- reaction shot timing
- motivated insert/cutaway use

### STEP 5 — WATERMARK / CONTAMINATION REPAIR
Perform before final color and sharpening when instructed. See Section 8.

### STEP 6 — SOUND EDIT
Dialogue / ambience / SFX / music / silence / transitions.
Sound must explain space and intention, not merely make the clip louder.

### STEP 7 — TEXT / SUBTITLES / GRAPHICS
Use only when they improve comprehension, retention or brand identity.

### STEP 8 — COLOR / LIGHT / IMAGE REPAIR
Match shots first; style second.
Do not crush blacks until important dark structure disappears.

### STEP 9 — RESTORATION / UPSCALE / FPS
Only after picture lock.
Never upscale bad motion and call it repaired.

### STEP 10 — EXPORT + QA
Run technical, visual and narrative QA before delivery/upload.

## 5. Colossus retention rules — data-driven V3

Current platform learning from the first measured set:
- Intent / visible behavior has stronger growth potential than scale alone.
- Continuous tension can retain viewers even when reach is modest.
- Classification reversal creates shareable curiosity.
- Biological-signal behavior is a strong recurring mechanism.
- A visually impressive giant object without a meaningful change is not enough.

### 11–15 second default beat map
- 0.00–0.50s: anomaly / contradiction already visible.
- 0.15–0.60s: first short text hook when text is needed.
- 0.50–2.50s: proposition / evidence.
- 2.50–4.80s: controlled escalation.
- 4.50–6.50s: one meaningful re-hook or pattern change.
- 6.00–9.50s: strongest evidence / reveal.
- 9.00–final 1s: consequence / intent / unresolved implication.
- final 0.5–0.8s: soft loop bridge when appropriate.

Rules:
- No dead intro, logo lead-in or slow fade from black unless story requires it.
- No random glitch/zoom/shake as fake retention.
- If source is already strong, do less.
- If the key visual event occurs too late, forward-trim where continuity permits.
- One clip = one primary payoff.

## 6. On-screen text / subtitle rules

### Colossus identity
- white condensed uppercase
- short cyan Signal Bar
- subtle shadow
- no hard rectangular HUD box
- no generic sci-fi interface clutter

### Retention text
- 2–6 words is preferred for hook text.
- Use a contradiction or observation, not clickbait.
- First beat asks / implies a question.
- Second beat reframes or escalates.
- Avoid covering faces, eyes, planet edges, entity silhouettes or the main anomaly.
- Remove text before the hero visual moment when possible.

### Narrative short films
- Do not force hook text over a scene if it damages cinematic tone.
- Dialogue subtitles should follow speech naturally and remain mobile-safe.
- Use word-level timing only when it improves readability/lip-sync; not for decorative karaoke by default.

## 7. Short-film editing skill rules

### Performance editing
- Select takes for intention and reaction, not merely technical cleanliness.
- The listener’s reaction can be more important than the speaker’s line.
- Hold after a line when the emotional consequence is the story.
- Use J-cuts and L-cuts to make dialogue feel continuous and cinematic.

### Continuity editing
- Maintain screen direction unless a deliberate disorientation beat motivates a break.
- Match eye-line height and direction.
- Preserve prop state, costume state, hand position and character geography.
- Cut on motion when useful, but cut on thought/intention when performance requires it.

### Story pacing
- Every scene needs an objective, obstacle and change.
- Remove repetition that does not deepen character, tension or information.
- Inserts/cutaways must add evidence, emotion or bridge continuity.
- Montage must have progression, not just pretty shots.

### AI short-film continuity
QA every shot for:
- face identity drift
- hairstyle / costume drift
- age/body-proportion drift
- hand/finger failure
- prop mutation
- background architecture drift
- lens/FOV discontinuity
- time-of-day / light-direction mismatch
- impossible screen direction
- lip-sync mismatch
- frame-to-frame geometry warping

If one layer fails, repair that layer while preserving passed layers.

## 8. WATERMARK REMOVAL — ACTIVE V3 RULE

### Explicit user-command rule
When the user explicitly orders removal of a watermark/logo from user-provided or project-authorized footage, removal is REQUIRED for the requested Final.

**DOLA AI watermark: REMOVE when instructed.**
A Final that still visibly contains DOLA AI after an explicit removal instruction cannot receive QA PASS.

This supersedes the V2 rule that required retaining third-party watermarks in every source-derived render.

### Preferred repair order
Choose the least destructive method that fully removes the mark:
1. Clean reframe/crop if composition, safe area and story remain intact.
2. Clean-plate patch / neighboring-pixel reconstruction for simple static corners.
3. FFmpeg `delogo` or equivalent localized repair for small fixed marks when visual quality is acceptable.
4. Tracked mask + patch/inpaint for moving camera or moving background.
5. Temporal video inpainting using a commercially compatible/licensed workflow when the watermark overlaps changing content.
6. Localized resynthesis only when simpler methods fail and continuity can still be verified.

Do NOT default to an obvious blur, black box or sticker unless the user explicitly asks for that look.

### Watermark QA
Inspect at minimum:
- first frame
- 25%
- 50%
- 75%
- final frame
- additional random frames around high-motion moments

Fail conditions:
- watermark letters/logo remain readable
- ghost edge or rectangular smear is obvious
- repair destroys face/entity/planet contour
- temporal shimmer appears where the mark was removed
- crop damages the story composition or text-safe area

If repair is not clean, mark WATERMARK QA = FAIL / REPAIR REQUIRED. Never claim removal succeeded when it did not.

### Licensing note for tools
- FFmpeg provides crop/delogo/filter workflows suitable for many fixed marks.
- STTN is an MIT-licensed video-inpainting codebase and may be evaluated for suitable production use after checking model/asset terms.
- ProPainter and E2FGVI are useful research references but their published repositories/models are non-commercial; do not make them the default for monetized Colossus production without appropriate permission.

## 9. Sound / dialogue / music skill stack

### Dialogue
- Remove noise without creating metallic speech.
- Preserve consonants and breath realism.
- Use de-esser/EQ/compression lightly.
- For multi-speaker material, maintain room tone between cuts.
- Never auto-delete all silence; performance silence can be story.

### Sound design
Use a hierarchy:
1. dialogue / required narrative sound
2. source ambience / room tone
3. signature event sound
4. supporting texture / foley
5. music

Colossus sound:
- restrained sub-bass
- monumental structural groan
- low atmospheric beds
- strategic micro-silence before reveal
- no repetitive trailer boom every few seconds

### Loudness house target
Use a practical social/cinematic target around -16 to -14 LUFS integrated with true peak protected around -1 dBTP unless the specific platform/master requires another target. This is a house delivery target, not a claim of a universal Facebook requirement.

## 10. Color / image / motion rules

### Color
- Match exposure and white balance between shots first.
- Keep Colossus blacks deep but readable.
- Preserve cold blue/charcoal/obsidian brand palette with restrained warm ember accents.
- Avoid oversaturation and crushed-detail “cinematic” presets.

### Upscale / restoration
- Use Real-ESRGAN or equivalent only when source resolution/detail genuinely benefits.
- Upscale does not repair broken anatomy, morphing or motion.
- No fake 4K claim.

### Frame interpolation
- Practical-RIFE or equivalent can be considered for specific motion repair/smoothing.
- Never default to 60fps.
- Use interpolation only when artifact QA passes on edges, hands, faces, planets, text and fast motion.

### Stabilization
- Stabilize only unwanted camera error.
- Do not remove deliberate cinematic drift.

## 11. Tool / skill matrix

### FFmpeg / ffprobe — core authority
Use for:
- technical inspection
- trim / concat / re-encode
- scale / crop / pad
- color transforms
- audio filters / `loudnorm`
- subtitles / drawtext when needed
- `delogo` / localized fixed-region repair
- CFR conversion
- final H.264/AAC delivery

### PySceneDetect
Use for:
- cut/fade detection
- automatic shot listing
- scene-boundary QC
- generating representative frames for long clips
Adaptive detection is preferred when camera motion causes false positives; content detection works well for normal hard cuts.

### WhisperX
Use when speech matters:
- transcription
- word-level forced alignment
- dialogue subtitle timing
- speaker diarization when useful
Do not rely on ASR output without language/spelling QA.

### OpenCV / Python QC
Use for:
- frame sampling
- freeze/repeated-frame detection
- black-frame detection
- crop/ROI checks
- temporal difference checks
- watermark region verification
- automated technical QA reports

### Real-ESRGAN
Use for:
- real-world restoration/upscaling after picture lock
- compression/detail recovery where it improves the source

### Practical-RIFE
Use for:
- selective interpolation only after motion QA

### UVR / stem separation
Use only when vocal/music separation is necessary and artifacts are acceptable.
Always A/B against the original mix.

### Video inpainting / object removal
Use commercially compatible/licensed methods for production. License suitability is part of tool selection, not an afterthought.

## 12. MV editing skills

Before editing an MV:
1. Mark song sections and key lyrical lines.
2. Identify performance master takes.
3. Build sync before visual effects.
4. Intercut story/performance by musical phrase.
5. Reserve visual escalation for chorus/drop/bridge or emotional peak.
6. Use B-roll/inserts to cover sync and continuity repairs.
7. Keep motif/color/lens language consistent.
8. Do not let transitions overpower the performer/song.

If a vocal performance is visible, lip-sync accuracy outranks flashy transitions.

## 13. Export standards

### Colossus social Reel default
- 1080x1920
- 9:16
- 30fps CFR unless source-specific authority justifies otherwise
- H.264
- yuv420p compatible output
- AAC 48kHz
- no accidental letterbox
- no clipped text / unsafe UI placement

### Short film / MV
Preserve intended aspect ratio and cinematic frame rate when requested. Do not force every film into 30fps or 9:16 merely because the Colossus Reel preset uses them.

## 14. Three-pass QA

### QA-A — TECHNICAL
- opens/decodes correctly
- duration correct
- resolution/aspect correct
- fps correct
- audio present/synced
- no black/frozen accidental frames
- no codec/container failure

### QA-B — STORY / CONTINUITY
- episode/scene identity correct
- hook/scene objective readable
- continuity preserved
- no morph/AI defect at important beats
- performance timing intact
- payoff is understandable

### QA-C — DELIVERY / PLATFORM
- watermark instruction satisfied
- text safe/readable
- loudness/transients acceptable
- loop/end feels intentional
- no wrong episode title/caption pairing
- no unapproved logos/text

Only when all required passes succeed may output status become FINAL / QA PASS.

## 15. Failure memory / hard prohibitions

Do not:
- trust filename over visual content
- upload a reel under the wrong episode
- forget explicitly requested on-screen text
- forget DOLA AI removal after the user ordered it
- stretch/crop a face, planet or entity into wrong proportions
- call a file “4K” just because it was upscaled
- create 60fps by default
- hide structural AI failure with blur/glow
- over-denoise speech until it sounds synthetic
- delete comedy/drama pauses only because they are silent
- add random glitch/HUD effects that violate Colossus identity
- change a verified Final mapping without visual verification

## 16. Default command behavior when user uploads a clip

If the user says “QA ถ้าผ่านให้ตัดตามกฎ” or equivalent:
1. Load latest project/editing state.
2. Inspect actual visual content.
3. Identify episode/scene.
4. QA source.
5. If PASS, edit automatically using the correct mode in this master.
6. Apply explicit watermark-removal instruction before Final QA.
7. Add required on-screen text / captions according to project identity.
8. Upscale/restoration only when it genuinely improves output.
9. Export and run three-pass QA.
10. Report what passed/failed and provide the finished file when available.

Do not stop to ask questions already answered by project sources.

## 17. Current Colossus production awareness

At this checkpoint, verified September production still requiring Final resolution is tracked in `CURRENT_VIDEO_PRODUCTION_STATE.md`. That state file remains episode authority for what already exists versus what is still pending.

This editing master governs HOW to edit. It does not invent or overwrite WHICH episode file is authoritative.
