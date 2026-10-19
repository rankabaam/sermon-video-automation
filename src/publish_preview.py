"""Synthetic, offline publication-state demonstration.

No YouTube or WordPress account, token, upload or publishing action is used.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable

SCOPES = ("edit_only", "video_only", "full_publish")
VISIBILITIES = ("private", "unlisted", "public")
VIDEO_ID = re.compile(r"^[A-Za-z0-9_-]{6,80}$")


def canonical_watch_url(video_id: str) -> str:
    if not VIDEO_ID.fullmatch(video_id):
        raise ValueError("Invalid synthetic video identifier")
    return f"https://www.youtube.com/watch?v={video_id}"


def is_public_embed(html: str, video_id: str) -> bool:
    """Minimal portfolio check, not a production DOM/browser acceptance test."""
    if not VIDEO_ID.fullmatch(video_id):
        return False
    return bool(re.search(
        r'<iframe\b[^>]*\bsrc=["\x27]https://www\.youtube\.com/embed/' +
        re.escape(video_id) + r'(?:\?[^"\x27]*)?["\x27]',
        html, re.IGNORECASE
    ))


@dataclass
class RunState:
    scope: str
    video_id: str
    post_id: str
    playlist_ids: list[str]
    visibility: str = "unlisted"
    recovery_attempts: int = 0
    verification: str = "pending"

    def __post_init__(self) -> None:
        if self.scope not in SCOPES:
            raise ValueError("Unknown scope")
        if self.visibility not in VISIBILITIES:
            raise ValueError("Unknown visibility")
        canonical_watch_url(self.video_id)
        if not self.post_id.startswith("DEMO-"):
            raise ValueError("Only synthetic post identifiers are accepted")
        if len(self.playlist_ids) != len(set(self.playlist_ids)):
            raise ValueError("Duplicate playlist id")


def verify_or_repair(
    state: RunState,
    *,
    fetch_public_html: Callable[[str], str],
    update_existing_post: Callable[[str, str], None],
) -> RunState:
    """No new post/video creation. One repair attempt at most, original IDs retained."""
    if state.scope != "full_publish":
        state.verification = "not_applicable"
        return state
    if state.verification in {"passed", "recreated_and_passed", "recreated_and_failed"}:
        return state
    if is_public_embed(fetch_public_html(state.post_id), state.video_id):
        state.verification = "passed"
        return state
    if state.recovery_attempts >= 1:
        state.verification = "recreated_and_failed"
        return state
    state.recovery_attempts += 1
    # Update the same fictional post in place. Never create an additional post or video.
    update_existing_post(state.post_id, canonical_watch_url(state.video_id))
    state.verification = (
        "recreated_and_passed"
        if is_public_embed(fetch_public_html(state.post_id), state.video_id)
        else "recreated_and_failed"
    )
    return state


def save_atomically(path: Path, state: RunState) -> None:
    """Write a complete synthetic run snapshot via atomic same-directory replacement."""
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(dir=path.parent, prefix=".run_state_", suffix=".tmp")
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(asdict(state), stream, indent=2)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


class FakePostStore:
    """In-memory invented post, not a network client."""
    def __init__(self, video_id: str) -> None:
        self.html = ""
        self.video_id = video_id
        self.update_calls = []
    def fetch(self, post_id: str) -> str:
        return self.html
    def repair(self, post_id: str, watch_url: str) -> None:
        self.update_calls.append((post_id, watch_url))
        self.html = (f'<div class="wp-block-embed"><a href="{watch_url}">Video</a>'
                     f'<iframe src="https://www.youtube.com/embed/{self.video_id}"></iframe></div>')


def simulate(scenario: str) -> RunState:
    state = RunState("full_publish", "DEMO_VIDEO_001", "DEMO-POST-001",
                     ["DEMO-PLAYLIST-A"], "unlisted")
    store = FakePostStore(state.video_id)
    if scenario == "valid":
        store.repair(state.post_id, canonical_watch_url(state.video_id))
        store.update_calls.clear()
    elif scenario == "unrecoverable":
        store.repair = lambda post_id, watch_url: None
    elif scenario != "recover":
        raise ValueError("Unknown scenario")
    return verify_or_repair(state, fetch_public_html=store.fetch,
                            update_existing_post=store.repair)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", choices=["valid", "recover", "unrecoverable"], default="recover")
    parser.add_argument("--output", type=Path, default=Path("output/portfolio_run_state.json"))
    args = parser.parse_args()
    state = simulate(args.scenario)
    save_atomically(args.output, state)
    print(f"{state.verification}: wrote {args.output} (synthetic data only)")


if __name__ == "__main__":
    main()
