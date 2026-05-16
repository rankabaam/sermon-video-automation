**# sermon-video-automation
A Python and FFmpeg workflow for preparing sermon video, thumbnail, and audio outputs.
**# Sermon Video Automation

A Python and FFmpeg workflow concept for preparing weekly sermon media outputs.

## Overview

Sermon Video Automation is a practical media workflow project designed to reduce repetitive post-production work for weekly church sermon recordings.

The project demonstrates how a recorded sermon video can be processed into organized output files for YouTube upload, thumbnail use, and CD audio preparation.

## Problem

Weekly sermon media production often involves repeated manual steps, including:

- Finding the latest recording
- Creating or applying a thumbnail intro
- Adding fade-in and fade-out transitions
- Exporting a final YouTube-ready video
- Creating a separate audio file
- Organizing completed files into consistent folders

Doing these steps manually can be time-consuming and inconsistent, especially when the workflow is repeated every week.

## Solution

This project demonstrates a workflow that:

- Detects the latest sermon recording
- Creates organized output folders
- Generates a final sermon video
- Adds a thumbnail intro
- Applies basic fade-in and fade-out transitions
- Exports a CD-ready audio file
- Copies final media into a YouTube-ready folder

## Sample Workflow

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
