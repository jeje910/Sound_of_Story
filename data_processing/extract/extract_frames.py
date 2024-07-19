from datetime import timedelta
import cv2
import numpy as np
import os
import sys
import shutil

from imagecluster.imagecluster import calc, io as icio, postproc


# i.e if video of duration 30 seconds, saves 10 frame per second = 300 frames saved in total
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
    # get the clip duration by dividing number of frames by the number of frames per second
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    # use np.arange() to make floating-point steps
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        s.append(i)
    return s

def extract_frames(video_file):
    filename, _ = os.path.splitext(video_file)
    filename = filename.replace('videos', 'frames') + "_frames"
    # make a folder by the name of the video file
    if not os.path.isdir(filename):
        os.mkdir(filename)
    # read the video file
    cap = cv2.VideoCapture(video_file)
    # get the FPS of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    # if the SAVING_FRAMES_PER_SECOND is above video FPS, then set it to FPS (as maximum)
    saving_frames_per_second = min(fps, SAVING_FRAMES_PER_SECOND)
    # get the list of duration spots to save
    saving_frames_durations = get_saving_frames_durations(cap, saving_frames_per_second)
    # start the loop
    count = 0
    while True:
        is_read, frame = cap.read()
        if not is_read:
            # break out of the loop if there are no frames to read
            break
        # get the duration by dividing the frame count by the FPS
        frame_duration = count / fps
        try:
            # get the earliest duration to save
            closest_duration = saving_frames_durations[0]
        except IndexError:
            # the list is empty, all duration frames were saved
            break
        if frame_duration >= closest_duration:
            # if closest duration is less than or equals the frame duration,
            # then save the frame
            frame_duration_formatted = format_timedelta(timedelta(seconds=frame_duration))
            cv2.imwrite(os.path.join(filename, f"frame{frame_duration_formatted}.jpg"), frame)
            # drop the duration spot from the list, since this duration spot is already saved
            try:
                saving_frames_durations.pop(0)
            except IndexError:
                pass
        # increment the frame count
        count += 1


if __name__ == "__main__":
    video_dir = sys.argv[1]
    frames_dir = sys.argv[2]

    clips = os.listdir(video_dir)

    for clip in clips:
        # extract frames from video directory
        clip_dir = video_dir+"/"+clip
        extract_frames(clip_dir)

        # get represent images
        frame_dir = os.path.join(frames_dir, clip[:-4] + "_frames")

        rep_image_list = []

        images, fingerprints, timestamps = icio.get_image_data(frame_dir)
        clusters = calc.cluster(fingerprints, sim=0.5)

        # cluster the image
        cluster_keys = clusters.keys()
        for key in cluster_keys:
            rep_image_list.append(clusters[key][0][0])

        # clean up the files
        outside_directory = frames_dir + "/../" + clip[:-4] + "_frames"
        if not os.path.isdir(outside_directory):
            os.mkdir(outside_directory)

        files = os.listdir(frame_dir)
        for file in files:
            file_name = os.path.join(frame_dir, file)
            dst_name = os.path.join(outside_directory, file)
            if file_name in rep_image_list:
                shutil.copy2(file_name, dst_name)
                continue
            elif file_name[-12:] == "imagecluster":
                continue
            else:
                os.remove(file_name)


