#!/usr/bin/env python3
"""Optional offline Ollama quality assistant (never publishes or modifies approved copy)."""
import argparse
import json
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = Path(__file__).with_name("config.json")


def get_copy(brand, episode_id, kind):
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    settings = config["brands"].get(brand)
    if not settings:
        raise ValueError("Unknown brand. Add it in config.json first.")
    path = ROOT / settings["content_path"]
    data = json.loads(path.read_text(encoding="utf-8"))
    eps = data.get("episodes", [])
    if data.get("halloween_special"):
        eps = eps + [data["halloween_special"]]
    ep = next((e for e in eps if e.get("id") == episode_id), None)
    if not ep:
        raise ValueError("Episode not found in approved brand registry")
    if settings.get("content_format") == "rls_ss3":
        caption = ep.get("still_caption") if kind == "still" else ep.get("reel_caption")
        comment = ep.get("first_comment") if kind == "still" else ep.get("reel_first_comment")
    else:
        asset = ep.get("still") if kind == "still" else ep.get("reel")
        caption, comment = asset.get("caption"), asset.get("first_comment")
    if not caption or not comment:
        raise ValueError("Approved caption/comment missing. Do not invent publication copy automatically.")
    return {"brand": brand, "episode_id": episode_id, "kind": kind,
            "title": ep.get("title"), "caption": caption, "first_comment": comment}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--brand", default="colossus")
    ap.add_argument("--episode", required=True)
    ap.add_argument("--kind", choices=("still", "reel"), default="reel")
    ap.add_argument("--model", default="qwen3:4b-instruct")
    args = ap.parse_args()
    content = get_copy(args.brand, args.episode, args.kind)
    instructions = (
        "You are a careful Facebook Page content QA reviewer for fictional AI-generated cinematic "
        "content targeting a US audience. Review the following already-approved copy. "
        "Check clarity, first two-second hook strength, hashtags, whether it describes the "
        "provided story without pretending fictional events are real, and whether the pinned "
        "comment is distinctive and non-spammy. Do not change character identities, episode "
        "numbers, or claim any media has been posted. Return three concise suggestions only. "
        "Never schedule or publish anything. Do not echo the entire submitted copy.\n"
    )
    req = Request(
        "http://127.0.0.1:11434/api/chat",
        data=json.dumps({"model": args.model, "stream": False,
                         "messages": [{"role": "system", "content": instructions},
                                      {"role": "user", "content": json.dumps(content, ensure_ascii=False)}],
                         "options": {"num_ctx": 4096, "temperature": 0.2}}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(req, timeout=300) as response:
            value = json.load(response)
    except Exception as exc:
        raise SystemExit(f"Ollama not available locally: {type(exc).__name__}. Run Ollama and pull the chosen model first.")
    print(json.dumps({"episode_id": args.episode, "kind": args.kind,
                      "approved_copy_unchanged": True,
                      "ai_review_suggestions": value.get("message", {}).get("content", "")},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
