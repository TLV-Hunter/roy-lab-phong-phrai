"""No-network regression tests: auditable missed vs API-confirmed content."""
import unittest
from unittest.mock import patch
from datetime import datetime
from zoneinfo import ZoneInfo
import audit_schedule as audit

TZ=ZoneInfo("Asia/Bangkok")
NOW=datetime(2026,10,24,7,0,tzinfo=TZ)
ITEM={"key":"colossus:CS-OCT-004:still","brand":"colossus",
      "episode_id":"CS-OCT-004","kind":"still","date":"2026-10-24",
      "time":"06:00","enabled":True}

class ReadOnlyAuditTests(unittest.TestCase):
    def run_check(self,items,records,now=NOW):
        with patch.object(audit,"make_plan",return_value=items):
            return audit.audit(now,{"timezone":"Asia/Bangkok"},{"items":records})
    def test_no_receipt_marks_missed(self):
        got=self.run_check([ITEM],{})
        self.assertEqual(got[0][0],"MISSED_NO_RECEIPT")
    def test_success_receipt_is_not_missed(self):
        got=self.run_check([ITEM],{ITEM["key"]:{"status":"PUBLISHED_API_SUCCESS"}})
        self.assertEqual(got[0][0],"API_CONFIRMED")
    def test_meta_verified_external_post_counts_as_confirmed(self):
        got=self.run_check([ITEM],{ITEM["key"]:{"status":"VERIFIED_EXISTING_PAGE_POST"}})
        self.assertEqual(got[0][0],"API_CONFIRMED")
    def test_reel_processing_needs_manual_confirmation(self):
        got=self.run_check([ITEM],{ITEM["key"]:{"status":"PUBLISH_ACCEPTED_PROCESSING"}})
        self.assertEqual(got[0][0],"UNVERIFIED_PROCESSING")
    def test_audit_never_revisits_old_misses(self):
        got=self.run_check([ITEM],{},datetime(2026,10,25,7,0,tzinfo=TZ))
        self.assertEqual(got,[])
    def test_future_is_not_missed(self):
        got=self.run_check([ITEM],{},datetime(2026,10,24,5,59,tzinfo=TZ))
        self.assertEqual(got,[])
    def test_too_early_for_audit(self):
        got=self.run_check([ITEM],{},datetime(2026,10,24,6,34,tzinfo=TZ))
        self.assertEqual(got,[])
    def test_no_external_page_is_audited(self):
        got=self.run_check([dict(ITEM,brand="rls")],{})
        self.assertEqual(got,[])

if __name__=="__main__":
    unittest.main()
