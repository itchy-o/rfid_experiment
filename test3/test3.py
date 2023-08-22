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

# About this code:
__repo__ = "https://github.com/itchy-o/rfid_experiment"
__version__ = "0.3.2.0"
# For what hardware was this code was developed:
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
    leds[i] = GREEN
    dio = DigitalInOut(cs_gpio)
    try:
        sensor = PN532_SPI(spi=spi, cs_pin=dio, irq=None, reset=None, debug=False)
        print(i, " : ", sensor, ", firmware_version ", sensor.firmware_version)
        leds[i] = BLUE
        sensor.SAM_configuration()
        leds[i] = BLACK
    except:
        sensor = None
        leds[i] = RED
    return sensor

def sensor_read(i, sensor):
    """Set the sensor's LED to indicate if the sensor detected a tag or not.
    """
    if sensor is None:
        return None
    leds[i] = WHITE
    tag_uid = sensor.read_passive_target(timeout=0.2)
    leds[i] = GREEN if tag_uid is not None else BLUE
    sensor.power_down()
    #time.sleep(0.1)
    return tag_uid

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

# List of handles to initialized sensor instances (or None).
SENSORS = [None] * len(CS_GPIOS)

def init_all():
    for i, cs_gpio in enumerate(CS_GPIOS):
        SENSORS[i] = sensor_init(i, cs_gpio)

def read_all():
    for i, sensor in enumerate(SENSORS):
        sensor_read(i, sensor)

def main():
    leds.fill(BLACK)
    init_all()
    while True:
        read_all()

# Make it so...
main()
