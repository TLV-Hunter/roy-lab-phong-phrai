#!/usr/bin/env python3
"""Read-only Colossus publication receipts audit. No Meta calls, no post API."""
import argparse
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo
from autopost import CONFIG, ROOT, STATE_PATH, load_json, make_plan

TZ = ZoneInfo("Asia/Bangkok")

def audit(now, config, receipts):
    """Returns list of (status, episode, kind, due_at, reason) for elapsed slots."""
    plan = make_plan(config, now)
    checks = []
    for item in plan:
        if item["brand"] != "colossus" or not item["enabled"]:
            continue
        if not item["date"]:
            continue
        due = datetime.fromisoformat(item["date"]+"T"+item["time"]).replace(tzinfo=TZ)
        elapsed = (now-due).total_seconds()
        # Only inspect recent slot; old missed items must not fail every future audit.
        if elapsed < 35*60 or elapsed > 3*3600:
            continue
        result = (receipts.get("items") or {}).get(item["key"])
        if result is None:
            checks.append(("MISSED_NO_RECEIPT",item["episode_id"],item["kind"],due.isoformat(),
                "No publisher receipt; no confirmed Facebook post. Check Actions and Page before manual recovery"))
            continue
        status = str(result.get("status","UNKNOWN"))
        if status == "PUBLISHED_API_SUCCESS":
            checks.append(("API_CONFIRMED",item["episode_id"],item["kind"],due.isoformat(),
                "Provider post ID saved; check Page UI for visibility and comment/pin"))
        elif status == "PUBLISH_ACCEPTED_PROCESSING":
            checks.append(("UNVERIFIED_PROCESSING",item["episode_id"],item["kind"],due.isoformat(),
                "Meta accepted Reel finish; video live state still unverified"))
        else:
            checks.append(("MANUAL_CHECK",item["episode_id"],item["kind"],due.isoformat(),
                f"Saved receipt state {status}, never blindly repost"))
    return checks

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--at",default=None,help="Override Bangkok ISO date-time for offline tests")
    p.add_argument("--strict",action="store_true",help="Fail CI if a due item is missing confirmation")
    a=p.parse_args()
    now=datetime.fromisoformat(a.at) if a.at else datetime.now(TZ)
    if now.tzinfo is None:
        raise ValueError("Audit must use a timezone-aware datetime")
    now=now.astimezone(TZ)
    cfg=load_json(CONFIG)
    receipts=load_json(ROOT/STATE_PATH)
    checks=audit(now,cfg,receipts)
    print(f"COLOSSUS AUDIT | time_Bangkok={now.isoformat()} | elapsed_slots={len(checks)} | read_only=true")
    errors=0
    for state,ep,kind,due,note in checks:
        print(f"COLOSSUS AUDIT | {state} | {ep} | {kind} | scheduled={due} | {note}")
        if state != "API_CONFIRMED":
            errors+=1
            print(f"::error title=Colossus {ep} {kind}::No confirmed Facebook post. State {state}; verify Page and Actions before retry")
    if a.strict and errors:
        raise SystemExit(1)

if __name__=="__main__":
    main()
