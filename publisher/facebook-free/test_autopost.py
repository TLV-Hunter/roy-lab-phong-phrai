"""Offline, no-secrets QA tests for free multi-page Facebook publisher."""
import importlib.util
import json
import os
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("autopost", HERE / "autopost.py")
publisher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publisher)


class SchedulingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.old_root = publisher.ROOT
        publisher.ROOT = Path(self.tmp.name)
        (publisher.ROOT / "fixture").mkdir()
        self.ep = {
            "id": "EP01",
            "master": {"url": "https://drive.google.com/file/d/aa/view", "qa": "PASS"},
            "still": {"caption": "MASTER still caption #tag", "first_comment": "Master first comment", "copy_qa": "PASS"},
            "reel": {"url": "https://drive.google.com/file/d/bb/view", "qa": "PASS",
                     "caption": "Reel caption #tag", "first_comment": "Reel first comment", "copy_qa": "PASS"},
            "publication": {"status": "UNCONFIRMED"},
        }
        (publisher.ROOT / "fixture" / "colossus.json").write_text(json.dumps({"episodes": [self.ep]}), encoding="utf-8")
        (publisher.ROOT / "fixture" / "future.json").write_text(json.dumps({"episodes": [{**self.ep, "id": "EP-NEW"}]}), encoding="utf-8")
        (publisher.ROOT / "fixture" / "rls.json").write_text(json.dumps({
            "episodes": [{"id": "RLS01",
                          "master_still": {"status": "ARCHIVED_JPEG_PREVIEW_NOT_FINAL_MASTER", "image_url": "./archived.jpg"},
                          "still_caption": "Archived caption", "first_comment": "Archived comment",
                          "final_reel": {"status": "LOCAL_QA_PASS_NOT_UPLOADED", "video_url": None},
                          "publication_status": "NOT_CONFIRMED"}]}), encoding="utf-8")
        self.config = {
            "timezone": "Asia/Bangkok",
            "brands": {
                "colossus": {"enabled": False, "content_path": "fixture/colossus.json",
                             "content_format": "canonical_ss3", "credential_key": "colossus",
                             "start_date": "2026-11-01", "slots": {"still": "06:00", "reel": "23:00"}},
                "rls": {"enabled": False, "content_path": "fixture/rls.json",
                        "content_format": "rls_ss3", "credential_key": "rls",
                        "start_date": "2026-11-01", "slots": {"still": "06:00", "reel": "23:00"}},
                "page_three": {"enabled": False, "content_path": "fixture/future.json",
                               "content_format": "canonical_ss3", "credential_key": "page_three",
                               "start_date": "2026-11-01", "slots": {"still": "06:00", "reel": "23:00"}},
            },
        }

    def tearDown(self):
        publisher.ROOT = self.old_root
        self.tmp.cleanup()

    def test_both_slots_same_all_brands(self):
        now = datetime(2026, 11, 1, 6, 10, tzinfo=ZoneInfo("Asia/Bangkok"))
        plan = publisher.make_plan(self.config, now)
        self.assertEqual(len(plan), 6)
        self.assertEqual({e["time"] for e in plan if e["kind"] == "still"}, {"06:00"})
        self.assertEqual({e["time"] for e in plan if e["kind"] == "reel"}, {"23:00"})
        self.assertEqual(len([e for e in plan if e["due"]]), 3)
        self.assertEqual(len([e for e in plan if e["enabled"]]), 0)

    def test_reel_23_due_not_at_six(self):
        now = datetime(2026, 11, 1, 23, 10, tzinfo=ZoneInfo("Asia/Bangkok"))
        plan = publisher.make_plan(self.config, now)
        self.assertTrue(all(e["due"] == (e["kind"] == "reel") for e in plan))

    def test_future_page_adapter_no_code_changes(self):
        plan = publisher.make_plan(self.config, datetime(2026, 11, 1, 6, 10, tzinfo=ZoneInfo("Asia/Bangkok")))
        self.assertEqual(len([x for x in plan if x["brand"] == "page_three" and x["ready"]]), 2)
        self.assertEqual(len([x for x in plan if x["brand"] == "colossus" and x["ready"]]), 2)

    def test_rls_holds_archived_media(self):
        plan = publisher.make_plan(self.config, datetime(2026, 11, 1, 6, 10, tzinfo=ZoneInfo("Asia/Bangkok")))
        self.assertTrue(all(not x["ready"] for x in plan if x["brand"] == "rls"))

    def test_banned_storyboard_not_published(self):
        self.assertEqual(publisher.eligible("canonical_ss3", self.ep, "still")[3], self.ep["still"]["caption"])
        self.assertEqual(publisher.eligible("canonical_ss3", self.ep, "reel")[3], self.ep["reel"]["caption"])

    def test_secret_unlimited_brand_keys(self):
        creds = {"page_three": {"page_id": "123", "access_token": "dummy"}}
        with patch.dict(os.environ, {"FB_PAGES_JSON": json.dumps(creds)}):
            self.assertEqual(publisher.page_credentials("page_three"), ("123", "dummy"))
            self.assertEqual(publisher.page_credentials("rls"), (None, None))

    def test_unknown_format_fails_closed(self):
        self.assertFalse(publisher.eligible("random_unverified", self.ep, "reel")[0])

    def test_no_backfill_after_30_minutes(self):
        now = datetime(2026, 11, 1, 6, 31, tzinfo=ZoneInfo("Asia/Bangkok"))
        plan = publisher.make_plan(self.config, now)
        self.assertFalse(any(p["due"] for p in plan))

    def test_google_drive_strict_identity(self):
        self.assertEqual(publisher.drive_file_id("https://drive.google.com/file/d/abc-123/view"), "abc-123")


if __name__ == "__main__":
    unittest.main()
