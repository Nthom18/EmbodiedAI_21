#!/usr/bin/python3

#### IMPORTS ####
import ev3dev.ev3 as ev3
from ev3dev2.sound import Sound
import time

from behaviour import Behaviour
from logger import Logger



#### SETUP ####
# Speaker setup
speaker = Sound()

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

    log.log_to_file(t, cl1.value(), cl2.value(), Egon.control_input, Egon.base_speed)
    t += 1

    # Claw control
    if ((us.value() < thrs_low) and (hugged == False)):
        mA.duty_cycle_sp = 0
        mD.duty_cycle_sp = 0
        speaker.speak('Target acquired')
        claw('close')
        hugged = True

    elif (( us.value() > thrs_up) and (hugged == True)):
        claw('open')
        hugged = False


    # Apply behaviours
    Egon.update(cl1.value(), cl2.value())

    mA.duty_cycle_sp = Egon.thrust_left
    mD.duty_cycle_sp = Egon.thrust_right
