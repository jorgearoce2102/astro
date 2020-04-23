import cv2
import numpy as np

target_original = cv2.imread("docs/target.jpg")
invert_global = 0

def draw_target(frame, position, r, invert):
    """draw a target on a given image
    args:
    frame: the image in which we are to draw the ball
    position: the target position
    r: new radious of the target drawing
    """

    #get parameters
    px, py = (position)

    #shape of target
    bh,bw,_ = np.shape(target_original)
    if bh == bw:    #if ball image is square
        d1 = bh

    #resize to diameter
    target = cv2.resize(target_original, (r*2,r*2), interpolation = cv2.INTER_NEAREST)

    #draw
    frame[(py-r):(py+r),(px-r):(px+r)] =  cv2.bitwise_xor(target,
                                        cv2.bitwise_and(cv2.bitwise_not(target),
                                            frame[(py-r):(py+r),(px-r):(px+r)]))
