#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import TouchSensor, LightSensor
from ev3dev2.button import Button
from ev3dev2.sound import Sound
from ev3dev2.led import Leds
import time


light_s1 = LightSensor(INPUT_1) # sensor 1 for light intensity
light_s1.MODE_REFLECT = "REFLECT"
light_s2 = LightSensor(INPUT_2) # sensor 1 for light intensity
light_s2.MODE_REFLECT = "REFLECT"

left_m = LargeMotor(OUTPUT_A)
right_m = LargeMotor(OUTPUT_B) # left motor on PORT A right motor on PORT B
tank_drive = MoveTank(OUTPUT_A,OUTPUT_B) # left motor on PORT A right motor on PORT B'''

def main():   
    a = 0.4 #constant for the accuracy 
    leftspeed =  SpeedPercent(50) # Speed in percent when driving straight
    rightspeed = SpeedPercent(50)
    #Button has to be pressed to start the initialization of d
    while not Button().any():
        continue
    d = a * (light_s2.reflected_light_intensity - light_s1.reflected_light_intensity)
    Sound().beep()
    time.sleep(2)
    #Button has to be pressed to start the while loop with the follow line procedure
    while not Button().any():
        continue
        
    Sound().beep()
    time.sleep(2)
    
    while True:
        s1 = light_s1.reflected_light_intensity
        s2 = light_s2.reflected_light_intensity
        '''
        if (s2-s1) > d:
      
            tank_drive.on_for_rotations(SpeedPercent(0),SpeedPercent(20), 1) # maybe change LEFT AND RIGHT
            
        elif (s1-s2) > d:
         
            tank_drive.on_for_rotations(SpeedPercent(20),SpeedPercent(0), 1) # maybe change LEFT AND RIGHT
            
        elif (s2-s1) <= d or (s2-s1) * -1 <= d:
        
            tank_drive.on_for_rotations(SpeedPercent(5),SpeedPercent(5), 1)
        '''
        if(s2-s1) > d:
            left_m.off()
            continue
        if(s1-s2) > d:
            right_m.off()
            continue
        
        tank_drive.on(leftspeed, rightspeed)
            
if __name__ == '__main__':
    main()
