import storage
import board, digitalio

button = digitalio.DigitalInOut(board.GP6)
button.pull = digitalio.Pull.UP

button2 = digitalio.DigitalInOut(board.GP9)
button2.pull = digitalio.Pull.UP


if button.value and button2.value:
   storage.disable_usb_drive()