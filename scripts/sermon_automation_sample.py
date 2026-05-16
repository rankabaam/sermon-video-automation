"""
Sermon Video Automation - Sample Script

This is a sanitized portfolio demo script.

It demonstrates the general structure of a Python + FFmpeg workflow for:
- finding the latest sermon recording
- preparing output folders
- building consistent output file names
- generating example FFmpeg commands
- organizing YouTube-ready output paths

This script does not include real sermon recordings, private church data,
production credentials, or copyrighted media.
"""

from pathlib import Path
from datetime import date


PROJECT_ROOT = Path("Church_Sermon_Automation")

FOLDERS = {
    "obs_recordings": PROJECT_ROOT / "00_OBS_Recordings",
    "inbox": PROJECT_ROOT / "01_Inbox",
    "working": PROJECT_ROOT / "02_Working",
    "completed": PROJECT_ROOT / "03_Completed",
}

OUTPUT_FOLDERS = {
    "sermon_video": FOLDERS["completed"] / "Sermon_Video",
    "cd_audio_wav": FOLDERS["completed"] / "CD_Audio_WAV",
    "thumbnail_image": FOLDERS["completed"] / "Thumbnail_Image",
    "youtube_ready": FOLDERS["completed"] / "YouTube_Ready",
}


def ensure_folders() -> None:
    """Create the sample folder structure if it does not already exist."""
    for folder in FOLDERS.values():
        folder.mkdir(parents=True, exist_ok=True)

    for folder in OUTPUT_FOLDERS.values():
        folder.mkdir(parents=True, exist_ok=True)


def find_latest_recording(recording_folder: Path) -> Path | None:
    """
    Find the latest MP4 recording in the recording folder.

    In a real workflow, this would search the OBS recording folder.
    This sample function only demonstrates the concept.
    """
    video_files = list(recording_folder.glob("*.mp4"))

    if not video_files:
        return None

    return max(video_files, key=lambda file: file.stat().st_mtime)


def build_output_paths(service_date: date) -> dict[str, Path]:
    """Build consistent output file names for sermon media."""
    date_prefix = service_date.strftime("%Y-%m-%d")
    sermon_slug = "sunday_sermon"

    final_video_name = f"{date_prefix}_{sermon_slug}_final.mp4"
    audio_name = f"{date_prefix}_{sermon_slug}_cd.wav"
    thumbnail_name = f"{date_prefix}_{sermon_slug}_thumbnail.png"

    youtube_folder = OUTPUT_FOLDERS["youtube_ready"] / f"{date_prefix}_{sermon_slug}"

    return {
        "final_video": OUTPUT_FOLDERS["sermon_video"] / final_video_name,
        "audio_wav": OUTPUT_FOLDERS["cd_audio_wav"] / audio_name,
        "thumbnail": OUTPUT_FOLDERS["thumbnail_image"] / thumbnail_name,
        "youtube_folder": youtube_folder,
        "youtube_video": youtube_folder / "final.mp4",
        "youtube_thumbnail": youtube_folder / "thumbnail.png",
    }


def build_final_video_command(input_video: Path, output_video: Path) -> list[str]:
    """
    Build an example FFmpeg command for final video export.

    This command is shown for demonstration and documentation purposes.
    """
    return [
        "ffmpeg",
        "-i", str(input_video),
        "-c:v", "libx264",
        "-crf", "18",
        "-preset", "medium",
        "-c:a", "aac",
        "-b:a", "192k",
        str(output_video),
    ]


def build_audio_export_command(input_video: Path, output_audio: Path) -> list[str]:
    """Build an example FFmpeg command for WAV audio export."""
    return [
        "ffmpeg",
        "-i", str(input_video),
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "44100",
        "-ac", "2",
        str(output_audio),
    ]


def print_command(command: list[str]) -> None:
    """Print an FFmpeg command in a readable format."""
    print(" ".join(command))


def main() -> None:
    """Run the sample automation workflow in dry-run mode."""
    print("Sermon Video Automation - Sample Dry Run")
    print("----------------------------------------")

    ensure_folders()

    latest_recording = find_latest_recording(FOLDERS["obs_recordings"])

    if latest_recording is None:
        latest_recording = Path("sample_input_sermon.mp4")
        print("No real recording found.")
        print(f"Using sample input placeholder: {latest_recording}")
    else:
        print(f"Latest recording found: {latest_recording}")

    output_paths = build_output_paths(date.today())
    output_paths["youtube_folder"].mkdir(parents=True, exist_ok=True)

    print("\nPlanned Output Files:")
    for label, path in output_paths.items():
        print(f"- {label}: {path}")

    print("\nExample FFmpeg Final Video Command:")
    final_video_command = build_final_video_command(
        latest_recording,
        output_paths["final_video"],
    )
    print_command(final_video_command)

    print("\nExample FFmpeg Audio Export Command:")
    audio_command = build_audio_export_command(
        latest_recording,
        output_paths["audio_wav"],
    )
    print_command(audio_command)

    print("\nDry run complete.")
    print("This sample script does not process real media files by default.")


if __name__ == "__main__":
    main()
