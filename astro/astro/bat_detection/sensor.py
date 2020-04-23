
from . import calibrate
import cv2
import numpy as np
calibrate = calibrate.calibrate

class Sensor():
    def __init__(self, cap, location):
        """Function that returns the mean value and the sigma value used during runtime,

        args:
        cap: cv2.videoCapture object """

        #cv2.videoCapture object
        self.cap = cap

        self.frame_width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) - 1
        self.frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) - 1

        #sensor location
        self.location = location
        [self.x, self.y, self.h, self.w] = location
        self.adjust_position()

        #calibrate calibrate sensor
        print("calibrating...")

        self.mean, self. sigma =  calibrate(cap, location)

        #set previous frame for future use
        ret, frame = cap.read()
        self.get_frame(frame)

        #kernel for bitwise_xor
        self.kernel = np.ones((5,5), np.uint8)

        #activate
        self.status = True

    def calibrate_sensor(self):
        """in case the camera has been moved"""

        #calibrate calibrate sensor
        self.mean, self. sigma =  calibrate(cap, self.location)

    def get_frame(self, frame):
        """function that reads the image and returns its processed version"""
        frame = self.process_frame(frame)
        self.previous = frame

    def process_frame(self, frame):
        """Function that returns that processes the frame and returns the -window-"""
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.GaussianBlur(frame, (7,7),  0)
        self.adjust_position()
        return frame[self.y:self.y+self.h,self.x:self.x+self.w]

    def is_active(self, frame):
        """return True if the sensor is activated"""

        #get previous and present window to compute their diference value
        self.present =  self.process_frame(frame)
        difference = np.sum(cv2.erode( cv2.bitwise_xor(self.present,self.previous), self.kernel, iterations=2))

        #evaluate if the difference value is between range
        if (self.mean + (6 * self.sigma)) > difference > (self.mean - (6* self.sigma)):
            #difference is within normal range
            return False and self.status
        else:
            #difference is out of range so Active
            return True and self.status
    def adjust_position(self):
        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        if (self.x+self.w) > self.frame_width:
            self.x = self.frame_width - self.w
        if (self.y+self.h) > self.frame_height:
            self.y = self.frame_height - self.h

#68 and 71, added differenc e in return
