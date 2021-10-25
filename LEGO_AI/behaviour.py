#!/usr/bin/python3

#### IMPORTS ####
import ev3dev.ev3 as ev3

#### CONSTANTS ####
# Sensors
REF_VALUE = 35
COMP_THRESHOLD = 10
BLACK = 1
WHITE = 0

# Motors
BASE_SPEED = 25


class Behavior:
    def __init__(self, mA, mB):

        self.state = 'init'
        
        self.motor_left = mA
        self.motor_right = mB


    def update(self, cl1, cl2):   # State Machine
        
        cl1_state = BLACK if cl1 < REF_VALUE else WHITE
        cl2_state = BLACK if cl2 < REF_VALUE else WHITE


        # STATE ACTIONS TODO: Call behaviours
        match self.state:
            case 'init':
                pass
            
            case 'solid line':
                pass

            case 'ghost line':
                pass

            case _:        
                pass


        # STATE CHANGING
        match self.state:
            case 'init':
                self.state = 'solid line'
            
            case 'solid line':
                if (cl1_state == WHITE and cl2_state == WHITE):
                    self.state = 'ghost line'
                else
                    self.state = 'solid line'

            case 'ghost line':
                if (cl1_state == BLACK or cl2_state == BLACK):
                    self.state = 'solid line'
                else
                    self.state = 'ghost line'

            case _:        
                self.state = 'init' # Default case

    
    def line_follow(self):
        pass


    # TODO - Find can
        # PID line following
        # Dottet line folowing 
        # Unconnected line searching
        # Wall following

    # TODO - Get can
        # Locate can
        # Hug can

    # TODO - Return can
        # Turn around
        # Same as find can with newly tuned PID


if __name__ == '__main__':
    pass

