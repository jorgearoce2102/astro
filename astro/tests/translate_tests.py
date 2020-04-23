from nose.tools import *
from astro import Pitch
import numpy as np
import cv2

get_next_direction = Pitch.sequenceTranslator.get_next_direction
create_masks = Pitch.sequenceTranslator.create_masks
directions = Pitch.sequenceTranslator.directions
direction_in_pixels = Pitch.sequenceTranslator.direction_in_pixels
origin = ()
translateInit = False
display = False
count=0

def mouse_event(event, x, y, flags, params):
    global translateInit, origin, display, count
    if event == cv2.EVENT_LBUTTONDOWN:
        origin = (x,y)
        translateInit = True
        display = True
        count = 0
    else:
        pass

def get_next_direction_test():

    global translateInit, origin, x, y

    im = cv2.imread("docs/pitches/pitch-3.png", cv2.IMREAD_GRAYSCALE)
    # imcopy = np.copy(im)
    # im = cv2.bitwise_not(im)
    cv2.namedWindow('Frame',cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("Frame", mouse_event)
    l = 21
    masks = create_masks(l)
    previous_direction = None
    sequence = np.array([], np.uint8)
    while True:


        cv2.imshow("Frame", im)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        if translateInit == True:

            change, new_direction = get_next_direction(im, masks, origin, previous_direction)

            if change:
                previous_direction = new_direction

                # translateInit = False
                cv2.circle(im, origin, 5, 0, 5)
                (x2,y2) = direction_in_pixels[new_direction]
                sequence = np.append(sequence, (x2,y2))
                origin = (origin[0] + x2, origin[1] + y2)

                cv2.waitKey(10)


    cv2.destroyAllWindows
    np.savetxt('sequences', sequence.reshape(int(len(sequence)/2),2),delimiter=',')

def kernels_test():


    im = cv2.imread("docs/pitches/pitch-1.png", cv2.IMREAD_GRAYSCALE)

    origin = (0,0)

    kernels = create_masks()

def get_sequence_of_image_test():

    im = cv2.imread("docs/pitches/pitch-2.png", cv2.IMREAD_GRAYSCALE)
    sequence = Pitch.sequenceTranslator.translateImageToSequence(im, l = 21)
    np.savetxt('docs/sequences-2', sequence.reshape(int(len(sequence)/2),2))

def given_sequence_test():
    global display, origin, count

    sequence = np.loadtxt('docs/sequences/sequences-6').astype(int)*10
    sequence = sequence[::5]
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('Frame',cv2.WINDOW_NORMAL)


    limit = len(sequence)
    count = 0

    while True:
        ret, frame = cap.read()
        cv2.setMouseCallback("Frame", mouse_event)
        if display:
            if count < limit:
                origin += sequence[count]
                x,y = origin[0], origin[1]
                cv2.circle(frame, (x,y) , 5+int((count/7)**2) , (255,0,0), -1)
                count += 1
            else:

                display = False

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

def translate_all_images_test():
    """This test is made to convert all image sequences to numpy arrays"""

    #since there are 13 files to translate

    for i in range(1,7):
        im = cv2.imread("docs/pitches/return-" + str(i) + ".png", cv2.IMREAD_GRAYSCALE)
        sequence = Pitch.sequenceTranslator.translateImageToSequence(im, l = 21)
        np.savetxt("docs/return-" + str(i), sequence.reshape(int(len(sequence)/2),2))
