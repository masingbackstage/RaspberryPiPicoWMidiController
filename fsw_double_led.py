import board
import digitalio
import asyncio

class LED:
    def __init__(self, pin1, pin2):
        self.red_led = digitalio.DigitalInOut(pin1)
        self.red_led.direction = digitalio.Direction.OUTPUT
        self.green_led = digitalio.DigitalInOut(pin2)
        self.green_led.direction = digitalio.Direction.OUTPUT

        self.red_led.value = True
        self.green_led.value = False

    async def short_press(self):
        self.red_led.value = not self.red_led.value
        self.green_led.value = not self.green_led.value

    async def long_press(self):
        end_time = asyncio.get_event_loop().time() + 0.5
        red_led_state = self.red_led
        while asyncio.get_event_loop().time() < end_time:
            if red_led_state == True:
                self.green_led.value = not self.green_led.value
            else:
                self.red_led.value = not self.red_led.value
            await asyncio.sleep(0.1)
        
        if red_led_state == True:
            self.red_led.value = True
            self.green_led.value = False
        else:
            self.red_led.value = False
            self.green_led.value = True
