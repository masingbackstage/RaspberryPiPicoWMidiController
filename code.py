import board
import digitalio
import asyncio
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
import adafruit_debouncer
from fsw_double_led import LED

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
    switch = adafruit_debouncer.Button(pin, 10, 500)
    switches.append(switch)

# Track the state of notes
note_states = [0] * len(button_pins)

# LED controller initialization 
red_led_pins =   [board.GP12, board.GP14, board.GP16, board.GP18]
green_led_pins = [board.GP13, board.GP15, board.GP17, board.GP19]
led_controllers = []
for i in range(4):
    led_controller = LED(red_led_pins[i],green_led_pins[i])
    led_controllers.append(led_controller)

async def handle_button(i, switch):
    while True:
        switch.update()
        if switch.long_press:  # Button pressed long
            note_states[i] = 1
            await led_controllers[i].long_press()  # Using the LED controller's long press method
        elif switch.pressed:  # Button pressed
            note_states[i] = 2
            await led_controllers[i].short_press()  # Using the LED controller's short press method
        elif switch.released:  # Button was released
            if note_states[i] == 1:
                print(note_mapping[i + 4])
                midi.send([NoteOn(note, 60) for note in note_mapping[i + 4]])
            elif note_states[i] == 2:
                print(note_mapping[i])
                midi.send([NoteOn(note, 60) for note in note_mapping[i]])

            print('released')
            midi.send([NoteOff(note, 0) for note in note_mapping[i]])
            midi.send([NoteOff(note, 0) for note in note_mapping[i + 4]])
            note_states[i] = 0

        await asyncio.sleep(0.01)

async def main():
    tasks = [asyncio.create_task(handle_button(i, switch)) for i, switch in enumerate(switches)]
    await asyncio.gather(*tasks)

# Start the asyncio event loop
asyncio.run(main())
