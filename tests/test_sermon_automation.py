from datetime import date
from pathlib import Path
import os, tempfile, unittest
from scripts.sermon_automation_sample import build_audio_command, build_intro_command, build_normalize_command, build_output_paths, find_latest_recording, load_config

ROOT=Path(__file__).resolve().parents[1]
CONFIG=load_config(ROOT/'config/config.example.yaml')

class SermonAutomationTests(unittest.TestCase):
    def test_output_naming(self):
        paths=build_output_paths(Path('/tmp/demo'),date(2026,7,23),CONFIG)
        self.assertTrue(paths.final_video.name.endswith('_final.mp4'))
        self.assertEqual(paths.audio_wav.name,'2026-07-23_sunday_sermon_cd.wav')
        self.assertEqual(paths.youtube_video.name,'final.mp4')

    def test_latest_recording(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder); older=root/'older.mp4'; newer=root/'newer.mkv'; ignored=root/'notes.txt'
            for item in (older,newer,ignored): item.write_text('x')
            old_time=older.stat().st_mtime-20; os.utime(older,(old_time,old_time))
            self.assertEqual(find_latest_recording(root),newer)

    def test_commands_use_configured_codecs(self):
        paths=build_output_paths(Path('/tmp/demo'),date(2026,7,23),CONFIG)
        self.assertIn('libx264',build_intro_command(paths,date(2026,7,23),CONFIG))
        self.assertIn('libx264',build_normalize_command(Path('input.mp4'),paths.normalized_video,60.0,CONFIG))
        self.assertIn('pcm_s16le',build_audio_command(paths.final_video,paths.audio_wav,CONFIG))

if __name__=='__main__': unittest.main()
