import board
import digitalio
import time
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

# Inicjalizacja MIDI
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)
print("Orzel leci")

# Definicje pinów dla przycisków
button_pins = [board.GP6, board.GP7, board.GP8, board.GP9]

# Mapa nut MIDI przypisana do przycisków
note_mapping = [["C3"], ["D3"], ["E3"], ["F3"], ["C4"], ["D4"], ["E4"], ["F4"]]

# Inicjalizacja przycisków
buttons = []
for bp in button_pins:
    button = digitalio.DigitalInOut(bp)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP
    buttons.append(button)

# Stany przycisków i ich aktywacje
pressed_keys = [False] * len(button_pins)
triggered_keys = [False] * len(button_pins)

# Czas do debouncingu
debounce_time = 0.05  # 50 ms
last_time = [time.monotonic()] * len(button_pins)

# Funkcja do obliczenia oktawy wyżej
def octave_up(note):
    note_name = note[:-1]
    octave = int(note[-1])
    return note_name + str(octave + 1)

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

    # Krótkie opóźnienie przed kolejną iteracją
    time.sleep(0.01)
