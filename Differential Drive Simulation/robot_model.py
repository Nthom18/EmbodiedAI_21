'''
Model of two-wheeled differential drive robot 

Author: Nicoline Louise Thomsen
Last update: 06-11-21
'''

import math
import numpy as np
import tkinter as tk


class Robot():

    def __init__(self, canvas, track, start_pos, size):
        self.canvas = canvas
        self.track = track

        self.init_flag = True

        self.size = size
        self.position = start_pos
        self.angle = math.radians(-90)

        self.sensor_light = 0


    def update(self, control_left, control_right):



        self.diff_drive(control_left, control_right)
        # self.diff_drive(0, 0)

        self.robot_structure()


        sensor_reading = self.track.get(int(self.sensor_pos[0]), int(self.sensor_pos[1]))
        self.sensor_light = sum(sensor_reading) / 3


    def diff_drive(self, ul_pwm, ur_pwm):
        max_speed = 0.05

        ul = max_speed * ul_pwm / 100
        ur = max_speed * ur_pwm / 100

        scale = self.size / 200
        r = self.size - (50 * scale) * 2
        L = self.size + 30 * scale

        self.angle += ((ul - ur) * r / L)

        self.position[0] += (ul + ur) * math.cos(self.angle) * r/2
        self.position[1] += (ul + ur) * math.sin(self.angle) * r/2


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
        sensor_offset = [self.size/2 + 10, -0.1*self.size, ]


        # # Translation
        # main_points = [
        #         [self.position[0] - size_bot/2, self.position[1] - size_bot/2],
        #         [self.position[0] + size_bot/2, self.position[1] - size_bot/2],
        #         [self.position[0] + size_bot/2, self.position[1] + size_bot/2],
        #         [self.position[0] - size_bot/2, self.position[1] + size_bot/2]]

        # leftWhell_points = [
        #         [self.position[0] - size_bot/2 - wheel_width, self.position[1] - size_bot/2 + wheel_margin],
        #         [self.position[0] - size_bot/2, self.position[1] - size_bot/2 + wheel_margin],
        #         [self.position[0] - size_bot/2, self.position[1] + size_bot/2 - wheel_margin],
        #         [self.position[0] - size_bot/2 - wheel_width, self.position[1] + size_bot/2 - wheel_margin]]

        # rightWhell_points = [
        #         [self.position[0] + size_bot/2 + wheel_width, self.position[1] - size_bot/2 + wheel_margin],
        #         [self.position[0] + size_bot/2, self.position[1] - size_bot/2 + wheel_margin],
        #         [self.position[0] + size_bot/2, self.position[1] + size_bot/2 - wheel_margin],
        #         [self.position[0] + size_bot/2 + wheel_width, self.position[1] + size_bot/2 - wheel_margin]]

        # self.sensor_point = [self.position[0] + sensor_offset[0], self.position[1] + sensor_offset[1]]


                # Translation
        main_points = [
                [self.position[0] - size_bot/2, self.position[1] - size_bot/2],
                [self.position[0] + size_bot/2, self.position[1] - size_bot/2],
                [self.position[0] + size_bot/2, self.position[1] + size_bot/2],
                [self.position[0] - size_bot/2, self.position[1] + size_bot/2]]

        leftWhell_points = [
                [self.position[0] - size_bot/2 + wheel_margin, self.position[1] - size_bot/2 - wheel_width],
                [self.position[0] + size_bot/2 - wheel_margin, self.position[1] - size_bot/2 - wheel_width],
                [self.position[0] + size_bot/2 - wheel_margin, self.position[1] - size_bot/2],
                [self.position[0] - size_bot/2 + wheel_margin, self.position[1] - size_bot/2]]

        rightWhell_points = [
                [self.position[0] - size_bot/2 + wheel_margin, self.position[1] + size_bot/2],
                [self.position[0] + size_bot/2 - wheel_margin, self.position[1] + size_bot/2],
                [self.position[0] + size_bot/2 - wheel_margin, self.position[1] + size_bot/2 + wheel_width],
                [self.position[0] - size_bot/2 + wheel_margin, self.position[1] + size_bot/2 + wheel_width]]

        self.sensor_point = [self.position[0] + sensor_offset[0], self.position[1] + sensor_offset[1]]


        # Rotation
        self.robot_main_visual = self.rotate_polygon(main_points, self.angle, self.position, 'gray75')
        self.wheel_left_visual = self.rotate_polygon(leftWhell_points, self.angle, self.position, 'brown4')
        self.wheel_right_visual = self.rotate_polygon(rightWhell_points, self.angle, self.position, 'brown4')
        
        self.sensor_pos, self.sensor_visual = self.rotate_point(self.sensor_point, self.angle, 'SpringGreen2')


    def rotate_polygon(self, points, angle, centre, colour):
        # Code from: https://stackoverflow.com/questions/36620766/rotating-a-square-on-tkinter-canvas

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