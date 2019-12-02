#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import TouchSensor, ColorSensor
from ev3dev2.led import Leds
from time import sleep

# TODO: Add code here

    colour_s1 = ColorSensor(INPUT_1) # sensor 1 for light intensity
    colour_s2 = ColorSensor(INPUT_2) # sensor 2 for light intensity
        
    lm = LargeMotor(OUTPUT_B);  # left motor on PORT B
    rm = LargeMotor(OUTPUT_C);  # right motor on PORT C
    
    a = 0.6;
    
    d = a * (colour_s2.reflected_light_intensity()  - colour_s1.reflected_light_intensity())
    
    while True:

        if (colour_s2.reflected_light_intensity()  - colour_s1.reflected_light_intensity()) > d:
            
            lm.on_for_rotations(SpeedPercent(100), 2) # maybe change LEFT AND RIGHT
            rm.on_for_rotations(SpeedPercent(0), 2)
            
        elif (colour_s1.reflected_light_intensity()  - colour_s2.reflected_light_intensity()) > d:
            
            lm.on_for_rotations(SpeedPercent(0), 2) # maybe change LEFT AND RIGHT
            rm.on_for_rotations(SpeedPercent(100), 2)
            
        elif ((colour_s2.reflected_light_intensity()  - colour_s1.reflected_light_intensity()) <= d
                or (colour_s2.reflected_light_intensity()  - colour_s1.reflected_light_intensity()) * -1 <= d):
        
            lm.on_for_rotations(SpeedPercent(100), 2)
            rm.on_for_rotations(SpeedPercent(100), 2)
