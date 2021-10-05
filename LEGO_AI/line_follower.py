#!/usr/bin/python3

#### IMPORTS ####
import ev3dev.ev3 as ev3


#### CONSTANTS ####
REF_VALUE = 35
BASE_SPEED = 5


#### FUNCTIONS ####
def line_follower(mA, mB, y):
    error = REF_VALUE - y
    Kp = 1.2

    if (error < 0):
        mA.duty_cycle_sp = BASE_SPEED + abs(error) * Kp
        mB.duty_cycle_sp = BASE_SPEED - abs(error) * Kp

    if (error > 0):
        mB.duty_cycle_sp = BASE_SPEED + abs(error) * Kp
        mA.duty_cycle_sp = BASE_SPEED - abs(error) * Kp

