from picozero import pico_led,LED, Button
from time import sleep



while True:
    print("Button Released")
    pico_led.off()
    sleep(2)
    print("Button Pressed")
    pico_led.on()
    sleep(2)
