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
# 2023-10-20

# About this code:
__version__ = "0.3.5.1"
__repo__ = "https://github.com/itchy-o/rfid_experiment.git"
__board_id__ = "raspberry_pi_pico"      # board.board_id
__impl_name__ = "circuitpython"         # sys.implementation.name
__impl_version__ = (8, 2, 7)            # sys.implementation.version

import board
import busio
import time
import atexit
#import valid_tids
import tag_coords
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI
from adafruit_dotstar import DotStar
from micropython import const
#from tidreader import TidReader

# Configure GPIOs for 8-LED APA102 strip.  Turn all LEDs off.
WHITE   = const(0x111111)
RED     = const(0x110000)
GREEN   = const(0x001100)
BLUE    = const(0x000022)
MAGENTA = const(0x110022)
CYAN    = const(0x001122)
BLACK   = const(0)
leds  = DotStar(clock=board.GP26, data=board.GP27, n=8)
leds.fill(BLACK)

# Configure GPIOs for Serial Peripheral Interface (SPI).
spi = busio.SPI(clock=board.GP18, MOSI=board.GP19, MISO=board.GP20)

class Sensor:
    """
    """
    def __init__(self, i, chip_select):
        self.i = i
        leds[self.i] = MAGENTA
        self.chip_select = chip_select
        self.cs_pin = DigitalInOut(self.chip_select)
        self.pn532 = None
        self.tid = None
        self.coord = None

        try:
            self.pn532 = PN532_SPI(spi=spi, cs_pin=self.cs_pin,
                                irq=None, reset=None, debug=False)
        except:
            leds[self.i] = RED
            return

        print(i, " : firmware_version ", self.pn532.firmware_version)
        self.pn532.SAM_configuration()
        leds[self.i] = BLACK

    def read(self):
        if self.pn532 is None:
            leds[self.i] = RED
            return

        leds[self.i] = WHITE
        id = self.pn532.read_passive_target(timeout=0.1)
        if id is None:
            leds[self.i] = BLACK
            return

        self.tid = "".join("{:02x}".format(i) for i in id)
        #print(self.tid)
        if self.tid not in tag_coords.data:
            leds[self.i] = CYAN
            self.coord = None
            return

        leds[self.i] = GREEN
        self.coord = tag_coords.data[self.tid]
        #self.pn532.power_down()
        #time.sleep(0.1)

class SensorDeck:
    """
    """
    def __init__(self, cs_gpios):
        self.sensors = [None] * len(cs_gpios)

# The GPIO pins controling each sensor's SPI chip-select (CS).
CS_GPIOS = (board.GP9,  board.GP10, board.GP11, board.GP12, board.GP13,
            board.GP14, board.GP15)

# List of handles to initialized sensor instances (or None).
SENSORS = [None] * len(CS_GPIOS)

def init_all():
    for i, cs_gpio in enumerate(CS_GPIOS):
        SENSORS[i] = Sensor(i, cs_gpio)

def read_all():
    for i, sensor in enumerate(SENSORS):
        SENSORS[i].read()

def main():
    init_all()
    while True:
        read_all()

@atexit.register
def shutdown():
    leds.fill(BLACK)

# vim: set sw=4 ts=8 et ic ai:
