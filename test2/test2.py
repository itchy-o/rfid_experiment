# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-FileCopyrightText: 2023 Mike Weiblen http://mew.cx/
#
# SPDX-License-Identifier: MIT

import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI

spi = busio.SPI(clock=board.GP18, MOSI=board.GP19, MISO=board.GP20)

SS1 = DigitalInOut(board.GP17)
SS2 = DigitalInOut(board.GP21)
SS3 = DigitalInOut(board.GP5)

RF1 = PN532_SPI(spi, SS1, debug=False)
RF2 = PN532_SPI(spi, SS2, debug=False)
RF3 = PN532_SPI(spi, SS3, debug=False)

print("RF1.firmware_version ", RF1.firmware_version)
print("RF2.firmware_version ", RF2.firmware_version)
print("RF3.firmware_version ", RF3.firmware_version)

RF1.SAM_configuration()
RF2.SAM_configuration()
RF3.SAM_configuration()

while True:
    uid = RF1.read_passive_target(timeout=0.5)
    if uid:
        print([hex(i) for i in uid], " ", end="")
    else:
        print("RF1 ", end="")

    uid = RF2.read_passive_target(timeout=0.5)
    if uid:
        print([hex(i) for i in uid], " ", end="")
    else:
        print("RF2 ", end="")

    uid = RF3.read_passive_target(timeout=0.5)
    if uid:
        print([hex(i) for i in uid], " ", end="")
    else:
        print("RF3 ", end="")

    print(" $")
