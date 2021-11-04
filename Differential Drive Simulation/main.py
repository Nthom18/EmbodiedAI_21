'''
Simple simulation of differential drive line-following robot.

Author: Nicoline Louise Thomsen
Last update: 04-11-21
'''

import numpy as np
import time
import tkinter as tk

from behaviour_COPY import Behaviour
from robot_model import BOARD_SIZE, Robot


class Board(tk.Canvas):

    def __init__(self):

        BOARD_SIZE = 864

        super().__init__(width=BOARD_SIZE, height=BOARD_SIZE,
            background="gray99", highlightthickness=0)

        self.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height

        self.pack(side = tk.LEFT)

        # DRAW OBSTACLES (Circular obstacles x, y, r ; box obstacles x, y, w, h)
        # self.obstacleList_box = [[BOARD_SIZE/2, BOARD_SIZE/2, 50, BOARD_SIZE]]
        self.obstacleList_box = []
        self.obstacleList_circle = []

        self.drawObstacles_circle() 
        self.drawObstacles_box()


    def drawObstacles_circle(self):

        for x, y, r in self.obstacleList_circle:
            x0 = x - r
            y0 = y - r
            x1 = x + r
            y1 = y + r       
            
            self.create_oval(x0, y0, x1, y1, fill = "black", outline = "")


    def drawObstacles_box(self):

        for x, y, w, h in self.obstacleList_box:
            x0 = x - w/2
            y0 = y - h/2
            x1 = x + w/2
            y1 = y + h/2       
        
            self.create_rectangle(x0, y0, x1, y1, fill = "black", outline = "")


class Frame(tk.Frame,):

    def __init__(self):
        super().__init__()

        self.master.title('Differential Drive Simulation')
        self.board = Board()

        # background_image=tk.PhotoImage('Tracks/smudge.png')
        # background_label = tk.Label(self.board, image=background_image)
        # background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.pack()



def main():

    root = tk.Tk()
    root.resizable(width = False, height = False)

    canvas = Frame().board

    bg_img = tk.PhotoImage(file = 'Tracks/bw_vertical_blur.png')
    canvas.create_image(BOARD_SIZE/2, BOARD_SIZE/2, image=bg_img)

    bot = Robot(canvas, bg_img)
    control = Behaviour()



    # MAIN LOOP #####################################
    while True:

        bot.update(control.thrust_left, control.thrust_right)
        print(control.thrust_left, control.thrust_right)
        control.update(bot.sensor_light, 0)
        # print(bot.sensor_light)


        # Update GUI
        root.update_idletasks()
        root.update()
        time.sleep(0.01)



    root.destroy()



if __name__ == '__main__':
    main()
