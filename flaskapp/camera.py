import cv2
import os
import time
import pygame
from datetime import datetime, timedelta

guide=cv2.imread('./static/images/guide_3.png',cv2.IMREAD_UNCHANGED)

mask=guide[:,:,3]
guide=guide[:,:,:-1]
h, w = mask.shape[:2]

guide = cv2.resize(guide,(640,480))
mask = cv2.resize(mask,(640,480))

class VideoCamera(object):
    def __init__(self):
       #capturing video
       self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    def __del__(self):
        #releasing camera
        self.video.release()

    def capture_frame(self):
        ret, frame = self.video.read()
        return frame

    def get_frame(self):
        ret, frame = self.video.read() 
        frame = cv2.flip(frame,1)
        cv2.copyTo(guide, mask, frame)

        ret, jpeg = cv2.imencode('.jpeg', frame)
        return jpeg.tobytes()