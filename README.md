# Sermon Video Automation

A sanitized Python and FFmpeg workflow for reducing repetitive weekly sermon-media production work.

## Overview

This project demonstrates how a recurring media workflow can be structured around consistent input discovery, file naming, video processing, audio export, thumbnail preparation, and upload-ready output organization.

## What the Project Demonstrates

- Detecting the newest recording from an input folder
- Creating repeatable working and output directories
- Building standardized output names from a service date
- Generating FFmpeg commands for video and audio processing
- Separating configuration from execution logic
- Supporting dry-run validation before processing large media files
- Designing privacy-safe automation around real recurring operations

## Generalized Workflow

```text
Recording source
      ↓
Input validation
      ↓
Working folder preparation
      ↓
Video processing and transitions
      ↓
Audio export
      ↓
Thumbnail and metadata preparation
      ↓
Upload-ready output package
```

## Repository Contents

| Path | Description |
|---|---|
| `scripts/sermon_automation_sample.py` | Sanitized Python dry-run example |
| `config/config.example.yaml` | Public-safe processing configuration |
| `docs/workflow.md` | End-to-end workflow description |
| `docs/file_structure.md` | Folder and output organization |
| `docs/ffmpeg_process.md` | Generalized FFmpeg processing notes |
| `samples/sample_output_structure.txt` | Example output layout |

## Portfolio Scope

This repository excludes real recordings, copyrighted media, private organization data, credentials, production paths, and upload account details. The sample code focuses on reusable workflow structure rather than production-specific content.

## Current Portfolio Direction

Planned public-safe improvements include:

- Reading the YAML configuration directly from the sample script
- Subprocess execution with explicit dry-run and production-safe modes
- Input and output validation
- Better error handling and process logging
- Synthetic thumbnail and intro-card examples
- Automated tests for naming and folder-generation logic
