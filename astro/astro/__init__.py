from . import Pitch, bat_detection, draw_ball, config, draw_target
import numpy as np
import cv2


#read functions
draw_ball = draw_ball.draw_ball
draw_target = draw_target.draw_target
Sensor = bat_detection.Sensor
create = config.load_config
Sequence = Pitch.Sequence

#initiate variables
cap = None                  #videoCapture object
sx,sy,sw,sh = 0,0,0,0       #coordinates x,y of sensor. and its size width and height
count = 0                   #to iterate through the sequence array, start from 0
size = 0                    #length of the sequence
origin = (0,0)              #origin of the pitch
x,y = 0,0                   #position of the baseball ball
sensor = None               #Sensor object
sequence = None             #Sequence object
config = {}                 #configuration of the game (parameters)
frame_width = 0             #frame width
frame_height = 0            #frame height
score = 0                   #score of user (number of balls hit)
shoot = True                #ball ready to be pitched
wait = 60                   #number of frames before pitching ball
w = 0                       #increment for wait

def create(config_local):

    global config, cap, sx, sy, sw, sh, count, size, origin,x,y,sensor, sequence, frame_width, frame_height

    # Load configuration
    config = config_local
    cap = cv2.VideoCapture(config["cap"])
    cv2.namedWindow('Frame',cv2.WINDOW_NORMAL)
    origin = config["pitch_start"]
    (x,y) = origin
    frame_width, frame_height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Load sequence
    speed =  config["speed" ]
    step = config["step"]
    sequence = Sequence( speed, step)
    sequence.set_sequence()
    size = sequence.get_size()

    # Load sensor Calibrate sensor
    sh, sw = config["sensor height and width"]
    end = np.sum(sequence.read(), axis=0)
    sx, sy = end + origin - [int(sw/2), int(sh/2)]
    i = -1
    while (sx < 0) or (sy<0) or (sy+sh)>480 or (sx+sw)>640:
        sx, sy = (sx,sy) - sequence.read()[i]#*((sx < 0) or (sy<0)) - sequence.read()[i]*((sy+sh)>480 or (sx+sw)>640)
        i -=1
    location = [sx, sy, sh, sw] #sensor x, sensor h, sensor height, sensor width
    sensor = Sensor(cap, location)

def restart():
    """The sequence is read again, so the parameters of the rest of the elements, are
    changed accordingly
    """
    global sequence, origin, sensor, count, sx, sy, sw, sh
    #Sequence
    count = 0
    sequence.set_sequence()
    origin = config["pitch_start"]
    (x,y) = origin

    #sensor
    sensor.status = True
    end = np.sum(sequence.read(), axis=0)
    sx, sy = end + origin - [int(sw/2), int(sh/2)]
    i = -1
    #if the speed of the ball is to fast(sequence is multiply by speed)
    #the resulting position at the end of the sequence will be outside of the frame
    #this filter will iterate back to place the sensor somewhere within the frame
    while (sx < 0) or (sy<0) or (sy+sh)>=480 or (sx+sw)>=640:
        try:
            sx, sy = (sx,sy) - sequence.read()[i]
        except:
            pass
        i -=1

    sensor.x, sensor.y = sx, sy

def ball_on_air():
    """ Funtion determines whether or not continue with the sequence.
    As long as there is a sequence to follow, return True.
    """
    global count, size

    #read size of the current sequence
    size = sequence.get_size()

    return count < size

def ball_on_strike_zone(present):
    """Function that determines if the ball is within the reach of the sensor
    args
    present = current frame of the player"""
    global sx, x, sx, sw, sy, y, sy, sh, sensor, sequence, count, size

    #if ball is in sensor area and the sensor is activated
    if (sx<x<(sx+sw)) and  (sy<y<(sy+sh)) and sensor.status:
        #check if there is movement in the sensor area
        if sensor.is_active(present):

            #turn sensor off, so that the ball won't activate more than once
            sensor.status = False

            #tell sequence that the ball has been hit, therefore the
            #sequence should be changed to the return sequence (ball flying)
            sequence.ball_hit()

            #set cound and size for ball_on_air()
            count = 0
            size = sequence.get_size()

            #the ball has been hit, continue
            return True

def run(background):
    """ Funtion that runs the game.
    Reset parameters, draw the ball and target, detect hit and miss
    """

    global cap, origin, s, x, y, sx, sy, sh, sw, sequence, sensor, shoot, w, wait, score, count

    while background.isOpened():                                 #TODO True?
        #read first frames from videoCapture objects
        _, web_cam = cap.read()                                               #read from camera
        ret, frame =  background.read()                                         #read from video
        if not ret:
            break
        web_cam= cv2.flip(web_cam, 1)                                           #flip for user perception
        present = np.copy(web_cam)                                              #copy for sensor

        #if background is available depending on the duration of the background video
        #shoot is "ready"
        if ret and shoot:

            #draw target depending on the position of the sensor
            draw_target(frame, (int(sx+sw/2),int(sy+sh/2)), int(sh/2), 0)

            #compute balls position
            if ball_on_air():

                #while the ball has not been hit
                if not sequence.hit:

                    #set current position of the ball
                    origin += sequence.read()[count]
                    x,y = origin[0], origin[1]

                    #get radious of the ball to draw according to the adjust_position
                    #and draw on frame
                    r = 5 + int(count*100/sequence.get_size()) #increment size
                    draw_ball(frame, (x,y), r, sequence.hit)

                    #continue with sequence by adding 1 to count
                    count += 1

                #ball has been hit
                else:

                    #set current position of the ball
                    origin += sequence.read_hit_sequence()[count]
                    x,y = origin[0], origin[1]

                    #get radious of the ball to draw according to the adjust_position
                    #and draw on frame
                    r -=  int(100/sequence.get_size())  #decrement size

                    try:
                        #ball can be drawn on the frame
                        draw_ball(frame, (x,y), r , sequence.hit )
                    except:
                        pass

                    #continue with sequence by adding 1 to count
                    count += 1

            else:
                #restart inning
                restart()
                sensor.get_frame(present)
                shoot = False
                w = 0

            #check if the ball is in the strike zone (sensor)
            if ball_on_strike_zone(present):

                #add point to the user
                score += 1

            #present frame becomes previous in sensor
            sensor.get_frame(present)

        #background is available, but the ball is on the air "flying".
        #Give user time to reposition
        else:

            #counting number of frames for wait time before pitching again
            if w == wait:
                #continue game,
                shoot = True
                w = 0
            w += 1

        #display frame to user
        cv2.imshow("Frame", frame)

        #exit
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
