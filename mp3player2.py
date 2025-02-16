from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
#import framebuff

# MicroPython SSD1306 OLED driver, I2C and SPI interfaces
import time
from time import sleep
from micropython import const
import framebuf



#
#
#
#
#
#
#



WIDTH=128
HEIGHT=64

# definde the i2c ports


# pico has 2 i2c ports
# I2C(which port (0/1), scl, sda)


i2c=I2C(0,scl=Pin(17),sda=Pin(16))
a=i2c.scan()
# this all chumma
print(a)
print("I2C ADDRESS	:	"+hex(i2c.scan()[0]).upper())
print("I2C CONFIG	:	"+str(i2c))
      
# assign oled as a 1306 display, and width height 128*64 and to which ports
# since i2c was defined before to ports
oled=SSD1306_I2C(WIDTH,HEIGHT,i2c)

# clear screem
oled.fill(0)


# define pins
button_next = Pin(0, Pin.IN, Pin.PULL_UP)  
button_play = Pin(2, Pin.IN, Pin.PULL_UP)  
button_prev = Pin(1, Pin.IN, Pin.PULL_UP) 
led = Pin(25, Pin.OUT) 


playing = True
strink = "Paused" # initialzed with paused for code convienince, below


def ifClicked(button, pin_num):
    """Detects a button press (press + release)."""
    global prev_state
    # .value()==0 is when its clicked
    if button.value() == 0: 
        time.sleep(0.05)  
        # untill the button is released
        while button.value() == 0:
            pass 
        # return yes this was clicked
        return True
    # .value()=1 if not pressed
    # return false, no button was not clicked
    return False

while True:
    oled.fill(0)
    if ifClicked(button_next, 15):
        strink = "Playing nxt song"
        # add code

    
    if ifClicked(button_play, 9):
        playing = not playing 
        strink = "Paused" if not playing else "Resumed"
        led.value(not playing)  
        # add code to "play/pause" song


    if ifClicked(button_prev, 3):
        strink = "Playing prv song"
        # add code


    # print onto screen
    oled.text(strink, 1, 20)  
    oled.show()


    # if prev,next button clicked, it displays it for 1 second and goes abck to playing again
    if(strink not in ["Resumed","Paused"]): # this was the code convienience 
        strink="Resumed"
        playing=True
        sleep(1)

    time.sleep(0.1)  

# the pasue/resume button works imperfectly during simulation somehow
