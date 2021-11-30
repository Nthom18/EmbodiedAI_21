#!/usr/bin/python3

import ev3dev.ev3 as ev3
import time

open = 1000
close = -1000

mC = ev3.MediumMotor('outC')
mC.run_direct()

mC.run_forever(speed_sp=open)

time.sleep(3.1)
mC.stop(stop_action="hold")

