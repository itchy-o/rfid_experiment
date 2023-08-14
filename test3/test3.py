# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-FileCopyrightText: 2023 Mike Weiblen http://mew.cx/
#
# SPDX-License-Identifier: MIT
#
# rfid_experiment/test3/test3.py
# Read NTAG21x RFID tags using up to seven PN532 sensor modules.
# Indicate which sensors are detecting tags using an LED strip.
# Part of the Sono Chapel position-sensing experiments.
# Demonstrated 2023-08-13


import board
import busio
import time
import adafruit_dotstar
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI

__repo__ = "https://github.com/itchy-o/rfid_experiment"
__version__ = "0.3.1.0"

# configure GPIO pins for LED strip, turn all LEDs off.
leds = adafruit_dotstar.DotStar(board.GP26, board.GP27, 8, brightness=0.2)
RED   = 0xff0000
GREEN = 0x00ff00
BLUE  = 0x0000ff
OFF   = 0
leds.fill(OFF)

# configure GPIO pins for Serial Peripheral Interface (SPI).
spi = busio.SPI(clock=board.GP18, MOSI=board.GP19, MISO=board.GP20)

# list of GPIO pins controling the sensors' SPI chip-select.
SENSORS = (
        board.GP9,
        board.GP10,
        board.GP11,
        board.GP12,
        board.GP13,
        board.GP14,
        board.GP15
)

PN = []

def rf_init(i,ss):
    leds[i] = 0x00ff00
    ssio = DigitalInOut(ss)
    dev = PN532_SPI(spi, ssio, debug=False)
    print("firmware_version(", i, ") = ", dev.firmware_version)
    leds[i] = 0x0000ff
    dev.SAM_configuration()
    leds[i] = 0
    PN.append(dev)

def read(i,dev):
    uid = dev.read_passive_target(timeout=0.3)
    if uid:
        leds[i] = 0xff0000
    else:
        leds[i] = 0x0000ff
    dev.power_down()
    #time.sleep(0.1)

def init():
    for i,ss in enumerate(SENSORS):
        rf_init(i,ss)

def main():
    init()
    while True:
        for i,dev in enumerate(PN):
            read(i,dev)

main()
