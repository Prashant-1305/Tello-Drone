import time
import cv2

from djitellopy import tello

global img
skynet = tello.Tello()
skynet.connect()
print(skynet.get_battery())

skynet.takeoff()
skynet.streamon()

skynet.move_forward(151)
skynet.send_rc_control(0, 0, 0, 0)
time.sleep(0.25)
skynet.send_rc_control(0, 0, 0, 0)
time.sleep(0.25)
skynet.send_rc_control(0, 0, 0, -70)
time.sleep(1)
skynet.send_rc_control(0, 0, 0, 0)

img = skynet.get_frame_read().frame
cv2.imshow("Image", img)
cv2.imwrite(f'Resources/Images/{time.time()}.jpg', img)
cv2.waitKey(1)

skynet.land()


