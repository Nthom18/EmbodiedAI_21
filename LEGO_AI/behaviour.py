#!/usr/bin/python3

#### IMPORTS ####
import numpy as np
# import ev3dev.ev3 as ev3

#### CONSTANTS ####
# Sensors
REF_VALUE = 35
COMP_THRESHOLD = 10
BLACK = 1
WHITE = 0

# Motors
BASE_SPEED = 25

# Robot Measurements
R = 2
L = 10


integral = 0
last_error = 0


class Behaviour:
    def __init__(self, mA, mB):

        self.state = 'init'
        
        self.motor_left = mA
        self.motor_right = mB

        # PID inits
        self.integral = 0
        self.last_error = 0


    def update(self, cl_control, cl_check):   # State Machine

        # print(self.state)
        
        cl1_state = BLACK if cl_control < REF_VALUE + 1 else WHITE
        cl2_state = BLACK if cl_check < REF_VALUE + 1 else WHITE


        # STATE CHANGING
        if (self.state == 'init'):
            self.state = 'solid line'


        elif (self.state == 'solid line'):
            if (cl1_state == WHITE and cl2_state == WHITE):
                self.state = 'ghost line'
            else:
                self.state = 'solid line'


        elif (self.state == 'ghost line'):
            if (cl1_state == BLACK or cl2_state == BLACK):
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


    def diff_drive(self, angle_v):
        diff = angle_v * L/R
        
        left = BASE_SPEED - diff / 2
        right = BASE_SPEED + diff / 2

        if (abs(left) > 100):
            left = np.sign(left) * 100
        if (abs(right) > 100):
            right = np.sign(right) * 100

        self.motor_left.duty_cycle_sp = left
        self.motor_right.duty_cycle_sp = right

        # print(left, right)


    def line_follow(self, light_value):

        Kp, Ki, Kd = (1, 0.5, 0.5)

        error = REF_VALUE - light_value
        self.integral += error
        derivative = error - self.last_error
        self.last_error = error

        control_input = error * Kp + self.integral * Ki + derivative * Kd

        self.diff_drive(control_input)


    def leap_of_faith(self):
        self.motor_left.duty_cycle_sp   = BASE_SPEED
        self.motor_right.duty_cycle_sp  = BASE_SPEED




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

    Robot = Behaviour(1, 1)

    Robot.update(50, 0)
    Robot.update(45, 0)
    Robot.update(40, 0)
    Robot.update(35, 0)
    Robot.update(30, 0)
    Robot.update(25, 0)
    Robot.update(30, 0)
    Robot.update(35, 0)
    Robot.update(35, 0)
    Robot.update(35, 0)

