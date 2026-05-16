# FFmpeg Process

This document describes the general FFmpeg processing concept used in the Sermon Video Automation project.

The commands shown here are examples for portfolio documentation and demonstration purposes.

## Purpose

FFmpeg is used to automate repeated video and audio processing tasks for weekly sermon media preparation.

The goal is to keep output settings consistent and reduce manual editing work.

## Main Processing Goals

The automation workflow may include:

- Detecting the sermon recording file
- Adding a thumbnail intro
- Applying fade-in and fade-out transitions
- Exporting a final MP4 video
- Extracting a separate WAV audio file
- Preparing files for YouTube upload

## Example Final Video Command

A simplified example command may look like this:

```bash
ffmpeg -i input_sermon.mp4 \
  -c:v libx264 \
  -crf 18 \
  -preset medium \
  -c:a aac \
  -b:a 192k \
  output_final.mp4
```

## Example Audio Export Command

A separate WAV audio file can be extracted from the sermon video:

```bash
ffmpeg -i input_sermon.mp4 \
  -vn \
  -acodec pcm_s16le \
  -ar 44100 \
  -ac 2 \
  output_audio.wav
```

## Example Fade-In and Fade-Out Concept

Fade effects can be applied using FFmpeg filters.

Example concept:

```bash
ffmpeg -i input_sermon.mp4 \
  -vf "fade=t=in:st=0:d=1,fade=t=out:st=1799:d=1" \
  -af "afade=t=in:st=0:d=1,afade=t=out:st=1799:d=1" \
  output_with_fades.mp4
```

In a real workflow, the fade-out start time would be calculated based on the actual video duration.

## Example Thumbnail Intro Concept

A still image can be converted into a short video intro and then combined with the sermon recording.

Example thumbnail intro creation:

```bash
ffmpeg -loop 1 -i thumbnail.png \
  -t 3 \
  -vf "scale=1920:1080,format=yuv420p" \
  thumbnail_intro.mp4
```

Example concat workflow concept:

```text
thumbnail_intro.mp4
        +
sermon_body.mp4
        ↓
final_sermon_video.mp4
```

## Output Quality Notes

The sample workflow uses common YouTube-friendly output settings:

| Setting | Example |
|---|---|
| Video codec | `libx264` |
| Quality | `-crf 18` |
| Preset | `medium` |
| Audio codec | `aac` |
| Audio bitrate | `192k` |
| Container | `.mp4` |

## Why FFmpeg

FFmpeg is useful for this workflow because it can:

- Run from a Python script
- Process video and audio consistently
- Avoid repeated manual editing
- Support batch-style automation
- Produce predictable output files

## Portfolio Note

This document contains generalized FFmpeg examples only.

It does not include real sermon recordings, private church media, copyrighted material, or production credentials.
