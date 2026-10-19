# v1.4 UI Preview — Portfolio Scope (October 2026)

The original software had an August 2026 `v1.4.0-ui-preview` stage emphasizing an easier operator interface, per-scope progress, publishing state and an in-place WordPress embed recovery strategy.

This independent public repository update **does not copy that application**. It adds two safe examples:

1. [Standalone dashboard mockup](../samples/dashboard_ui_preview.html) — browser-only interaction, fake progress, independent fictional playlist identifiers, visibility choice, and scope modes.
2. [Publication state simulation](../src/publish_preview.py) — standard-library Python example of read/validate/one-time repair of a **fictional existing post**, with an atomic local `run_state.json` snapshot.

## Run

```bash
python -m src.publish_preview --scenario recover --output output/portfolio_run_state.json
python -m src.publish_preview --scenario unrecoverable --output output/portfolio_failed_state.json
python -m unittest discover -s tests -v
```

To see the UI, download `samples/dashboard_ui_preview.html` and open in a browser.

## Recovery behavior demonstrated

- Use a canonical public `watch?v=` URL.
- Validate whether an invented public HTML response contains a corresponding YouTube iframe.
- Attempt at most one in-place repair, preserving the **same** fictional post ID and video ID.
- Persist `recreated_and_passed` or `recreated_and_failed`; refuse repeated retry from a terminal state.
- There is no function to create, delete, or upload posts/videos.

This is an illustrative state model. It does not use WordPress REST, a browser to confirm embed playback, YouTube APIs, OAuth, OBS, or real media files.

## Actual deployment status

The original `v1.4.0-ui-preview` work had local tests and edit-only smoke checks, but live YouTube/WordPress acceptance and full weekly production operation were **not verified**. Do not treat either this sample or the original preview status as evidence of a live publishing rollout.
