#!/usr/bin/python3

#### IMPORTS ####
import ev3dev.ev3 as ev3


#### CONSTANTS ####
REF_VALUE = 35
BASE_SPEED = 25


#### FUNCTIONS ####
def line_follower(mA, mB, y):
    error = REF_VALUE - y
    Kp = 0.9

    if (error < 0):
        mA.duty_cycle_sp = BASE_SPEED + abs(error) * Kp
        mB.duty_cycle_sp = BASE_SPEED - abs(error) * Kp

    elif (error > 0):
        mB.duty_cycle_sp = BASE_SPEED + abs(error) * Kp
        mA.duty_cycle_sp = BASE_SPEED - abs(error) * Kp

    else:
        mA.duty_cycle_sp = BASE_SPEED
        mB.duty_cycle_sp = BASE_SPEED