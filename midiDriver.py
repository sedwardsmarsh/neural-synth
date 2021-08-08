# Midi command format explanation:
# - At least 1 command byte
# - Followed by 0, 1 or more additional bytes
# --------------------------------------------------------------------------
# We're using Channel messages which require two or three bytes. 
# - First byte is interpreted as two nybbles
#	- first nybble contains message name
#	- second nybble contains MIDI channel number
# - Second byte 2^[0, 127] can represent the control number (kind of knob).
# - Third byte 2^[0, 127] can represent the control state 
# --------------------------------------------------------------------------
# To update a parameter we want to send a "control change" message.
# --------------------------------------------------------------------------
# Information above is paraphrased from Yamaha "What's MIDI?" booklet
# Additional source: 
# https://www.circuitbread.com/tutorials/midi-controller-knobs-buttons
# --------------------------------------------------------------------------
# The Massive midi configurations for this project can be saved inside
# Massive. The conf. is recognized after closing and reopening Massive.
# Use midiMapper.py to make a new midi configuration for Massive.

# test 1, control a single oscillator:
# - Wt-position, Intensity, Amp

import time
import rtmidi

CH_MSG = 0xB0

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

if available_ports:
    midiout.open_port(0)
else:
    midiout.open_virtual_port("Virtual AwDeOh")

# sends array of midi messages to update Massive parameters
# - messages: array of tuples
#	- [(control number, control state)]
def update_controls(messages):
	
	with midiout:

		for control, value in messages:
			print(f'control is {control}, value is {value}')
			ctrl_msg = [CH_MSG, control, value]
			midiout.send_message(ctrl_msg)

	del midiout
