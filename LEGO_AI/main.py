#!/usr/bin/python3

#### IMPORTS ####
import ev3dev.ev3 as ev3
from ev3dev2.sound import Sound
import time
import sys

from behaviour import Behaviour
from logger import Logger



#### SETUP ####
# Speaker setup
speaker = Sound()

# Button on Brick setup
btn = ev3.Button()

# Colour sensor setup
clR = ev3.ColorSensor('in2')
clL = ev3.ColorSensor('in1')
clL.mode = 'COL-REFLECT'
clR.mode = 'COL-REFLECT'

# Sonic sensor setup
us = ev3.UltrasonicSensor('in3')
# us.mode = 'US-DIST-CM'

# Motor Setup
mR = ev3.LargeMotor('outD')
mR.run_direct()
mL = ev3.LargeMotor('outA')
mL.run_direct()
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
speaker.beep(1)
while True:
    
    try:
        log.log_to_file(t, clL.value(), clR.value(), Egon.last_seen)
        # log.log_to_file(t, clL.value(), clR.value(), Egon.control_input, Egon.base_speed)
        # log.log_to_file(t, Egon.thrust_left, Egon.thrust_right, Egon.error, Egon.control_input, Egon.base_speed)
        t += 1

        # Claw control
        if ((us.value() < thrs_low) and (hugged == False)):
            mR.duty_cycle_sp = 0
            mL.duty_cycle_sp = 0
            # speaker.speak('Target acquired')
            claw('close')
            hugged = True

        # elif (( us.value() > thrs_up) and (hugged == True)):
        #     claw('open')
        #     hugged = False


        # Apply behaviours
        Egon.update(clL.value(), clR.value(), hugged)

        mR.duty_cycle_sp = Egon.thrust_right
        mL.duty_cycle_sp = Egon.thrust_left
        
        print(t, clL.value(), clR.value(), Egon.last_seen)
 

    except KeyboardInterrupt: # CATCHES CTRL+C
        mR.duty_cycle_sp = 0
        mL.duty_cycle_sp = 0
        sys.exit()
