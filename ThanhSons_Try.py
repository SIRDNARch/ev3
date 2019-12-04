#!/usr/bin/env python3
from ev3dev2 import *
from time import time, sleep

c1 = ColorSensor(INPUT_1)
c2 = ColorSensor(INPUT_2)

def run():

