# SPDX-FileCopyrightText: 2023 Mike Weiblen http://mew.cx/
#
# SPDX-License-Identifier: MIT
#
# assign_xy.py
# Enter X,Y tag locations.
# Turn on logging to save the data.
# 2023-10-20 2025-01-12

import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI

class TidReader:

    def __init__(self,chip_select):
        self.chip_select = chip_select
        self.cs = DigitalInOut(self.chip_select)
        self.spi = busio.SPI(clock=board.GP18, MOSI=board.GP19, MISO=board.GP20)
        self.pn532 = PN532_SPI(self.spi, self.cs, debug=False)

        ic, ver, rev, support = self.pn532.firmware_version
        print("PN532 firmware: {1}.{2} ic: {0} support: {3}\n".format(ic, ver, rev, support))

        self.pn532.SAM_configuration()

    def read(self):
        tid = self.pn532.read_passive_target(timeout=0.5)
        if tid is not None:
            # reformat binary tid as readable hex
            tid = "".join("{:02x}".format(i) for i in tid)
        return tid


def test():
    """
    Simple exerciser for TidReader
    """
    reader = TidReader(board.GP13)
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
    reader = TidReader(board.GP13)
    while True:
        t = reader.read()
        if t is None:
            continue

        print(t)
        is_valid(t)

# vim: set sw=4 ts=8 et ic ai:
