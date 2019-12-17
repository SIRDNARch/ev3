#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, LightSensor, UltrasonicSensor, ColorSensor
from ev3dev2.button import Button
from ev3dev2.sound import Sound
from ev3dev2.led import Leds
import time


light_s1 = LightSensor(INPUT_1) # sensor 1 for light intensity
light_s1.MODE_REFLECT = "REFLECT"
light_s2 = LightSensor(INPUT_2) # sensor 1 for light intensity
light_s2.MODE_REFLECT = "REFLECT"
light_s3 = ColorSensor(INPUT_3)
light_s3.mode = "COL-REFLECT"
usonic_s1 = UltrasonicSensor(INPUT_4)

left_m = LargeMotor(OUTPUT_A)
right_m = LargeMotor(OUTPUT_B) # left motor on PORT A right motor on PORT B
tank_drive = MoveTank(OUTPUT_A,OUTPUT_B) # left motor on PORT A right motor on PORT B'''
state = 0


def main():
    a = 0.4 #constant for the accuracy
    leftspeed =  SpeedPercent(40) # Speed in percent when driving straight
    rightspeed = SpeedPercent(40)
    #Button has to be pressed to start the initialization of d
    Sound().beep()
    while not Button().any():
        continue
    d = a * (light_s2.reflected_light_intensity - light_s1.reflected_light_intensity)
    black = light_s1.reflected_light_intensity * 1.1

    #time.sleep(2)
    #Button has to be pressed to start the while loop with the follow line procedure
    while not Button().any():
        continue

    Sound().beep()
    #time.sleep(2)

    while True:

        while not object_detection(20):
            s1 = light_s1.reflected_light_intensity
            s2 = light_s2.reflected_light_intensity
            follow_line(s1, s2, leftspeed, rightspeed, d, 0)
        left_m.polarity = "inversed"
        tank_drive.on_for_rotations(leftspeed, rightspeed, 1.6)
        left_m.polarity="normal"
        time.sleep(0.5)

        while not object_detection(20):
            s1 = light_s1.reflected_light_intensity
            s2 = light_s2.reflected_light_intensity
            follow_line(s1, s2, leftspeed, rightspeed, d,0)

        while object_detection(20):
            tank_drive.off()
            time.sleep(1)

        test = True
        while test:
            if light_s1.reflected_light_intensity <= black and light_s2.reflected_light_intensity <= black and light_s3.reflected_light_intensity <= black or object_detection(12):
                Sound().beep()
                test = False
            s1 = light_s1.reflected_light_intensity
            s2 = light_s2.reflected_light_intensity
            follow_line(s1, s2, leftspeed, rightspeed, d, 0.2)

        tank_drive.off()

        return

def object_detection(x: int) -> bool:
    if usonic_s1.distance_centimeters <= x:
        return True
    else:
        return False

def follow_line(s1: int, s2: int, leftspeed: float, rightspeed: float, d: float, t: float) -> int:
    if(s2-s1) > d:
        left_m.off()
        time.sleep(t)
        return 1
    if(s1-s2) > d:
        right_m.off()
        return 2
    tank_drive.on(leftspeed, rightspeed)
    return 3
if __name__ == '__main__':
    main()
