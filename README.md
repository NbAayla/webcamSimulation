# webcamSimulation

A Python program that uses [v4l2loopback](https://github.com/umlaeute/v4l2loopback), [OpenCV](https://opencv.org), and [ffmpeg](https://ffmpeg.org) to use video files as a fake webcam usable in programs like Zoom and Microsoft Teams.

## Usage
1. Install the requirements with ``pip install -r requirements.txt``
2. Run the script with ``python3 main.py [ARGUMENTS]``

### Arguments
This information can also be accessed with the ``-h`` argument.
```
usage: Emulate a webcam through a list of video or image files
       [-h] video_device input_files [input_files ...]

positional arguments:
  video_device  /dev/video device to write output to
  input_files   video files to simulate the webcam with

optional arguments:
  -h, --help    show this help message and exit
```
