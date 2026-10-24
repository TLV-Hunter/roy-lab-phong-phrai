#!/usr/bin/env python3
"""Safely record an already-existing Colossus EP04 Page post, without publishing."""
import os
from datetime import datetime
from zoneinfo import ZoneInfo
import requests
from autopost import (
    load_json,CONFIG,ROOT,page_credentials,state_read,state_write,TIMEOUT,
)
TZ=ZoneInfo("Asia/Bangkok")
KEY="colossus:CS-OCT-004:still"
def fb_read(path,token,params):
    r=requests.get(
        f"https://graph.facebook.com/{os.getenv('FB_GRAPH_VERSION') or 'v26.0'}/{path}",
        params=params,headers={"Authorization":"Bearer "+token},timeout=TIMEOUT)
    if not r.ok or r.json().get("error"):
        raise RuntimeError(f"Meta read-only reconciliation rejected request HTTP {r.status_code}")
    return r.json()
def main():
    cfg=load_json(CONFIG)
    brand=cfg["brands"]["colossus"]
    if not(brand["enabled"] and brand["start_episode_id"]=="CS-OCT-004"
           and brand["start_date"]=="2026-10-24"):
        raise RuntimeError("Colossus campaign was modified, no reconciliation")
    src=load_json(ROOT/brand["content_path"])
    ep=next(e for e in src["episodes"] if e.get("id")=="CS-OCT-004")
    pid,token=page_credentials("colossus")
    gh_token,repo=os.getenv("GITHUB_TOKEN"),os.getenv("GITHUB_REPOSITORY")
    if not all((pid,token,gh_token,repo)):
        raise RuntimeError("Missing Page or GitHub authorization")
    recorded,*_=state_read(gh_token,repo)
    if KEY in recorded.get("items",{}):
        print("EP04 RECEIPT: existing record, leaving unchanged")
        return
    page=fb_read(pid,token,{"fields":"id,name"})
    if str(page.get("id"))!=str(pid) or "colossus" not in page.get("name","").casefold():
        raise RuntimeError("Meta Page identity mismatch")
    feed=fb_read(f"{pid}/posts",token,{"fields":"id,message,created_time","limit":75})
    expected=" ".join(ep["still"]["caption"].split())
    exact=[p for p in feed.get("data",[]) if " ".join(str(p.get("message","")).split())==expected]
    if len(exact)!=1:
        print(f"EP04 RECEIPT HOLD: expected exactly one matching approved caption, found {len(exact)}")
        return
    matched=exact[0]
    timestamp=datetime.fromisoformat(matched["created_time"].replace("Z","+00:00")).astimezone(TZ)
    if timestamp.date().isoformat()!="2026-10-24":
        raise RuntimeError("Existing post's date differs from approved Oct 24 slot")
    post_id=str(matched.get("id",""))
    if not post_id.startswith(str(pid)+"_"):
        raise RuntimeError("Existing Facebook post ID does not belong to authorized Page")
    comments=fb_read(f"{post_id}/comments",token,{"fields":"id,message,created_time","limit":100})
    first=" ".join(ep["still"]["first_comment"].split())
    matched_comments=[c for c in comments.get("data",[]) if " ".join(str(c.get("message","")).split())==first]
    if len(matched_comments)>1:
        raise RuntimeError("Duplicate approved first comments exist; reconcile manually")
    cm=matched_comments[0] if matched_comments else None
    # An existing Page post can originate outside this publisher. The audit must
    # not falsely label it as an API success emitted by our scheduled workflow.
    entry={
        "status":"VERIFIED_EXISTING_PAGE_POST",
        "provider_post_id":post_id,
        "scheduled_date":"2026-10-24",
        "time":"06:00",
        "published_at":timestamp.isoformat(),
        "reconciled_at":datetime.now(TZ).isoformat(),
        "publication_confirmation":"META_PAGE_POSTS_EXACT_CAPTION_MATCH",
        "origin":"UNKNOWN_EXISTING_FACEBOOK_POST",
        "comment_status":"VERIFIED_EXISTING_PAGE_COMMENT" if cm else "EXTERNAL_COMMENT_NOT_VERIFIED",
        "pin_status":"MANUAL_PIN_VERIFICATION_REQUIRED",
    }
    if cm:entry["provider_comment_id"]=str(cm["id"])
    ok=state_write(gh_token,repo,entry,{"key":KEY})
    print("EP04 RECEIPT: reconciled Meta-confirmed existing Page post and approved first comment" if ok else
          "EP04 RECEIPT: another writer reserved same key; no duplicate")
    print("EP04 RECEIPT: no Facebook POST attempted; manual pin check still required")
if __name__=="__main__":
    main()
