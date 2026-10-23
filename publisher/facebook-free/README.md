# Free Facebook Multi-Page Publisher — Colossus + RLS

A **safe, zero-subscription prototype** integrated with the existing TalentVee GitHub repo.
It does **not** replace `publisher.html` or `.github/workflows/publisher-cron.yml`.

## Current operational status

- Preview/queue planner: **INSTALLED**
- GitHub-hosted runner: **INSTALLED**, no Windows PC needs to stay on
- Facebook posting: **DISABLED** (no credentials/approval configured)
- Confirmed live Facebook posts from this module: **0**
- Source: Colossus SS3 approved registry and RLS SS3 registry, not generated captions
- Never writes public captions for Starter/Storyboard
- Never changes the Master Still / Final Reel assets or their QA status

## Independent brand schedules (Asia/Bangkok)

| Brand | Master Still | Reel | Source readiness |
| --- | --- | --- | --- |
| COLOSSUS SIGNAL SS3 | **06:00 daily** (owner confirmed) | **20:00** (provisional: changeable) | 11/11 approved Still + Reel mapped to Drive |
| RLS / The Hidden Forest SS3 | 10:00 daily | 20:00 daily | Currently **HOLD**: RLS SS3 site has archived JPEG previews and local-only/not-mapped videos. Must not post those as Finals |

The series begin only after an explicit `start_date` is entered for each brand. The default is `null`.
Publishing also requires `brands.<name>.enabled=true` and `FB_AUTOPUBLISH_ENABLED=true` separately.
No catch-up or dumping previous dated episodes occurs automatically. To avoid duplicates, a receipt is reserved **before** the Meta request. Ambiguous failures remain on hold for manual reconciliation.

## Setup (owner must authorize Facebook and Google)

1. Open the workflow file `.github/workflows/facebook-free-multipage.yml` in **Actions** and review the automatic **preview** job. A pushed change to this folder runs dry-run checks without posting.
2. Create/configure a Meta Developer App authorized to manage the two Facebook Pages; get valid Page tokens with the permissions needed for Page photo/Reel publishing and, if using first comments, engagement. No credentials are placed in source or UI. Some Facebook features require Meta App Review / appropriate Page roles.
3. Add these **repository Actions Secrets** in Settings → Secrets and variables → Actions (never put their values in chat or public files):
   - `FB_PAGE_ID_COLOSSUS`, `FB_PAGE_TOKEN_COLOSSUS`
   - `FB_PAGE_ID_RLS`, `FB_PAGE_TOKEN_RLS`
   - `GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET`, `GOOGLE_OAUTH_REFRESH_TOKEN` (Google Drive API read permission for private media)
4. Test both Page permissions, Drive file access, Reel upload and comment permissions on an authorized test Page first. Test token expiry/renewal as well.
5. Fill `config.json` → `start_date` (YYYY-MM-DD), correct Reel time and mark each brand `enabled=true` **only once the respective approved assets and copy are ready**. RLS is blocked until approved final master files and reels are actually mapped.
6. Set repository **variable** `FB_AUTOPUBLISH_ENABLED=true` only after end-to-end tests. Set `FB_GRAPH_VERSION=v26.0` or a version verified for your Meta App. Optionally set `FB_ENABLE_FIRST_COMMENT=true` only after verifying permissions.

## What gets posted

Colossus data is read from `colossus/ss3-season.json`:
- **Still**: `master.url` + `still.caption` (hashtags already inside) + `still.first_comment`
- **Reel**: `reel.url` + `reel.caption` (hashtags already inside) + `reel.first_comment`
- No Starter/Storyboard public posting. The script checks source QA and existing publication status for every item.

RLS data is read from `colossus/rls-ss3-content.json` but requires proper, public-post-approved *Master Still* and *Final Reel* media URLs, correctly flagged PASS, plus distinct Still/Reel copy. It intentionally rejects local-only videos and archived JPEG preview assets.

## Media and accessibility

Colossus media is stored on private Google Drive. Google Drive share links **cannot be passed as public CDN links** to Facebook and are not downloadable by anonymous GitHub runners. This publisher obtains an authorized Google Drive OAuth access token to download the approved file into the ephemeral Actions runner. Master Still PNG is converted to a temporary JPEG under the Facebook photo size cap **without modifying the original approved Master**.

## Run scheduling

GitHub Actions cron triggers at Bangkok 06:00, 10:00 and 20:00, and again 15 minutes later as a failsafe. This is **best-effort**, **not guaranteed exact to the minute**: GitHub documents occasional delayed/dropped scheduled jobs. The code only publishes due items within a 30-minute window; outside the window it will not secretly backfill previous content.

## First comment / pinned comment

- `reel.first_comment` and `still.first_comment` are already in the source registry and supported as separate fields.
- **Posting** comments via Meta Graph API is an optional, disabled flag until verified against the live app/Page permission.
- **Pinning** a comment is not implemented and must not be advertised as automatic.
- Publishing success and comment success are independently recorded in `receipts.json`.

## Security and failure gates

- `FB_AUTOPUBLISH_ENABLED` default false; individual brands default false.
- Missing media, QA fail, unpublished RLS assets, missing Page tokens or start dates → HOLD.
- `receipts.json` is a persistent reserve-first log; it prevents automatic duplicates across repeated cron runs.
- On API failure or ambiguous state, the entry remains reserved and requires manual reconciliation; it is **not** deleted automatically.
- GitHub receipts store content IDs and Facebook post IDs, **not** tokens, media bytes or full captions.
- No token or Google credential belongs in a public repo, GitHub Pages or chat.

## Verified references

- Meta-owned Postman Facebook Reels API collection: https://www.postman.com/meta/facebook/documentation/r56bjfd/facebook-api
- Official Meta Pages API: https://developers.facebook.com/docs/pages-api/
- GitHub scheduled workflows: https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule

This is an implementation scaffold, not proof that a Page has been connected, that app permissions have been approved or that a post has gone live.
