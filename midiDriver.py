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
NOTE_ON_MSG = 0x90
NOTE_OFF_MSG = 0x80
MIN_VEL = 0
MAX_VEL = 127

# initializes rtmidi: virtual midi output port
def init_rtmidi():
	midiout = rtmidi.MidiOut()
	available_ports = midiout.get_ports()

	if available_ports:
		midiout.open_port(0)
	else:
		midiout.open_virtual_port("Virtual AwDeOh")

	return midiout

# sends array of midi messages to update Massive parameters
# - messages: array of tuples
#	- [(control number, control state)]
def update_controls(messages):

	midiout = init_rtmidi()
	with midiout:

		for c_number, c_state in messages:
			print(f'control is {c_number}, value is {c_state}')
			ctrl_msg = [CH_MSG, c_number, c_state]
			midiout.send_message(ctrl_msg)

	del midiout

# send array of midi notes for Massive to play
# - notes: array of tuples
#	- [(note number, note duration in seconds)]
def play_notes(notes):

	midiout = init_rtmidi()
	with midiout:

		for note_num, note_dur in notes:
			print(f'note number is {note_num}, note duration is {note_dur}s, playing...', end=' ')
			# play note
			note_on_msg = [NOTE_ON_MSG, note_num, MAX_VEL]
			midiout.send_message(note_on_msg)
			time.sleep(note_dur)
			# stop note
			note_off_msg = [NOTE_OFF_MSG, note_num, MAX_VEL]
			midiout.send_message(note_off_msg)
			print('done')

	del midiout

# simple function that plays A @ 440Hz, MIDI note = 69
def test_tone():
	play_notes([(69, 2)])
