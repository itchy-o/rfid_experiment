# SPDX-FileCopyrightText: 2023-2025 Mike Weiblen http://mew.cx/
#
# SPDX-License-Identifier: MIT
#
# assign_xy.py
# Enter X,Y tag locations.
# Turn on logging to save the data.
# 2023-10-20 2025-02-21

import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI

class TidReader:

    def __init__(self):
        self.chip_select = board.GP13
        self.cs = DigitalInOut(self.chip_select)
        self.spi = busio.SPI(clock=board.GP18, MOSI=board.GP19, MISO=board.GP20)
        self.pn532 = PN532_SPI(self.spi, self.cs, debug=False)

        ic, ver, rev, support = self.pn532.firmware_version
        print("PN532 firmware: {1}.{2} ic: {0} support: {3}\n".format(ic, ver, rev, support))

        self.pn532.SAM_configuration()

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
#            print("#", tid)
            if tid != prev:
                prev = None
                count = 0
                continue

            count += 1
            if count > 5:
                return tid


def test():
    "Simple exerciser for TidReader"
    reader = TidReader()
    while True:
        print(reader.read())

#############################################################################

def is_valid(tid):
    xy = input("enter X,Y: ")
    if xy != '':
        xy = eval(xy)
        tid = repr(tid)
        print("data[", tid, "] = ", xy)

def main():
    reader = TidReader()
    x = eval(input("starting X: "))
    y = eval(input("starting Y: "))
    data = {}

    while True:
        xy = (x,y)

        while True:
            tid = reader.read()
            if tid not in data:
                print(x, y, tid)
                data[tid] = xy
                y+=2
                break
            else:
                print("#",tid,data[tid])


# vim: set sw=4 ts=8 et ic ai:
