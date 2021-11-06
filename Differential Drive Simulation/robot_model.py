'''
Model of differential drive robot to draw in simulation

Author: Nicoline Louise Thomsen
Last update: 06-11-21
'''

import math
import numpy as np
import tkinter as tk


BOARD_SIZE = 864


class Robot():

    def __init__(self, canvas, track):
        self.canvas = canvas
        self.track = track

        self.init_flag = True

        self.size = 100
        self.position = [BOARD_SIZE/2, BOARD_SIZE/2]
        self.angle = 0
        self.angle_velocity = 0

        self.sensor_light = 0


    def update(self, control_left, control_right):

        self.diff_drive(control_left, control_right)

        self.robot_structure()


        sensor_reading = self.track.get(int(self.sensor_pos[0]), int(self.sensor_pos[1]))
        self.sensor_light = sum(sensor_reading) / 3

    
    def diff_drive(self, ur, ul):
        power_limit = 0.005

        scale = self.size / 200
        r = self.size - (50 * scale) / 2
        L = self.size + 30 * scale

        self.angle += ((ur - ul) * r / L) * power_limit

        # self.position[0] += (ul + ur) * math.cos(self.angle) * r/2 * power_limit
        # self.position[1] += (ul + ur) * math.sin(self.angle) * r/2 * power_limit
        # self.position[1] -= 0.1


    def robot_structure(self):
        
        if (self.init_flag == True):
            self.init_flag = False

        else:
            self.canvas.delete(self.robot_main_visual)
            self.canvas.delete(self.wheel_left_visual)
            self.canvas.delete(self.wheel_right_visual)
            self.canvas.delete(self.sensor_visual)


        scale = self.size / 200
        size_bot = 200 * scale
        wheel_width = 30 * scale
        wheel_margin = 50 * scale
        sensor_offset = [-0.1*self.size, -self.size/2 - 10]


        # Translation
        main_points = [
                [self.position[0] - size_bot/2, self.position[1] - size_bot/2],
                [self.position[0] + size_bot/2, self.position[1] - size_bot/2],
                [self.position[0] + size_bot/2, self.position[1] + size_bot/2],
                [self.position[0] - size_bot/2, self.position[1] + size_bot/2]]

        leftWhell_points = [
                [self.position[0] - size_bot/2 - wheel_width, self.position[1] - size_bot/2 + wheel_margin],
                [self.position[0] - size_bot/2, self.position[1] - size_bot/2 + wheel_margin],
                [self.position[0] - size_bot/2, self.position[1] + size_bot/2 - wheel_margin],
                [self.position[0] - size_bot/2 - wheel_width, self.position[1] + size_bot/2 - wheel_margin]]

        rightWhell_points = [
                [self.position[0] + size_bot/2 + wheel_width, self.position[1] - size_bot/2 + wheel_margin],
                [self.position[0] + size_bot/2, self.position[1] - size_bot/2 + wheel_margin],
                [self.position[0] + size_bot/2, self.position[1] + size_bot/2 - wheel_margin],
                [self.position[0] + size_bot/2 + wheel_width, self.position[1] + size_bot/2 - wheel_margin]]

        self.sensor_point = [self.position[0] + sensor_offset[0], self.position[1] + sensor_offset[1]]


        # Rotation
        self.robot_main_visual = self.rotate_polygon(main_points, self.angle, self.position, 'red')
        self.wheel_left_visual = self.rotate_polygon(leftWhell_points, self.angle, self.position, 'blue')
        self.wheel_right_visual = self.rotate_polygon(rightWhell_points, self.angle, self.position, 'blue')
        
        self.sensor_pos, self.sensor_visual = self.rotate_point(self.sensor_point, self.angle, 'green')


    def rotate_polygon(self, points, angle, centre, colour):
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


    def rotate_point(self, points, angle, colour):
        angle = math.radians(angle)
        
        x1 = math.cos(angle) * (points[0] - self.position[0]) - math.sin(angle) * (points[1] - self.position[1])
        y1 = math.sin(angle) * (points[0] - self.position[0]) + math.cos(angle) * (points[1] - self.position[1])

        new_pos = [x1 + self.position[0], y1 + self.position[1]]

        return new_pos, self.makeDot(new_pos, colour)


    def makeDot(self, centre, colour):

        x = int(centre[0])
        y = int(centre[1])

        x0 = x - 5
        y0 = y - 5
        x1 = x + 5
        y1 = y + 5
        
        return self.canvas.create_oval(x0, y0, x1, y1, fill = colour, outline = "")