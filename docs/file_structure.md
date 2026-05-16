# File Structure

This document describes the sample folder structure used by the Sermon Video Automation project.

The structure is designed to keep weekly sermon media outputs organized and predictable.

## Example Project Structure

```text
sermon-video-automation/
├── README.md
├── docs/
│   ├── workflow.md
│   ├── file_structure.md
│   └── ffmpeg_process.md
├── config/
│   └── config.example.yaml
├── scripts/
│   └── sermon_automation_sample.py
└── samples/
    └── sample_output_structure.txt
```

## Example Working Folder Structure

A production workflow may use folders similar to the following:

```text
Church_Sermon_Automation/
├── 00_OBS_Recordings/
├── 01_Inbox/
├── 02_Working/
└── 03_Completed/
    ├── Sermon_Video/
    ├── CD_Audio_WAV/
    ├── Thumbnail_Image/
    └── YouTube_Ready/
```

## Folder Descriptions

| Folder | Purpose |
|---|---|
| `00_OBS_Recordings/` | Stores original sermon recordings from OBS or another recording system |
| `01_Inbox/` | Holds the recording selected for processing |
| `02_Working/` | Temporary working folder used during processing |
| `03_Completed/Sermon_Video/` | Stores the final sermon video output |
| `03_Completed/CD_Audio_WAV/` | Stores the exported audio file |
| `03_Completed/Thumbnail_Image/` | Stores the generated or selected thumbnail image |
| `03_Completed/YouTube_Ready/` | Stores final upload-ready video and thumbnail files |

## Example Completed Output

```text
03_Completed/
├── Sermon_Video/
│   └── 2026-04-24_sunday_sermon_final.mp4
├── CD_Audio_WAV/
│   └── 2026-04-24_sunday_sermon_cd.wav
├── Thumbnail_Image/
│   └── 2026-04-24_sunday_sermon_thumbnail.png
└── YouTube_Ready/
    └── 2026-04-24_sunday_sermon/
        ├── final.mp4
        └── thumbnail.png
```

## Naming Convention

The sample workflow uses a consistent naming pattern:

```text
YYYY-MM-DD_sunday_sermon_final.mp4
YYYY-MM-DD_sunday_sermon_cd.wav
YYYY-MM-DD_sunday_sermon_thumbnail.png
```

Example:

```text
2026-04-24_sunday_sermon_final.mp4
```

## Portfolio Note

This file structure is a generalized example for portfolio demonstration.

It does not include private church files, real recordings, personal information, copyrighted material, or production credentials.
