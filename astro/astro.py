import cv2
import numpy as np
import astro as a

if __name__ == '__main__':

    #load background from video
    background = cv2.VideoCapture('docs/background/background.avi')

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
