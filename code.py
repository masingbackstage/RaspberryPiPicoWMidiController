import board
import digitalio
import time
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
import adafruit_debouncer

# MIDI initialization
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

print("Eagle")  

# Pin definitions for buttons
button_pins = [board.GP6, board.GP7, board.GP8, board.GP9]

# MIDI note mapping assigned to buttons
note_mapping = [["C3"], ["D3"], ["E3"], ["F3"], ["C4"], ["D4"], ["E4"], ["F4"]]

# Button initialization
pins = []
switches = []
for bp in button_pins:
    pin = digitalio.DigitalInOut(bp)
    pin.direction = digitalio.Direction.INPUT
    pin.pull = digitalio.Pull.UP
    pins.append(pin)
    # Debouncer initialization with DigitalInOut objects
    switch = adafruit_debouncer.Button(pin, 10, 1000)
    switches.append(switch)

# Track the state of notes
note_states = [False] * len(button_pins)




# Main loop
while True:
    for i, switch in enumerate(switches):
        switch.update()
        


        if switch.long_press:  # Button was pressed
            print(note_mapping[i + 4])
            midi.send([NoteOn(note, 60) for note in note_mapping[i + 4]])
            note_states[i] = True

        elif switch.pressed and not switch.long_press:
            print(note_mapping[i])
            midi.send([NoteOn(note, 60) for note in note_mapping[i]])
            note_states[i] = True  

        elif switch.released:  # Button was released
            print('not pressed')
            midi.send([NoteOff(note, 0) for note in note_mapping[i]])
            note_states[i] = False

    # Short delay before the next iteration
    time.sleep(0.01)