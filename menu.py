from machine import Pin, ADC, I2C, reset
import time
import random
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

snake = [(64, 32)]
direction = "RIGHT"
food = (random.randint(0, WIDTH // SNAKE_SIZE - 1) * SNAKE_SIZE, 
        random.randint(0, HEIGHT // SNAKE_SIZE - 1) * SNAKE_SIZE)
score = 0
speed = 0.2

Highscore_Snake=[0,0,0]
Highscore_Birdy=[0,0,0]

def show_high_scores_snake():
    print("is this running")
    global Highscore_Snake
    oled.fill(0)
    oled.text(f"1: {Highscore_Snake[0]}",50,10)
    oled.text(f"2: {Highscore_Snake[1]}",50,30)
    oled.text(f"3: {Highscore_Snake[2]}",50,50)
    oled.show()
    time.sleep(3)
    show_menu()
    
def show_high_scores_bird():
    print("is this running")
    global Highscore_Snake
    oled.fill(0)
    oled.text(f"1: {Highscore_Birdy[0]}",50,10)
    oled.text(f"2: {Highscore_Birdy[1]}",50,30)
    oled.text(f"3: {Highscore_Birdy[2]}",50,50)
    oled.show()
    time.sleep(3)
    show_menu()

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
        oled.text("PICO-CHU", 30, 5)
        oled.hline(0, 15, WIDTH, 1)
        
        oled.text("> Snake" if selected == 0 else "  Snake", 13, 25)
        oled.text("> Flappy Bird" if selected == 1 else "  Flappy Bird", 13, 35)
        
        oled.show()
        time.sleep(0.15)
        
        new_direction = read_joystick()
        if new_direction == "UP" or new_direction == "DOWN":
            selected = 1 - selected  # Toggle between Snake and Flappy Bird
        if not joy_button.value():
            if selected == 0:
                show_snake_menu()
            else:
                play_flappy_bird()

def show_snake_menu():
    selected = 0  # 0 = Play, 1 = High Score
    while True:
        oled.fill(0)
        oled.text("Snake Game", 30, 10)
        oled.hline(0, 20, WIDTH, 1)
        oled.text("> Play" if selected == 0 else "  Play", 20, 30)
        oled.text("> High Score" if selected == 1 else "  High Score", 20, 40)
        oled.show()
        
        time.sleep(0.15)
        new_direction = read_joystick()
        if new_direction == "UP" or new_direction == "DOWN":
            selected = 1 - selected
        if not joy_button.value():
            if selected == 0:
                play_snake()
            else:
                show_high_scores_snake()

def play_snake():

    while True:
        global food, direction, snake, score, Highscore_Snake
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
            oled.text(f"Score: {score}", 30, 40)
            oled.show()
            
            if score > Highscore_Snake[2]:  # Only insert if num is greater than the smallest in the list
                Highscore_Snake.append(score)  # Add new number
                Highscore_Snake.sort(reverse=True)  # Sort in descending order
                Highscore_Snake.pop()
            print(Highscore_Snake)
            
            time.sleep(3)
            snake = [(64, 32)]
            direction = "RIGHT"
#            food = (random.randint(0, WIDTH // SNAKE_SIZE - 1) * SNAKE_SIZE, 
#                    random.randint(0, HEIGHT // SNAKE_SIZE - 1) * SNAKE_SIZE)
            score = 0
#            speed = 0.2
            show_menu()
        
        for segment in snake:
            oled.rect(segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE, 1)
        oled.fill_rect(food[0], food[1], SNAKE_SIZE, SNAKE_SIZE, 1)
        oled.text(f"{score}", 0, 0, 1)
        oled.show()
        time.sleep(speed)

def move_snake():
    global food, direction, snake, score
    head_x, head_y = snake[0]
    print("heheheh")
    
    if direction == "UP":
        head_y -= SNAKE_SIZE
    elif direction == "DOWN":
        head_y += SNAKE_SIZE
    elif direction == "LEFT":
        head_x -= SNAKE_SIZE
    elif direction == "RIGHT":
        head_x += SNAKE_SIZE
    print("hah")
    
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

def play_flappy_bird():
    bird_y = HEIGHT // 2
    velocity = 0
    gravity = 1
    pipe_x = WIDTH
    pipe_gap = 30
    score = 0
    
    while True:
        oled.fill(0)
        velocity += gravity
        bird_y += velocity
        if not joy_button.value():
            velocity = -5
        
        pipe_x -= 3
        if pipe_x < -10:
            pipe_x = WIDTH
            pipe_gap = random.randint(10, HEIGHT - 40)
            score += 1
        
        if bird_y >= HEIGHT or bird_y <= 0 or (10 < pipe_x < 14 and not (pipe_gap < bird_y < pipe_gap + 30)):

            oled.fill(0)
            oled.text("GAME OVER", 30, 30)
            oled.text(f"Score: {score}", 30, 40)
            oled.show()
            time.sleep(3)
            show_menu()
        
        oled.fill(0)
        oled.text(f"{score}", 0, 0, 1)
        oled.fill_rect(10, bird_y, 4, 4, 1)
        oled.rect(pipe_x, 0, 10, pipe_gap, 1)
        oled.rect(pipe_x, pipe_gap + 30, 10, HEIGHT - pipe_gap - 30, 1)
        oled.show()
        time.sleep(0.1)

show_menu()
