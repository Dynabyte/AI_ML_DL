import os
import numpy as np
import cv2

filename = 'video.mp4' # .avi .mp4

cap = cv2.VideoCapture(0)
frames_per_seconds = 24.0
my_res = '720p' #1080p

def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)


# Standard Video Dimensions Sizes
STD_DIMENSIONS = {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (2840, 2160),
}

def get_dims(cap, res='1080p'):
    width, height = STD_DIMENSIONS['480p']
    if res in STD_DIMENSIONS:
        width, height = STD_DIMENSIONS[res]
    change_res(cap, width, height)
    return width, height

# Video Encoding, might require additional installs
# Types of Codes: http://www.fourcc.org/codecs.php
VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    #'mp4': cv2.VideoWriter_fourcc(*'H264'),
    'mp4': cv2.VideoWriter_fourcc(*'MPEG'),
}

def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
      return  VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']


def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)


dims = get_dims(cap, res=my_res)
video_type_cv2 = get_video_type(filename)


# To save a grayscale video in Windows 10 and Python 3.7,
# I added the clause "isColor=False" when constructing the following line:
# "out = cv2.VideoWriter(filename, video_type_cv2, fps, my_res, isColor=False)".
# Worked like a charm! #
out = cv2.VideoWriter(filename, video_type_cv2, frames_per_seconds, dims)

while True:
    ret, frame = cap.read()
    out.write(frame)

    frame = rescale_frame(frame, percent=100)

    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('gray', gray)


    cv2.imshow('frame', frame) #imshow

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

#When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()