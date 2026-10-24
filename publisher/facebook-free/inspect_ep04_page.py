#!/usr/bin/env python3
"""Read-only Meta Page reconciliation: exact approved EP04 Still caption."""
import os
from datetime import datetime
from zoneinfo import ZoneInfo
import requests
from autopost import load_json, CONFIG, ROOT, page_credentials

def main():
    cfg=load_json(CONFIG)
    item=next(x for x in load_json(ROOT / cfg["brands"]["colossus"]["content_path"])["episodes"] if x["id"]=="CS-OCT-004")
    target=" ".join(item["still"]["caption"].split())
    pid,tok=page_credentials("colossus")
    if not pid or not tok:
        print("EP04 READONLY: HOLD missing Meta Page authorization");return
    base=f"https://graph.facebook.com/{os.getenv('FB_GRAPH_VERSION') or 'v26.0'}"
    for endpoint,params in [(f"/{pid}",{"fields":"id,name"}),(f"/{pid}/posts",{"fields":"id,message,created_time","limit":75})]:
        r=requests.get(base+endpoint,params=params,headers={"Authorization":"Bearer "+tok},timeout=30)
        if not r.ok:
            print(f"EP04 READONLY: HOLD Meta GET failed HTTP {r.status_code}");return
        obj=r.json()
        if endpoint==f"/{pid}":
            if str(obj.get("id"))!=str(pid) or "colossus" not in str(obj.get("name","")).casefold():
                print("EP04 READONLY: HOLD Page ID/name mismatch");return
            continue
        posts=obj.get("data",[])
        exact=[x for x in posts if " ".join(str(x.get("message","")).split())==target]
        print(f"EP04 READONLY: exact_approved_caption_matches={len(exact)}")
        for post in exact:
            public_post=str(post.get("id",""))
            utc_date=post.get("created_time","UNKNOWN")
            try:
                bangkok=datetime.fromisoformat(utc_date.replace("Z","+00:00")).astimezone(ZoneInfo("Asia/Bangkok")).isoformat()
            except ValueError:
                bangkok="UNKNOWN"
            print(f"EP04 READONLY: VERIFIED_EXISTING post_id={public_post} created_Bangkok={bangkok}")
            if not public_post:continue
            cr=requests.get(f"{base}/{public_post}/comments",
                params={"fields":"id,message,created_time","limit":100},
                headers={"Authorization":"Bearer "+tok},timeout=30)
            if not cr.ok:
                print(f"EP04 READONLY: comment_list=UNAVAILABLE HTTP {cr.status_code}")
                continue
            cm=cr.json().get("data",[])
            approved=" ".join(item["still"]["first_comment"].split())
            match=sum(" ".join(str(c.get("message","")).split())==approved for c in cm)
            print(f"EP04 READONLY: approved_first_comment_matches={match}; total_retrieved_comments={len(cm)}")
if __name__=="__main__":
    main()
