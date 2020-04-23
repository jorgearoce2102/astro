
import cv2
import numpy as np

directions = ["east", "southeast", "south", "southwest", "west", "northwest", "north", "northeast"]
direction_in_pixels = [(1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1) ]
origin = ()
translateInit = False

def mouse_event(event, x, y, flags, params):
    global translateInit, origin
    if event == cv2.EVENT_LBUTTONDOWN:
        origin = (x,y)
        translateInit = True
    else:
        pass

def create_masks(l=11):
        """******************Create direcional masks*************************************
        a directional mask, is a kernel of shape (l,l) where l is odd and equal or greater than 3 that contains
        a direccion to which the ball might travel (once projected in the screen)
        Exemple: consider the following kernel
                    [[  0,   0,   0,   0,   0],
                     [  0,   0,   0,   0,   0],
                     [  0,   0,   1,   1,   1],
                     [  0,   0,   0,   0,   0],
                     [  0,   0,   0,   0,   0]]
        where l = 5, and its direccion is east. This masks represents the probability
        of the the pixel moving one pixel to the right."""

        kernels = np.zeros((8,l,l), np.uint8)
        angles =  np.arange(0,2*np.pi, np.pi/4)      #angles used to iterate over the directions
        k = int(l/2)
        center = (k,k)
        for i in range(8):
            x2 = int( center[0] + 2*k * np.cos(angles[i])  )
            y2 = int( center[1] + 2*k * np.sin(angles[i])  )
            cv2.line(kernels[i], center, (x2,y2), 255, 10)
        return kernels

def get_next_direction(image, masks, origin = (0,0), previous_direction = None):
    """Function that returns the direction to follow from an input image showing the
    projection of the baseball ball trajectory in the strike zone

    args:
    image: the image of the projection
    origin: coordinates (x,y) of the origin of the balls renderTrajectory
    ks: kernel size

    returns:
    direction: integer used int the directions dictionary """



    (y,x) = origin
    ks = int(len(masks[0])/2)                                                   #shape of the masks

    #area of the image to inspect
    crop = np.array(np.copy(image[x-ks:x+ks+1, y-ks:y+ks+1]))

    weight = 0

    finalDirection = None
    change = False
    for mask, d in zip(masks, range(8)):                                        #Inspect all masks (directions)

        #maskW: overlap between images, the greater the value the greater de probability to transit towards
        #the direction represented by the mask
        maskW = np.sum(cv2.bitwise_and(crop,mask))

        if weight < maskW:
                weight = maskW
                finalDirection = d
                change = True

    if change:
        return True, finalDirection
    else:
        return False, finalDirection

def translateImageToSequence(im, l = 21):
    """Function that returns the whole sequence to follow from an input image showed in the input
    image. The image is printed to in a windows for the user to select the starting point

    args:
    image: the image of the projection.
            It has to be all zeros and the sequence followed in 255 (black and white)
    l: length of masks with cardinal directions

    returns:
    sequence: Numpy array of shape (unknown length, 2)
              containing all the steps for the baseball ball to take """

    global translateInit, origin, x, y

    cv2.namedWindow('Frame',cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("Frame", mouse_event)

    #Create masks of all the posible cardinal directions to take
    masks = create_masks(l)

    h, w = np.shape(im)

    #initialize previous direction and sequence array
    previous_direction = None
    sequence = np.array([], np.uint8)

    while True:
        #display image for user and get origin from mouse event (click)
        cv2.imshow("Frame", im)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        if translateInit == True and origin[0] < (w - int(l/2))  and origin[1] < (h - int(l/2)):
            change, new_direction = get_next_direction(im, masks, origin, previous_direction)

            #while origin is within the limits of the image and if theres is movement
            if change:
                previous_direction = new_direction

                # translateInit = False
                cv2.circle(im, origin, 5, 0, 5)
                (x2,y2) = direction_in_pixels[new_direction]
                sequence = np.append(sequence, (x2,y2))
                origin = (origin[0] + x2, origin[1] + y2)
                cv2.waitKey(10)


            else:
                translateInit = False

    cv2.destroyAllWindows
    return sequence
