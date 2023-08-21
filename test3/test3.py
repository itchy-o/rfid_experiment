# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-FileCopyrightText: 2023 Mike Weiblen http://mew.cx/
#
# SPDX-License-Identifier: MIT
#
# rfid_experiment/test3/test3.py
# Developed using CircuitPython 8.x on Raspberry Pi Pico MCU.
# Read NTAG21x RFID tags using up to seven PN532 sensor modules.
# Indicate which sensors are detecting tags using an LED strip.
# Part of the Sono Chapel position-sensing experiments.
# Demonstrated at iOHQ 2023-08-13

import board
import busio
import time
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI
from adafruit_dotstar import DotStar

# about this code:
__repo__ = "https://github.com/itchy-o/rfid_experiment"
__version__ = "0.3.1.0"
# for what hardware was this code was developed:
__cpy_dev__ = "raspberry_pi_pico"       # from board.board_id
__cpy_ver__ = "8.2.2"                   # from os.uname().release

# Configure GPIO for 8-LED strip, turn all LEDs off.
leds  = DotStar(clock=board.GP26, data=board.GP27, n=8, brightness=0.5)
WHITE = 0xffffff
RED   = 0xff0000
GREEN = 0x00ff00
BLUE  = 0x0000ff
BLACK = 0
leds.fill(BLACK)

# Configure GPIO for Serial Peripheral Interface (SPI).
spi = busio.SPI(clock=board.GP18, MOSI=board.GP19, MISO=board.GP20)

def sensor_init(i, cs_gpio):
    """Initialize a PN532 RFID sensor.
    Show progress on-screen and the sensor's LED
    """
    # Create a SPI driver instance for the PN532 sensor.
    leds[i] = GREEN
    dio = DigitalInOut(cs_gpio)
    # TODO: try; use kwargs
    sensor = None
    sensor = PN532_SPI(spi, dio, debug=False)
    print("firmware_version ", i, " = ", sensor.firmware_version)

    # Configure the sensor
    leds[i] = BLUE
    sensor.SAM_configuration()
    leds[i] = BLACK

def sensor_read(i, sensor):
    """Set the sensor's LED to indicate if the sensor detected a
    tag or not.
    """
    leds[i] = WHITE
    uid = sensor.read_passive_target(timeout=0.3)
    leds[i] = BLUE if uid is None else RED
    sensor.power_down()
    #time.sleep(0.1)

# The GPIO pins controling each sensor's SPI chip-select (CS).
CS_GPIOS = (
        board.GP9,
        board.GP10,
        board.GP11,
        board.GP12,
        board.GP13,
        board.GP14,
        board.GP15,
)

# List of handles to initialized/configured sensor instances.
SENSORS = []

def init_all():
    SENSORS = list(len(CS_GPIOS), None)
    for i, cs_gpio in enumerate(CS_GPIOS):
        SENSORS[i] = sensor_init(i, cs_gpio)

def read_all():
    for i, sensor in enumerate(SENSORS):
        sensor_read(i, sensor)

def main():
    init_all()
    while True:
        read_all()

# Make it so...
main()
