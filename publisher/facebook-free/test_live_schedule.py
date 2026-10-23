"""Zero-network regression for Colossus EP04–special live schedule and comments."""
import json
import os
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch
from zoneinfo import ZoneInfo
import autopost as p

TZ=ZoneInfo("Asia/Bangkok")

class ExactColossusScheduleTests(unittest.TestCase):
    def test_approved_colossus_oct24_starts_at_ep04(self):
        cfg=p.load_json(p.CONFIG)
        brand=cfg["brands"]["colossus"]
        self.assertEqual(brand["start_date"],"2026-10-24")
        self.assertEqual(brand["start_episode_id"],"CS-OCT-004")
        self.assertEqual(brand["end_episode_id"],"CS-OCT-SP01")
        self.assertTrue(brand["enabled"])
        self.assertTrue(brand["comments_enabled"])
        self.assertFalse(cfg["brands"]["rls"]["enabled"])
        plan=p.make_plan(cfg,datetime(2026,10,24,6,0,tzinfo=TZ))
        entries=[x for x in plan if x["brand"]=="colossus"]
        self.assertEqual(len(entries),16)
        self.assertEqual([(a["episode_id"],a["date"],a["time"]) for a in entries[::2]],
                         [(f"CS-OCT-{n:03}",f"2026-10-{24+n-4:02}","06:00") for n in range(4,11)] +
                         [("CS-OCT-SP01","2026-10-31","06:00")])
        self.assertEqual({x["time"] for x in entries if x["kind"]=="reel"},{"23:00"})
        self.assertEqual(sum(x["due"] for x in entries),1)
        self.assertTrue(all(x["ready"] for x in entries))
        self.assertFalse(any(x["episode_id"] in ("CS-OCT-001","CS-OCT-002","CS-OCT-003") for x in entries))

class FiveMinuteCommentReceiptTests(unittest.TestCase):
    def setUp(self):
        self.config={"timezone":"Asia/Bangkok","brands":{"colossus":{"enabled":True,"comments_enabled":True}}}
        self.item={"key":"colossus:CS-OCT-004:still","brand":"colossus","enabled":True,"ready":True,
                   "date":"2026-10-24","time":"06:00","first_comment":"Approved EP04 first comment",
                   "credential_key":"colossus"}
        self.receipt={"status":"PUBLISHED_API_SUCCESS","comment_status":"NOT_ATTEMPTED",
                      "published_at":"2026-10-24T06:00:10+07:00","provider_post_id":"12345_67890"}
    def simulate(self,at,receipt=None):
        with patch.dict(os.environ,{"FB_AUTOPUBLISH_ENABLED":"true","GITHUB_TOKEN":"fake","GITHUB_REPOSITORY":"test/repo"}):
            with patch.object(p,"state_read",return_value=({"items":{self.item["key"]:receipt if receipt is not None else self.receipt}},"sha","url",{})):
                with patch.object(p,"state_replace") as save:
                    with patch.object(p,"publish_comment",return_value="987654") as publish:
                        with patch.object(p,"page_credentials",return_value=("page","token")):
                            p.process_pending_comments(self.config,datetime.fromisoformat(at),[self.item])
                            return save.call_args_list,publish.call_args_list
    def test_not_before_actual_post_plus_five_minutes(self):
        saves,calls=self.simulate("2026-10-24T06:05:00+07:00")
        self.assertEqual(len(calls),0)
        self.assertEqual(len(saves),0)
    def test_publish_comment_after_five_actual_minutes_and_mark_pin_manual(self):
        saves,calls=self.simulate("2026-10-24T06:05:10+07:00")
        self.assertEqual(len(calls),1)
        self.assertEqual(len(saves),2)
        self.assertEqual(saves[1].args[3]["pin_status"],"NEEDS_MANUAL_PIN")
    def test_never_double_comment(self):
        rec={**self.receipt,"comment_status":"POSTED_PIN_MANUAL"}
        saves,calls=self.simulate("2026-10-24T06:10:10+07:00",rec)
        self.assertEqual(len(calls),0)
    def test_never_backfill_expired_comments(self):
        saves,calls=self.simulate("2026-10-24T08:10:00+07:00")
        self.assertEqual(len(calls),0)


class ReelPublishingPhaseTests(unittest.TestCase):
    def test_meta_finish_ack_is_not_publication(self):
        mock=type("Response",(),{"ok":True,"json":lambda self:{"status":{
            "video_status":"processing","publishing_phase":{"publish_status":"processing"}}}})()
        with patch.object(p.requests,"get",return_value=mock):
            self.assertEqual(p.reel_publishing_status("123","tok"),"processing")

    def test_meta_published_status(self):
        mock=type("Response",(),{"ok":True,"json":lambda self:{"status":{
            "video_status":"ready","publishing_phase":{"publish_status":"published"}}}})()
        with patch.object(p.requests,"get",return_value=mock):
            self.assertEqual(p.reel_publishing_status("123","tok"),"published")

    def test_meta_error_halts(self):
        mock=type("Response",(),{"ok":True,"json":lambda self:{"status":{
            "video_status":"upload_failed","publishing_phase":{"publish_status":"error"}}}})()
        with patch.object(p.requests,"get",return_value=mock):
            self.assertEqual(p.reel_publishing_status("123","tok"),"failed")

if __name__=="__main__":
    unittest.main()
