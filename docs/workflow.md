# Workflow

This document describes the general workflow concept behind the Sermon Video Automation project.

## Purpose

The Sermon Video Automation project is designed to reduce repetitive manual work in weekly church media production.

The goal is to take a recorded sermon video and prepare organized output files for YouTube upload, thumbnail use, and audio distribution.

## General Workflow

```text
OBS Recording
      ↓
Inbox Folder
      ↓
Python Automation Script
      ↓
FFmpeg Processing
      ↓
Final Video Output
      ↓
Audio Output
      ↓
YouTube Ready Folder
```

## Step 1: Recording Is Created

The workflow begins with a sermon recording created by OBS or another recording system.

The recording is placed into an input folder for processing.

## Step 2: Latest Recording Is Selected

The automation script identifies the latest available recording file.

This helps reduce the need to manually search through multiple recorded files.

## Step 3: Output Folders Are Prepared

The script creates or updates organized output folders for completed media files.

Example folders may include:

- Final sermon video
- CD audio output
- Thumbnail image
- YouTube-ready package

## Step 4: Video Processing

FFmpeg is used to process the video.

The processing workflow may include:

- Adding a thumbnail intro
- Applying fade-in and fade-out transitions
- Exporting a final MP4 video
- Keeping output settings consistent between weeks

## Step 5: Audio Export

A separate audio file can be exported from the sermon recording.

This may be used for CD preparation, archiving, or other audio distribution workflows.

## Step 6: YouTube-Ready Folder

The final video and thumbnail image are copied into a dedicated YouTube-ready folder.

This helps make the upload process more consistent and reduces the chance of selecting the wrong file.

## Operational Value

This workflow is intended to reduce repetitive post-production work and improve consistency in weekly sermon media preparation.

The project demonstrates how Python and FFmpeg can be used to automate a recurring media workflow with predictable output structure.

## Privacy and Data Handling

This repository uses documentation and sample structures only.

No real sermon recordings, private church data, personal information, copyrighted media, or production credentials are included.
