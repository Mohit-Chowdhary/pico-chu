from picozero import pico_led,LED, Button
from time import sleep

button = Button(18)

while True:
    if button.is_released:
        print("Button Released")
        pico_led.off()
    else:
        print("Button Pressed")
        pico_led.on()
    sleep(0.1)
