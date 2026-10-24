#!/usr/bin/env python3
"""One-time authorized catch-up for missed Colossus EP04 Master Still, 24 Oct 2026.

Fail closed, verify Page/Drive and consult recent live Page posts to prevent
duplicate public content. Never touches EP04 Reel nor any other episode.
"""
import os
import time
import json
from datetime import datetime, date, timedelta
from zoneinfo import ZoneInfo
import requests

from autopost import (
    CONFIG, ROOT, load_json, eligible, fetch_drive_bytes, page_credentials,
    state_read, state_write, state_replace, publish_photo, publish_comment, TIMEOUT,
)

TZ=ZoneInfo("Asia/Bangkok")
KEY="colossus:CS-OCT-004:still"
EP_ID="CS-OCT-004"
EXPECTED_PAGE_WORD="colossus"
EXPECTED_DAY=date(2026,10,24)
EARLIEST="07:30"
LATEST="10:00"

def gql(page_id, page_token, endpoint, params):
    r=requests.get(
        f"https://graph.facebook.com/{os.getenv('FB_GRAPH_VERSION') or 'v26.0'}/{page_id}/{endpoint}",
        params=params, headers={"Authorization": "Bearer "+page_token}, timeout=TIMEOUT)
    if not r.ok: raise RuntimeError(f"Meta read-only preflight returned HTTP {r.status_code}")
    obj=r.json()
    if not isinstance(obj,dict) or "error" in obj:
        raise RuntimeError("Meta read-only preflight rejected Page token")
    return obj

def main():
    now=datetime.now(TZ)
    if now.date()!=EXPECTED_DAY or not(EARLIEST<=now.strftime("%H:%M")<=LATEST):
        print("RECOVERY HOLD: only approved Colossus EP04 missing 06:00 Still on 2026-10-24 before 10:00 Bangkok is allowed")
        return
    if os.getenv("FB_EP04_CATCHUP_AUTHORIZED")!="true":
        print("RECOVERY HOLD: explicit one-time authorization is not set")
        return
    cfg=load_json(CONFIG)
    brand=cfg["brands"]["colossus"]
    if not (brand["enabled"] and brand["start_date"]=="2026-10-24"
            and brand["start_episode_id"]==EP_ID and brand["media_download_mode"]=="public_drive"):
        raise RuntimeError("Colossus authorized campaign settings changed")
    src=load_json(ROOT/brand["content_path"])
    matches=[e for e in src["episodes"] if e.get("id")==EP_ID]
    if len(matches)!=1: raise RuntimeError("EP04 source is missing or ambiguous")
    ep=matches[0]
    okay, reason, media_url, caption, first_comment=eligible("canonical_ss3",ep,"still")
    if not okay: raise RuntimeError(f"EP04 photo/copy QA gate rejected: {reason}")

    github_token=os.getenv("GITHUB_TOKEN")
    repo=os.getenv("GITHUB_REPOSITORY")
    page_id,page_token=page_credentials("colossus")
    if not github_token or not repo or not page_id or not page_token:
        raise RuntimeError("Required GitHub/Page authorization missing")
    state,*_=state_read(github_token,repo)
    if KEY in state.get("items",{}):
        print("RECOVERY SKIP: existing EP04 Still receipt detected; never post again")
        return

    # Confirm this is the intended Page, not an unrelated Page accessible by the token.
    page=gql(page_id,page_token,"",{"fields":"id,name"})
    if str(page.get("id"))!=str(page_id) or EXPECTED_PAGE_WORD not in page.get("name","").casefold():
        raise RuntimeError("Page identity mismatch; refusing publish")

    # Search the Page feed BEFORE posting. A manually published EP04 using our
    # approved caption should be treated as already posted, not repeated.
    posts=gql(page_id,page_token,"posts",{"fields":"id,message,created_time","limit":75})
    if not isinstance(posts.get("data"),list):
        raise RuntimeError("Page posts not accessible; no safe duplication check")
    canonical = " ".join(caption.split())
    for post in posts["data"]:
        message=" ".join(str(post.get("message","")).split())
        if message==canonical or (len(canonical)>70 and canonical[:100] in message):
            print("RECOVERY SKIP: Colossus EP04 approved caption already appears on Page; no duplicate post")
            return

    # Recheck GitHub receipt in atomic reservation (same key as daily scheduler).
    accepted=state_write(github_token,repo,{
        "status":"RESERVED","scheduled_date":"2026-10-24",
        "time":"06:00","created_at":now.isoformat(),
        "mode":"AUTHORIZED_ONE_TIME_MISSED_SLOT_RECOVERY",
        "comment_status":"NOT_ATTEMPTED",
    },{"key":KEY})
    if not accepted:
        print("RECOVERY SKIP: receipt became reserved by another worker")
        return

    try:
        data=fetch_drive_bytes(media_url,"public_drive")
        # Only canonical EP04 image, never EP03 oneoff derivative or a Reel.
        post_id=publish_photo(page_id,page_token,data,caption)
        if not post_id: raise RuntimeError("Meta photo post response has no post ID")
        stamp=datetime.now(TZ)
        state_replace(github_token,repo,KEY,{
            "status":"PUBLISHED_API_SUCCESS","provider_post_id":str(post_id),
            "published_at":stamp.isoformat(),"publication_confirmation":"META_PHOTO_POST_ACK",
            "recovery_reason":"GitHub 06:00 slot did not start within allowed time",
        })
        print("RECOVERY PHOTO: Meta API returned a Page post ID; receipt saved")
    except Exception as exc:
        try:
            state_replace(github_token,repo,KEY,{"status":"ERROR_NEEDS_MANUAL_CHECK"})
        except Exception: pass
        print(f"RECOVERY STOP: {type(exc).__name__}; do not retry blindly")
        raise

    # First comment must be 5+ minutes after actual photo, not original 06:00.
    try:
        target=stamp+timedelta(minutes=5)
        pause=max(0,(target-datetime.now(TZ)).total_seconds())
        if pause: time.sleep(pause)
        state_replace(github_token,repo,KEY,{
            "comment_status":"RESERVED","comment_reserved_at":datetime.now(TZ).isoformat()})
        cid=publish_comment(page_id,page_token,str(post_id),first_comment)
        state_replace(github_token,repo,KEY,{
            "comment_status":"POSTED_PIN_MANUAL","provider_comment_id":str(cid),
            "commented_at":datetime.now(TZ).isoformat(),
            "pin_status":"NEEDS_MANUAL_PIN",
        })
        print("RECOVERY COMMENT: first comment sent >=5 min after photo; manual pin required")
    except Exception as exc:
        try: state_replace(github_token,repo,KEY,{"comment_status":"ERROR_NEEDS_MANUAL_CHECK"})
        except Exception: pass
        print(f"RECOVERY COMMENT HOLD: {type(exc).__name__}; check Facebook UI, no blind retry")

if __name__=="__main__":
    main()
