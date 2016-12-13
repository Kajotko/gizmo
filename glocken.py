#!/usr/bin/env python
# External module imports GPIO
import RPi.GPIO as GPIO
# Library to slow or give a rest to the script
import time

# Assign pins for each musical note and the drum input
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
GPIO.setup(Drum, GPIO.IN,pull_up_down=GPIO.PUD_DOWN) #drum pin set as input

GPIO.output(E, GPIO.LOW) #initial state of pins to prevent solenoids form overheating
GPIO.output(G, GPIO.LOW)
GPIO.output(B, GPIO.LOW)
GPIO.output(D, GPIO.LOW)

#trancribe songs into a list of tuples which contain pitch and length of each note, then add them to playlist list
playlist=[]
loopsong_short=[(E,1),(G, 0.5), (G,0.5),(B,1),(G,1),(B,0.5),(D,0.5),(B, 0.5),(G,0.5),(B,2),(G,1),(B,0.5),(B,0.5),(D,1),(B,1),(D,0.5),(B,0.5),(G,0.5),(E,0.5),(G,2)]
playlist.append(loopsong_short)

loopsong_long=[(E,1),(G, 0.5), (G,0.5),(B,1),(G,1),(B,0.5),(D,0.5),(B, 0.5),(G,0.5),(B,2),(G,1),(B,0.5),(B,0.5),(D,1),(B,1),(D,0.5),(B,0.5),(G,0.5),(E,0.5),(G,2),(B, 0.5),(B, 0.5),(B, 0.5),(B, 0.5),(D,1),(B,1),(B, 0.5),(B, 0.5),(D, 0.5),(B, 0.5),(G,2),(E, 1),(G, 0.5),(G, 0.5),(B,1),(G,1),(B, 0.5),(D, 0.5),(B, 0.5),(G, 0.5),(G,2)]
playlist.append(loopsong_long)

mc_donald=[(G, 0.5),(G, 0.5),(G, 0.5),(E, 0.5),(B, 0.5),(B, 0.5),(G, 1),(D, 0.5),(D, 0.5),(B, 0.5),(B, 0.5),(G,2),(G, 0.5),(G, 0.5),(G, 0.5),(E, 0.5),(B, 0.5),(B, 0.5),(G,1),(D, 0.5),(D, 0.5),(B, 0.5),(B, 0.5),(G, 1.5),(E,0.5),(B, 0.5),(B, 0.5),(B, 0.5),(E, 0.5),(B, 0.5),(B, 0.5),(B, 0.5),(E, 0.5),(B, 0.5),(E,0.5),(B, 0.5),(E, 0.5),(B, 0.5),(E,0.5),(B, 0.5),(E, 0.5),(G, 0.5),(G,0.5),(G, 0.5),(E, 0.5),(B, 0.5),(B,0.5),(G, 1),(D,0.5),(D, 0.5),(B, 0.5),(B, 0.5),(G,2)]
playlist.append(mc_donald)

#Allow user to choose which song to play
i=int(raw_input('Choose a song number:'))
song=playlist[i-1]

#Start a list to note timing of beats and define initial variables value
beat_times=[]
quiet=0 
note=0 #initial note, start playing from the beginning
bar=0 #keeps track how many notes in bar have been played
prev=0 #previous reading of the input pin, initially 0 before drum is hit
start_time = time.time()#registers current time

#Function to retrieve pitch and length of note from the list quickly
def pitch(note):
    return song[note][0]
def length(note):
    return song[note][1]

try:
    while 1:
        # The input() function will return either a True or False
        # indicating whether the pin is HIGH or LOW.
	drum=GPIO.input(Drum)
	#Define conditions to interpret input as a hit
        if drum and prev==False:
	    hit=True
	    #print 'Hit'
        else:
	    hit=False
	    #print 'Nothing'
	#overwrite previous reading with current reading to use in next loop iteration
	prev=drum
        if hit or bar!=int(bar):  #Drum detects a hit or the next note has to come between hits
            if bar>=4: #reset bar if a full bar has been played
                bar=0
            if bar == int(bar): #check if drum was hit
                start_time = time.time() #register time
                beat_times.append(start_time)
		if len(beat_times)<=4: #do not play glockenspiel for the first 4 beats
			time.sleep(0.1)
			continue
            else: #if the drum was not hit but the glockenspiel wants to play note between drum beats
		halfbeat=(beat_times[-1]-beat_times[-2])/2 #calculate half the time between beats
                time.sleep(halfbeat) #have glockenspiel wait
            if note == len(song):  # when you've reached the last note reset
                note = 0
            if quiet: #do not play if a 2-beat note has just been played, advance song
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
                quiet=1 #keep quiet for the next hit if so...
            else:
                note+=1 #...advance song if not
            time.sleep(0.1)
        else:  #Drum pin signal Low
            end_time = time.time() #note time now
            elapsed_time = (end_time - start_time)  #measure time since last beat
            if elapsed_time > 5:  # if drum has not been played in 5s reset song
                note = 0


except KeyboardInterrupt:  # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup()
