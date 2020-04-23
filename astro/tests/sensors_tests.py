from nose.tools import *
import numpy as np
import cv2
from astro import bat_detection
calibrate = bat_detection.calibrate
Sensor = bat_detection.Sensor
from astro import Pitch
Sequence = Pitch.Sequence

def background_test():
    cap = cv2.VideoCapture(0)
    path = '/home/jorge/Documents/2-Programming/astro/astro/'
    back = cv2.imread(path+ 'background.jpg')
    count = 0
    ret, frame = cap.read()
    #Poisition and size of sensor
    x = 200
    y = 200
    h = 250
    w = 150
    previous =  np.copy(frame[y:y+w,x:x+h])

    #set parameters for mean value of sensor
    sum_xi = True
    i = 0
    sampleNbMean = 50
    xi = np.empty((0, sampleNbMean))
    calculateMean = True
    kernel = np.ones((5,5), np.uint8)
    while(True):
        # Capture frame, draw the window and display to the user
        ret, frame = cap.read()
        image = cv2.rectangle(frame, (x,y), (x+h,y+w), (255, 0, 0) , 5)
        cv2.namedWindow('frame',cv2.WINDOW_NORMAL)
        cv2.imshow('frame',image)

        #get present window
        present = frame[y:y+w,x:x+h]

        #exit
        key = cv2.waitKey(1)
        if key == ord('c'):
            # write frame back to file
            cv2.imwrite(path + "background.jpg", frame)
            previous = np.copy(present)
            calculateMean = True

        elif key == ord('q'):
            break

        # Our operations on the frame come here
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(frame, (7,7),  0)

        #mean and std deviation
        if calculateMean:

            xi = np.append(xi,
                np.sum(
                    cv2.erode(
                        cv2.bitwise_xor(present,previous), kernel, iterations=1)))             #add  diference of window with prieviuos
            # cv2.imshow("mean", cv2.erode( cv2.bitwise_xor(present,previous), kernel, iterations=1))
            i += 1

        #calcular sigma
        if i == sampleNbMean and calculateMean:
            mean = np.sum(xi)/len(xi)
            sum = 0
            for sample in xi:
                sum += np.power(sample - mean, 2)
            sigma = np.sqrt(sum/len(xi))
            i = 0
            calculateMean = False

        #compare present sensor with previous, get weight and validate if ON/OFF
        # print(np.sum(cv2.bitwise_xor(present, previous)))
        if calculateMean == False:
            if (mean + 2.58 * sigma) > np.sum(cv2.erode( cv2.bitwise_xor(present,previous), kernel, iterations=1)) > (mean - 2.58 * sigma):
                # window = np.copy(image[x:x+h,y:y+w])
                print("OFF")
            else:
                print("ON")

        #present image becomes previous before steping into next image
        previous = present


    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

def background_bitwise_test():

    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    previous = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    previous = cv2.GaussianBlur(previous, (7,7),  0)
    # path = '/home/jorge/Documents/2-Programming/astro/astro/'
    # background = cv2.imread(path+ 'background.jpg')
    # background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
    cv2.namedWindow('frame',cv2.WINDOW_NORMAL)

    while(True):
        # Capture frame, draw the window and display to the user
        ret, frame = cap.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        frame = cv2.GaussianBlur(frame, (7,7),  0)

        # Taking a matrix of size 5 as the kernel
        kernel = np.ones((5,5), np.uint8)
        cv2.imshow('frame', cv2.erode( cv2.bitwise_xor(frame,previous), kernel, iterations=1))

        key = cv2.waitKey(1)
        if key == ord('q'):
            cv2.destroyWindow('Calibrate')
            break

        previous = frame

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

def calibration_and_sensor_test():
    """thest the calibration function"""

    #load camera
    cap = cv2.VideoCapture(0)

    x = 200
    y = 200
    h = 150
    w = 250
    location = [x, y, h, w]

    #define sensor
    sensor = Sensor(cap, location)
    cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
    swing_av = 0
    count = 0
    difference_sum = 0
    while True:
        _, frame = cap.read()
        image= cv2.rectangle(frame, (x,y), (x+w,y+h), (255, 0, 0) , 5)
        cv2.imshow("frame", image)
        active, difference = sensor.is_active(frame)

        if active:
            difference_sum += difference
            count +=1
        else:
            pass
        if cv2.waitKey(1) == ord('q'):
            print(difference_sum/count)
            break
        elif cv2.waitKey(1) == ord('s'):
            print(difference_sum/count)
            swing_av = 0
            count = 0
        sensor.get_frame(frame)
    cv2.destroyAllWindows()
def adjust_position_test():
    """Function that makes sure that the sensor windows is always within the frame"""
    config = np.load('docs/config.npy',allow_pickle='TRUE').item()
    origin = config["pitch_start"]
    sh, sw = config["sensor height and width"]
    # Load sequence
    speed =  config["speed" ]
    step = config["step"]+speed
    sequence = Sequence( speed, step)
    for s in range(1,22):
        s= 11
        # print(s)
        sequence.set_sequence(s)
        size = sequence.get_size()

        #TODO
        end = np.sum(sequence.read(), axis=0)
        sx, sy = end + origin - [int(sw/2), int(sh/2)]
        i = -1
        # print(sx,sy)
        while (sx < 0) or (sy<0) or (sx+sw)>=640 or (sy+sh)>=480 :
            # print((sx,sy) - sequence.read()[i])
            sx, sy = (sx,sy) - sequence.read()[i]
            i -=1
        # print((sx+sw),(sy+sh))


    # sensor = Sensor(cap, location)
    # sensor.adjust_position()
