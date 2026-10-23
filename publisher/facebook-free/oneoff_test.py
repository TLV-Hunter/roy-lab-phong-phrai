#!/usr/bin/env python3
"""Single-image Colossus test publisher. Fail closed; never backfill or touch season queue."""
import argparse
import io
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo
from PIL import Image, ImageEnhance
from autopost import fetch_drive_bytes, page_credentials, publish_photo, state_write, state_replace

HERE = Path(__file__).resolve().parent
QUEUE_PATH = HERE / "test-posts" / "2026-10-24_colossus_0045.json"
OUT_PATH = Path(os.environ.get("ONEOFF_PREVIEW_PATH", "/tmp/colossus-oneoff-preview.jpg"))
EXPECTED_SOURCE_ID = "1UMNwIHgn9zGkcg2B51N3OpWw4PBPOLoc"

def read_queue():
    job = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))
    m = job["media"]
    if not (job["target_page"] == "colossus"
            and job["type"] == "photo"
            and m["source_url"].startswith("https://drive.google.com/file/d/"+EXPECTED_SOURCE_ID+"/")
            and m["derivative"] == "cyan_fissure_macro_4x5_no_text"
            and str(m["qa"]).startswith("PASS")
            and job["timezone"] == "Asia/Bangkok"
            and "ep03" not in job["caption"].casefold()):
        raise RuntimeError("Unapproved test asset, page, source or caption")
    return job

def make_variant(source_bytes):
    """A deterministic close crop of the canonical shell; excludes lower master lettering."""
    import numpy as np
    original = Image.open(io.BytesIO(source_bytes)).convert("RGB")
    w, h = original.size
    if w < 900 or h < 1600 or h / w < 1.65:
        raise ValueError("Approved canonical master dimensions not met")
    left, top = int(.072*w), int(.09*h)
    cropw = int(.83*w)
    croph = int(cropw*1.25)
    box = left, top, left+cropw, top+croph
    if box[3] > int(.77*h):
        raise ValueError("Crop could include original master title text")
    im = original.crop(box).resize((1600,2000), Image.Resampling.LANCZOS)
    im = ImageEnhance.Contrast(im).enhance(1.17)
    im = ImageEnhance.Color(im).enhance(.88)
    arr = np.array(im).astype(np.float32)
    y,x = np.ogrid[:2000,:1600]
    radius = np.sqrt(((x-800)/1000)**2+((y-940)/1350)**2)
    v = np.clip(1-.23*radius**1.9,.71,1.0)
    arr *= v[...,None]
    arr[:,:,0] *= .96
    arr[:,:,2] *= 1.04
    im = Image.fromarray(np.uint8(np.clip(arr,0,255)),'RGB')
    buf = io.BytesIO()
    im.save(buf,format="JPEG",quality=94,optimize=True,subsampling=0)
    return buf.getvalue()

def scheduled_status(job, now):
    scheduled = datetime.fromisoformat(job["scheduled_at"])
    if scheduled.tzinfo is None or scheduled.utcoffset() != timedelta(hours=7):
        raise ValueError("One-off schedule must specify Bangkok timezone")
    delay = (now - scheduled).total_seconds()
    if delay < 0:
        return "WAITING"
    if delay > min(int(job["constraints"]["max_delay_minutes"]),30)*60:
        return "EXPIRED_NOT_POSTED"
    return "DUE"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode",choices=["preview","publish"],default="preview")
    parser.add_argument("--confirm",default="")
    parser.add_argument("--local-source",default="")
    args=parser.parse_args()
    job=read_queue()
    now = datetime.now(ZoneInfo("Asia/Bangkok"))
    status=scheduled_status(job,now)
    print(f"COLOSSUS ONEOFF | {job['key']} | {job['scheduled_at']} | {status}")
    print(f"COLOSSUS ONEOFF | enabled={job['enabled']} | QA={job['media']['qa']}")
    if args.mode=="publish":
        if not job["enabled"] or os.environ.get("FB_ONEOFF_TEST_ENABLED") != "true":
            print("SAFE HOLD: one-off publishing disabled")
            return
        if status != "DUE":
            print("SAFE HOLD: not in requested post window; no backfill")
            return
        if os.getenv("GITHUB_EVENT_NAME") != "schedule" and args.confirm != "PUBLISH":
            print("SAFE HOLD: explicit manual confirmation missing")
            return
        if not os.environ.get("GITHUB_TOKEN") or not os.environ.get("GITHUB_REPOSITORY"):
            raise RuntimeError("Missing GitHub receipt authorization")
    if args.local_source:
        source_bytes=Path(args.local_source).read_bytes()
    else:
        source_bytes=fetch_drive_bytes(job["media"]["source_url"],"public_drive")
    image_bytes=make_variant(source_bytes)
    OUT_PATH.parent.mkdir(parents=True,exist_ok=True)
    OUT_PATH.write_bytes(image_bytes)
    print(f"COLOSSUS ONEOFF | new image prepared 1600x2000, bytes={len(image_bytes)}, zero title/episode labels")
    if args.mode=="preview":
        print("COLOSSUS ONEOFF | PREVIEW ONLY; no Facebook POST")
        return
    page_id,page_token=page_credentials("colossus")
    if not page_id or not page_token:
        raise RuntimeError("Colossus Page credentials missing")
    repo,token=os.environ["GITHUB_REPOSITORY"],os.environ["GITHUB_TOKEN"]
    key=job["key"]
    if not state_write(token,repo,{"status":"RESERVED","scheduled_at":job["scheduled_at"],"created_at":now.isoformat()},{"key":key}):
        print("COLOSSUS ONEOFF | SKIP: receipt exists; never duplicate")
        return
    try:
        post_id=publish_photo(page_id,page_token,image_bytes,job["caption"])
        state_replace(token,repo,key,{"status":"PUBLISHED_API_SUCCESS",
           "provider_post_id":str(post_id),"published_at":datetime.now(ZoneInfo("Asia/Bangkok")).isoformat()})
        if job.get("first_comment_enabled"):
            from autopost import publish_comment
            try:
                cid=publish_comment(page_id,page_token,post_id,job["first_comment"])
                state_replace(token,repo,key,{"comment_status":"POSTED","comment_id":str(cid)})
            except Exception:
                state_replace(token,repo,key,{"comment_status":"HOLD_MANUAL_CHECK"})
        print("COLOSSUS ONEOFF | PHOTO SENT, receipt saved (post ID deliberately omitted from logs)")
    except Exception as exc:
        try:
            state_replace(token,repo,key,{"status":"ERROR_NEEDS_MANUAL_CHECK"})
        except Exception:
            pass
        print(f"COLOSSUS ONEOFF | HALT {type(exc).__name__}; never retry blindly")
        raise

if __name__=="__main__":
    main()
