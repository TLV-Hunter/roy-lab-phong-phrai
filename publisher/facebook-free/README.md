# Free Multi-Page Facebook Publisher — Colossus + RLS + future Pages

## Operational truth (2026-10-23)

- Workflow, safe previews, source validation, anti-duplicate receipts and **offline unit tests**: INSTALLED. GitHub Actions preview + tests: PASS.
- The **exact same content slots** apply to every Page: **Master Still at 06:00**, **Reel at 23:00**, `Asia/Bangkok`.
- For each slot the workflow triggers at :00 with retry triggers at :17 and :27. GitHub cron is best-effort, so posts may be late; exact-to-the-minute publication is NOT guaranteed.
- **LIVE POSTS: DISABLED.** No Facebook Page Access Tokens, valid Google Drive OAuth refresh credentials, future episode start dates or activation have been configured by the account owner. Neither Colossus nor RLS has been posted from this module.
- **Colossus SS3:** 11/11 approved 4K Still + Reel media links and independent caption/comments exist in `colossus/ss3-season.json`. Photo+Reel are independent posts.
- **RLS SS3:** Separate `colossus/rls-ss3-content.json` still has archived JPEG preview Masters and locally rendered/unmapped Reel files; these cannot pass the production gates. RLS is kept on HOLD until canonical approved source links and separate Reel captions/comments are registered.
- Existing TalentVee Publisher web UI and `publisher-cron.yml` are NOT replaced or edited. Never store secrets in public files.

## Planned schedule / start date

| Page | Still (Master image) | Reel (Final video) | Zone |
| --- | --- | --- | --- |
| Colossus Signal | **06:00** every day | **23:00** every day | Asia/Bangkok |
| RLS — The Hidden Forest | **06:00** every day | **23:00** every day | Asia/Bangkok |
| Any future Page | **06:00** default | **23:00** default | Asia/Bangkok |

Episode 1 is assigned to the owner's future `start_date`; Episode 2 to the following day, and so forth (no historical backfill). For each Page the dates can be changed independently, while Still and Reel for the same EP remain paired on the same day.

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

## Additional required private GitHub Secrets

`GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET`, `GOOGLE_OAUTH_REFRESH_TOKEN` for approved private Google Drive file reads (only a refresh token with the needed permission).
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

Only after successful authorization, source QA, preview, and an explicit go-live decision, change the relevant Page to `enabled=true`, set a **future** `start_date`, and set GitHub Actions **variable** `FB_AUTOPUBLISH_ENABLED=true`.

At most once per EP/kind/Page, `receipts.json` records a reservation before upload. If Meta responds ambiguously, the publisher HALTS and requires reconciliation; automatic retry could create duplicate content. The first comment is OFF by default (`FB_ENABLE_FIRST_COMMENT=false`), as is pinning (NOT SUPPORTED by this script).

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
