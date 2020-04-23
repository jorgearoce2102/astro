
import cv2
import numpy as np

def calibrate(cap, location):
    """Function that returns the mean value and the sigma value used during runtime,

    args:
    cap: cv2.videoCapture object
    position: of the square window
    size: of the square window

    return:
    mean:
    sigma:
    """

    #Poisition and size of sensor
    [x, y, h, w] = location

    #show square to user and wait for key
    print("please, step away to clear the blue square displayed on screen and press q to continue")
    while True:
        ret, frame = cap.read()
        cv2.namedWindow('Calibrate',cv2.WINDOW_NORMAL)
        show =  cv2.rectangle(frame, (x,y), (x+w,y+h), (255, 0, 0) , 5)
        cv2.imshow('Calibrate', show)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    #get first image, process and define window previous for iteration
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.GaussianBlur(frame, (7,7),  0)
    previous = frame[y:y+w,x:x+h]

    #set parameters for mean value of sensor, kernel of erode function,
    sampleNbMean = 50
    xi = np.empty((0, sampleNbMean))
    kernel = np.ones((5,5), np.uint8)

    #iterate over each frame until sample number
    for iteration in range(sampleNbMean):

        # Capture frame, draw the window and display to the user
        ret, frame = cap.read()
        # Image operation
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.GaussianBlur(frame, (7,7),  0)

        #get present window
        present = frame[y:y+w,x:x+h]

        #add sample for mean,  add  diference of window with prieviuos
        xi = np.append(xi,
            np.sum(
                cv2.erode(
                    cv2.bitwise_xor(present,previous), kernel, iterations=1)))

        #present image becomes previous before steping into next image
        previous = present

    #mean
    mean = np.sum(xi)/len(xi)

    #sigma
    sum = 0
    for sample in xi:
        sum += np.power(sample - mean, 2)
    sigma = np.sqrt(sum/len(xi))

    #close window
    cv2.destroyWindow('Calibrate')

    return mean, sigma
