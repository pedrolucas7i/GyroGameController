import time
import board
import busio
import math
import usb_hid
import adafruit_mpu6050
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse

# I2C Configuration
i2c = busio.I2C(board.GP27, board.GP26)
mpu = adafruit_mpu6050.MPU6050(i2c)

# USB HID Configuration
keyboard = Keyboard(usb_hid.devices)
mouse = Mouse(usb_hid.devices)

# Stability Parameters
ANGLE_THRESHOLD = 20  # Minimum angle to activate keys
DEADZONE = 5          # Dead zone to prevent small tremors
SLEEP_TIME = 0.025    # Time between readings
MOUSE_SENSITIVITY = 20  # Sensitivity multiplier for mouse movement

# Last pressed keys
last_keys = set()

def get_angles():
    """Gets accelerometer angles relative to the Z-axis."""
    accel_x, accel_y, accel_z = mpu.acceleration
    angle_x = math.atan2(accel_y, accel_z) * (180 / math.pi)
    angle_y = math.atan2(accel_x, accel_z) * (180 / math.pi)
    return angle_x, angle_y

def get_rotation():
    """Gets gyroscope rotation around the Z-axis for mouse control."""
    _, _, gyro_z = mpu.gyro
    return gyro_z

def get_pressed_keys(angle_x, angle_y):
    """Returns a set of keys based on angles."""
    keys = set()
    
    if abs(angle_x) > DEADZONE or abs(angle_y) > DEADZONE:
        if angle_x > ANGLE_THRESHOLD:
            keys.add(Keycode.D)
        elif angle_x < -ANGLE_THRESHOLD:
            keys.add(Keycode.A)
        
        if angle_y > ANGLE_THRESHOLD:
            keys.add(Keycode.S)
        elif angle_y < -ANGLE_THRESHOLD:
            keys.add(Keycode.W)
    
    return keys

# Wait 5 seconds before starting
time.sleep(5)

# Main loop
while True:
    angle_x, angle_y = get_angles()
    rotation_z = get_rotation()
    current_keys = get_pressed_keys(angle_x, angle_y)
    
    # Press only new keys
    for key in current_keys - last_keys:
        keyboard.press(key)
    
    # Release only keys that are no longer needed
    for key in last_keys - current_keys:
        keyboard.release(key)
    
    # Move mouse based on gyroscope Z-axis rotation
    mouse.move(x=int(-rotation_z * MOUSE_SENSITIVITY))
    
    last_keys = current_keys
    time.sleep(SLEEP_TIME)
