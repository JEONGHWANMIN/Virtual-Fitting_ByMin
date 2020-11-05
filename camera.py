import cv2
import os
import time
import pygame
from datetime import datetime, timedelta


pygame.mixer.init()
pygame.mixer.music.load('audio/sound.mp3')
count=pygame.mixer.Sound('audio/4second.wav')
count.set_volume(0.3)
period = timedelta(seconds=6)

guide=cv2.imread('./image/guide_3.png',cv2.IMREAD_UNCHANGED)

mask=guide[:,:,3]
guide=guide[:,:,:-1]
h, w = mask.shape[:2]

guide = cv2.resize(guide,(640,480))
mask = cv2.resize(mask,(640,480))

video_capture = cv2.VideoCapture(0)

while(True):
    ret, frame = video_capture.read() 
    frame = cv2.flip(frame,1)
    next_time = datetime.now() + period

    if(cv2.waitKey(1) & 0xFF == ord('q')):
        while(True):
            delta = next_time-datetime.now()
            if(delta.seconds<=6):
                count.play()
                print(delta.seconds+1)
            if(delta.seconds==0):
                count.stop()
                pygame.mixer.music.play()
                path="result"
                cv2.imwrite(os.path.join(path, str(now) + ".png"), frame)
                break
                
    
    cv2.copyTo(guide, mask, frame)
    now = datetime.now().strftime("%d_%H-%M-%S")
    cv2.imshow('Video', frame)
    if(cv2.waitKey(1) == 27): 
        break



video_capture.release()
cv2.destroyAllWindows()
