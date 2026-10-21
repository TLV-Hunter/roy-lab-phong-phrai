# COLOSSUS SIGNAL — SS3 CURRENT PRODUCTION STATE

Updated: 2026-10-21 Asia/Bangkok

## Identity and release map
- Project: COLOSSUS SIGNAL (not RLS).
- Season: SS3 / WHAT THE GIANTS FEARED.
- 10 main episodes CS-OCT-001 through CS-OCT-010, editorial dates 21–30 October 2026.
- Halloween Special CS-OCT-SP01 on 31 October 2026 remains a **placeholder**.
- Theme: Dark Cosmic Horror, gigantic living cosmic entities and overwhelming scale.
- Original SS1 and SS2 source registries, approvals and links remain unchanged.

## Production truth (not social-publication truth)
- MASTER STILLS: **10/10 QA PASS**, 2160x3840 vertical PNG created by **upscaling 941x1672 source images** (not native generated 4K).
- Masters uploaded to Google Drive individually and folder listing rechecked as 10/10.
- Drive 4K folder: https://drive.google.com/drive/folders/19bahpbot_ZnuJK5bf375X32da4Wh0eD4
- Starter Frames: **0/10 READY / WAITING**.
- Video Prompts: **WAITING** (do not misrepresent stale drafts as approved).
- Final Reels: **0/10 READY / WAITING**.
- Still Caption / CTA / Hashtags / Keywords / First Comment: **WAITING**, no copy approved.
- Reel Caption / First Comment: **WAITING**, no copy approved.
- Halloween Special Master / Starter / Reel / Copy: **NOT CREATED**.
- Facebook publish or scheduled state: **NOT VERIFIED / DO NOT CLAIM PUBLISHED**.

## New website and data architecture
- Website: https://tlv-hunter.github.io/roy-lab-phong-phrai/colossus/ss3-season.html
- Registry: `colossus/ss3-season.json` — canonical source for the new SS3 desk.
- SS3 is now selectable from `colossus/index.html` and `colossus/august-season.html`.
- User can choose an individual episode, show all, use PREV / NEXT and preview available Master images via Google Drive, open/download each 4K PNG.
- Three production panels per episode: MASTER STILL, STARTER FRAME, FINAL REEL, with STILL copy and REEL copy sections.
- Empty assets/copy remain clearly WAITING; no placeholder falsely claims PASS.
- Updating `ss3-season.json` automatically updates cards and progress counters on the static GitHub Pages site without rebuilding the page UI.
- The 4K masters reside in Google Drive, not copied into GitHub. Google Drive embedded previews can require Google account access or sharing permissions; links still open for authorized users. No public access granted here.
- Website is an internal production desk, not a Facebook publishing action.

## Data update gates
1. Every image/video new URL must map to the exact `CS-OCT-00N` ID, with QA evidence; do not infer ID from filenames.
2. For Starter, update `starter.url`, `starter.qa`, `starter.prompt`, `starter.prompt_qa` only when each part passes.
3. For Reel, update `reel.url`, `reel.qa`, `reel.caption`, `reel.first_comment`, `reel.copy_qa` individually after respective QA passes.
4. For Still copy, update `still.caption`, `still.first_comment`, `still.copy_qa`, `keywords`, `hashtags`, `cta`; no captions invented for unpublished video.
5. `publication.status` remains UNCONFIRMED until owner/provider evidence proves scheduled/published.
6. Do not copy or alter RLS SS3 files. Do not supersede SS1/SS2 character and video authority.
7. Source and website updates must be verified against actual file / deployed Pages status.

Previous candidate generation logs and rejected batches are history only, not current Master Still authority.
