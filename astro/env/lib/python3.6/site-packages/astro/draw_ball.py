
import cv2
import numpy as np
import random
ball_global = cv2.imread("docs/ball2.jpg")
theta = 0
invert_global = 0
speed = 0
def draw_ball(frame, position, r, invert):
    """draw a baseball ball on a given image
    args:
    frame: the image in which we are to draw the ball
    position: the balls position
    r: new radious of the ball
    """
    #ball is an image of a baseball ball with a black background
    #the image must be square (height = width)
    global ball_global, theta, invert_global, speed

    frame_height, frame_width, _ = np.shape(frame)
    ball = np.copy(ball_global)
    x, y = position

    # substract radious from the position so that the ball might be centered to the position
    x -= r
    y -= r

    #new diameter
    d = 2*r

    #rotate
    if invert != invert_global:
        speed = random.randrange(0,90)
        invert_global = invert
    theta -= 45+(speed*invert)  #if invert is true then -45

    #resize to new diameter and rotate ball image
    ball = cv2.resize(ball, (d,d), interpolation = cv2.INTER_NEAREST)
    M = cv2.getRotationMatrix2D((int(d/2), int(d/2)), theta, 1)
    ball = cv2.warpAffine(ball, M, (d,d))
    bw,bh,_ = np.shape(ball)                 #since image is square, diameter is height and width

    #process image for bitwise operations, threshold  image so that
    #the pixels that contain the ball image become 255 and those who dont remain 0
    ball_gray = cv2.cvtColor(ball, cv2.COLOR_BGR2GRAY)
    ret,thresh1 = cv2.threshold(ball_gray,10,255,cv2.THRESH_BINARY)
    ball2 = cv2.merge((thresh1 ,thresh1 ,thresh1 ))

    #So that the ball is always on the frame, certain rules must be applied
    bw -= ((x+bw)>frame_width)*(x+bw-frame_width)       #if ball image is located above the width
    bh -= ((y+bh)>frame_height)*(y+bh-frame_height)     #if ball image is located above the height
    bw += (x<0)*(x)                                     #if ball image is located under 0
    bh += (y<0)*(y)                                     #if ball image is located under 0
    bx = (x<0)*-x                                       #if ball image is located under 0
    by = (y<0)*-y                                       #if ball image is located under 0
    x *= (x>0)                                          #if ball image is located under 0
    y *= (y>0)                                          #if ball image is located under 0

    try:
        frame[y:y+bh,x:x+bw] =  cv2.bitwise_xor(ball[by:by+bh,bx:bx+bw],
                                        cv2.bitwise_and(cv2.bitwise_not(ball2[by:by+bh,bx:bx+bw]),
                                        frame[y:y+bh,x:x+bw] ))
    except:
        pass
