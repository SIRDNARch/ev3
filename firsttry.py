#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import TouchSensor, ColorSensor
from ev3dev2.led import Leds
import time


colour_s1 = ColorSensor() # sensor 1 for light intensity
colour_s1.MODE_COL_REFLECT = "COL-REFLECT"

tank_drive = MoveTank(OUTPUT_A,OUTPUT_B) # left motor on PORT A right motor on PORT B

def main():   
    a = 0.6
    
    d = a * (5 - colour_s1.reflected_light_intensity())
 
    while True:
        if (5  - colour_s1.reflected_light_intensity()) > d:
      
            tank_drive.on_for_rotations(SpeedPercent(100),SpeedPercent(0), 2) # maybe change LEFT AND RIGHT
            
        elif (colour_s1.reflected_light_intensity()  - 5) > d:
         
            tank_drive.on_for_rotations(SpeedPercent(0),SpeedPercent(100), 2) # maybe change LEFT AND RIGHT
            
        elif (5  - colour_s1.reflected_light_intensity()) <= d or (5  - colour_s1.reflected_light_intensity() * -1 <= d):
        
            tank_drive.on_for_rotations(SpeedPercent(100),SpeedPercent(100), 2)
        
if __name__ == '__main__':
    main()
