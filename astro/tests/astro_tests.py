from nose.tools import *
import numpy as np
import cv2
import astro as a

def draw_ball_test():
    """draw the ball backwards"""

    # Get frames and edit
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('frame',cv2.WINDOW_NORMAL)
    while True:
        #get parameters
        _, frame = cap.read() #(480, 640, 3) (y, x)
        px, py = 200, 200
        r = 50
        draw_ball(frame, (px,py), r)
        cv2.imshow('frame',frame )

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cv2.destroyAllWindows()

def setup_test():
    """test all set up:
    load sequences, calibrate movement sensor, first test
    """
    config = {
    "pitch_start" : (430, 200), #start cordinates of the pitch sequence (x,y)
    "speed" : 25,                #speed slow
    "cap" : 0,
    "step": 1,
    "sensor height and width": (100, 150),
    "dificulty": 1
    }

    # Save
    np.save('docs/config.npy', config)

    # Load
    read_dictionary = np.load('docs/config.npy',allow_pickle='TRUE').item()

def sequence_and_display_draft_test():
    """display a selected sequence"""
    background = cv2.VideoCapture('/home/jorge/Documents/2-Programming/astro/docs/background/background.avi')
    config = np.load('docs/config.npy',allow_pickle='TRUE').item()
    a.create(config)
    score = 0
    shoot = True
    wait = 20
    w = 0

    #run display
    while True:

        ret, frame = a.cap.read()
        ret, back =  background.read()
        frame = cv2.flip(frame, 1)
        present = np.copy(frame)
        frame = back

        if ret and shoot:
            a.draw_target(frame, (int(a.sx+a.sw/2),int(a.sy+a.sh/2)), int(a.sh/2), 0)
            #compute balls position
            if a.ball_on_air():
                if not a.sequence.hit:
                    a.origin += a.sequence.read()[a.count]
                    a.x,a.y = a.origin[0], a.origin[1]
                    r = 5 + int(a.count*100/a.sequence.get_size())
                    a.draw_ball(frame, (a.x,a.y), r, a.sequence.hit)
                    a.count += 1
                else:

                    a.origin += a.sequence.read_hit_sequence()[a.count]
                    a.x,a.y = a.origin[0], a.origin[1]
                    r -=  int(100/a.sequence.get_size())
                    try:
                        a.draw_ball(frame, (a.x,a.y), r  , a.sequence.hit )
                    except:
                        pass
                    a.count += 1


            else:
                a.restart()
                a.sensor.get_frame(present)
                shoot = False
                w = 0


            if a.ball_on_strike_zone(present):
                score += 1
                print("hit")



            #present frame becomes previous
            a.sensor.get_frame(present)
        else:
            if w == wait:
                print("shoot ")
                shoot = True
                w = 0
            w += 1
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    print("total score{}".format(score))
    a.cap.release()
    background.release()
    cv2.destroyAllWindows()

def sequence_and_display_test():
    """display a selected sequence"""

    #video with background
    background = cv2.VideoCapture('/home/jorge/Documents/2-Programming/astro/docs/background/background.avi')

    #load configuration
    config = np.load('docs/config.npy',allow_pickle='TRUE').item()

    #initialize game
    a.create(config)

    #run display
    a.run(background)

    print("total score{}".format(a.score))
    a.cap.release()
    background.release()
    cv2.destroyAllWindows()
