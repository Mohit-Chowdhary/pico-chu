from machine import Pin, ADC, I2C, reset
import time
import random
import framebuf
from ssd1306 import SSD1306_I2C

WIDTH = 128
HEIGHT = 64
SNAKE_SIZE = 8

# Initialize I2C and OLED
i2c = I2C(0, scl=Pin(17), sda=Pin(16))
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

# Initialize Joystick
joy_x = ADC(Pin(27))
joy_y = ADC(Pin(26))
joy_button = Pin(22, Pin.IN, Pin.PULL_UP)

THRESHOLD_LOW = 30000
THRESHOLD_HIGH = 40000

# Joystick for Flappy Bird
joystick_sw = Pin(22, Pin.IN, Pin.PULL_UP)

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

def show_menu():
    selected = 0  # 0 = Snake, 1 = Flappy Bird
    while True:
        oled.fill(0)
        oled.text("PICO CHU", 30, 5)
        oled.hline(0, 15, WIDTH, 1)
        oled.text("> Snake", 20, 30 if selected == 0 else 40, 1)
        oled.text("Flappy Bird", 20, 40 if selected == 0 else 30, 1)
        oled.show()

        time.sleep(0.15)
        new_direction = read_joystick()
        if new_direction in ["UP", "DOWN"]:
            selected = 1 - selected
        if not joy_button.value():
            if selected == 0:
                play_snake()
            else:
                play_flappy()

def play_snake():
    snake = [(64, 32)]
    direction = "RIGHT"
    food = (random.randint(0, WIDTH // SNAKE_SIZE - 1) * SNAKE_SIZE, 
            random.randint(0, HEIGHT // SNAKE_SIZE - 1) * SNAKE_SIZE)
    
    while True:
        oled.fill(0)
        new_direction = read_joystick()
        if new_direction and new_direction != direction:
            if not (direction == "UP" and new_direction == "DOWN" or
                    direction == "DOWN" and new_direction == "UP" or
                    direction == "LEFT" and new_direction == "RIGHT" or
                    direction == "RIGHT" and new_direction == "LEFT"):
                direction = new_direction
        
        if not move_snake(snake, direction, food):
            game_over()
            return

        for segment in snake:
            oled.rect(segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE, 1)
        oled.rect(food[0], food[1], SNAKE_SIZE, SNAKE_SIZE, 1)
        oled.show()
        time.sleep(0.2)

def move_snake(snake, direction, food):
    head_x, head_y = snake[0]
    if direction == "UP":
        head_y -= SNAKE_SIZE
    elif direction == "DOWN":
        head_y += SNAKE_SIZE
    elif direction == "LEFT":
        head_x -= SNAKE_SIZE
    elif direction == "RIGHT":
        head_x += SNAKE_SIZE
    
    head_x %= WIDTH
    head_y %= HEIGHT
    new_head = (head_x, head_y)
    
    if new_head in snake:
        return False
    
    snake.insert(0, new_head)
    if new_head == food:
        food = (random.randint(0, WIDTH // SNAKE_SIZE - 1) * SNAKE_SIZE,
                random.randint(0, HEIGHT // SNAKE_SIZE - 1) * SNAKE_SIZE)
    else:
        snake.pop()
    
    return True

def play_flappy():
    bird_y = HEIGHT // 2
    velocity = 0
    g = 1
    flap_strength = -4
    wall_x = WIDTH - 1
    walls = [1] * 8
    
    def generate_walls():
        gap_start = random.randint(1, 4)
        return [1 if i < gap_start or i > gap_start + 2 else 0 for i in range(8)]
    
    walls = generate_walls()
    while True:
        oled.fill(0)
        velocity += g
        bird_y += velocity
        if not joystick_sw.value():
            velocity = flap_strength
        
        wall_x -= 2
        if wall_x < 0:
            wall_x = WIDTH - 1
            walls = generate_walls()
        
        if bird_y < 0 or bird_y + 8 > HEIGHT or (wall_x == 20 and walls[bird_y // 8]):
            game_over()
            return
        
        for i in range(8):
            if walls[i]:
                oled.fill_rect(wall_x, i * 8, 6, 8, 1)
        oled.fill_rect(20, bird_y, 4, 4, 1)
        oled.show()
        time.sleep(0.1)

def game_over():
    oled.fill(0)
    oled.text("GAME OVER", 30, 30, 1)
    oled.show()
    time.sleep(2)
    show_menu()

show_menu()
