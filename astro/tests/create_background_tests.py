from nose.tools import *
import numpy as np
import cv2

def convert_and_save_test():
    cap = cv2.VideoCapture('/home/jorge/Documents/2-Programming/astro/docs/background/IMG_0011.MOV')
    fps = cap.get(cv2.CAP_PROP_FPS)
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter('/home/jorge/Documents/2-Programming/astro/docs/background/background.avi', fourcc, fps*2, (640,480))
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            resized = cv2.resize(frame, (640,480), interpolation = cv2.INTER_AREA)
            out.write(resized)
            cv2.imshow("frame", resized)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()
