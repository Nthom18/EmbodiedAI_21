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
assert cl.connected, "LightSensorLeft(ColorSensor) is noot connected"
# colors = ('unknown', 'black', 'blue', 'green', 'yellow', 'red', 'white', 'brown')

# Motor Setup
mA = ev3.LargeMotor('outA')
mA.run_direct()
mB = ev3.LargeMotor('outB')
mB.run_direct()


#### PROGRAM LOOP ####
while True:

    # print(cl.value())

    line_follower(mA, mB, cl.value())




