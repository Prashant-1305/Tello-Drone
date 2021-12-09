import logging
import time
import cv2
import numpy as np
from djitellopy import tello
import keypress as kp
from time import sleep

def findFace(img):
    faceCascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.3, 8)
    myFaceListC = []
    myFaceListArea = []

    for (x, y, w, h) in faces:
        cv2.rectangle(img,(x,y),(x+w, y+h),(0, 0, 255),2)
        cx = x + w//2
        cy = y + h//2
        area = w*h
        cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        myFaceListC.append([cx,cy])
        myFaceListArea.append(area)

    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        infotext = "Area:{0} X:{1} Y:{2}".format(area , cx, cy)
        cv2.putText(img, infotext, (cx+20, cy), font, fontScale, fontColor, lineThickness)
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        return img, [[0, 0], 0]

def trackFace(me, img, info, w, h, pid, detectRange, pErrorRotate, pErrorUp):
    area = info[1]
    x, y = info[0][0], info[0][1]
    fb = 0
    errorRotate = x - w/2
    errorUp = h/2 - y
    cv2.circle(img, (int(w/2), int(h/2)), 5, (0, 255, 0), cv2.FILLED)
    if x >10 or y >10:
        cv2.line(img, (int(w/2), int(h/2)), (x,y), (255, 0, 0), lineThickness)
    rotatespeed = pid[0]*errorRotate + pid[1]*(errorRotate - pErrorRotate)
    updownspeed = pid[0]*errorUp + pid[1]*(errorUp - pErrorUp)
    rotatespeed = int(np.clip(rotatespeed, -40, 40))
    updownspeed = int(np.clip(updownspeed, -60, 60))

    area = info[1]
    if area > detectRange[0] and area < detectRange[1]:
        fb = 0
        # updownspeed = 0
        # rotatespeed = 0
        infoText = "Hold Speed:{0} Rotate:{1} Up:{2}".format(fb, rotatespeed, updownspeed)
        cv2.putText(img, InfoText, (10, 60), font, fontScale, fontColor, lineThickness)
        me.send_rc_control(0, fb, updownspeed, rotatespeed)
    elif area > detectRange[1]:
        fb = -20
        infoText = "Backward Speed:{0} Rotate:{1} Up:{2}".format(fb, rotatespeed, updownspeed)
        cv2.putText(img, infoText, (10, 60), font, fontScale, fontColor, lineThickness)
        me.send_rc_control(0, fb, updownspeed, rotatespeed)
    elif area < detectRange[0] and area > 1000:
        fb = 20
        infoText = "Forward Speed:{0} Rotate:{1} Up:{2}".format(fb, rotatespeed, updownspeed)
        cv2.putText(img, infoText, (10, 60), font, fontScale, fontColor, lineThickness)
        me.send_rc_control(0, fb, updownspeed, rotatespeed)
    else:
        me.send_rc_control(0, 0, 0, 0)

    if x == 0:
        speed = 0
        error = 0
    return errorRotate, errorUp


def getKeyboardInput(drone, speed, image):
    lr, fb, ud, yv = 0, 0, 0, 0
    key_pressed = 0
    if kp.getKey("e"):
        cv2.imwrite('/Resources/snap-{}.jpg'.format(time.strftime("%H%M%S", time.localtime())), image)

    if kp.getKey("UP"):
        drone.takeoff()

    elif kp.getKey("DOWN"):
        drone.land()

    if kp.getKey("LEFT"):
        key_pressed = 1
        lr = -speed

    elif kp.getKey("RIGHT"):
        key_pressed = 1
        lr = speed

    if kp.getKey("f"):
        key_pressed = 1
        fb = speed

    elif kp.getKey("b"):
        key_pressed = 1
        fb = -speed

    if kp.getKey("u"):
        key_pressed = 1
        ud = speed

    elif kp.getKey("d"):
        key_pressed = 1
        ud = -speed

    if kp.getKey("a"):
        key_pressed = 1
        yv = -speed

    elif kp.getKey("s"):
        key_pressed = 1
        yv = speed

    info = "battery : {0}% height: {1}cm   time: {2}".format(drone.get_battery(), drone.get_height(), time.strftime("%H:%M:%S",time.localtime()))
    cv2.putText(image, info, (10, 20), font, fontScale, (0, 0, 255), lineThickness)
    if key_pressed == 1:
        info = "Command : lr:{0}% fb:{1} ud:{2} yv:{3}".format(lr, fb, ud, yv)
        cv2.putText(image, info, (10, 40), font, fontScale, (0, 0, 255), lineThickness)

    drone.send_rc_control(lr, fb, ud, yv)


# Main Program
# Camera Setting

detectRange = [500, 2500]  # DetectRange[0]
PID_Parameter = [0.5, 0.0004, 0.4]
pErrorRotate, pErrorUp = 0, 0

# Font Settings
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.5
fontColor = (255, 0, 0)
lineThickness = 1

# Tello Init
Drone = tello.Tello() #Instantiate Tello
Drone.connect()  # Connect Tello 
Drone.streamon()  # Camera
Drone.LOGGER.setLevel(logging.ERROR)  # Logging
sleep(5)  

# KeyPress Initalization
kp.init()  

camera_width = 720
camera_height = 480
while True:
    OriginalImage = Drone.get_frame_read().frame
    Image = cv2.resize(OriginalImage, (camera_Width, camera_height))
    getKeyboardInput(drone=Drone, speed=50, image=Image)
    img, info = findFace(Image)
    #pErrorRotate, pErrorUp = trackFace(Drone, img, info, camera_width, camera_height, PID_Parameter, detectRange, pErrorRotate, pErrorUp)
    cv2.imshow("Drone Control Centre", Image)
    cv2.waitKey(1)
