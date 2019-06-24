import picamera
import picamera.array
import cv2 as cv
import numpy as np
import time
from threading import Thread

def get_frames():
    with picamera.PiCamera() as cam:
        global recent_frame
        cam.resolution = (352, 352) 
        with picamera.array.PiRGBArray(cam) as raw:
            for frame in cam.capture_continuous(raw, 'bgr', use_video_port=True):
                recent_frame = raw.array
                raw.truncate(0)

frm_thread = Thread(target=get_frames, args=())
frm_thread.start()

frames = 0
det = cv.createLineSegmentDetector()

global low
global high

low = 65
high = 76

def change_l_threshold():
    return

def change_h_threshold():
    return
    
cv.namedWindow('Canny Threshold Control')

cv.createTrackbar('Threshold Limit 1', 'Canny Threshold Control', 75, 500,
                  change_l_threshold)

cv.createTrackbar('Threshold Limit 2', 'Canny Threshold Control', 140, 500,
                  change_h_threshold)

time.sleep(1)

while True:
    try:
        low = cv.getTrackbarPos('Threshold Limit 1', 'Threshold Control')
        high = cv.getTrackbarPos('Threshold Limit 2', 'Threshold Control')
        
        current_frame = cv.cvtColor(recent_frame, cv.COLOR_BGR2GRAY)
        edge_img = cv.Canny(current_frame, low, high)

        empty = np.zeros(current_frame.shape, current_frame.dtype)
        lines = det.detect(current_frame)[0]
        line_img = det.drawSegments(empty, lines)
        
        cv.imshow('Edge Output', edge_img)
        cv.imshow('BGR Output', recent_frame)
        cv.imshow('Line Output', line_img)
        cv.waitKey(1)

        frames += 1
        
    except KeyboardInterrupt:
        cv.destroyAllWindows()
        break
