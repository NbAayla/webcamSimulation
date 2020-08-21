import argparse
import cv2
from subprocess import Popen, PIPE
import numpy as np
import os
import time

args = argparse.ArgumentParser("Emulate a webcam through a list of video or image files")
args.add_argument("video_device", help="/dev/video device to write output to")
args.add_argument("--resolution", "-r", help="resolution of webcam output (default is 1280x720)", default="1280x720")
args.add_argument("--loop", "-l", help="replay the files forever as a constant webcam", action="store_true")
args.add_argument("input_files", nargs="+", help="video files to simulate the webcam with")
args = args.parse_args()

# Test that a proper resolution was provided and create the outputRes variable
assert "x" in args.resolution
outputRes = [int(res) for res in args.resolution.split("x")[:2]]
# Test that provided videos exist
for file in args.input_files:
    assert os.path.exists(file)
# Test that the provided /dev/video file exists
assert os.path.exists(args.video_device)

# ffmpeg command to take raw video (numpy arrays provided through stdin pipe as bytes) and format it into YUV 4:2:2 that
# can be read by programs that read webcams
p = Popen(['ffmpeg', '-loglevel', 'panic', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', args.resolution, '-i',
           '-', '-pix_fmt', 'yuyv422', '-f', 'v4l2', args.video_device], stdin=PIPE)

if len(args.input_files) == 1:
    inputFile = cv2.VideoCapture(args.input_files[0])
    # cv2.CAP_PROP_FRAME_COUNT doesn't work, so this crude solution will have to work
    frames = []
    while inputFile.isOpened():
        ret, frame = inputFile.read()
        if frame is None or len(frames) > 1:
            break
        frames.append(frame)
    if len(frames) == 1:
        print("Input is a single frame. Storing in memory.")
        # Store frame in memory
        frame = cv2.resize(frames[0], (outputRes[0], outputRes[1])).tobytes()
        while True:
            # Display frame at 1fps
            p.stdin.write(frame)
            time.sleep(1)
while True:
    for file in args.input_files:
        print(f"Opening file {file}")
        # Load the file and get its framerate so it can be fed at the correct speed
        inputVideo = cv2.VideoCapture(file)
        framerate = inputVideo.get(cv2.CAP_PROP_FPS)
        # Clear time array between files
        timeArray = np.array([0])
    # Loop through the video file
        while inputVideo.isOpened():
            # Record the time each frame starts processing
            startTime = time.time()
            ret, frame = inputVideo.read()
            if frame is None:
                break
            # Resize the frame to the correct output and write it to p.stdin
            frame = cv2.resize(frame, (outputRes[0], outputRes[1]))
            p.stdin.write(frame.tobytes())

            # Add delta T to the array of times taken for frames to process
            timeArray = np.append(timeArray, time.time() - startTime)

            # By sleeping by the hypothetical perfect framerate minus the average delta T for frame processing,
            # the framerate of the fake "webcam" should get more accurate to the source file the longer it plays
            # for. This array is cleared to prevent any excess memory use or time spent calculating the average
            # and because different files may require different amounts of time to process their frames depending
            # on factors such as codec, resolution, pixel format, etc.

            sleep = (1/framerate) - timeArray.mean()
            if sleep > 0:
                time.sleep(sleep)
    # Break the loop if the user did not request a constant feed
    if not args.loop:
        break
