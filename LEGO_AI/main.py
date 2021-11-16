#!/usr/bin/python3

#### IMPORTS ####
import ev3dev.ev3 as ev3

from behaviour import Behaviour
from line_follower import line_follower


#### SETUP ####
# Button on Brick setup
btn = ev3.Button()

# Colour sensor setup
cl1 = ev3.ColorSensor('in1')
cl1.mode = 'COL-REFLECT'
cl2 = ev3.ColorSensor('in2')
cl2.mode = 'COL-REFLECT'

# Motor Setup
mA = ev3.LargeMotor('outA')
mA.run_direct()
mB = ev3.LargeMotor('outB')
mB.run_direct()

# Behavior setup
Egon = Behaviour()

#### PROGRAM LOOP ####
while True:

    # Apply behaviours
    Egon.update(cl1.value(), cl2.value())

    mA.duty_cycle_sp = Egon.thrust_left
    mB.duty_cycle_sp = Egon.thrust_right


    # line_follower(mA, mB, cl.value())     # First line follower
