#!/usr/bin/env python3
'''Hello to the world from ev3dev.org'''

import os
import sys
import time
from ev3dev.ev3 import *
import os
#import logging 
from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MoveDifferential
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor
from ev3dev2.led import Leds
from ev3dev2.wheel import EV3Tire
from ev3dev2.sound import Sound
from ev3dev2.button import Button

# from motor.py

from ev3dev2.motor import follow_for_forever, SpeedNativeUnits

from logging import getLogger


from ev3dev2.motor import (
    OUTPUT_B,
    OUTPUT_C,
    SpeedDPS,
    MoveTank,
    SpeedPercent,
    follow_for_ms,
    LineFollowErrorTooFast,
    LineFollowErrorLostLine
)

from ev3dev2.sensor import INPUT_1 , INPUT_2, INPUT_3 ,INPUT_4
from ev3dev2.sensor.lego import  ColorSensor ,UltrasonicSensor

""" LOGLEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
} """
IO = {
    "motor": MoveTank(OUTPUT_C, OUTPUT_B),
    "color": {"links": ColorSensor(INPUT_3),"vorne": ColorSensor(INPUT_2), "rechts": ColorSensor(INPUT_1) }, #"r": ColorSensor(INPUT_4)},
    #"touch": TouchSensor(INPUT_2),
    "distance": UltrasonicSensor(INPUT_4)
}

warte_counter = 0

steuerung = MoveDifferential(OUTPUT_C,OUTPUT_B,EV3Tire,140)

def Situation()->str:
    entfernung = False
    hell_links = True
    hell_rechts = True
    hell_vorne = True
    ret_str = "error"

    # check IO

    if IO["distance"].distance_centimeters < 7:
        entfernung = True
        #sound.speak("close object")
    
    if IO["color"]["links"].reflected_light_intensity < 9:
        hell_links = False
        #sound.speak("left dark")

    if IO["color"]["rechts"].reflected_light_intensity < 9:
        hell_rechts = False
        #sound.speak("right dark")
    
    if IO["color"]["vorne"].reflected_light_intensity < 9:
        hell_vorne = False
        #sound.speak("front dark")
        

    # set counter

    if entfernung == False:
        global warte_counter
        warte_counter = 0

    #set Flags

    
    if ((not hell_rechts) and (not hell_links) and (not hell_vorne) and (not entfernung) ):
        ret_str = "anykurve"
        return ret_str
    
    if ((not hell_rechts) and (not hell_links) and (not hell_vorne) and entfernung ):
        ret_str = "360Grad"
        return ret_str
    
    if ( hell_rechts and  hell_links and  hell_vorne ):
        ret_str = "vorw"
        return ret_str 

    if ( hell_rechts and  hell_links and  hell_vorne and entfernung):
            ret_str = "ende"
            return ret_str

    if ( hell_rechts and  hell_links and (not hell_vorne) and entfernung and (warte_counter == 0)): 
        ret_str = "warte"
        return ret_str

    if ( hell_rechts and (not hell_links) and (not hell_vorne)):
        ret_str = "Strichcode"
    
    if ((not hell_rechts ) and  hell_links ):
        ret_str = "linie_rechts"
        return ret_str

    if ( hell_rechts and  (not hell_links) ):
        ret_str = "linie_links"
        return ret_str

    if ( hell_rechts and  hell_links and (not hell_vorne) ):
        ret_str = "beschl"
        return ret_str
    
    if(hell_vorne and (not hell_rechts) and (not hell_links)):
        ret_str = "calibrate"


    """ if ((not hell_rechts) and  hell_links ):
        #ret_str = "rechtsk"
        ret_str = "linie_rechts"
        return ret_str

    if ( hell_rechts and  (not hell_links) and  hell_vorne ):
        #ret_str = "linksk"
        ret_str = "linie_links"
        return ret_str """

    

    

    """ if ( hell_rechts and  hell_links and (not hell_vorne) and entfernung and (warte_counter != 0) ):
        ret_str = "beschl"
        return ret_str """

    
    
    #sound.speak(ret_str)
    text = "distance  "+ str(entfernung) + "hell links  "+ str(hell_links) +"hell rechts  " + str(hell_rechts) + "hell vorne  " + str(hell_vorne) 
    debug_print(text)

    return ret_str






sound = Sound()
#logger = logging.getLogger(__name__)

sg= []

# state constants
ON = True
OFF = False

linienliste= ["links","rechts", "geradeaus"]

def linienanpassung():
    while(IO["color"]["hinten"].color != 1 ):
        #sound.speak('stay straight!')
        steuerung.turn_right(4,2)

def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.

    This shows up in the output panel in VS Code.
    '''
    print(*args, **kwargs, file=sys.stderr)


def reset_console():
    '''Resets the console to the default state'''
    print('\x1Bc', end='')


def set_cursor(state):
    '''Turn the cursor on or off'''
    if state:
        print('\x1B[?25h', end='')
    else:
        print('\x1B[?25l', end='')


def set_font(name):
    '''Sets the console font

    A full list of fonts can be found with `ls /usr/share/consolefonts`
    '''
    os.system('setfont ' + name)


def main():

    """  counter = 0
    ausgleichs_zaehler = 0
    #urnsignal = 0
    check = True """

    # NEUER TEIL

    st_speed = 80
    #ausgl_speed = 30
    beschl_speed = 25
    slow_speed = 15
    finish = False
    #old_select = linienliste[2]
    #select = linienliste[2]
    debug_print("start")
    normal_speed = st_speed
    p = 1.5

    while (not Button().any):
            continue

    while True:
        debug_print("start loop")

        
        #start_var = True

        sit = Situation()
        debug_print(sit)
        #debug_print("mid loop")

        if sit == "error":
            IO["motor"].stop
            #sound.speak("error")

        #if sit == "calibrate":
            #sound.speak("calibrate")

        if sit == "Strichcode":
        
            IO["motor"].on(0,0)
            IO["motor"].stop
            sound.speak = "code"
            steuerung.odometry_start()
            steuerung.on_for_distance(20,100)
            steuerung.odometry_stop()


        if sit == "anykurve":
            IO["motor"].on(0,0)
            IO["motor"].stop
            #sound.speak("any curve")
            steuerung.odometry_start()
            steuerung.turn_left(5,-90)
            steuerung.on_for_distance(15,80)
            steuerung.odometry_stop()

        """ if sit == "rechtsk":
            IO["motor"].stop
            sound.speak("right curve")
            steuerung.odometry_start
            steuerung.turn_right(5,-90)
            steuerung.on_for_distance(15,80)
            steuerung.odometry_stop

        if sit == "linksk":
            IO["motor"].stop
            sound.speak("left curve")
            steuerung.odometry_start
            steuerung.turn_left(5,-90)
            steuerung.on_for_distance(15,80)
            steuerung.odometry_stop

        if sit == "vorw":
            IO["motor"].on_for_rotations(st_speed,st_speed,0.35)"""

        if sit == "linie_rechts":
            p = 1.6
            normal_speed = slow_speed
        

        if sit == "linie_links":
            p = 1.6
            normal_speed = slow_speed

        
        if sit == "beschl":
            p = 2.4
            normal_speed = beschl_speed

        if sit == "360Grad":
            IO["motor"].on(0,0)
            IO["motor"].stop 
            #sound.speak(" 180")
            steuerung.odometry_start()
            steuerung.turn_to_angle(5,180)
            steuerung.on_for_distance(15,100)
            steuerung.odometry_stop()

        

        if sit == "warte":
            IO["motor"].on(0,0)
            IO["motor"].stop
            #sound.speak("Obstacle")
            time.sleep(10)
            global warte_counter
            warte_counter = warte_counter +1


        if sit == "ende":
            IO["motor"].on(0,0)
            IO["motor"].stop
            #sound.speak("finish!")
            finish = True

        if finish :
            break

        left_speed = normal_speed
        right_speed= normal_speed


        hell_r = IO["color"]["links"].reflected_light_intensity
        hell_l = IO["color"]["rechts"].reflected_light_intensity

        dif = hell_l - hell_r
        if dif < 2  and dif > -2:
            dif = 0

        debug_print(dif)

        

        """ if ((dif ) > 22):
            left_speed = slow_speed
            right_speed = ausgl_speed
            select = linienliste[1]

        if ((hell_r - hell_l ) > 22):
            right_speed = slow_speed
            left_speed = ausgl_speed
            select = linienliste[0] """

        
        
        """ if ((select != old_select) or start_var):
            old_select = select 
        else: 
            continue  """

        #debug_print(select)

        end_left_speed = SpeedPercent( (left_speed - p * dif) % 100)
        end_right_speed = SpeedPercent( (right_speed + p * dif ) % 100)
        
        debug_print(end_left_speed)
        debug_print(end_right_speed)

        IO["motor"].on(end_left_speed, end_right_speed)


        time.sleep(0.01)
        debug_print("end loop")


        
        

        #ALTER TEIL

        """ ausgleichs_zaehler = ausgleichs_zaehler +1
        if ausgleichs_zaehler > 5:
            ausgleichs_zaehler = 0
            counter = 0
        debug_print("counter: %d", counter) 

        if IO["color"]["v"].reflected_light_intensity > 25:
            counter = counter +1 
        #wenden!
        if counter > 1:    
            #check = not check
            counter = 0
            #sound.speak('Start turning!')
            steuerung.odometry_start()
             steuerung.turn_right(10,100)
            steuerung.on_for_distance(15,150)
            steuerung.turn_right(10,40)
            while IO["color"]["v"].color != 1:
                steuerung.on_for_distance(5,5)
            counter = 0
            steuerung.odometry_stop()
            #sound.speak('finished turning!')
            #turnsignal = 0  
            while IO["color"]["v"].color != 1:
                steuerung.turn_right(5,5)

        try:

            IO["motor"].cs = IO["color"]["v"]
            IO["motor"].follow_line(
                kp= 12, #kp,  # 10.2
                ki= 0.8 ,#ki,  # 0.05,
                kd=2, #kd,  # 5.00
                speed=SpeedPercent(12),
                target_light_intensity= 20,
                white=33,
                follow_left_edge=check,
                off_line_count_max=60,
                follow_for=follow_for_ms,
                ms=1000
                
            )
           
        except LineFollowErrorTooFast:
            IO["motor"].stop()
            #sound.speak("Error one!")
            
        except LineFollowErrorLostLine:
            IO["motor"].stop()
            #sound.speak("Error two!")
            # turnsignal = turnsignal +1
            

        if IO["distance"].distance_centimeters < 20:            
            #sound.speak('Obstacle!')
            time.sleep(10)  
        
        # set the console just how we want it
        reset_console()
        set_cursor(OFF)
        set_font('Lat15-Terminus24x12')

        # print something to the screen of the device
        print(counter) """






if __name__ == '__main__':
    main()
