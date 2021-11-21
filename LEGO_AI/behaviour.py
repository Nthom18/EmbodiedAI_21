#!/usr/bin/python3

#### IMPORTS ####
# import numpy as np

import constants


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


    def update(self, cl_control, cl_check):   # State Machine

        # print(self.state)
        
        control_state = BLACK if cl_control < REF_VALUE + 1 else WHITE
        check_state = BLACK if cl_check < REF_VALUE + 1 else WHITE


        # STATE CHANGING
        if (self.state == 'init'):
            if (control_state == BLACK or check_state == BLACK):
                self.state = 'solid line'
            else:
                self.state = 'ghost line'


        elif (self.state == 'solid line'):
            if (control_state == WHITE and check_state == WHITE):
                self.state = 'ghost line'
            else:
                self.state = 'solid line'


        elif (self.state == 'ghost line'):
            if (control_state == BLACK or check_state == BLACK):
                self.state = 'solid line'
            else:
                self.state = 'ghost line'


        else:      
            self.state = 'init' # Default case


        # STATE ACTIONS
        if (self.state == 'init'):
            pass


        elif (self.state == 'solid line'):
            self.line_follow(cl_control)
            print("SOLID LINE")


        elif (self.state == 'ghost line'):
            self.leap_of_faith()
            print("GHOST LINE")


        else:      
            pass


    def diff_drive(self, angle_velocity):
        diff = angle_velocity * ROBOT_L/ROBOT_R
        
        left = BASE_SPEED - diff / 2
        right = BASE_SPEED + diff / 2

        # PWM is percent -> max 100
        if (abs(left) > 100):
            # left = np.sign(left) * 100    // No Numpy ;(
            if (left < 0):
                left = -1 * 100
            else:
                left = 100

        if (abs(right) > 100):
            # right = np.sign(right) * 100  // No Numpy ;(
            if (right < 0):
                right = -1 * 100
            else:
                right = 100

        self.thrust_left = left
        self.thrust_right = right

        print(left, right)


    def line_follow(self, light_value):

        Kp, Ki, Kd = (1, 0.5, 0.5)

        error = REF_VALUE - light_value
        self.integral += error
        derivative = error - self.last_error
        self.last_error = error

        control_input = error * Kp + self.integral * Ki + derivative * Kd

        self.diff_drive(control_input)


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

    Robot.update(50, 40)
    Robot.update(45, 36)
    Robot.update(40, 30)
    Robot.update(35, 25)
    Robot.update(30, 20)
    Robot.update(25, 15)
    Robot.update(30, 20)
    Robot.update(35, 25)
    Robot.update(35, 25)
    Robot.update(35, 25)

