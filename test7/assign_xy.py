# SPDX-FileCopyrightText: 2023-2025 Mike Weiblen http://mew.cx/
#
# SPDX-License-Identifier: MIT
#
# assign_xy.py
# Associate tag_ids with X,Y coordinates.
# Turn on logging to save the data.
# 2023-10-20 2025-02-28

import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI

data = {}
#from tag_coords import data
print("\n\nlen(data)", len(data))

#############################################################################

class TidReader:

    def __init__(self):
        self.chip_select = board.GP13
        self.cs = DigitalInOut(self.chip_select)
        self.spi = busio.SPI(clock=board.GP18, MOSI=board.GP19, MISO=board.GP20)
        self.pn532 = PN532_SPI(self.spi, self.cs, debug=False)

        ic, ver, rev, support = self.pn532.firmware_version
        print("PN532 firmware: {1}.{2} ic: {0} support: {3}\n".format(ic, ver, rev, support))

        self.pn532.SAM_configuration()

    # tag readings can be jittery; read several times to ensure stability.
    def read(self):
        prev = None
        tid = None
        count = 0
        while True:
            prev = tid
            tid = self.pn532.read_passive_target(timeout=0.2)
            if tid is None:
                prev = None
                count = 0
                continue

            tid = "".join("{:02x}".format(i) for i in tid)

            # if reading is not stable, reset.
            if tid != prev:
                prev = None
                count = 0
                continue

            # have we read the same value enough times to be confident?
            count += 1
            if count > 5:
                return tid

#############################################################################

def main():
    reader = TidReader()
    y = eval(input("starting Y: "))
    x = eval(input("starting X: "))

    while True:                 # forever: assign the next coordinate
        while True:             # reader is returning a tag_id
            tid = reader.read()
            if tid not in data:
                # add a new tid
                print(x, y, tid)
                data[tid] = (x,y)
                #y+=2
                x+=2
                break
            else:
                # tid already defined: show its coord
                print("#",tid,data[tid])

# vim: set sw=4 ts=8 et ic ai:
