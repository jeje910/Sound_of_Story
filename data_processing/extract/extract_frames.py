from datetime import timedelta
import os
import ast
import sys
import cv2
import json
import copy
import numpy as np

SAVING_FRAMES_PER_SECOND = 10

def format_timedelta(td):
    """Utility function to format timedelta objects in a cool way (e.g 00:00:20.05)
    omitting microseconds and retaining milliseconds"""
    result = str(td)
    try:
        result, ms = result.split(".")
    except ValueError:
        return result + ".00".replace(":", "-")
    ms = int(ms)
    ms = round(ms / 1e4)
    return f"{result}.{ms:02}".replace(":", "-")


def get_saving_frames_durations(cap, saving_fps):
    """A function that returns the list of durations where to save the frames"""
    s = []
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        s.append(i)
    return s

def extract_frames(video_file):
    filename, _ = os.path.splitext(video_file)
    filename = filename.replace('videos', 'frames') + "_frames"
    dst_path = '../data/frames'
    filename = os.path.join(dst_path, filename.split('/')[2])
    if not os.path.exists(filename):
        os.makedirs(filename)
    cap = cv2.VideoCapture(video_file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    saving_frames_per_second = min(fps, SAVING_FRAMES_PER_SECOND)
    saving_frames_durations = get_saving_frames_durations(cap, saving_frames_per_second)
    count = 0
    while True:
        is_read, frame = cap.read()
        if not is_read:
            break
        frame_duration = count / fps
        try:
            closest_duration = saving_frames_durations[0]
        except IndexError:
            break
        if frame_duration >= closest_duration:
            frame_duration_formatted = format_timedelta(timedelta(seconds=frame_duration))
            cv2.imwrite(os.path.join(filename, f"frame{frame_duration_formatted}.jpg"), frame)
            try:
                saving_frames_durations.pop(0)
            except IndexError:
                pass
        count += 1



def main(dir_path):
    
    json_data = []
    movie_names = []
    with open("../data/data.jsonl", "r") as file:
        for line in file:
            json_data.append(json.loads(line))
            movie_names.append(ast.literal_eval(line)['Movie'])
            
    for video in sorted(os.listdir(dir_path)):
        video_path = os.path.join(dir_path, video)
        extract_frames(video_path)
        frame_num = json_data[movie_names.index(video[:-4])]['Frames']
        dst_dir = os.path.join('../data/frames', video[:-4]+"_frames")
        for frame in sorted(os.listdir(dst_dir)):
            if frame == "frame0:00:00.00.jpg":
                temp = copy.deepcopy(frame)
                frame = "frame0-00-00.00.jpg"
                os.rename(os.path.join(dst_dir, temp), os.path.join(dst_dir, frame))
            if not frame in frame_num:
                os.remove(os.path.join(dst_dir, frame))

if __name__ == "__main__":
    dir_path = sys.argv[1]
    main(dir_path)