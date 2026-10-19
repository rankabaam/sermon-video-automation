import json
import tempfile
import unittest
from pathlib import Path

from src.publish_preview import (
    FakePostStore, RunState, canonical_watch_url, is_public_embed,
    save_atomically, simulate, verify_or_repair,
)


class PublicationPreviewTests(unittest.TestCase):
    def state(self, scope="full_publish"):
        return RunState(scope, "DEMO_VIDEO_001", "DEMO-POST-001", ["DEMO-PL-01"])

    def test_watch_url_is_canonical(self):
        self.assertEqual(canonical_watch_url("DEMO_VIDEO_001"),
                         "https://www.youtube.com/watch?v=DEMO_VIDEO_001")

    def test_invalid_video_id_rejected(self):
        with self.assertRaises(ValueError):
            canonical_watch_url("https://evil.example/")

    def test_public_embed_requires_iframe(self):
        self.assertFalse(is_public_embed('<a href="https://www.youtube.com/watch?v=DEMO_VIDEO_001">x</a>', "DEMO_VIDEO_001"))
        self.assertTrue(is_public_embed(
            '<iframe src="https://www.youtube.com/embed/DEMO_VIDEO_001"></iframe>',
            "DEMO_VIDEO_001"))

    def test_already_valid_needs_no_repair(self):
        store = FakePostStore("DEMO_VIDEO_001")
        store.repair("DEMO-POST-001", canonical_watch_url("DEMO_VIDEO_001"))
        store.update_calls.clear()
        state = verify_or_repair(self.state(), fetch_public_html=store.fetch, update_existing_post=store.repair)
        self.assertEqual(state.verification, "passed")
        self.assertEqual(store.update_calls, [])

    def test_repairs_one_existing_post_once(self):
        store = FakePostStore("DEMO_VIDEO_001")
        state = self.state()
        verify_or_repair(state, fetch_public_html=store.fetch, update_existing_post=store.repair)
        self.assertEqual(state.verification, "recreated_and_passed")
        self.assertEqual(state.recovery_attempts, 1)
        self.assertEqual(len(store.update_calls), 1)
        self.assertEqual(store.update_calls[0][0], "DEMO-POST-001")
        verify_or_repair(state, fetch_public_html=store.fetch, update_existing_post=store.repair)
        self.assertEqual(len(store.update_calls), 1)

    def test_persistent_failure_stops_after_once(self):
        state = simulate("unrecoverable")
        self.assertEqual(state.verification, "recreated_and_failed")
        self.assertEqual(state.recovery_attempts, 1)

    def test_other_scope_skips_publication(self):
        store = FakePostStore("DEMO_VIDEO_001")
        state = verify_or_repair(self.state("edit_only"), fetch_public_html=store.fetch, update_existing_post=store.repair)
        self.assertEqual(state.verification, "not_applicable")
        self.assertEqual(store.update_calls, [])

    def test_atomically_written_state(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "run_state.json"
            save_atomically(output, self.state())
            data = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(data["post_id"], "DEMO-POST-001")
            self.assertEqual(data["recovery_attempts"], 0)

    def test_duplicate_playlist_rejected(self):
        with self.assertRaises(ValueError):
            RunState("edit_only", "DEMO_VIDEO_001", "DEMO-POST-001", ["DEMO-PL-01", "DEMO-PL-01"])


if __name__ == "__main__":
    unittest.main()
