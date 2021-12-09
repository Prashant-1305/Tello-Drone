from djitellopy import tello
from time import sleep
import cv2

skynet = tello.Tello()
skynet.connect()
print(skynet.get_battery())

skynet.streamon()

while True:
    img = skynet.get_frame_read().frame
    #img = cv2.resize(img, (360, 240))
    cv2.imshow("Image", img)
    cv2.waitKey(1)