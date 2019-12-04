#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import TouchSensor, LightSensor
from ev3dev2.led import Leds
import time


light_s1 = LightSensor(INPUT_1) # sensor 1 for light intensity
light_s1.MODE_REFLECT = "REFLECT"
light_s2 = LightSensor(INPUT_2) # sensor 1 for light intensity
light_s2.MODE_REFLECT = "REFLECT"

tank_drive = MoveTank(OUTPUT_A,OUTPUT_B) # left motor on PORT A right motor on PORT B

def main():   
    a = 0.4
    
    d = a * (light_s2.reflected_light_intensity - light_s1.reflected_light_intensity)
 
    while True:
        s1 = light_s1.reflected_light_intensity
        s2 = light_s2.reflected_light_intensity
        if (s2-s1) > d:
      
            tank_drive.on_for_rotations(SpeedPercent(0),SpeedPercent(20), 1) # maybe change LEFT AND RIGHT
            
        elif (s1-s2) > d:
         
            tank_drive.on_for_rotations(SpeedPercent(20),SpeedPercent(0), 1) # maybe change LEFT AND RIGHT
            
        elif (s2-s1) <= d or (s2-s1) * -1 <= d:
        
            tank_drive.on_for_rotations(SpeedPercent(5),SpeedPercent(5), 1)
        
if __name__ == '__main__':
    main()
