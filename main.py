import sounddevice as sd
import numpy
import pyenttec as dmx
import sys

motd = """
  ..---..  
 /       \      ／￣￣￣￣￣￣￣￣ ￣ ￣
|         |    <   MasterBulb v0.1
:         ;     ＼＿＿＿＿＿＿ ＿
 \  \~/  /
  `, Y ,'
   |_|_|
   |===|
   |===|
    \_/
"""
print(motd)

def print_sound(indata, frames, time, status):
	volume = numpy.linalg.norm(indata)*10
	dmx_value = int(max(min(255, ((volume / 1000) * 255)), 0))
	port.dmx_frame[5] = dmx_value
	port.render()
	bargraph = dmx_value / 8
	percentage = int(dmx_value / 2.55)
	sys.stdout.write(("\rListening: {0:0=2d}% - [" + ("#" * int(bargraph)).ljust(32," ")).format(percentage) + "]")
	sys.stdout.flush()

# Setup DMX Connection
print("------------------------------------------------------------")
print ("Let's do some setup...")
print("------------------------------------------------------------")
print("SOUND SETUP:")
sound_input = None
while sound_input == None:
	print("Available sound devices:")
	print(sd.query_devices())
	sound_input = int(input("Which device is your input? "))

print("Selected Device {}".format(sound_input))
print("------------------------------------------------------------")
print("DMX SETUP:")
port = dmx.select_port()
print("------------------------------------------------------------")
print (" (v)   I'm ready to speak now...")
print ("  =    Press Ctrl+C to kill me at any time.")
print("------------------------------------------------------------")


 

try:
	while True:
		with sd.InputStream(callback=print_sound, device=sound_input):
			sd.sleep(100000)
except KeyboardInterrupt:
	port.dmx_frame[5] = 0
	port.render()
	port.close()
	print("\rTerminated with Ctrl+C. See you tomorrow night!")
	pass




