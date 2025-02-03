# GYRO GAME CONTROLLER
![Raspberry Pi RP2040](https://img.shields.io/badge/Raspberry%20Pi%20RP2040-black?logo=raspberrypi&logoColor=raspberrypi) ![](https://img.shields.io/badge/Programming-black?logo=C&logoColor=white)


## Description
This project implements a game control system using the **Raspberry Pi Pico / Raspberry Pi Pico W**. It can be used to map the **MPU6050** sensor to control the `W`, `A`, `S`, `D` keys via **USB** connection to the device, allowing for intuitive and innovative movement in games.

## Features
- **Tilt detection** with the MPU6050 sensor.
- **Mapping of WASD keys** based on the tilt.
- **Execution via CircuitPython** directly on the Raspberry Pi Pico.
- **Ready to GO** with just a USB connection needed.

## Requirements
- Raspberry Pi Pico / Raspberry Pi Pico W.
- MPU6050 sensor.
- CircuitPython installed on the Raspberry Pi Pico.
- Libraries inside the Raspberry Pi Pico folder.

## How to Set Up and Run
1. **Install CircuitPython** on the Raspberry Pi Pico by following [this guide](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython) and placing this [UF2](https://github.com/pedrolucas7i/GyroGameController/raw/refs/heads/main/CircuitPython%209.2.4/adafruit-circuitpython-raspberry_pi_pico-en_US-9.2.4.uf2).

2. **Copy the necessary files** to the Pico.

3. **Install libraries**:
   - Copy the libraries from the project folder `lib\9.x` to the `lib/` folder on the Pico.

4. **Run the code**:
   - Save and place the Python code (`main.py` and `boot.py`) at the root of the Pico.
   - Restart the device (unplug and plug the USB back in) to start the controller.

## Usage
1. Tilt the Raspberry Pi Pico forward/backward/left/right to trigger the `W`, `A`, `S`, `D` keys.
2. The movement will be interpreted and sent as keyboard input to the game.
3. To stop the controller, disconnect the Pico or remove the code.

## Credits
   - [**Pedro Lucas**](https://github.com/pedrolucas7i)

## License
This project is distributed under the **GPL-3.0 license**.
