# A utility script for building a midi mapping in Massive
# - in massive's menu: File > Options... > Midi
# - prefix each configuration in Massive with 'py'
# --------------------------------------------------------------------------
# Source: https://spotlightkid.github.io/python-rtmidi/#usage-example

import time
import rtmidi

CH_MSG = 0xB0

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

if available_ports:
    midiout.open_port(0)
else:
    midiout.open_virtual_port("My virtual output")

print('right click on control in Massive and select \'midi learn\'')
print('change the control value each time, to map to different controls')

control = 2

with midiout:
    print(f'control = {control} is mapped')
    ctrl_msg_left = [CH_MSG, control, 0]
    ctrl_msg_right = [CH_MSG, control, 127]
    midiout.send_message(ctrl_msg_left)
    time.sleep(0.1)
    midiout.send_message(ctrl_msg_right)
    time.sleep(0.1)

del midiout