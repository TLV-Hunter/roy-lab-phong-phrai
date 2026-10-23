"""Pure time-window and media QA tests for isolated Colossus one-off publisher."""
import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch
import oneoff_test

class OneOffWindowTests(unittest.TestCase):
    def setUp(self):
        self.job = {
            "scheduled_at": "2026-10-24T00:45:00+07:00",
            "constraints": {"max_delay_minutes": 5},
        }
    def test_due_at_target(self):
        self.assertEqual("DUE",oneoff_test.scheduled_status(
            self.job,datetime.fromisoformat("2026-10-24T00:45:00+07:00")))
    def test_early_not_published(self):
        self.assertEqual("WAITING",oneoff_test.scheduled_status(
            self.job,datetime.fromisoformat("2026-10-24T00:44:59+07:00")))
    def test_missed_window_never_backfilled(self):
        self.assertEqual("EXPIRED_NOT_POSTED",oneoff_test.scheduled_status(
            self.job,datetime.fromisoformat("2026-10-24T00:50:01+07:00")))
    def test_next_day_never_backfilled(self):
        self.assertEqual("EXPIRED_NOT_POSTED",oneoff_test.scheduled_status(
            self.job,datetime.fromisoformat("2026-10-25T00:45:00+07:00")))

if __name__=="__main__":
    unittest.main()
