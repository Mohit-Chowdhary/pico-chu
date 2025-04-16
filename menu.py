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
        
        oled.text("> Snake" if selected == 0 else "  Snake", 14, 25)
        oled.text("> Flappy Bird" if selected == 1 else "  Flappy Bird", 14, 35)
        oled.text("> 2048" if selected == 2 else "  2048", 14, 45)
        
        oled.show()
        time.sleep(0.15)
        
        new_direction = read_joystick()
        if new_direction == "UP":
            selected = (selected - 1) % 3
        elif new_direction == "DOWN":
            selected = (selected + 1) % 3
        if not joy_button.value():
            if selected == 0:
                show_snake_menu()
            elif selected==1:
                show_bird_menu()
            else:
                play_2048()
                #play_flappy_bird()

def show_snake_menu():
    selected = 0  # 0 = Play, 1 = High Score
    while True:
        oled.fill(0)
        oled.text("Snake Game", 30, 5)
        oled.hline(0, 15, WIDTH, 1)
        oled.text("> Play" if selected == 0 else "  Play", 14, 25)
        oled.text("> High Score" if selected == 1 else "  High Score", 14, 35)
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

def show_bird_menu():
    selected = 0  # 0 = Play, 1 = High Score
    while True:
        oled.fill(0)
        oled.text("Flappy Bird", 30, 5)
        oled.hline(0, 15, WIDTH, 1)
        oled.text("> Play" if selected == 0 else "  Play", 14, 25)
        oled.text("> High Score" if selected == 1 else "  High Score", 14, 35)
        oled.show()
        
        time.sleep(0.15)
        new_direction = read_joystick()
        if new_direction == "UP" or new_direction == "DOWN":
            selected = 1 - selected
        if not joy_button.value():
            if selected == 0:
                play_flappy_bird()
            else:
                show_high_scores_bird()

def play_flappy_bird():
    bird_y = HEIGHT // 2
    velocity = 0
    gravity = 1
    pipe_x = WIDTH
    pipe_gap = 30
    score = 0
    
    while True:
        global Highscore_Birdy
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
            
            if score > Highscore_Birdy[2]:  # Only insert if num is greater than the smallest in the list
                Highscore_Birdy.append(score)  # Add new number
                Highscore_Birdy.sort(reverse=True)  # Sort in descending order
                Highscore_Birdy.pop()
            print(Highscore_Birdy)
            
            time.sleep(3)
            show_menu()
        
        oled.fill(0)
        oled.text(f"{score}", 0, 0, 1)
        oled.fill_rect(10, bird_y, 4, 4, 1)
        oled.rect(pipe_x, 0, 10, pipe_gap, 1)
        oled.rect(pipe_x, pipe_gap + 30, 10, HEIGHT - pipe_gap - 30, 1)
        oled.show()
        time.sleep(0.1)
        
#2048
        
board = [[0 for _ in range(4)] for _ in range(4)]

def get_empty_cells(board):
    empty = []
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                empty.append((i, j))
    return empty

def add_random_tile(board):
    empty_cells = get_empty_cells(board)
    if not empty_cells:
        return False  # No space left

    i, j = random.choice(empty_cells)
    board[i][j] = 4 if random.random() < 0.1 else 2  # 10% chance of 4, else 2
    return True

def slide_left(row):
    new = [i for i in row if i != 0]
    merged = []
    skip = False
    for i in range(len(new)):
        if skip:
            skip = False
            continue
        if i + 1 < len(new) and new[i] == new[i+1]:
            merged.append(new[i]*2)
            skip = True
        else:
            merged.append(new[i])
    while len(merged) < 4:
        merged.append(0)
    return merged

def move_left(board):
    changed = False
    for i in range(4):
        new_row = slide_left(board[i])
        if new_row != board[i]:
            board[i] = new_row
            changed = True
    return changed

def move_right(board):
    changed = False
    for i in range(4):
        reversed_row = list(reversed(board[i]))
        new_row = slide_left(reversed_row)
        new_row.reverse()
        if new_row != board[i]:
            board[i] = new_row
            changed = True
    return changed

def move_up(board):
    changed = False
    for j in range(4):
        col = [board[i][j] for i in range(4)]
        new_col = slide_left(col)
        for i in range(4):
            if board[i][j] != new_col[i]:
                board[i][j] = new_col[i]
                changed = True
    return changed

def move_down(board):
    changed = False
    for j in range(4):
        col = [board[i][j] for i in range(4)][::-1]
        new_col = slide_left(col)
        new_col.reverse()
        for i in range(4):
            if board[i][j] != new_col[i]:
                board[i][j] = new_col[i]
                changed = True
    return changed

def draw_board(oled, board):
    oled.fill(0)
    tile_w = 30  # width of each tile
    tile_h = 15  # height of each tile

    for i in range(4):
        for j in range(4):
            x = j * tile_w
            y = i * tile_h
            oled.rect(x, y, tile_w, tile_h, 1)  # draw rectangle
            val = str(board[i][j]) if board[i][j] != 0 else ""
            # center text inside the tile
            text_x = x + (tile_w - len(val)*8) // 2
            text_y = y + (tile_h - 8) // 2
            oled.text(val, text_x, text_y)
    oled.show()
        
def play_2048():
    add_random_tile(board)
    add_random_tile(board)
    while(True):
        draw_board(oled, board)
        
        direct_2048=read_joystick()
        
        if direct_2048 == "UP" and move_up(board):
            add_random_tile(board)
            time.sleep(0.3)
        elif direct_2048 == "DOWN" and move_down(board):
            add_random_tile(board)
            time.sleep(0.3)
        elif direct_2048 == "LEFT" and move_left(board):
            add_random_tile(board)
            time.sleep(0.3)
        elif direct_2048 == "RIGHT" and move_right(board):
            add_random_tile(board)
            time.sleep(0.3)
        #elif not move_up(board) and not move_right(board) and not move_left(board) and move_down(board):
            #show_menu()

        time.sleep(0.05)
        

show_menu()
