#!/usr/bin/env python
# External module imports GPIO
import RPi.GPIO as GPIO
# Library to slow or give a rest to the script
import time

E = 18  
G = 23
B = 17
D = 22
Drum=19
GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme

GPIO.setup(E, GPIO.OUT)  # glockenspiel pins set as output
GPIO.setup(G, GPIO.OUT)
GPIO.setup(B, GPIO.OUT)
GPIO.setup(D, GPIO.OUT)
GPIO.setup(Drum, GPIO.IN,pull_up_down=GPIO.PUD_DOWN) #piezo pin set as input

GPIO.output(E, GPIO.LOW) #initial state of pins
GPIO.output(G, GPIO.LOW)
GPIO.output(B, GPIO.LOW)
GPIO.output(D, GPIO.LOW)

playlist=[]
loopsong_short=[(E,1),(G, 0.5), (G,0.5),(B,1),(G,1),(B,0.5),(D,0.5),(B, 0.5),(G,0.5),(B,2),(G,1),(B,0.5),(B,0.5),(D,1),(B,1),(D,0.5),(B,0.5),(G,0.5),(E,0.5),(G,2)]
playlist.append(loopsong_short)

loopsong_long=[(E,1),(G, 0.5), (G,0.5),(B,1),(G,1),(B,0.5),(D,0.5),(B, 0.5),(G,0.5),(B,2),(G,1),(B,0.5),(B,0.5),(D,1),(B,1),(D,0.5),(B,0.5),(G,0.5),(E,0.5),(G,2),(B, 0.5),(B, 0.5),(B, 0.5),(B, 0.5),(D,1),(B,1),(B, 0.5),(B, 0.5),(D, 0.5),(B, 0.5),(G,2),(E, 1),(G, 0.5),(G, 0.5),(B,1),(G,1),(B, 0.5),(D, 0.5),(B, 0.5),(G, 0.5),(G,2)]
playlist.append(loopsong_long)

mc_donald=[(G, 0.5),(G, 0.5),(G, 0.5),(E, 0.5),(B, 0.5),(B, 0.5),(G, 1),(D, 0.5),(D, 0.5),(B, 0.5),(B, 0.5),(G,2),(G, 0.5),(G, 0.5),(G, 0.5),(E, 0.5),(B, 0.5),(B, 0.5),(G,1),(D, 0.5),(D, 0.5),(B, 0.5),(B, 0.5),(G, 1.5),(E,0.5),(B, 0.5),(B, 0.5),(B, 0.5),(E, 0.5),(B, 0.5),(B, 0.5),(B, 0.5),(E, 0.5),(B, 0.5),(E,0.5),(B, 0.5),(E, 0.5),(B, 0.5),(E,0.5),(B, 0.5),(E, 0.5),(G, 0.5),(G,0.5),(G, 0.5),(E, 0.5),(B, 0.5),(B,0.5),(G, 1),(D,0.5),(D, 0.5),(B, 0.5),(B, 0.5),(G,2)]
playlist.append(mc_donald)

i=int(raw_input('Choose a song number:'))
song=playlist[i-1]
beat_times=[]
quiet=0
note=0 #initial note, start playing from the beginning
bar=0 #keeps track how many notes in bar have been played
start_time = time.time()
def pitch(note):
    return song[note][0]
def length(note):
    return song[note][1]

prev=0


try:
    while 1:
        # The input() function will return either a True or False
        # indicating whether the pin is HIGH or LOW.
	drum=GPIO.input(Drum)
        if drum and prev==False:
	    hit=True
	    #print 'Hit'
        else:
	    hit=False
	    #print 'Nothing'
	prev=drum
        if hit or bar!=int(bar):  #Piezo detects a hit or the next note has to come between hits
            if bar>=4: #reset bar if a full bar has been played
                bar=0
            if len(beat_times)>=2: #check if there have been at least 2 drum hits
                halfbeat=(beat_times[-1]-beat_times[-2])/2 #calculate half the time between beats
            else:
                halfbeat=0.5
            if bar == int(bar): #check if drum was hit
                start_time = time.time() #register time
                beat_times.append(start_time)
		if len(beat_times)<=4:
			time.sleep(0.1)
			continue
            else:
                time.sleep(halfbeat) #if the glockenspiel wants to play note between drum beats have it wait
            if note == len(song):  # when you've reached the last note reset
                note = 0
            if quiet: #do not play if the halfnote has just been played, advance song
                quiet=0
                note+=1
		time.sleep(0.1)
		continue
            else: #play note and add length to bar
                GPIO.output(pitch(note), GPIO.HIGH)
                time.sleep(0.05)
                GPIO.output(pitch(note), GPIO.LOW)
                bar += length(note)
            if length(note)>1: #check if a note longer than one has been played
                quiet=1 #keep quiet if so...
            else:
                note+=1 #...advance song if not
            time.sleep(0.1)
        else:  # Piezo sends no signal i.e no hit detected:
            end_time = time.time()
            elapsed_time = (end_time - start_time)  # * 1000000#measure time
            if elapsed_time > 10:  # if the timer is over 10 s reset note
                note = 0


except KeyboardInterrupt:  # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup()
