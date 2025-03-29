from machine import Pin, ADC
import time

from machine import Pin, SoftI2C

# You can choose any other combination of I2C pins
i2c = SoftI2C(scl=Pin(17), sda=Pin(16))

print('I2C SCANNER')
devices = i2c.scan()

    
# Joystick connections (as per your setup)
joystick_x = ADC(Pin(27))  # VRX connected to GP27 (ADC1)
joystick_y = ADC(Pin(26))  # VRY connected to GP26 (ADC0)
joystick_btn = Pin(22, Pin.IN, Pin.PULL_UP)  # Button connected to GP22

while True:
    x_val = joystick_x.read_u16()  # Read X-axis (0-65535)
    y_val = joystick_y.read_u16()  # Read Y-axis (0-65535)
    btn_state = joystick_btn.value()  # Read button state (0 = pressed, 1 = not pressed)

    print(f"X: {x_val}, Y: {y_val}, Button: {'Pressed' if btn_state == 0 else 'Not Pressed'}")
    
    time.sleep(0.1)  # Small delay to avoid spam
    
    if len(devices) == 0:
      print("No i2c device !")
    else:
      print('i2c devices found:', len(devices))

      for device in devices:
        print("I2C hexadecimal address: ", hex(device))
