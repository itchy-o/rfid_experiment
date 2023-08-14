# test3.py 2023-08-13
# SPDX-FileCopyrightText: 2023 Mike Weiblen http://mew.cx/
#
# SPDX-License-Identifier: MIT

import board
import busio
import time
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI
import adafruit_dotstar

leds = adafruit_dotstar.DotStar(board.GP26, board.GP27, 8, brightness=0.2)
spi = busio.SPI(clock=board.GP18, MOSI=board.GP19, MISO=board.GP20)

#leds.fill(0xff0000); time.sleep(0.1)
#leds.fill(0x00ff00); time.sleep(0.1)
#leds.fill(0x0000ff); time.sleep(0.1)
leds.fill(0)

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
    #print("init ", i)
    leds[i] = 0x00ff00
    #ss = SENSORS[i]
    ssio = DigitalInOut(ss)
    dev = PN532_SPI(spi, ssio, debug=False)
    print(i, "firmware_version(", i, ") = ", dev.firmware_version)
    leds[i] = 0x0000ff
    dev.SAM_configuration()
    leds[i] = 0
    PN.append(dev)

def read(i,dev):
    #print(">> ", i, " - ", dev)
    uid = dev.read_passive_target(timeout=0.3)
    if uid:
        leds[i] = 0xff0000
    else:
        leds[i] = 0x0000ff
    dev.power_down()
    #time.sleep(0.1)

def init():
    leds.fill(0)
    for i,ss in enumerate(SENSORS):
        rf_init(i,ss)

def main():
    init()
    #print("len(PN) = ", len(PN))

    while True:
        for i,dev in enumerate(PN):
            #print(i)
            read(i,dev)

main()
