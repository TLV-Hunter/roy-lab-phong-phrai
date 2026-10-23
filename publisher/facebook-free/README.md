# Free Multi-Page Facebook Publisher — Colossus + RLS + future Pages

## Operational truth (2026-10-24)

- Workflow, safe previews, source validation, anti-duplicate receipts and **offline unit tests**: INSTALLED. GitHub Actions preview + tests: PASS.
- The **exact same content slots** apply to every Page: **Master Still at 06:00**, **Reel at 23:00**, `Asia/Bangkok`.
- For each slot the workflow triggers at :00 with retry triggers at :17 and :27. GitHub cron is best-effort, so posts may be late; exact-to-the-minute publication is NOT guaranteed.
- **COLOSSUS SCHEDULE ARMED BY OWNER (2026-10-24).** Colossus Facebook Page ID and Page Token PASS, EP04 and final Special Master/Reel public Drive download PASS. Exact Colossus source range is EP04 Oct24 through special CS-OCT-SP01 Oct31; 06:00 Still and 23:00 Reel Asia/Bangkok. Meta does not have future posts pre-scheduled in Planner: our GitHub Actions scheduler will attempt the API post at due time. As of configuration time NO scheduled live posts had been sent from this module. RLS remains OFF.
- **Colossus SS3:** 11/11 approved 4K Still + Reel media links and independent caption/comments exist in `colossus/ss3-season.json`. Photo+Reel are independent posts.
- **RLS SS3:** Separate `colossus/rls-ss3-content.json` still has archived JPEG preview Masters and locally rendered/unmapped Reel files; these cannot pass the production gates. RLS is kept on HOLD until canonical approved source links and separate Reel captions/comments are registered.
- Existing TalentVee Publisher web UI and `publisher-cron.yml` are NOT replaced or edited. Never store secrets in public files.

## Planned schedule / start date

| Page | Still (Master image) | Reel (Final video) | Zone |
| --- | --- | --- | --- |
| Colossus Signal | **06:00** every day | **23:00** every day | Asia/Bangkok |
| RLS — The Hidden Forest | **06:00** every day | **23:00** every day | Asia/Bangkok |
| Any future Page | **06:00** default | **23:00** default | Asia/Bangkok |

For Colossus `start_episode_id=CS-OCT-004`, `start_date=2026-10-24`, `end_episode_id=CS-OCT-SP01`. EP04..EP10 are scheduled Oct24..Oct30; SP01 (the season's eighth remaining episode) is scheduled Oct31. EP01–EP03 are excluded. For new brands with no `start_episode_id`, indexing starts at their Episode 1.

## How to add a 3rd/4th/etc Page — no Python or workflow edits

1. Prepare a separate brand-approved JSON source in this repository with `episodes`, each containing `id`, `master: {url, qa}`, `still: {caption, first_comment, copy_qa}`, `reel: {url, qa, caption, first_comment, copy_qa}`, `publication: {status}`. Alternatively select an already supported `content_format` (e.g. RLS SS3).
2. Add a new `brands.<slug>` entry in `config.json`, using `future_page_template`, changing `content_path`, `credential_key`, and `start_date`. The default 06:00/23:00 slots can be reused.
3. Update one GitHub Actions **secret** named `FB_PAGES_JSON` to include the new Page's `page_id` and `access_token` (example below). This secret must NEVER be saved to GitHub public files, Issues, website UI, or ChatGPT.
4. Validate that every media URL is accessible to the runner by the authorized Google account, not merely a Drive preview URL.
5. Execute the preview in GitHub Actions and perform an authorized test Page upload; finally enable the specific brand and go-live variable after QA.

`FB_PAGES_JSON` secret value structure (**PLACEHOLDERS ONLY**):

```json
{
  "colossus": {"page_id": "PAGE_ID_1", "access_token": "TOKEN_1"},
  "rls": {"page_id": "PAGE_ID_2", "access_token": "TOKEN_2"},
  "newpage": {"page_id": "PAGE_ID_3", "access_token": "TOKEN_3"}
}
```

Keep this JSON only in **Settings → Secrets and variables → Actions → Repository secrets**. `FB_PAGES_JSON` is a single, extensible store. For backwards compatibility, `FB_PAGE_ID_COLOSSUS`/`FB_PAGE_TOKEN_COLOSSUS` and analogous RLS secrets may also work, but new Pages should use the JSON map.

## Isolated Colossus test image and once-only queue (October 24)

**This is a separate test queue; it never changes EP03's previously published 06:00 post or the 06:00/23:00 season settings.**

- [Queue JSON](test-posts/2026-10-24_colossus_0045.json) — approved Colossus source EP03 Master Still, target `2026-10-24T00:45:00+07:00`, currently **EXPIRED_NOT_PUBLISHED / enabled false**. The requested 00:45 time was missed; NEVER post or backfill this exact queue automatically.
- [One-off preview/publish workflow](../../.github/workflows/colossus-oneoff-test.yml) — still supports manual preview; its old 00:45 daily cron was removed after the missed test slot, avoiding needless scheduled jobs.
- [One-off script](oneoff_test.py) — downloads the already approved Master from public-link Google Drive, then creates a distinct 1600×2000 detail crop focusing on canonical obsidian armor + cyan fissure + Earth. **No new Drive upload is needed**, and there are **no EP markers, captions, logos or human additions inside the image**. Existing source media is NEVER modified.
- **Preview artifact** from an actual GitHub Actions runner: https://github.com/TLV-Hunter/roy-lab-phong-phrai/actions/runs/39998356682/artifacts/12520912743 . The preview was successfully generated by the cloud runner. It is not a Facebook post.
- An approved English caption and separate first-comment draft reside in queue JSON. First comment is intentionally disabled for the initial isolated photo test; it requires a separately verified `pages_manage_engagement` permission.
- To schedule a **new, explicitly authorized future** isolated test: change `scheduled_at` to the approved future Bangkok date at 00:45, set `enabled` to true only after preview QA, ensure `status` reflects ARMED, and create GitHub Actions **repository variable** `FB_ONEOFF_TEST_ENABLED=true` after owner approval. These two independent flags prevent accidental publication. The original 2026-10-24 expired test must not be secretly rescheduled.
- For a future manual trial, use the workflow's Run workflow → mode `preview` first. `publish` requires the manual input `PUBLISH` and still refuses to publish outside the approved schedule. Every success/uncertain error gets a once-only reserved receipt in `receipts.json` to prevent duplicate retries.
- GitHub Actions cron is best effort. No exact-minute publication is guaranteed. If the user must publish precisely at 00:45, Meta Business Suite scheduling or another provider with an explicit scheduled publishing guarantee may be more appropriate than GitHub cron.

## Google Drive access — recommended service account (no OAuth refresh tokens)

**Recommended for Colossus and future Pages.** This method works on a free Google Cloud project (subject to Google's quota/policy) and does not require keeping the owner's personal OAuth refresh token current.

1. Open https://console.cloud.google.com/ and create/select a project.
2. APIs & Services → Library → search **Google Drive API** → Enable.
3. IAM & Admin → Service Accounts → Create Service Account; name it `talentvee-drive-reader`. Project IAM role can be left empty; this account needs only access to the Drive folder you explicitly share.
4. Open the service account → Keys → Add Key → Create new key → JSON. Download the private JSON file only to your machine, never to GitHub files or chat. If key creation is blocked by organization policy, use the existing OAuth fallback.
5. Open the folder containing the Colossus SS3 Master Stills and Final Reels:
   https://drive.google.com/drive/folders/19bahpbot_ZnuJK5bf375X32da4Wh0eD4
   Share → paste the `client_email` shown in the JSON, choose **Viewer**, disable notifications if offered, Share. Do not enable anonymous link sharing.
6. In https://github.com/TLV-Hunter/roy-lab-phong-phrai/settings/secrets/actions → New repository secret → Name `GOOGLE_SERVICE_ACCOUNT_JSON`, Value **the entire private JSON file content**, then save. Never use a plain GitHub variable for keys.
7. Go to https://github.com/TLV-Hunter/roy-lab-phong-phrai/actions/workflows/facebook-free-multipage.yml → **Run workflow**. The read-only probe shows `drive_auth PASS`, `drive_still_access PASS`, and `drive_reel_access PASS` when correctly configured. It does NOT publish anything.

Google's official guidance allows sharing a Drive folder with a service account email without domain-wide delegation or an IAM project role:
https://developers.google.com/workspace/guides/create-credentials

Existing alternative: GitHub Secrets `GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET`, `GOOGLE_OAUTH_REFRESH_TOKEN`. If `GOOGLE_SERVICE_ACCOUNT_JSON` is present, the app prefers it over OAuth. Both credentials types use read-only Drive access in this publisher.

## Optional legacy Google Drive OAuth Secrets

`GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET`, `GOOGLE_OAUTH_REFRESH_TOKEN` are needed **only if you do not use** the recommended Service Account JSON secret.
The workflow automatically provides a scoped `GITHUB_TOKEN` to persist receipts. In **Actions variables**, eventually set `FB_GRAPH_VERSION` to an API version supported by the connected Meta App (default in script `v26.0`). Do NOT expose secrets in local files or browser.

For Facebook Page permissions, request those actually needed via Meta's official app/consent flow: `pages_show_list`, `pages_read_engagement`, `pages_manage_posts`, plus `pages_manage_engagement` if posting first comments. App review and token renewal requirements depend on the Page/App relationship. Uploading media/finishing Reels and posting comments must be tested live on an authorized test Page; do not mistake an HTTP upload acceptance for verification of a published Facebook post.

## Safe activation — deliberately not yet performed

The `config.json` values start as:

```text
colossus.enabled = false
rls.enabled = false
colossus.start_date = null
rls.start_date = null
```

After explicit owner approval, Colossus config has already been armed (`enabled=true`, `start_date=2026-10-24`, first episode EP04). Scheduled workflow jobs pass an internal on flag and check each brand's `enabled`, QA and due-time gates. GitHub Actions repository variables are NOT needed to enable this Colossus schedule. To emergency-disable before the next slot, edit `brands.colossus.enabled=false` and commit. Keep RLS disabled.

At most once per EP/kind/Page, `receipts.json` reserves before posting, and records Meta photo acknowledgment or Reel finish acknowledgment separately from actual published Reel status. If Meta responds ambiguously, no automatic duplicate is sent. Colossus first comments are ENABLED using separate GitHub cron jobs: they send approved Page-owned comments at least 300 seconds after photo success or confirmed Reel publishing. Actual delay may be later because GitHub Actions cron is best-effort. Comment posting needs `pages_manage_engagement`/MODERATE access. **Pinning a comment is not supported by the verified Graph API**, so each posted comment gets `pin_status=NEEDS_MANUAL_PIN` and must be pinned via Facebook UI.

**IMPORTANT:** The existing public page files are for production, not a secure credentials UI. Do not type tokens into the page or store them in the JSON sources.

## Optional Local AI (no GPU needed, does not need to stay on)

Only for editorial QA, not the timer or Facebook authentication. On the user's Windows 11 CPU / 16 GB RAM machine:

```powershell
ollama pull qwen3:4b-instruct
python publisher/facebook-free/local_ai_review.py --brand colossus --episode CS-OCT-002 --kind reel --model qwen3:4b-instruct
```

Ollama's Qwen3 4B Instruct quantized model is about 2.5 GB to download. It runs on CPU but may take time. The script calls only `127.0.0.1:11434`; it merely suggests copy improvements. It does NOT modify approved source, publish Facebook posts, handle secrets or become required for daily automation.

## Verification and provenance

- Automated tests: `python -m unittest discover -s publisher/facebook-free -p 'test_*.py' -v`
- Preview (no network posting): `python publisher/facebook-free/autopost.py --preview`
- GitHub workflow: `.github/workflows/facebook-free-multipage.yml`
- Durable anti-duplicate receipts: `publisher/facebook-free/receipts.json`
- Official [Meta Page Photos](https://developers.facebook.com/docs/graph-api/reference/page/photos/)
- Official [Meta Facebook API Reels Postman collection](https://www.postman.com/meta/facebook/documentation/r56bjfd/facebook-api)
- Official [GitHub Actions scheduling](https://docs.github.com/actions/using-workflows/events-that-trigger-workflows#schedule)

No actual Facebook post is claimed until the provider returns IDs and the Page/Feed has been verified.
