#!/usr/bin/python3

#### IMPORTS ####
import ev3dev.ev3 as ev3


#### CONSTANTS ####
REF_VALUE = 35
BASE_SPEED = 25


#### FUNCTIONS ####
def line_follower(mA, mB, y):
    error = REF_VALUE - y
    Kp = 0.4

    if (error < 0):
        mA.duty_cycle_sp = BASE_SPEED + abs(error) * Kp
        mB.duty_cycle_sp = BASE_SPEED - abs(error) * Kp * 3

    elif (error > 0):
        mB.duty_cycle_sp = BASE_SPEED + abs(error) * Kp
        mA.duty_cycle_sp = BASE_SPEED - abs(error) * Kp * 3

    else:
        mA.duty_cycle_sp = BASE_SPEED
        mB.duty_cycle_sp = BASE_SPEED

if __name__ == '__main__':

    # Colour sensor setup
    cl = ev3.ColorSensor('in1')
    cl.mode = 'COL-REFLECT'
    assert cl.connected, "LightSensorLeft(ColorSensor) is noot connected"

    # Motor Setup
    mA = ev3.LargeMotor('outA')
    mA.run_direct()
    mB = ev3.LargeMotor('outB')
    mB.run_direct()

    line_follower(mA, mB, y)