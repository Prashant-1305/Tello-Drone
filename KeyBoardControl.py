import KeyPressModule as kp
from djitellopy import tello
from time import sleep

kp.init()

skynet = tello.Tello()
skynet.connect()
print(skynet.get_battery())

def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50

    if kp.getKey("LEFT"): lr = -speed
    elif kp.getKey("RIGHT"): lr = speed

    if kp.getKey("UP"): fb = speed
    elif kp.getKey("DOWN"): fb = -speed

    if kp.getKey("u"): ud = speed
    elif kp.getKey("d"): ud = -speed

    if kp.getKey("c"): yv = speed
    elif kp.getKey("a"): yv = -speed

    if kp.getKey("t"): skynet.takeoff()
    if kp.getKey("l"): skynet.land()

    return [lr, fb, ud, yv]


while True:
    keyVals = getKeyboardInput()
    skynet.send_rc_control(keyVals[0], keyVals[1], keyVals[2], keyVals[3])
    sleep(1)