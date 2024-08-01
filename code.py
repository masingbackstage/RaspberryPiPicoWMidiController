import board
import digitalio
import time
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

# MIDI initialization
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)
print("Orzel leci")  # "The eagle is flying" in Polish

# Pin definitions for buttons
button_pins = [board.GP6, board.GP7, board.GP8, board.GP9]

# MIDI note mapping assigned to buttons
note_mapping = [["C3"], ["D3"], ["E3"], ["F3"]]

# Button initialization
buttons = []
for bp in button_pins:
    button = digitalio.DigitalInOut(bp)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP
    buttons.append(button)

# States of buttons and their activations
pressed_keys = [False] * len(button_pins)
triggered_keys = [False] * len(button_pins)

# Debouncing time
debounce_time = 0.05  # 50 ms
last_time = [time.monotonic()] * len(button_pins)


while True:
    current_time = time.monotonic()
    for ix, btn in enumerate(buttons):
        if current_time - last_time[ix] > debounce_time:
            pressed = not btn.value
            if pressed != pressed_keys[ix]:
                pressed_keys[ix] = pressed
                last_time[ix] = current_time
                    
                if pressed and not triggered_keys[ix]:
                    print(f"note {ix} started")
                    midi.send([NoteOn(note, 60) for note in note_mapping[ix]])
                    triggered_keys[ix] = True
                elif not pressed and triggered_keys[ix]:
                    print(f"note {ix} stopped")
                    midi.send([NoteOff(note, 0) for note in note_mapping[ix]])
                    triggered_keys[ix] = False

    # Short delay before the next iteration
    time.sleep(0.01)