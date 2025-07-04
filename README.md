<img width="316" alt="pico-chu" src="https://github.com/user-attachments/assets/555d352a-5dca-4917-9a9c-02fe24b0ff7f" />


# pico-chu
📟 Pico-Chu – A Multi-Game Console on Raspberry Pi Pico
For my MPMC (Microprocessors and Microcontrollers) project, I built a full-featured game menu system called Pico-Chu — running on a Raspberry Pi Pico with joystick input and an SSD1306 OLED screen.

This was one of the most fun things I built all semester. I tested dozens of ideas, trial games, and demos — but this main menu project brings together everything I did with the Pico: hardware interfacing, ADCs, I2C, GPIO, and embedded game logic.

🎮 Included Games & Features
Menu system with joystick navigation
Scroll, select, and switch between games using the joystick and button

Snake
Classic Snake game with collision, self-wrap, score, and high-score tracking

Flappy Bird
Obstacle jumping with vertical velocity, gravity physics, pipe generation, and scoring

2048
Fully playable 2048 tile puzzle with smooth grid updates and logic in MicroPython

High Score System
Stores top 3 scores for Snake and Flappy Bird

💡 Tech Used
Raspberry Pi Pico

MicroPython

SSD1306 OLED display (128x64)

Analog joystick using ADC (X, Y axes)

GPIO digital input for button press

I2C for OLED communication

ADC, Pin, and machine modules

📚 What I Learned
Real-time game loop logic with tight RAM constraints

Reading analog joystick inputs via ADC

Writing full games with just rectangles and pixel math

Building a responsive UI using a 1-bit OLED screen

Managing multi-game structure in MicroPython on a microcontroller

🛠 How to Run
You’ll need:

Raspberry Pi Pico

SSD1306 OLED (I2C) wired to GP16 (SDA) and GP17 (SCL)

Analog joystick on GP26 (Y), GP27 (X), and GP22 (Button)

Upload main.py to the Pico. It will boot into the Pico-Chu game menu.

🧪 Trial Projects
Other code experiments and smaller game ideas I tried out during the semester (like LED blinking, MPU6050 sensor, IR input, or accelerometer-controlled games) are stored in other files — but this menu project is the one that ties everything together.


Microprocessor project
