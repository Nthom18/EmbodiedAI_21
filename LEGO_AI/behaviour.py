#!/usr/bin/python3

#### IMPORTS ####
# import numpy as np

import constants
from math import sqrt


#### IMPORT CONSTANTS ####
# Sensors
REF_VALUE = constants.REF_VALUE
COMP_THRESHOLD = 10
BLACK = 1
WHITE = 0

# Motors
BASE_SPEED = constants.BASE_SPEED

# Robot Measurements
ROBOT_R = constants.R
ROBOT_L = constants.L


integral = 0
last_error = 0


class Behaviour:
    def __init__(self):

        self.state = 'init'

        self.thrust_left = 0
        self.thrust_right = 0

        # PID inits
        self.integral = 0
        self.last_error = 0

        self.control_input = 0
        self.base_speed = 0
        self.error = 0


    def update(self, cl_control, cl_check):   # State Machine
        
        control_state = BLACK if cl_control < REF_VALUE + 1 else WHITE
        check_state = BLACK if cl_check < REF_VALUE + 1 else WHITE


        # STATE CHANGING
        if (self.state == 'init'):
            self.state = 'solid line'
            # if (control_state == BLACK or check_state == BLACK):
            #     self.state = 'solid line'
            # else:
            #     self.state = 'ghost line'


        elif (self.state == 'solid line'):
            self.state = 'solid line'

            # if (control_state == WHITE and check_state == WHITE):
            #     self.state = 'ghost line'
            # else:
            #     self.state = 'solid line'


        # elif (self.state == 'ghost line'):
        #     if (control_state == BLACK or check_state == BLACK):
        #         self.state = 'solid line'
        #     else:
        #         self.state = 'ghost line'


        else:      
            self.state = 'init' # Default case


        # STATE ACTIONS
        if (self.state == 'init'):
            pass


        elif (self.state == 'solid line'):
            self.line_follow(cl_control, cl_check)
            # print("SOLID LINE")


        elif (self.state == 'ghost line'):
            self.leap_of_faith()
            # print("GHOST LINE")


        else:      
            pass


    def diff_drive(self, control):
        diff = (control * ROBOT_L/ROBOT_R) / 4   # Divide by 4 is to account for PWM 

        self.base_speed = -control * 2.1 + 30
        if self.base_speed < 0: self.base_speed = 0


        left = 30 - diff
        right = 30 + diff


        # PWM is percent -> max 100
        def actuate_pwm(pwm):
            if (abs(pwm) > 100):
                # pwm = np.sign(pwm) * 100    // No Numpy ;(
                if (pwm < 0):
                    pwm = -1 * 100
                else:
                    pwm = 100
            return(pwm)

        self.thrust_left = actuate_pwm(left)
        self.thrust_right = actuate_pwm(right)


    def line_follow(self, light_1, light_2):

        Kp, Ki, Kd = (0.5, 0, 0)

        # self.error = REF_VALUE - light_value
        # if abs(self.error) < 5: self.error = 0  # Error margin

        self.error = light_2 - light_1


        max_int = 100
        if (self.integral > max_int):   # Anti-windup
            self.integral += self.error
        
        derivative = self.error - self.last_error
        self.last_error = self.error

        self.control_input = self.error * Kp + self.integral * Ki + derivative * Kd

        self.diff_drive(self.control_input)


    def leap_of_faith(self):
        self.thrust_left    = BASE_SPEED
        self.thrust_right   = BASE_SPEED




    # TODO - Find can
        # Implement integrator wind-up
        # Ghost line folowing 
        # Keep track of last sensor to see black, to know if we're off track or the line has stopped.

    # TODO - Get can
        # Locate can
        # Hug can

    # TODO - Return can
        # Turn around
        # Same as find can with newly tuned PID


if __name__ == '__main__':

    Robot = Behaviour()

