#!/usr/bin/env python3
"""Colossus-only API authorization and media-access probe. Read-only; NEVER publishes."""
import json
import os
from pathlib import Path
from urllib.parse import quote
import requests

ROOT = Path(__file__).resolve().parents[2]
CONFIG = json.loads((Path(__file__).with_name("config.json")).read_text(encoding="utf-8"))
CONTENT = json.loads((ROOT / CONFIG["brands"]["colossus"]["content_path"]).read_text(encoding="utf-8"))
EPISODES = CONTENT["episodes"] + ([CONTENT["halloween_special"]] if CONTENT.get("halloween_special") else [])


def result(step, state, note):
    print(f"COLOSSUS PROBE | {step} | {state} | {note}")


def media_file_id(url):
    from urllib.parse import urlparse
    u = urlparse(url or "")
    if u.netloc != "drive.google.com" or "/file/d/" not in u.path:
        raise ValueError("Not an approved Google Drive file link")
    return u.path.split("/file/d/")[1].split("/")[0]


def main():
    stills = [e for e in EPISODES if e["master"].get("url") and
              str(e["master"].get("qa", "")).startswith("PASS") and
              e["still"].get("caption") and e["still"].get("first_comment")]
    reels = [e for e in EPISODES if e["reel"].get("url") and
             str(e["reel"].get("qa", "")).startswith("PASS") and
             e["reel"].get("caption") and e["reel"].get("first_comment")]
    result("approved_content", "PASS" if len(stills) == len(reels) == 11 else "HOLD",
           f"Master Still {len(stills)}/11; Reel {len(reels)}/11; no upload attempted")
    if len(stills) != 11 or len(reels) != 11:
        return

    # Check actual Colossus-only credentials in GitHub Secrets; print NO secrets.
    page_id, page_token = None, None
    blob = os.getenv("FB_PAGES_JSON", "")
    if blob:
        try:
            profile = json.loads(blob).get("colossus", {})
            page_id, page_token = profile.get("page_id"), profile.get("access_token")
        except (ValueError, AttributeError):
            result("facebook_credentials", "HOLD", "FB_PAGES_JSON secret is invalid JSON")
            return
    if not page_id or not page_token:
        page_id = os.getenv("FB_PAGE_ID_COLOSSUS")
        page_token = os.getenv("FB_PAGE_TOKEN_COLOSSUS")
    if not page_id or not page_token:
        result("facebook_credentials", "HOLD", "No Colossus Facebook Page authorization in GitHub Actions Secrets")
    else:
        try:
            data = requests.get(
                f"https://graph.facebook.com/{os.getenv('FB_GRAPH_VERSION') or 'v26.0'}/{quote(str(page_id), safe='')}",
                params={"fields": "id,name"},
                headers={"Authorization": "Bearer " + page_token},
                timeout=25)
            found = data.json() if data.ok else {}
            id_match = str(found.get("id")) == str(page_id)
            name_match = "colossus" in str(found.get("name", "")).casefold()
            if data.ok and id_match and name_match:
                result("facebook_page_read", "PASS", "Authorized Colossus Page ID and name confirmed")
            elif data.ok and id_match:
                result("facebook_page_read", "HOLD", "Page ID accessible, but Page name does not contain Colossus; check target identity")
            else:
                result("facebook_page_read", "HOLD", f"Page API returned HTTP {data.status_code} or mismatched Page ID; check token permissions")
        except requests.RequestException:
            result("facebook_page_read", "HOLD", "Facebook API not reachable from GitHub runner")

    from autopost import get_drive_access_token
    has_service = bool(os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON"))
    has_oauth = all(os.getenv(k) for k in (
        "GOOGLE_OAUTH_CLIENT_ID", "GOOGLE_OAUTH_CLIENT_SECRET", "GOOGLE_OAUTH_REFRESH_TOKEN"))
    if not has_service and not has_oauth:
        result("drive_credentials", "HOLD", "No Google Service Account or OAuth access in Actions Secrets")
    else:
        try:
            access = get_drive_access_token()
            if not access:
                raise RuntimeError("No usable Drive access token")
            result("drive_auth", "PASS", "Authorized read-only Google Drive token obtained")
            for kind, ep in (("still", stills[0]), ("reel", reels[0])):
                file_url = ep["master"]["url"] if kind == "still" else ep["reel"]["url"]
                fid = media_file_id(file_url)
                info = requests.get(
                    f"https://www.googleapis.com/drive/v3/files/{quote(fid, safe='')}",
                    headers={"Authorization": "Bearer " + access},
                    params={"fields": "id,mimeType,size,capabilities(canDownload)"},
                    timeout=25)
                obj = info.json() if info.ok else {}
                expected = "image/" if kind == "still" else "video/"
                okay = info.ok and obj.get("mimeType", "").startswith(expected) and (
                    obj.get("capabilities", {}).get("canDownload", True))
                result("drive_" + kind + "_access", "PASS" if okay else "HOLD",
                       "Approved Colossus media accessible" if okay else
                       "Media not shared with Service Account / Drive API denied")
        except Exception:
            # No credential content, access tokens or API response bodies are logged.
            result("drive_auth", "HOLD", "Google Drive authorization failed; check service account secret and API")

    result("live_publish", "OFF", "Read-only probe; NEVER calls Facebook POST or changes auto-publish flags")


if __name__ == "__main__":
    main()
