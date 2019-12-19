#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, LightSensor, UltrasonicSensor, ColorSensor
from ev3dev2.button import Button
from ev3dev2.sound import Sound
from ev3dev2.led import Leds
import time

# light sensor 1 LEFT for light intensity
light_s1 = LightSensor(INPUT_1)
light_s1.MODE_REFLECT = "REFLECT"
# light sensor 2 RIGHT for light intensity
light_s2 = LightSensor(INPUT_2)
light_s2.MODE_REFLECT = "REFLECT"
# color sensor 3 MIDDLE for pattern detection
light_s3 = ColorSensor(INPUT_3)

# ultrasonic sensor for object detection
usonic_s1 = UltrasonicSensor(INPUT_4)
usonic_s1.MODE_US_DIST_CM = "US-DIST-CM"
#motors left motor on PORT A right motor on PORT B
left_m = LargeMotor(OUTPUT_A)
right_m = LargeMotor(OUTPUT_B)
tank_drive = MoveTank(OUTPUT_A,OUTPUT_B) # control both motors

def main():
    #variables
    diff = ((light_s1.reflected_light_intensity + light_s2.reflected_light_intensity)/2 - light_s3.reflected_light_intensity)/3
    white = (light_s1.reflected_light_intensity + light_s2.reflected_light_intensity)/2
    black = light_s3.reflected_light_intensity
    up_threshold = abs((2*white+black)/3)
    low_threshold = abs((white+2*black)/3)
    max_speed = SpeedPercent(100)

    #follow till detecting object then turn
    while(not object_detection(20)):
        follow_line_return(light_s1, light_s3, light_s2, diff, up_threshold, low_threshold, max_speed)
    #TURN HERE

    while not object_detection(10):
        follow_line_return(light_s1, light_s3, light_s2, diff, up_threshold, low_threshold, max_speed)
    tank_drive.off()
    while object_detection(20):
        continue

def follow_line_idontgetit(left: int, mid: int, right: int, diff: int, up_threshold: int, low_threshold: int, max_speed: int):
    if abs(left - mid) > diff and abs(right - mid) > diff: #mid black, left and right white !
        if left_m.speed != right_m.speed:
            left_m_speed = left_m.speed
            right_m_speed = right_m.speed
            tank_drive.on(max_speed, max_speed)
            for i in range(25):
                state = follow_line_return(light_s1, light_s3, light_s2, diff, up_threshold, low_threshold, max_speed)
                if left_m.speed != right_m.speed:
                    return state
                time.sleep(0.1)
            tank_drive.on(left_m_speed/2, right_m_speed/2)
            time.sleep(0.25)
    if left - right > diff: #left white, right black
        if mid - right > diff: # mid also white
            right_m.polarity = "inversed"
            tank_drive.on(max_speed, max_speed/5)
            right_m.polarity = "normal"
        else:                   # mid is also black 
            right_m.polarity = "inversed"
            tank_drive.on(max_speed, max_speed/3)
            right_m.polarity = "normal"
        return 1
    if right - left > diff: #left black, right white
        if mid - left > diff: # mid also white
            left_m.polarity = "inversed"
            tank_drive.on(max_speed/5, max_speed)
            left_m.polarity = "normal"
        else:                   # mid is also black 
            left_m.polarity = "inversed"
            tank_drive.on(max_speed/3, max_speed)
            left_m.polarity = "normal"
        return 2
    if left > up_threshold and mid > up_threshold and right > up_threshold: # all white
        # was line mid 
        left_m.polarity = "inversed"
        right_m.polarity =  "inversed"
        tank_drive.on(max_speed/2, max_speed/2)
        left_m.polarity = "normal"
        right_m.polarity =  "normal"
        while light_s1.reflected_light_intensity > low_threshold and light_s3.reflected_light_intensity > low_threshold and light_s2.reflected_light_intensity > low_threshold:
            continue
        time.sleep(0.5)
        if abs(light_s1.reflected_light_intensity - light_s3.reflected_light_intensity) < diff or abs(light_s2.reflected_light_intensity - light_s3.reflected_light_intensity) < diff or abs(light_s1.reflected_light_intensity - light_s2.reflected_light_intensity) < diff:
            return 3
        # go right if line was mid
        tank_drive.on(max_speed, max_speed)
        time.sleep(3)
        right_m.polarity = "inversed"
        tank_drive.on(max_speed*0.65, max_speed*0.65)
        right_m.polarity = "normal"
        time.sleep(3,5)
        while (light_s1.reflected_light_intensity + light_s2.reflected_light_intensity + light_s3.reflected_light_intensity)/3 > up_threshold:
            continue
        return 4
    if (left+ mid + right)/3 < low_threshold: # all black
        tank_drive.off()
        return 5
    return 6
def object_detection(distance: int) -> bool:
    if usonic_s1.distance_centimeters <= distance:
        return True
    else:
        return False

def follow_line_return(left: int, mid: int, right: int, diff: int, up_threshold: int, low_threshold: int, max_speed: int) -> int:
    if left - mid > diff and right - mid > diff: #mid black, left and right white !
        tank_drive.on(max_speed, max_speed)
        return 0
    if left - right > diff: #left white, right black
        if mid - right > diff: # mid also white
            right_m.polarity = "inversed"
            tank_drive.on(max_speed, max_speed/5)
            right_m.polarity = "normal"
        else:                   # mid is also black 
            right_m.polarity = "inversed"
            tank_drive.on(max_speed, max_speed/3)
            right_m.polarity = "normal"
        return 1
    if right - left > diff: #left black, right white
        if mid - left > diff: # mid also white
            left_m.polarity = "inversed"
            tank_drive.on(max_speed/5, max_speed)
            left_m.polarity = "normal"
        else:                   # mid is also black 
            left_m.polarity = "inversed"
            tank_drive.on(max_speed/3, max_speed)
            left_m.polarity = "normal"
        return 2
    if left > up_threshold and mid > up_threshold and right > up_threshold: # all white
        # was line mid 
        left_m.polarity = "inversed"
        right_m.polarity =  "inversed"
        tank_drive.on(max_speed/2, max_speed/2)
        left_m.polarity = "normal"
        right_m.polarity =  "normal"
        while light_s1.reflected_light_intensity > low_threshold and light_s3.reflected_light_intensity > low_threshold and light_s2.reflected_light_intensity > low_threshold:
            continue
        time.sleep(0.5)
        if abs(light_s1.reflected_light_intensity - light_s3.reflected_light_intensity) < diff or abs(light_s2.reflected_light_intensity - light_s3.reflected_light_intensity) < diff or abs(light_s1.reflected_light_intensity - light_s2.reflected_light_intensity) < diff:
            return 3
        # go right if line was mid
        tank_drive.on(max_speed, max_speed)
        time.sleep(3)
        right_m.polarity = "inversed"
        tank_drive.on(max_speed*0.65, max_speed*0.65)
        right_m.polarity = "normal"
        time.sleep(3,5)
        while (light_s1.reflected_light_intensity + light_s2.reflected_light_intensity + light_s3.reflected_light_intensity)/3 > up_threshold:
            continue
        return 4
    if (left+ mid + right)/3 < low_threshold: # all black
        tank_drive.off()
        return 5
    return 6


if __name__ == "__main__":
    main()
