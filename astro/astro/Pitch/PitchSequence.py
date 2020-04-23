
from . import  sequenceTranslator
import numpy as np
import cv2
import random

class Sequence(object):
    def __init__(self,  speed, step):
        self.sequenceNo = random.randrange(1,22)
        self.speed = speed
        self.step = step
        self.hit = False


    def set_sequence(self, sequenceNo = 0):
        self.speed = random.randrange(5,10)
        self.step = self.speed
        self.set_sequence_hit()
        self.hit = False
        if sequenceNo:
            self.sequenceNo =sequenceNo
        else:
            self.sequenceNo =  random.randrange(1,22)
        self.sequence = np.loadtxt("docs/sequences/sequences-" + str(self.sequenceNo)).astype(int)*self.speed
        self.sequence = self.sequence[::self.step]

    def set_sequence_hit(self):
        self.hit_seq_no = random.randrange(1,7)
        self.hit_sequence = np.loadtxt("docs/sequences/return-" + str(self.hit_seq_no)).astype(int)*int(self.speed*.7)
        self.hit_sequence = self.hit_sequence[::self.step]

    def get_size(self):
        if self.hit:
            return len(self.hit_sequence)
        return len(self.sequence)
    def read(self):

        if self.hit:
            return self.hit_sequence
        return self.sequence
    def ball_hit(self):
        self.hit = True
    def read_hit_sequence(self):
        return self.hit_sequence
