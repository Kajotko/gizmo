#Works for the specific melody
#Does not account for single eighth notes
#does not account for full notes
#Notes played as drum is hit, eigths separated by fixed time=0.5s

!/usr/bin/env python
#External module imports GPIO
import RPi.GPIO as GPIO
# Library to slow or give a rest to the script
import time
import numpy as np
E = 11  # Broadcom pin 23 (P1 pin 16)
G = 13
B = 15
D = 17
Piezo=12
GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme

GPIO.setup(E, GPIO.OUT)  # glockenspiel pins set as output
GPIO.setup(G, GPIO.OUT)
GPIO.setup(B, GPIO.OUT)
GPIO.setup(D, GPIO.OUT)
GPIO.setup(Piezo, GPIO.IN) #piezo pin set as input

GPIO.output(E, GPIO.LOW) #initial state of pins
GPIO.output(G, GPIO.LOW)
GPIO.output(B, GPIO.LOW)
GPIO.output(D, GPIO.LOW)

song=[(E,1),(G, 0.5), (G,0.5),(B,1),(G,1),(B,0.5),(D,0.5),(B, 0.5),(G,0.5),(B,2),(G,1),(B,0.5),(B,0.5),(D,1),(B,1),(D,0.5),(B,0.5),(G,0.5),(E,0.5),(G,2)]

note=0 #initial note, start playing from the beginning
def pitch(note)
    return song[note][0]
def length(note):
    return song[note][1]

try:
    while 1:
        # The input() function will return either a True or False
        # indicating whether the pin is HIGH or LOW.
        if GPIO.input(Piezo):  #Piezo detects a hit
            start_time = time.time()
            if note == len(song):  # when you've reached the last note reset
                note = 0
            if quiet: #do not play if the halfnote has just been played, advance song
                quiet=0
                note+=1
            elif length(note)<1: #play two eigth notes before next hit and advance the song
                GPIO.output(pitch(note), GPIO.HIGH)
                time.sleep(0.05)
                GPIO.output(pitch(note), GPIO.LOW)
                time.sleep(0.5)
                note+=1
                GPIO.output(pitch(note), GPIO.HIGH)
                time.sleep(0.05)
                GPIO.output(pitch(note), GPIO.LOW)
                note += 1
            elif length(note)==1: #play quarter note then advance the song
                GPIO.output(pitch(note), GPIO.HIGH)
                time.sleep(0.05)
                GPIO.output(pitch(note), GPIO.LOW)
                note += 1
            else: #play half note, do not advance the song
                GPIO.output(pitch(note), GPIO.HIGH)
                time.sleep(0.05)
                GPIO.output(pitch(note), GPIO.LOW)
                quiet=1

        else:  # Piezo sends no signal i.e no hit detected:
            end_time = time.time()
            elapsed_time = (end_time - start_time) #* 1000000#measure time
            if elapsed_time>10:#if the timer is over 10 s reset note
                note=0



except KeyboardInterrupt:  # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup()
