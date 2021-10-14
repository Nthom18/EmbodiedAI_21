#!/usr/bin/python3

#### IMPORTS ####
import ev3dev.ev3 as ev3
from line_follower import line_follower


#### SETUP ####
# Button on Brick setup
btn = ev3.Button()

# Colour sensor setup
cl = ev3.ColorSensor('in1')
cl.mode = 'COL-REFLECT'

# Motor Setup
mA = ev3.LargeMotor('outA')
mA.run_direct()
mB = ev3.LargeMotor('outB')
mB.run_direct()


#### PROGRAM LOOP ####
while True:

    mA.duty_cycle_sp = 50
    mB.duty_cycle_sp = 50

    # line_follower(mA, mB, cl.value())




