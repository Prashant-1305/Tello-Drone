from djitellopy import tello
from time import sleep
skynet = tello.Tello()
skynet.connect()
print(skynet.get_battery())
skynet.takeoff()
skynet.move_forward(200)
#sleep(3)
skynet.send_rc_control(0, 0, 0, 0)
#sleep(3)
#skynet.send_rc_control(0, 0, 0, 0)
# sleep(3)
''' skynet.send_rc_control(0, 0, 0, 100)
sleep(3) '''
skynet.land()
