#!/usr/bin/python3

#### IMPORTS ####
# import numpy as np

import constants
from math import sqrt

# from ev3dev2.sound import Sound
# # Speaker setup
# speaker = Sound()


#### IMPORT CONSTANTS ####
# Sensors
REF_BLACK = constants.REF_BLACK
REF_WHITE = constants.REF_WHITE
COMP_THRESHOLD = 10
BLACK = 1
WHITE = 0
GRAY = 2
TIME_OUT = 14
# TIME_OUT = 11

# Motors
BASE_SPEED = constants.BASE_SPEED

# Robot Measurements
ROBOT_R = constants.R
ROBOT_L = constants.L

# Control
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

        self.last_seen = [999, 999]
        
        self.hug_flag = False


    def update(self, cl_left, cl_right, hugged):   # State Machine
        sharp_direction = 'null'
        
        # control_left = BLACK if cl_left < REF_BLACK + 1 else WHITE

        if (cl_left < REF_BLACK):
            control_left = BLACK
        elif (cl_left > REF_WHITE):
            control_left = WHITE
        else:
            control_left = GRAY

        if (cl_right < REF_BLACK):
            control_right = BLACK
        elif (cl_right > REF_WHITE):
            control_right = WHITE
        else:
            control_right = GRAY


        if (control_left == BLACK):
            self.last_seen[0] = 0
        else:
            self.last_seen[0] += 1
    
        if (control_right == BLACK):
            self.last_seen[1] = 0
        else:
            self.last_seen[1] += 1


        # STATE CHANGING
        if (self.state == 'init'):
            if (control_left != WHITE or control_right != WHITE):
                self.state = 'solid line'


        elif (self.state == 'solid line'):
            if (control_left == WHITE and control_right == WHITE):
                if((self.last_seen[0] < TIME_OUT) or (self.last_seen[1] < TIME_OUT)):
                    self.state = 'sharp corner'
                    sharp_direction = 'left' if self.last_seen[0] < self.last_seen[1] else 'right'

                else:
                    self.state = 'ghost line'
                    
            elif(hugged == True and self.hug_flag == False):
                self.hug_flag = True
                self.state = 'retrieve can'

            else:
                self.state = 'solid line'
                

        elif (self.state == 'sharp corner'):
            cond1 = (control_left == GRAY and control_right == BLACK)
            cond2 = (control_left == BLACK and control_right == GRAY)
            if (cond1 or cond2):
                self.state = 'solid line'
                
            elif(hugged == True and self.hug_flag == False):
                self.hug_flag = True
                self.state = 'retrieve can'
                
            else:
                self.state = 'sharp corner'


        elif (self.state == 'ghost line'):
            if (control_left != WHITE or control_right != WHITE):
                self.state = 'solid line'
                
            elif(hugged == True and self.hug_flag == False):
                self.hug_flag = True
                self.state = 'retrieve can'
                
            else:
                self.state = 'ghost line'
                
                
        elif (self.state == 'retrieve can'):
            if(control_left == BLACK):  # Turning counter clockwise
                self.state = 'sharp corner'
            else:
                self.state = 'retrieve can'
  

        else:      
            self.state = 'init' # Default case



        # STATE ACTIONS
        if (self.state == 'init'):
            pass


        elif (self.state == 'solid line'):
            self.line_follow(cl_left, cl_right)
            
            
        elif (self.state == 'sharp corner'):            
            self.sharp_turn(sharp_direction)


        elif (self.state == 'ghost line'):
            self.leap_of_faith()
            
        
        elif (self.state == 'retrieve can'):
            self.sharp_turn('left')


        else:      
            pass


    def diff_drive(self, control):
        diff = (control * ROBOT_L/ROBOT_R) / 4   # Divide by 4 is to account for PWM 

        # self.base_speed = -control + 40
        # if self.base_speed < 0: self.base_speed = 0
        
        self.base_speed = 30

        left = self.base_speed + diff
        right = self.base_speed - diff


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


    def line_follow(self, light_left, light_right):

        Kp, Ki, Kd = (0.3, 0, 0)

        # self.error = REF_VALUE - light_value
        # if abs(self.error) < 5: self.error = 0  # Error margin

        self.error = light_left - light_right


        max_int = 100
        if (self.integral > max_int):   # Anti-windup
            self.integral += self.error
        
        derivative = self.error - self.last_error
        self.last_error = self.error

        self.control_input = self.error * Kp + self.integral * Ki + derivative * Kd

        self.diff_drive(self.control_input)


    def sharp_turn(self, sharp_direction):
        if (sharp_direction == 'left'):
            self.thrust_left = - BASE_SPEED - 4
            self.thrust_right = BASE_SPEED
        elif (sharp_direction == 'right'):
            self.thrust_left = BASE_SPEED + 4
            self.thrust_right = - BASE_SPEED


    def leap_of_faith(self):
        self.thrust_left    = BASE_SPEED + 4    # Left wheel too slow
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

