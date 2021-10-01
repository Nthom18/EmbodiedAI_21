#!/usr/bin/python3

import ev3dev.ev3 as ev3
from time import sleep
import signal


btn = ev3.Button()

# mA = Motor(Port.A)
# mB = Motor(Port.B)

mA = ev3.LargeMotor('outA')
mB = ev3.LargeMotor('outB')

THRESHOLD_LEFT = 30
THRESHOLD_RIGHT = 350

BASE_SPEED = 30
TURN_SPEED = 80

# cl = ev3.ColorSensor('in1')

# TouchSensor = ev3.TouchSensor('in3')

# cl.mode = 'COL-COLOR'

# assert cl.connected, "LightSensorLeft(ColorSensor) is noot connected"
# assert TouchSensor.connected, "Touch sensor is noot connected"

# colors = ('unknown', 'black', 'blue', 'green', 'yellow', 'red', 'white', 'brown')

gy = ev3.GyroSensor('in2')
gy.mode = 'GYRO-ANG'

us = ev3.UltrasonicSensor('in4')
us.mode = 'US-DIST-CM'

while True:
    mA.duty_cycle_sp = BASE_SPEED
    mB.duty_cycle_sp = BASE_SPEED
    # tou_val = TouchSensor.value()

    # if tou_val == 1:
    #     ev3.Sound.beep().wait()
    #     mA.duty_cycle_sp = 0
    #     mB.duty_cycle_sp = 0
    #     # exit()
    # else: 
    #     print(colors[cl.value()])

    # dis = us.value() / 10
    # unit = "cm"
    # print(str(dis) + " " + unit)

    ang = gy.value()
    print(str(ang))

