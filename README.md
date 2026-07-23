# Sermon Video Automation

A sanitized, config-driven Python and FFmpeg workflow for reducing repetitive weekly sermon-media production work.

## Runnable Demo

```bash
pip install -r requirements.txt
python scripts/sermon_automation_sample.py --date 2026-07-23
python scripts/sermon_automation_sample.py --execute --input path/to/authorized_recording.mp4
```

Dry-run is the default. Execute mode requires `ffmpeg` and `ffprobe` on `PATH` and media the operator owns or is authorized to process.

## Current Workflow

```text
Newest authorized recording or explicit input
                  ↓
Configuration and input validation
                  ↓
Generated title-card intro
                  ↓
Resolution normalization + fade processing
                  ↓
Intro and sermon concatenation
                  ↓
CD-ready WAV export
                  ↓
Upload-ready package
```

## What the Project Demonstrates

- YAML configuration loaded by the executable script
- Portable relative folders instead of production-specific paths
- Latest-recording discovery across common video formats
- Dry-run validation before large media processing
- FFmpeg and FFprobe command construction
- Generated title-card intro without copyrighted artwork
- Resolution normalization, padding, and audio/video fades
- WAV extraction and upload-ready packaging
- Explicit errors and independently testable functions

## Repository Contents

| Path | Description |
|---|---|
| `scripts/sermon_automation_sample.py` | Config-driven dry-run and execution workflow |
| `config/config.example.yaml` | Public-safe example configuration |
| `tests/test_sermon_automation.py` | Tests for discovery, naming, and commands |
| `docs/workflow.md` | End-to-end processing explanation |
| `requirements.txt` | Python dependencies |

## Validation

```bash
python -m unittest discover -s tests
```

The tests do not process media. They validate naming, latest-file selection, configuration, and command construction.

## Privacy and Copyright Scope

This repository contains no real recordings, transcripts, copyrighted artwork, upload credentials, production paths, or private organizational records.
