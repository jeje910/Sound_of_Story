import subprocess
import os
import sys
import re

def convert_video_to_audio_ffmpeg(video_file, output_ext="wav", year=2014):
    """Converts video to audio directly using `ffmpeg` command
    with the help of subprocess module"""
    filename, ext = os.path.splitext(video_file)
    
    if not os.path.exists("../data/audio_files"):
        os.makedirs("../data/audio_files")
    dst_path = os.path.join("../data/audio_files", filename.split('/')[2])
    subprocess.call(["ffmpeg", "-y", "-i", video_file, f"{dst_path}.{output_ext}"], 
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)

if __name__ == "__main__":
    
    vf = sys.argv[1]
    clips = os.listdir(vf)
    
    for clip in clips:
        clip = vf+"/"+clip
        print("converting ", clip)
        convert_video_to_audio_ffmpeg(clip)

