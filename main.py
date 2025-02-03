import time
import board
import busio
import digitalio
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
try:
    devices = list(usb_hid.devices)
    keyboard = Keyboard(devices)
    mouse = Mouse(devices)
    print("HID Devices Initialized")
except Exception as e:
    print("HID Error:", e)


# Stability Parameters
ANGLE_THRESHOLD = 20  # Minimum angle to activate keys
DEADZONE = 5          # Dead zone to prevent small tremors
SLEEP_TIME = 0.025    # Time between readings
MOUSE_SENSITIVITY = 30  # Sensitivity multiplier for mouse movement
GYRO_THRESHOLD = 0.5  # Ignore small gyro drifts

# Last pressed keys
last_keys = set()

aim = digitalio.DigitalInOut(board.GP16)  # Adjust pin if necessary
aim.direction = digitalio.Direction.INPUT
aim.pull = digitalio.Pull.UP

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

def aim_button():
    """Function triggered when AIM Button is pressed."""
    mouse.press(Mouse.RIGHT_BUTTON)

def release_aim():
    """Function triggered when AIM Button is released."""
    mouse.release(Mouse.RIGHT_BUTTON)

# Wait 5 seconds before starting (useful for debugging)
print("Starting in 5 seconds...")
time.sleep(5)
print("Started!")

# Main loop
while True:
    # Check if AIM Button is pressed
    if aim.value:
        aim_button()
    else:
        release_aim()
    
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
    if abs(rotation_z) > GYRO_THRESHOLD:  # Ignore small movements
        mouse.move(x=int(-rotation_z * MOUSE_SENSITIVITY))
    
    last_keys = current_keys
    time.sleep(SLEEP_TIME)
