#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
import time
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank

ts = TouchSensor()
leds = Leds()

def main():
    while True:
        if ts.is_pressed:
            leds.set_color("LEFT", "GREEN")
            leds.set_color("RIGHT", "GREEN")
            tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
            tank_drive.on(SpeedPercent(100), SpeedPercent(100))
        else:
            leds.set_color("LEFT", "RED")
            leds.set_color("RIGHT", "RED")
            tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
            tank_drive.on(SpeedPercent(0), SpeedPercent(0))


if __name__ == '__main__':
    main()
