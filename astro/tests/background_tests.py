from nose.tools import *
import numpy as np
import cv2
import astro as a

def background_test():
    cap = cv2.VideoCapture(0)
    path = '/home/jorge/Documents/2-Programming/astro/astro/'
    back = cv2.imread(path+ 'background.jpg')
    # back = cv2.cvtColor(back, cv2.COLOR_BGR2GRAY)
    count = 0
    ret, frame = cap.read()
    x = 250
    y = 250
    h = 50
    w = 50

    window = np.copy(frame[x:x+h,y:y+w])
    sum_xi = True
    i = 0
    sampleNbMean = 50
    xi = np.empty((0, sampleNbMean))
    calculateMean = True

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        image = cv2.rectangle(frame, (x,y), (x+h,y+w), (255, 0, 0) , 5)
        cv2.namedWindow('frame',cv2.WINDOW_NORMAL)
        cv2.imshow('frame',image)

        key = cv2.waitKey(1)

        if key == ord('c'):
            # back = cv2.cvtColor(back, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(path + "background.jpg", frame)
            window = np.copy(frame[x:x+h,y:y+w])
            calculateMean = True

        elif key == ord('q'):
            break

        # Our operations on the frame come here
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(frame, (7,7),  0)
        gray = cv2.GaussianBlur(gray, (7,7),  0)

        #calcular media

        if calculateMean:

            xi = np.append(xi, np.sum(image[x:x+h,y:y+w] - window))
            window = image[x:x+h,y:y+w]
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

        #comparar resta.
        if calculateMean == False:
            # print("sigma", sigma)
            # print((mean + (2.58 * sigma)),
            #     np.sum(image[x:x+50,y:y+50] - window),
            #     (mean - (2.58 * sigma)))
            if (mean + 2.58 * sigma) > np.sum(image[x:x+h,y:y+w] - window) > (mean - 2.58 * sigma):
                # window = np.copy(image[x:x+h,y:y+w])
                print("OFF")
            else:
                print("ON")

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

def baseball_AND_test():
    """test to draw a baseball ball on a given image"""



    # Get frames and edit
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('frame',cv2.WINDOW_NORMAL)
    while True:
        #get parameters
        _, frame = cap.read() #(480, 640, 3) (y, x)
        a.draw_target(frame, (200,200), 50, 0)
        cv2.imshow('frame',frame )

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cv2.destroyAllWindows()


def background_change_test():
    cap = cv2.VideoCapture(0)
    cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
    ret, back = cap.read()
    back = cv2.cvtColor(back, cv2.COLOR_BGR2GRAY)

    while True:
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        k = cv2.waitKey(1)
        if k == ord('y'):
            back = np.copy(frame)
        elif k == ord('q'):
            break
        filtered = cv2.bitwise_xor(frame,back)
        ret, f = cv2.threshold(filtered,90,255,cv2.THRESH_BINARY)
        cv2.imshow("frame",f)

    cv2.destroyAllWindows()
