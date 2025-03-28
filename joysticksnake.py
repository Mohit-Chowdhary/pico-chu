from machine import Pin, ADC, I2C
import time
import random
from micropython import const
import framebuf
from ssd1306 import SSD1306_I2C


WIDTH = 128
HEIGHT = 64
SNAKE_SIZE = 8

# Initialize I2C and OLED
i2c = I2C(0, scl=Pin(17), sda=Pin(16))
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

# Initialize Joystick
joy_x = ADC(Pin(27))  # X-axis
joy_y = ADC(Pin(26))  # Y-axis
joy_button = Pin(22, Pin.IN, Pin.PULL_UP)

THRESHOLD_LOW = 30000
THRESHOLD_HIGH = 40000

def read_joystick():
    x_val = joy_x.read_u16() 
    y_val = joy_y.read_u16()
    
    if x_val < THRESHOLD_LOW:
        return "LEFT"
    elif x_val > THRESHOLD_HIGH:
        return "RIGHT"
    elif y_val < THRESHOLD_LOW:
        return "UP"
    elif y_val > THRESHOLD_HIGH:
        return "DOWN"
    
    return None

# Snake initialization
snake = [(64, 32)]
direction = "RIGHT"
food = (random.randint(0, WIDTH // SNAKE_SIZE - 1) * SNAKE_SIZE, 
        random.randint(0, HEIGHT // SNAKE_SIZE - 1) * SNAKE_SIZE)
score = 0
speed = 0.2

def move_snake():
    global food, direction, snake, score
    head_x, head_y = snake[0]
    
    if direction == "UP":
        head_y -= SNAKE_SIZE
    elif direction == "DOWN":
        head_y += SNAKE_SIZE
    elif direction == "LEFT":
        head_x -= SNAKE_SIZE
    elif direction == "RIGHT":
        head_x += SNAKE_SIZE
    
    head_x %= WIDTH  # Wrap around edges
    head_y %= HEIGHT
    
    new_head = (head_x, head_y)
    if new_head in snake:
        return False  # Game over
    
    snake.insert(0, new_head)
    
    if new_head == food:
        score += 1
        food = (random.randint(0, WIDTH // SNAKE_SIZE - 1) * SNAKE_SIZE,
                random.randint(0, HEIGHT // SNAKE_SIZE - 1) * SNAKE_SIZE)
    else:
        snake.pop()
    
    return True

while True:
    oled.fill(0)
    new_direction = read_joystick()
    if new_direction and new_direction != direction:
        if not (direction == "UP" and new_direction == "DOWN" or
                direction == "DOWN" and new_direction == "UP" or
                direction == "LEFT" and new_direction == "RIGHT" or
                direction == "RIGHT" and new_direction == "LEFT"):
            direction = new_direction
    
    if not move_snake():
        oled.fill(0)
        oled.text("GAME OVER", 30, 30)
        oled.text(f"Score: {score}", 20, 40)
        oled.show()
        time.sleep(3)  # Show Game Over screen
        
        # Reset game
        snake = [(64, 32)]
        direction = "RIGHT"
        food = (random.randint(0, WIDTH // SNAKE_SIZE - 1) * SNAKE_SIZE,
                random.randint(0, HEIGHT // SNAKE_SIZE - 1) * SNAKE_SIZE)
        score = 0
        speed = 0.2
    
    for segment in snake:
        oled.rect(segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE, 1)
    oled.rect(food[0], food[1], SNAKE_SIZE, SNAKE_SIZE, 1)
    oled.text(f"Score: {score}", 0, 0, 1)
    oled.show()
    time.sleep(speed)
