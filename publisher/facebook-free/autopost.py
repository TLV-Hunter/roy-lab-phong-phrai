#!/usr/bin/env python3
"""Fail-closed multi-Page Facebook Still/Reel publisher. No secrets or media in git."""
import argparse
import base64
import io
import json
import os
import re
from datetime import datetime, date, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

ROOT = Path(__file__).resolve().parents[2]
CONFIG = Path(__file__).with_name("config.json")
STATE_PATH = "publisher/facebook-free/receipts.json"
TIMEOUT = 80


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def eligible(content_format, episode, kind):
    """Return (eligible, reason, media_url, caption, first_comment)."""
    if content_format in ("canonical_ss3", "colossus_ss3"):
        asset = episode.get("master", {}) if kind == "still" else episode.get("reel", {})
        copy = episode.get("still", {}) if kind == "still" else episode.get("reel", {})
        url = asset.get("url")
        good_media = bool(url and str(asset.get("qa", "")).startswith("PASS"))
        good_copy = bool(copy.get("caption") and copy.get("first_comment") and
                         str(copy.get("copy_qa", "")).startswith("PASS"))
        if episode.get("publication", {}).get("status") in ("PUBLISHED", "SCHEDULED"):
            return False, "already recorded as published/scheduled", None, None, None
        if not (good_media and good_copy):
            return False, "master/final Reel or corresponding public copy not QA PASS", None, None, None
        return True, "QA READY", url, copy["caption"], copy["first_comment"]
    if content_format == "rls_ss3":
        # RLS SS3 has historical JPEG previews and local-only videos: block until
        # real approved assets are mapped, not even a thumbnail fallback.
        if kind == "still":
            a = episode.get("master_still", {})
            url = a.get("image_url")
            verified = str(a.get("status", "")).startswith("PASS") and \
                       (str(url).startswith("https://drive.google.com/file/d/"))
            copy = episode.get("still_caption")
            comment = episode.get("first_comment")
        else:
            a = episode.get("final_reel", {})
            url = a.get("video_url")
            verified = str(a.get("status", "")).startswith("PASS") and \
                       (str(url).startswith("https://drive.google.com/file/d/"))
            copy = episode.get("reel_caption")
            comment = episode.get("reel_first_comment")
        if episode.get("publication_status") in ("PUBLISHED", "SCHEDULED"):
            return False, "already recorded as published/scheduled", None, None, None
        if not (verified and copy and comment):
            return False, "RLS SS3 authoritative media or separate copy not yet verified/imported", None, None, None
        return True, "QA READY", url, copy, comment
    return False, "unknown/unapproved content format", None, None, None


def make_plan(config, now):
    tz = ZoneInfo(config["timezone"])
    result = []
    for brand, settings in config["brands"].items():
        if not re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,40}", brand):
            raise ValueError("Invalid brand slug in config")
        rel = Path(settings["content_path"])
        if rel.is_absolute() or ".." in rel.parts:
            raise ValueError("Unsafe brand content path")
        source = load_json(ROOT / rel)
        episodes = list(source["episodes"])
        if source.get("halloween_special"):
            episodes.append(source["halloween_special"])
        start = settings.get("start_date")
        for i, ep in enumerate(episodes):
            for kind in ("still", "reel"):
                ok, reason, media_url, caption, first_comment = eligible(settings.get("content_format", "canonical_ss3"), ep, kind)
                slot = settings.get("slots", config.get("defaults", {}).get("slots", {"still":"06:00","reel":"23:00"}))[kind]
                day = (date.fromisoformat(start) + timedelta(days=i)).isoformat() if start else None
                when = datetime.fromisoformat(day + "T" + slot).replace(tzinfo=tz) if day else None
                result.append({
                    "key": f"{brand}:{ep['id']}:{kind}",
                    "brand": brand,
                    "episode_id": ep["id"],
                    "kind": kind,
                    "date": day,
                    "time": slot,
                    "timezone": config["timezone"],
                    "due": bool(when and 0 <= (now - when).total_seconds() <= 30 * 60),
                    "enabled": bool(settings["enabled"]),
                    "ready": ok,
                    "reason": reason,
                    "media_url": media_url,
                    "caption": caption,
                    "first_comment": first_comment,
                    "credential_key": settings.get("credential_key", brand),
                    "media_mode": settings.get("media_download_mode", "private_oauth"),
                })
    return result


def drive_file_id(url):
    from urllib.parse import urlparse
    parts = urlparse(url).path.split("/")
    if "d" not in parts:
        raise RuntimeError("Media must be an approved Google Drive /file/d/ URL")
    return parts[parts.index("d") + 1]


def get_drive_access_token():
    """Prefer read-only Google Service Account. Retain OAuth refresh-token fallback.

    Only the owner-shared Drive folder is accessible to the service account.
    Never print, store or return the private key anywhere except in-memory.
    """
    service_info = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "").strip()
    if service_info:
        try:
            from google.oauth2 import service_account
            from google.auth.transport.requests import Request as GoogleAuthRequest
            info = json.loads(service_info)
            if info.get("type") != "service_account":
                raise ValueError("wrong credential type")
            creds = service_account.Credentials.from_service_account_info(
                info, scopes=["https://www.googleapis.com/auth/drive.readonly"])
            creds.refresh(GoogleAuthRequest())
            return creds.token
        except Exception as exc:
            raise RuntimeError("Google Service Account authentication failed; verify private key and Drive API") from None

    keys = ("GOOGLE_OAUTH_CLIENT_ID", "GOOGLE_OAUTH_CLIENT_SECRET", "GOOGLE_OAUTH_REFRESH_TOKEN")
    if not all(os.environ.get(k) for k in keys):
        raise RuntimeError("Google Drive credentials not configured (read-only Service Account or OAuth)")
    token = requests.post(
        "https://oauth2.googleapis.com/token",
        data={"client_id": os.environ["GOOGLE_OAUTH_CLIENT_ID"],
              "client_secret": os.environ["GOOGLE_OAUTH_CLIENT_SECRET"],
              "refresh_token": os.environ["GOOGLE_OAUTH_REFRESH_TOKEN"],
              "grant_type": "refresh_token"}, timeout=TIMEOUT,
    )
    token.raise_for_status()
    return token.json()["access_token"]


def fetch_public_drive_bytes(url):
    """Explicit opt-in to anonymous downloads; never uses a browser session or Google cookies."""
    import tempfile
    import gdown
    fid = drive_file_id(url)
    with tempfile.TemporaryDirectory() as directory:
        filename = str(Path(directory) / "approved-media.bin")
        path = gdown.download(id=fid, output=filename, quiet=True, use_cookies=False)
        if path != filename or not Path(filename).is_file():
            raise RuntimeError("Public Drive download failed. File/folder sharing must allow Anyone with the link")
        file_size = Path(filename).stat().st_size
        if not 1000 < file_size < 1_073_741_824:
            raise RuntimeError("Downloaded media file missing or too large")
        raw = Path(filename).read_bytes()
        if not (raw.startswith(b"\\x89PNG\\r\\n\\x1a\\n") or
                raw.startswith(b"\\xff\\xd8\\xff") or
                b"ftyp" in raw[4:16]):
            raise RuntimeError("Public Drive returned a non-media file instead of approved image/video")
        return raw


def fetch_drive_bytes(url, mode="private_oauth"):
    if mode == "public_drive":
        return fetch_public_drive_bytes(url)
    if mode != "private_oauth":
        raise ValueError("Unknown Drive access method: fail closed")
    access = get_drive_access_token()
    fid = drive_file_id(url)
    media = requests.get(
        f"https://www.googleapis.com/drive/v3/files/{fid}",
        params={"alt": "media"}, headers={"Authorization": f"Bearer {access}"},
        timeout=180, stream=True,
    )
    media.raise_for_status()
    chunks = io.BytesIO()
    for chunk in media.iter_content(1024 * 1024):
        if chunk:
            chunks.write(chunk)
    return chunks.getvalue()

def fb_json(response):
    if not response.ok:
        # Never log Meta request, token, upload URL or raw response.
        raise RuntimeError(f"Facebook HTTP {response.status_code}; check Page permissions and Meta logs")
    result = response.json()
    if result.get("error"):
        raise RuntimeError(f"Facebook API rejected request: code {result['error'].get('code', 'unknown')}")
    return result


def publish_photo(page_id, token, data, caption):
    from PIL import Image
    image = Image.open(io.BytesIO(data)).convert("RGB")
    # Preserve Master Still on Drive; this smaller JPEG is an upload-only rendition.
    output = io.BytesIO()
    for quality in (90, 82, 72, 62):
        output.seek(0)
        output.truncate(0)
        image.save(output, format="JPEG", quality=quality, optimize=True)
        if output.tell() < 9_000_000:
            break
    if output.tell() >= 10_000_000:
        raise RuntimeError("Facebook image upload exceeded the 10 MB cap")
    response = requests.post(
        f"https://graph.facebook.com/{os.getenv('FB_GRAPH_VERSION','v26.0')}/{page_id}/photos",
        data={"access_token": token, "caption": caption, "published": "true"},
        files={"source": ("master-still.jpg", output.getvalue(), "image/jpeg")},
        timeout=150,
    )
    payload = fb_json(response)
    return payload.get("post_id") or payload.get("id")


def publish_reel(page_id, token, data, caption, title):
    base = f"https://graph.facebook.com/{os.getenv('FB_GRAPH_VERSION','v26.0')}/{page_id}/video_reels"
    started = fb_json(requests.post(
        base, data={"access_token": token, "upload_phase": "start"}, timeout=TIMEOUT))
    video_id, upload_url = started["video_id"], started["upload_url"]
    # Meta's official Reels resumable upload endpoint; single small/medium file.
    uploaded = requests.post(
        upload_url,
        headers={"Authorization": f"OAuth {token}", "offset": "0",
                 "file_size": str(len(data)), "Content-Type": "application/octet-stream"},
        data=data, timeout=300,
    )
    fb_json(uploaded)
    fb_json(requests.post(
        base, data={"access_token": token, "upload_phase": "finish",
                    "video_id": video_id, "video_state": "PUBLISHED",
                    "description": caption, "title": title},
        timeout=180,
    ))
    return video_id


def publish_comment(page_id, token, post_id, message):
    return fb_json(requests.post(
        f"https://graph.facebook.com/{os.getenv('FB_GRAPH_VERSION','v26.0')}/{post_id}/comments",
        data={"access_token": token, "message": message}, timeout=TIMEOUT,
    )).get("id")


def state_read(token, repository):
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json",
               "X-GitHub-Api-Version": "2022-11-28"}
    uri = f"https://api.github.com/repos/{repository}/contents/{STATE_PATH}"
    result = requests.get(uri, headers=headers, timeout=TIMEOUT)
    result.raise_for_status()
    obj = result.json()
    raw = base64.b64decode(obj["content"]).decode("utf-8")
    return json.loads(raw), obj["sha"], uri, headers


def state_write(token, repository, items, action):
    state, sha, uri, headers = state_read(token, repository)
    key = action["key"]
    if key in state["items"]:
        return False
    state["items"][key] = items
    result = requests.put(uri, headers=headers, timeout=TIMEOUT, json={
        "message": f"publisher: reserve {key} [skip ci]",
        "content": base64.b64encode((json.dumps(state, indent=2) + "\n").encode()).decode(),
        "sha": sha, "branch": "main",
    })
    result.raise_for_status()
    return True


def state_replace(token, repository, key, new_data):
    state, sha, uri, headers = state_read(token, repository)
    if key not in state["items"]:
        raise RuntimeError("Receipt reservation unexpectedly missing")
    state["items"][key].update(new_data)
    r = requests.put(uri, headers=headers, timeout=TIMEOUT, json={
        "message": f"publisher: result {key} [skip ci]",
        "content": base64.b64encode((json.dumps(state, indent=2) + "\n").encode()).decode(),
        "sha": sha, "branch": "main",
    })
    r.raise_for_status()



def page_credentials(credential_key):
    """Allow unlimited brand keys without new workflow YAML edits.

    Single GitHub Actions secret FB_PAGES_JSON:
      {"colossus":{"page_id":"...","access_token":"..."},
       "rls":{"page_id":"...","access_token":"..."}}
    Legacy per-brand secrets remain optional for backward compatibility.
    Never print or commit these values.
    """
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,40}", credential_key):
        raise ValueError("Invalid credential key")
    all_pages = os.environ.get("FB_PAGES_JSON", "").strip()
    if all_pages:
        try:
            pages = json.loads(all_pages)
            settings = pages.get(credential_key, {})
            return settings.get("page_id"), settings.get("access_token")
        except (ValueError, TypeError):
            raise RuntimeError("FB_PAGES_JSON secret must be a JSON object")
    legacy = credential_key.upper().replace("-", "_")
    return (os.environ.get("FB_PAGE_ID_" + legacy),
            os.environ.get("FB_PAGE_TOKEN_" + legacy))


def run(args):
    config = load_json(CONFIG)
    assert config["timezone"] == "Asia/Bangkok", "Publishing timezone must remain Asia/Bangkok"
    now = datetime.now(ZoneInfo(config["timezone"]))
    plan = make_plan(config, now)
    if args.preview:
        for item in plan:
            print(f"{item['brand']:9} {item['episode_id']:12} {item['kind']:5} "
                  f"{str(item['date']):10} {item['time']} | "
                  f"{'READY' if item['ready'] else 'HOLD'} | {item['reason']}")
        print(f"PREVIEW: {len(plan)} planned entries; no Facebook API calls made.")
        return
    if os.getenv("FB_AUTOPUBLISH_ENABLED") != "true":
        print("SAFE HOLD: FB_AUTOPUBLISH_ENABLED is not true. No posts sent.")
        return
    token = os.environ.get("GITHUB_TOKEN")
    repository = os.environ.get("GITHUB_REPOSITORY")
    if not token or not repository:
        raise RuntimeError("GitHub write token and repository required for idempotent receipts")
    for item in plan:
        if not (item["enabled"] and item["ready"] and item["due"]):
            continue
        page_id, page_token = page_credentials(item["credential_key"])
        if not page_id or not page_token:
            print(f"HOLD {item['key']}: authorized Page secrets missing")
            continue
        reserved = state_write(token, repository, {
            "status": "RESERVED", "scheduled_date": item["date"],
            "time": item["time"], "created_at": now.isoformat(),
            "comment_status": "NOT_ATTEMPTED",
        }, item)
        if not reserved:
            print(f"SKIP duplicate/reserved: {item['key']}")
            continue
        try:
            data = fetch_drive_bytes(item["media_url"], item["media_mode"])
            if item["kind"] == "still":
                post_id = publish_photo(page_id, page_token, data, item["caption"])
            else:
                post_id = publish_reel(page_id, page_token, data, item["caption"], item["episode_id"])
            state_replace(token, repository, item["key"], {
                "status": "PUBLISHED_API_SUCCESS", "provider_post_id": str(post_id),
                "published_at": datetime.now(ZoneInfo(config["timezone"])).isoformat(),
            })
            if os.getenv("FB_ENABLE_FIRST_COMMENT") == "true":
                try:
                    comment_id = publish_comment(page_id, page_token, post_id, item["first_comment"])
                    state_replace(token, repository, item["key"], {
                        "comment_status": "POSTED", "provider_comment_id": comment_id})
                except Exception:
                    state_replace(token, repository, item["key"], {
                        "comment_status": "ERROR_NEEDS_MANUAL_CHECK"})
            print(f"RECEIPT SAVED {item['key']} (manual pinning, if desired, remains separate)")
        except Exception as exc:
            # Reservation is deliberately NOT deleted: prevents blind duplicate retries.
            try:
                state_replace(token, repository, item["key"], {"status": "ERROR_NEEDS_MANUAL_CHECK"})
            except Exception:
                pass
            print(f"HALT {item['key']}: {type(exc).__name__}; check API/account; no automatic retry")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true")
    run(parser.parse_args())
