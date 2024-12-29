# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-FileCopyrightText: 2023-2024 Mike Weiblen http://mew.cx/
#
# SPDX-License-Identifier: MIT
#
# rfid_experiment/test6/test6.py
# Developed using CircuitPython 9.2.x on Raspberry Pi Pico W.
# Read NTAG21x RFID tags using four PN532 sensor modules.
# Indicate which sensors are detecting tags using an LED strip.
# Part of the Sono Chapel position-sensing experiments.
# 2024-12-29
# TODO WIP WIP WIP
# TODO: migrate from DotStar to neopixel

# About this code:
__version__ = "0.5.3.0"
__repo__ = "https://github.com/itchy-o/rfid_experiment.git"
__impl_name__ = 'circuitpython'         # sys.implementation.name
__impl_version__ = (9, 2, 1, '')        # sys.implementation.version
__board_id__ = "raspberry_pi_pico_w"    # board.board_id


import board
import busio
import time
import atexit
import neopixel
import tag_coords
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI
from micropython import const

# Configure GPIOs for 4-LED neopixel strip.  Turn all LEDs off.
WHITE   = const(0x040404)
RED     = const(0x110000)
GREEN   = const(0x001100)
BLUE    = const(0x000022)
MAGENTA = const(0x110022)
CYAN    = const(0x001122)
BLACK   = const(0)
leds  = DotStar(clock=board.GP26, data=board.GP27, n=4)

#PIXEL_PIN = board.MOSI
#NUM_PIXELS = 4
#pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, auto_write=False)
leds.fill(BLACK)

# Configure GPIOs for Serial Peripheral Interface (SPI).
spi = busio.SPI(clock=board.GP18, MOSI=board.GP19, MISO=board.GP20)

#############################################################################

class Sensor:
    """
    """
    def __init__(self, i, chip_select):
        self.i = i
        leds[self.i] = CYAN
        self.chip_select = chip_select
        self.cs_pin = DigitalInOut(self.chip_select)
        self.pn532 = None
        self.tid = None
        self.coord = None

        try:
            self.pn532 = PN532_SPI(spi=spi, cs_pin=self.cs_pin,
                                irq=None, reset=None, debug=False)
        except:
            # sensor not responding, flag it as disabled
            self.pn532 = None
            leds[self.i] = RED
            return

        print(i, " : firmware_version ", self.pn532.firmware_version)
        self.pn532.SAM_configuration()
        leds[self.i] = BLACK

    def read(self):
        "Read the sensor; if it detects a valid tag, update its coordinate."
        if self.pn532 is None:
            # Skip this disabled sensor
            leds[self.i] = RED
            return False

        leds[self.i] = WHITE
        id = self.pn532.read_passive_target(timeout=0.1)
        if id is None:
            # No tag was detected
            leds[self.i] = BLACK
            return False

        self.tid = "".join("{:02x}".format(i) for i in id)
        if self.tid not in tag_coords.data:
            # This tag id is not in the coordinate table! A rogue tag??
            leds[self.i] = MAGENTA
            self.coord = None
            return False

        # This tag is valid, so update the sensor's coordinate.
        leds[self.i] = GREEN
        self.coord = tag_coords.data[self.tid]
        #self.pn532.power_down()
        #time.sleep(0.1)
        return True

#############################################################################

class SensorDeck:
    """
    """
    def __init__(self, cs_gpios):
        self.num_sensors = len(cs_gpios)
        self.sensors = [None] * self.num_sensors
        for i, cs_gpio in enumerate(cs_gpios):
            self.sensors[i] = Sensor(i, cs_gpio)

    def read(self):
        "Read all sensors, return the number of actual tags detected."
        n = 0
        for s in self.sensors:
            if s.read():
                n += 1
        return n

    def coord(self):
        "Return the average of the sensors that have a valid coordinate."
        x = 0.0
        y = 0.0
        n = 0.0
        for s in self.sensors:
            c = s.coord
            if c is not None:
                x += float(c[0])
                y += float(c[1])
                n += 1.0

        if n > 0.0:
            return x/n, y/n

        # No sensors have valid coordinates.
        return None

#############################################################################

# The GPIO pins controling each sensor's SPI chip-select (CS).
# TODO four sensors for test6
CS_GPIOS = (board.GP9,  board.GP10, board.GP11, board.GP12, board.GP13,
            board.GP14, board.GP15)

def main():
    sd = SensorDeck(CS_GPIOS)
    while True:
        count = sd.read()
        coord = sd.coord()
        print(coord, count)

@atexit.register
def shutdown():
    leds.fill(BLACK)
    leds.show()

# vim: set sw=4 ts=8 et ic ai:
