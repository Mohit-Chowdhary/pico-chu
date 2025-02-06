from picozero import pico_led
from picozero import LED
from time import sleep
pico_led.blink(on_time=1,off_time=1,n=10,wait=True)