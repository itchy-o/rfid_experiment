# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-FileCopyrightText: 2023 Mike Weiblen http://mew.cx/
#
# SPDX-License-Identifier: MIT
#
# rfid_experiment/test4/test4.py
# Developed using CircuitPython 8.x on Raspberry Pi Pico MCU.
# Read NTAG21x RFID tags using up to seven PN532 sensor modules.
# Indicate which sensors are detecting tags using an LED strip.
# Part of the Sono Chapel position-sensing experiments.
# 2023-10-18

import board
import busio
import time
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI
from adafruit_dotstar import DotStar
from micropython import const

# About this code:
__version__ = "0.3.5.0"
__repo__ = "https://github.com/itchy-o/rfid_experiment.git"
__board_id__ = "raspberry_pi_pico"      # board.board_id
__impl_name__ = "circuitpython"         # sys.implementation.name
__impl_version__ = (8, 2, 6)            # sys.implementation.version

# Configure SPI1 GPIO for 8-LED APA102 strip.  Turn all LEDs off.
leds  = DotStar(clock=board.GP26, data=board.GP27, n=8)
WHITE = 0x777777
RED   = 0x770000
GREEN = 0x007700
BLUE  = 0x000077
BLACK = 0
leds.fill(BLACK)

# Configure SPI0 GPIO for Serial Peripheral Interface (SPI).
spi = busio.SPI(clock=board.GP18, MOSI=board.GP19, MISO=board.GP20)

def sensor_init(i, cs_gpio):
    """Initialize a PN532 RFID sensor.
    """
    leds[i] = GREEN
    dio = DigitalInOut(cs_gpio)
    try:
        sensor = PN532_SPI(spi=spi, cs_pin=dio, irq=None, reset=None, debug=False)
    except:
        leds[i] = RED
        return None
    print(i, " : ", sensor, ", firmware_version ", sensor.firmware_version)
    leds[i] = BLUE
    sensor.SAM_configuration()
    leds[i] = BLACK
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
