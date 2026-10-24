#!/usr/bin/env python3
"""Read-only SS3 public Page state audit; NEVER sends Facebook POST."""
import os
from datetime import datetime
from zoneinfo import ZoneInfo
import requests
from autopost import load_json, CONFIG, ROOT, page_credentials
TZ=ZoneInfo("Asia/Bangkok")
def norm(s): return " ".join(str(s or "").split())
def fetch_page_data(page_id,token,kind,params):
    base=f"https://graph.facebook.com/{os.getenv('FB_GRAPH_VERSION') or 'v26.0'}/{page_id}/{kind}"
    r=requests.get(base,params=params,headers={"Authorization":"Bearer "+token},timeout=40)
    if not r.ok: return None,f"HTTP_{r.status_code}"
    j=r.json()
    if "error" in j:return None,"META_ERROR"
    # Limit to the most recent 100, not a comprehensive historical crawl.
    return j.get("data",[]),"OK"
def local_time(val):
    try:return datetime.fromisoformat(val.replace("Z","+00:00")).astimezone(TZ).isoformat()
    except Exception:return "UNKNOWN"
def main():
    cfg=load_json(CONFIG)
    source=load_json(ROOT/cfg["brands"]["colossus"]["content_path"])
    episodes=source["episodes"]+[source["halloween_special"]]
    page_id,token=page_credentials("colossus")
    if not page_id or not token: raise RuntimeError("No Colossus Page authorization")
    u=f"https://graph.facebook.com/{os.getenv('FB_GRAPH_VERSION') or 'v26.0'}/{page_id}"
    resp=requests.get(u,params={"fields":"id,name"},headers={"Authorization":"Bearer "+token},timeout=35)
    if not resp.ok or str(resp.json().get("id"))!=str(page_id) or "colossus" not in resp.json().get("name","").casefold():
        raise RuntimeError("Page identity verification failed")
    posts,p_status=fetch_page_data(page_id,token,"posts",{"fields":"id,message,created_time","limit":100})
    videos,v_status=fetch_page_data(page_id,token,"videos",{"fields":"id,description,created_time","limit":100})
    print(f"SS3 FACEBOOK AUDIT | READ ONLY | Page posts={p_status} | Page videos={v_status}")
    total_stills=total_videos=0
    for ep in episodes:
        eid=ep["id"]
        caption=norm(ep.get("still",{}).get("caption"))
        found=[p for p in posts or [] if norm(p.get("message"))==caption] if p_status=="OK" and caption else []
        if found:total_stills+=1
        when=local_time(found[0].get("created_time","")) if found else "-"
        # Reel /video discovery is best effort; missing via /videos does not prove absent on Facebook Reels.
        video_caption=norm(ep.get("reel",{}).get("caption"))
        matching_videos=[v for v in videos or [] if norm(v.get("description"))==video_caption] if v_status=="OK" and video_caption else []
        if matching_videos:total_videos+=1
        vreel_time=local_time(matching_videos[0].get("created_time","")) if matching_videos else "-"
        print(f"SS3 | {eid} | still_exact={'YES' if found else 'NOT_FOUND_IN_RECENT_POSTS'} | still_BKK={when} | reel_exact_in_page_videos={'YES' if matching_videos else 'NOT_VERIFIED'} | reel_BKK={vreel_time}")
    print(f"SS3 FACEBOOK AUDIT SUMMARY | exactStillMatches={total_stills}/11 | exactReelMatchesViaVideos={total_videos}/11 | note=not_all_FB_Reels_may_appear_in_Page_videos | never equate missing with unpublished")
if __name__=="__main__":main()
