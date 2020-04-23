from nose.tools import *
import astro
import numpy as np
import cv2

def initiate_test():

    """
    ******************initiate sequence object**************************
    Type is an argument that will be passed in the console or that can be
    randomly chosen and can be chosen from the dictionary
    """
    type = "PROTOTYPE"
    origin = (0, 0)

    pitch = Pitch.Sequence(type, origin)

    eq_(pitch.type, 0)

def getSequence_test():
    """ check origin"""
    h, w = 250,300
    window = np.zeros((h,w,3), np.uint8)
    type = "PROTOTYPE"
    origin = (w/2, h/2)
    pitch = Pitch.Sequence(type, origin)
    sequence = pitch.get_sequence()

def renderBall_test():
    """ visualize sequence on screen"""

    #*********Create sequence*************
    h, w = 250,300
    window = np.zeros((h,w,3), np.uint8)
    type = "PROTOTYPE"
    origin = (w/2-100, h/2-100)
    pitch = Pitch.Sequence(type, origin)
    pitch.get_sequence()

    #*************render sequence***************

    cv2.namedWindow('frame',cv2.WINDOW_NORMAL)

    for s in range(0, pitch.duration):
        if s == 1:
            cv2.waitKey(5000)
        else:
            cv2.imshow('frame',pitch.renderTrajectory(instant = s))
            cv2.waitKey(25)
    cv2.destroyAllWindows()

def get_sequence_test():
    # sequence = np.loadtxt('docs/sequences/sequences-3').astype(int)*10
    # sequence = sequence[::5]
    # limit = len(sequence)
    # count = 0
    speed = 10
    step = 5
    sequenceObject = astro.Sequence(3, speed, step)
    sequence = sequenceObject.get_sequence()
    size = sequenceObject.get_size()

    # Load sequence
    sequence2 = np.loadtxt('docs/sequences/sequences-3').astype(int)*10
    sequence2 = sequence2[::5]
    limit = len(sequence)
    count = 0
    np.testing.assert_array_equal(sequence2, sequence)
