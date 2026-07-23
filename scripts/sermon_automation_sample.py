"""Config-driven public demo for recurring sermon-media preparation.

Dry-run is the default. Use --execute only with authorized media.
"""
from __future__ import annotations
import argparse, logging, shutil, subprocess, sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Iterable
import yaml

VIDEO_EXTENSIONS={'.mkv','.mp4','.mov','.avi'}

@dataclass(frozen=True)
class OutputPaths:
    intro: Path
    normalized_video: Path
    final_video: Path
    audio_wav: Path
    youtube_folder: Path
    youtube_video: Path

def load_config(path: Path)->dict[str,Any]:
    if not path.is_file(): raise FileNotFoundError(f'Configuration not found: {path}')
    data=yaml.safe_load(path.read_text(encoding='utf-8'))
    if not isinstance(data,dict): raise ValueError('Configuration root must be a mapping.')
    return data

def find_latest_recording(folder: Path)->Path:
    if not folder.is_dir(): raise FileNotFoundError(f'Recording folder not found: {folder}')
    items=[p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in VIDEO_EXTENSIONS]
    if not items: raise FileNotFoundError(f'No supported video files found in: {folder}')
    return max(items,key=lambda p:p.stat().st_mtime)

def build_output_paths(root:Path,service_date:date,config:dict[str,Any])->OutputPaths:
    naming=config['naming']; completed=root/config['folders']['completed']; working=root/config['folders']['working']
    base=f"{service_date.strftime(naming['date_format'])}_{naming['sermon_slug']}"; youtube=completed/'YouTube_Ready'/base
    return OutputPaths(working/'intro'/f'{base}_intro.mp4',working/'normalized'/f'{base}_normalized.mp4',completed/'Sermon_Video'/f"{base}_{naming['final_video_suffix']}.mp4",completed/'CD_Audio_WAV'/f"{base}_{naming['audio_suffix']}.wav",youtube,youtube/config['youtube_ready']['final_video_name'])

def ensure_directories(paths:OutputPaths)->None:
    for p in (paths.intro.parent,paths.normalized_video.parent,paths.final_video.parent,paths.audio_wav.parent,paths.youtube_folder): p.mkdir(parents=True,exist_ok=True)

def check_tool(name:str)->None:
    if shutil.which(name) is None: raise RuntimeError(f'Required executable is not available on PATH: {name}')

def run_command(command:list[str],execute:bool)->None:
    logging.info('%s',subprocess.list2cmdline(command))
    if execute:
        result=subprocess.run(command,check=False)
        if result.returncode: raise RuntimeError(f'Command failed ({result.returncode}): {command[0]}')

def probe_duration(video:Path)->float:
    result=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(video)],check=True,capture_output=True,text=True)
    return float(result.stdout.strip())

def escape_drawtext(value:str)->str:
    return value.replace('\\','\\\\').replace(':','\\:').replace("'","\\'")

def build_intro_command(paths:OutputPaths,service_date:date,config:dict[str,Any])->list[str]:
    v=config['video']; w,h=map(int,v['output_resolution'].split('x')); duration=float(v['intro_duration_seconds']); fade=float(v['fade_out_seconds'])
    title=escape_drawtext(config['project']['display_title']); d=escape_drawtext(service_date.isoformat())
    vf=f"drawtext=text='{title}':fontcolor=white:fontsize=64:x=(w-text_w)/2:y=(h-text_h)/2-40,drawtext=text='{d}':fontcolor=white:fontsize=36:x=(w-text_w)/2:y=(h-text_h)/2+50,fade=t=in:st=0:d={v['fade_in_seconds']},fade=t=out:st={max(0,duration-fade)}:d={fade},format=yuv420p"
    return ['ffmpeg','-y','-f','lavfi','-i',f'color=c=#17375e:s={w}x{h}:d={duration}','-f','lavfi','-i','anullsrc=channel_layout=stereo:sample_rate=48000','-vf',vf,'-shortest','-c:v',v['video_codec'],'-preset',v['preset'],'-crf',str(v['crf']),'-c:a',v['audio_codec'],'-b:a',v['audio_bitrate'],str(paths.intro)]

def build_normalize_command(source:Path,destination:Path,duration:float,config:dict[str,Any])->list[str]:
    v=config['video']; w,h=map(int,v['output_resolution'].split('x')); fi=float(v['fade_in_seconds']); fo=float(v['fade_out_seconds']); start=max(0,duration-fo)
    vf=f'scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2,fade=t=in:st=0:d={fi},fade=t=out:st={start}:d={fo},format=yuv420p'; af=f'afade=t=in:st=0:d={fi},afade=t=out:st={start}:d={fo}'
    return ['ffmpeg','-y','-i',str(source),'-vf',vf,'-af',af,'-c:v',v['video_codec'],'-preset',v['preset'],'-crf',str(v['crf']),'-c:a',v['audio_codec'],'-b:a',v['audio_bitrate'],str(destination)]

def write_concat_list(path:Path,inputs:Iterable[Path])->None:
    path.write_text('\n'.join(f"file '{p.resolve().as_posix()}'" for p in inputs)+'\n',encoding='utf-8')

def build_concat_command(concat_list:Path,output:Path)->list[str]:
    return ['ffmpeg','-y','-f','concat','-safe','0','-i',str(concat_list),'-c','copy',str(output)]

def build_audio_command(final_video:Path,output:Path,config:dict[str,Any])->list[str]:
    a=config['audio']; return ['ffmpeg','-y','-i',str(final_video),'-vn','-acodec',a['codec'],'-ar',str(a['sample_rate']),'-ac',str(a['channels']),str(output)]

def process(root:Path,config_path:Path,service_date:date,source:Path|None,execute:bool)->OutputPaths:
    config=load_config(config_path); paths=build_output_paths(root,service_date,config); ensure_directories(paths); recordings=root/config['folders']['obs_recordings']
    source_video=source or (find_latest_recording(recordings) if execute else recordings/'sample_recording.mp4')
    if execute:
        check_tool('ffmpeg'); check_tool('ffprobe')
        if not source_video.is_file(): raise FileNotFoundError(f'Input video not found: {source_video}')
        duration=probe_duration(source_video)
    else: duration=float(config['demo']['synthetic_duration_seconds'])
    run_command(build_intro_command(paths,service_date,config),execute); run_command(build_normalize_command(source_video,paths.normalized_video,duration,config),execute)
    concat=paths.normalized_video.parent/'concat.txt'; write_concat_list(concat,[paths.intro,paths.normalized_video]); run_command(build_concat_command(concat,paths.final_video),execute); run_command(build_audio_command(paths.final_video,paths.audio_wav,config),execute)
    if execute and config['youtube_ready']['copy_final_video']:
        paths.youtube_folder.mkdir(parents=True,exist_ok=True); shutil.copy2(paths.final_video,paths.youtube_video)
    return paths

def main()->int:
    parser=argparse.ArgumentParser(); parser.add_argument('--root',type=Path,default=Path('.')); parser.add_argument('--config',type=Path,default=Path('config/config.example.yaml')); parser.add_argument('--date',type=date.fromisoformat,default=date.today()); parser.add_argument('--input',type=Path); parser.add_argument('--execute',action='store_true'); args=parser.parse_args(); logging.basicConfig(level=logging.INFO,format='%(levelname)s: %(message)s')
    try: paths=process(args.root.resolve(),args.config.resolve(),args.date,args.input.resolve() if args.input else None,args.execute)
    except (FileNotFoundError,KeyError,ValueError,RuntimeError,subprocess.SubprocessError) as exc: logging.error('%s',exc); return 1
    logging.info('Final video: %s',paths.final_video); logging.info('Audio WAV: %s',paths.audio_wav); return 0

if __name__=='__main__': sys.exit(main())
