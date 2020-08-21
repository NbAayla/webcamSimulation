[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/aaylafetzer/webcamSimulation)
# webcamSimulation

A Python program that uses [v4l2loopback](https://github.com/umlaeute/v4l2loopback), [OpenCV](https://opencv.org), and [ffmpeg](https://ffmpeg.org) to use video files as a fake webcam usable in programs like Zoom and Microsoft Teams.

## Usage
1. Make a new device with ``sudo modprobe v4l2loopback devices=1``
2. Install the requirements with ``pip install -r requirements.txt``
3. Run the script with ``python3 main.py [ARGUMENTS]``

``nowebcam.png`` is included for your personal use if you don't have a webcam but a program requires one to use. To use it:
```shell script
python3 main.py /dev/video0 -l nowebcam.png
```
Replace ``/dev/video0`` with your loopback device. It can be easily found with ``ls /dev/video*``.
### Arguments
This information can also be accessed with the ``-h`` argument.
```
usage: Emulate a webcam through a list of video or image files
       [-h] [--resolution RESOLUTION] [--loop]
       video_device input_files [input_files ...]

positional arguments:
  video_device          /dev/video device to write output to
  input_files           video files to simulate the webcam with

optional arguments:
  -h, --help            show this help message and exit
  --resolution RESOLUTION, -r RESOLUTION
                        resolution of webcam output (default is 1280x720)
  --loop, -l            replay the files forever as a constant webcam
```
