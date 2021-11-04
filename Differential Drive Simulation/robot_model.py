'''
Model of differential drive robot to draw in simulation

Author: Nicoline Louise Thomsen
Last update: 04-11-21
'''

import math
import numpy as np
import tkinter as tk


BOARD_SIZE = 864


class Robot():

    def __init__(self, canvas):
        self.canvas = canvas

        self.init_flag = True

        self.centre_pos = [BOARD_SIZE/2, BOARD_SIZE/2]
        self.angle = 45
        self.angle_velocity = 2

        null_vertices = [[0, 0],
                        [0, 0],
                        [0, 0],
                        [0, 0]]



    def update(self):
        
        self.angle += self.angle_velocity
        self.robot_structure()


    def robot_structure(self):

        centre_bot = [BOARD_SIZE/2, BOARD_SIZE/2]
        
        if (self.init_flag == True):
            
            self.init_flag = False

            scale = 0.5
            size_bot = 200 * scale
            wheel_width = 30 * scale
            wheel_margin = 50 * scale

            self.main_points = [
                    [centre_bot[0] - size_bot/2, centre_bot[1] - size_bot/2],
                    [centre_bot[0] + size_bot/2, centre_bot[1] - size_bot/2],
                    [centre_bot[0] + size_bot/2, centre_bot[1] + size_bot/2],
                    [centre_bot[0] - size_bot/2, centre_bot[1] + size_bot/2]]

            self.leftWhell_points = [
                    [centre_bot[0] - size_bot/2 - wheel_width, centre_bot[1] - size_bot/2 + wheel_margin],
                    [centre_bot[0] - size_bot/2, centre_bot[1] - size_bot/2 + wheel_margin],
                    [centre_bot[0] - size_bot/2, centre_bot[1] + size_bot/2 - wheel_margin],
                    [centre_bot[0] - size_bot/2 - wheel_width, centre_bot[1] + size_bot/2 - wheel_margin]]

            self.rightWhell_points = [
                    [centre_bot[0] + size_bot/2 + wheel_width, centre_bot[1] - size_bot/2 + wheel_margin],
                    [centre_bot[0] + size_bot/2, centre_bot[1] - size_bot/2 + wheel_margin],
                    [centre_bot[0] + size_bot/2, centre_bot[1] + size_bot/2 - wheel_margin],
                    [centre_bot[0] + size_bot/2 + wheel_width, centre_bot[1] + size_bot/2 - wheel_margin]]

        else:

            self.canvas.delete(self.robot_main)
            self.canvas.delete(self.wheel_left)
            self.canvas.delete(self.wheel_right)


        self.robot_main = self.rotate(self.main_points, self.angle, centre_bot, 'red')
        self.wheel_left = self.rotate(self.leftWhell_points, self.angle, centre_bot, 'blue')
        self.wheel_right = self.rotate(self.rightWhell_points, self.angle, centre_bot, 'blue')


    def rotate(self, points, angle, centre, colour):
        # Code from: https://stackoverflow.com/questions/36620766/rotating-a-square-on-tkinter-canvas

        angle = math.radians(angle)
        cos_val = math.cos(angle)
        sin_val = math.sin(angle)
        cx, cy = centre
        new_points = []
        
        for x_old, y_old in points:
            x_old -= cx
            y_old -= cy
            x_new = x_old * cos_val - y_old * sin_val
            y_new = x_old * sin_val + y_old * cos_val
            new_points.append([x_new + cx, y_new + cy])

        return self.canvas.create_polygon(new_points, fill=colour)
