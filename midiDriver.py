# Midi command format explanation:
# - At least 1 command byte
# - Followed by 0, 1 or more additional bytes
# --------------------------------------------------------------------------
# We're using Channel messages which require two or three bytes. 
# - First byte is interpreted as two nybbles
#	- first nybble contains message name
#	- second nybble contains MIDI channel number
# - Second byte 2^[0, 127] can represent the control number (kind of knob).
# - Third byte 2^[0, 127] can represent the signal value 
# --------------------------------------------------------------------------
# To update a parameter we want to send a "control change" message.
# --------------------------------------------------------------------------
# Information above is paraphrased from Yamaha "What's MIDI?" booklet
# Additional source: 
# https://www.circuitbread.com/tutorials/midi-controller-knobs-buttons

import time
import rtmidi

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

if available_ports:
    midiout.open_port(0)
else:
    midiout.open_virtual_port("My virtual output")

while True:
	with midiout:
		for i in range(3):
			print('new loop') 
			# channel 1, middle C, velocity 112
			note_on = [0x90, 60, 112]
			note_off = [0x80, 60, 0]
			midiout.send_message(note_on)
			time.sleep(0.5)
			midiout.send_message(note_off)
			time.sleep(0.1)

del midiout
