#!/usr/bin/python3

#### IMPORTS ####
import ev3dev.ev3 as ev3
import time

from behaviour import Behaviour
from line_follower import line_follower
from logger import Logger



#### SETUP ####
# Button on Brick setup
btn = ev3.Button()

# Colour sensor setup
cl1 = ev3.ColorSensor('in1')
cl1.mode = 'COL-REFLECT'
cl2 = ev3.ColorSensor('in2')
cl2.mode = 'COL-REFLECT'

# Sonic sensor setup
us = ev3.UltrasonicSensor('in3')
# us.mode = 'US-DIST-CM'

# Motor Setup
mA = ev3.LargeMotor('outA')
mA.run_direct()
mD = ev3.LargeMotor('outD')
mD.run_direct()
mC = ev3.MediumMotor('outC')
mC.run_direct()

# Behavior setup
Egon = Behaviour()



def claw(dir):
    if (dir == 'open'):
        mC.run_forever(speed_sp=1000)
    elif (dir == 'close'):
        mC.run_forever(speed_sp=-1000)

    time.sleep(2)
    mC.stop(stop_action="hold")


hugged = False
thrs_low = 40
thrs_up = 70


log = Logger()
t = 0

#### PROGRAM LOOP ####
while True:

    dis = us.value()
    # print(str(dis))


    if ((dis < thrs_low) and (hugged == False)):
        ev3.Sound.beep().wait()
        claw('close')
        hugged = True

    elif ((dis > thrs_up) and (hugged == True)):
        claw('open')
        hugged = False


    log.log_to_file(t, cl1.value(), cl2.value())
    t += 1
    print(cl1.value(), cl2.value())

    # Apply behaviours
    # Egon.update(cl1.value(), cl2.value())

    # mA.duty_cycle_sp = Egon.thrust_left
    # mD.duty_cycle_sp = Egon.thrust_right


    # TESTING

    # mA.duty_cycle_sp = 40
    # mD.duty_cycle_sp = 40
    # mC.duty_cycle_sp = 50


    

    line_follower(mA, mD, cl1.value())     # First line follower
