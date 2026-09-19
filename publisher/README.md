# TalentVee Unified Publisher

This folder defines the automation handoff for COLOSSUS, RLS and Mayor Bruno.

## Current state
- GitHub Pages UI: READY
- Queue schema: READY
- GitHub Actions cron hook: READY
- Meta/Facebook publisher backend: NOT CONNECTED
- No access tokens are stored in the public repository.

## Backend contract
The frontend sends one queue item as JSON via POST to the configured Publisher API URL.

Required fields:
- queue_id
- brand
- platform
- content_type
- content_id
- scheduled_at
- timezone
- media_url
- caption
- first_comment
- auto_publish
- status

Backend should return JSON containing at least:
- status
- provider_post_id when publishing succeeds
- error when publishing fails

## Security
Keep Page Access Tokens, App Secrets, Page IDs and provider credentials in backend/GitHub secrets only. Never place them in publisher.html, queue JSON, or other public files.
