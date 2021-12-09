import time
import cv2
from djitellopy import tello

global img
skynet = tello.Tello()
skynet.connect()
print(skynet.get_battery())

def unmannedFlightPlan(dis,rot,stops,upHi,doHi):
    skynet.streamon()
    skynet.takeoff()
    skynet.move_forward(dis)
    time.sleep(0.25)
    skynet.rotate_clockwise(rot)
    print('Rotation Complete')
    for i in range (stops):
        skynet.move_up(upHi)
        time.sleep(0.25)
        captureImage()
        skynet.move_down(doHi)
        time.sleep(0.25)
        captureImage()

def captureImage():
    img = skynet.get_frame_read().frame
    cv2.imshow("Image", img)
    cv2.imwrite(f'Resources/Images/{time.time()}.jpg', img)
    cv2.waitKey(1)

unmannedFlightPlan(173, 90, 2, 34, 27)
skynet.land()
