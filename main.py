import time
import board
import busio
import math
import usb_hid
import adafruit_mpu6050
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Configurações I2C
i2c = busio.I2C(board.GP27, board.GP26)
mpu = adafruit_mpu6050.MPU6050(i2c)

# Configurações USB HID
keyboard = Keyboard(usb_hid.devices)

# Esperar 2 segundos antes de iniciar
time.sleep(5)

# Loop principal
while True:
    accel_x, accel_y, accel_z = mpu.acceleration
    angle_x = math.atan2(accel_y, accel_z) * (180 / math.pi)
    angle_y = math.atan2(accel_x, accel_z) * (180 / math.pi)

    # Movimento horizontal (Eixo X)
    if angle_x > 20:
        keyboard.press(Keycode.D)
    elif angle_x < -20:
        keyboard.press(Keycode.A)
    
    # Movimento vertical (Eixo Y)
    if angle_y > 20:
        keyboard.press(Keycode.W)
    elif angle_y < -20:
        keyboard.press(Keycode.S)
    
    keyboard.release(Keycode.A)
    keyboard.release(Keycode.D)
    keyboard.release(Keycode.W)
    keyboard.release(Keycode.S)
    time.sleep(0.05)
