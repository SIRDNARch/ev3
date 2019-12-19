#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, LightSensor, UltrasonicSensor, ColorSensor
from ev3dev2.button import Button
from ev3dev2.sound import Sound
from ev3dev2.led import Leds
import time


light_left = LightSensor(INPUT_1) #left for light intensity
light_left.MODE_REFLECT = "REFLECT"

light_right = LightSensor(INPUT_2) #right for light intensity
light_right.MODE_REFLECT = "REFLECT"

light_mid = ColorSensor(INPUT_3) #mid for light intensity
light_mid.mode = "COL-REFLECT"

usonic_sensor = UltrasonicSensor(INPUT_4)#Ultrasonic Sensor for object detection

#left motor on PORT A right motor on PORT B
left_m = LargeMotor(OUTPUT_A)
right_m = LargeMotor(OUTPUT_B)
tank_drive = MoveTank(OUTPUT_A,OUTPUT_B) 


def main():
    a = 0.4 #constant for the accuracy
    max_speed = SpeedPercent(100)
    left_speed = SpeedPercent(40)
    right_speed = SpeedPercent(40)
    #beep when ready
    Sound().beep()
    #button has to be pressed to start the initialization of d
    while not Button().any():
        continue
    white = (light_right.reflected_light_intensity + light_left.reflected_light_intensity)/2
    black = light_mid.reflected_light_intensity
    d = white - black * a # difference between white and black
    two_white = (2*white + black)/3
    two_black = (white + 2*black)/3

    #button has to be pressed to start the while loop with the follow line procedure
    while not Button().any():
        continue
    #beed when done with initialization
    Sound().beep()

    while True:
        #follow line till sensor detects object
        while not object_detection(20):
            follow_line(light_left.reflected_light_intensity, light_right.reflected_light_intensity, light_mid.reflected_light_intensity, max_speed, left_speed, right_speed, d, two_black, two_white)

        # turn around
        left_m.polarity = "inversed"
        tank_drive.on_for_rotations(left_speed, right_speed, 1.6)
        left_m.polarity="normal"
        time.sleep(0.5)

        #follow line till sensor detects object
        while not object_detection(20):
            follow_line(light_left.reflected_light_intensity, light_right.reflected_light_intensity, light_mid.reflected_light_intensity, max_speed, left_speed, right_speed, d, two_black, two_white)

        #wait till object gets removed
        while object_detection(20):
            tank_drive.off()
            time.sleep(0.5)

        #follow till sensor detect all black then stop !
        while not follow_line(light_left.reflected_light_intensity, light_right.reflected_light_intensity, light_mid.reflected_light_intensity, max_speed, left_speed, right_speed, d, two_black, two_white) == 3:
            continue
        tank_drive.off()
        return # end of test line / stop program


def object_detection(x: int) -> bool:
    if usonic_sensor.distance_centimeters <= x:
        return True
    else:
        return False

def follow_line(left: int, right: int, mid: int, max_speed: float, left_speed: float, right_speed: float, d: float, two_black: float, two_white: float) -> int:
    if left-mid > d and right - mid > d: # left AND right white, mid black
        tank_drive.on(max_speed/2.5, max_speed/2.5)
        return 0
    if(right-left) > d: #left black
        left_m.off()
        if(mid-left) > d: #mid white
            right_m.on(max_speed/2)
        else:              #mid black
            right_m.on(max_speed/3)
        return 1
    if(left-right) > d: #right black
        right_m.off()
        if(mid-right) > d: #mid white
            left_m.on(max_speed/2)
        else:              #mid black
            left_m.on(max_speed/3)
        return 2
    if (left+right+mid)/3 < two_black: #all three black
        return 3
        #return 4
    if (left+right+mid)/3 > two_white: #all three white
        #try to detect code
        left_m.polarity = "inversed"
        right_m.polarity = "inversed"
        tank_drive.on(max_speed/2, max_speed/2)
        while light_left.reflected_light_intensity > two_black and light_mid.reflected_light_intensity > two_black and light_right.reflected_light_intensity > two_black:
            continue
        time.sleep(0.5)
        if abs(light_left.reflected_light_intensity - light_mid.reflected_light_intensity) < d or abs(light_right.reflected_light_intensity - light_mid.reflected_light_intensity):
            return 5
        #code detected then go right PROBABLY NOT CORRECT NEEDS TO BE TESTED MAYBE DO IT IN main() method
        left_m.polarity = "normal"
        right_m.polarity = "normal"
        tank_drive.on(max_speed/2, max_speed/2)
        time.sleep(2)
        right_m.polarity = "inversed"
        tank_drive.on(0.65*max_speed, 0.65*max_speed)
        time.sleep(2)

        while (left+right+mid)/3 > two_white:
            continue
        return 6
    return 7 #if something went wrong

if __name__ == '__main__':
    main()
