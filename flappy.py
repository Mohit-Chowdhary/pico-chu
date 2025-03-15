from machine import Pin, I2C
import ssd1306
import utime
import random

i2c = I2C(0, scl=Pin(17), sda=Pin(16))  # oled screen talk setup

oled = ssd1306.SSD1306_I2C(128, 64, i2c)  # screen size setting

button = Pin(14, Pin.IN, Pin.PULL_DOWN)  # flap button

GRAVITY = 1  # how fast bird falls
FLAP_STRENGTH = -4  # how much it goes up when u press
PIPE_WIDTH = 20
GAP_HEIGHT = 30  # space between pipes

bird_y = 32  # where bird starts
bird_velocity = 0  # speed of bird up/down

pipe_x = 128  # pipe starts offscreen
pipe_gap_y = random.randint(10, 40)  # pipe hole moves up/down

score = 0  # keep track of score

def draw():
    oled.fill(0)  # clear screen
    oled.rect(10, int(bird_y), 6, 6, 1)  # bird box
    oled.rect(pipe_x, 0, PIPE_WIDTH, pipe_gap_y, 1)  # top pipe
    oled.rect(pipe_x, pipe_gap_y + GAP_HEIGHT, PIPE_WIDTH, 64 - pipe_gap_y - GAP_HEIGHT, 1)  # bottom pipe
    oled.text(str(score), 60, 5, 1)  # score display
    oled.show()

def update():
    global bird_y, bird_velocity, pipe_x, pipe_gap_y, score
    
    bird_velocity += GRAVITY  # bird goes down coz gravity
    bird_y += bird_velocity  # update bird pos
    
    if button.value():
        bird_velocity = FLAP_STRENGTH  # bird jumps up
    
    pipe_x -= 2  # pipes move left
    if pipe_x < -PIPE_WIDTH:
        pipe_x = 128  # reset pipe to right
        pipe_gap_y = random.randint(10, 40)  # new hole place
        score += 1  # add score
    
    if bird_y < 0 or bird_y > 58:  # hit top or bottom
        return True  # game over
    if 10 < pipe_x < 16 and (bird_y < pipe_gap_y or bird_y > pipe_gap_y + GAP_HEIGHT):  # hit pipe
        return True  # game over
    
    return False  # game continues

def game_loop():
    global bird_y, bird_velocity, pipe_x, score
    
    bird_y = 32  # reset bird
    bird_velocity = 0
    pipe_x = 128  # reset pipe
    score = 0
    
    while True:
        if update():
            break  # stop loop if dead
        draw()
        utime.sleep(0.05)  # slow down game
    
    oled.fill(0)
    oled.text("game over!", 40, 25, 1)  # sad times
    oled.text("score: " + str(score), 45, 35, 1)  # show final score
    oled.show()
    utime.sleep(2)  # wait before restart

game_loop()  # start game
