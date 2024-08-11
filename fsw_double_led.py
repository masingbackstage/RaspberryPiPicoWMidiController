import board
import digitalio
import asyncio
import time  # Use time for timing functions

class LED:
    def __init__(self, pin1, pin2):
        self.red_led = digitalio.DigitalInOut(pin1)
        self.red_led.direction = digitalio.Direction.OUTPUT
        self.green_led = digitalio.DigitalInOut(pin2)
        self.green_led.direction = digitalio.Direction.OUTPUT

        self.red_led.value = True
        self.green_led.value = False

    async def short_press(self):
        # Toggle the LED states
        self.red_led.value = not self.red_led.value
        self.green_led.value = not self.green_led.value

    async def long_press(self):
        # Use time.monotonic() instead of asyncio.get_event_loop().time()
        end_time = time.monotonic() + 0.5  # Set a 0.5 second timer
        red_led_state = self.red_led.value  # Capture the initial state of the red LED

        while time.monotonic() < end_time:
            if red_led_state:  # If the red LED was initially on
                self.green_led.value = not self.green_led.value
            else:  # If the red LED was initially off
                self.red_led.value = not self.red_led.value
            await asyncio.sleep(0.1)
        
        # Restore the LEDs to their original states after the loop
        if red_led_state:
            self.red_led.value = True
            self.green_led.value = False
        else:
            self.red_led.value = False
            self.green_led.value = True
