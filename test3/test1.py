# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-FileCopyrightText: 2023 Mike Weiblen http://mew.cx/
#
# SPDX-License-Identifier: MIT

import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI

spi = busio.SPI(clock=board.GP18, MOSI=board.GP19, MISO=board.GP16)
cs = DigitalInOut(board.GP17)
pn532 = PN532_SPI(spi, cs, debug=False)

ic, ver, rev, support = pn532.firmware_version
print("PN532 firmware: {1}.{2} ic: {0} support: {3}\n".format(ic, ver, rev, support))

pn532.SAM_configuration()

print("Waiting for RFID/NFC card...")
while True:
    uid = pn532.read_passive_target(timeout=0.5)
    if uid is None:
        print(".", end="")
    else:
        print("\ncard UID:", [hex(i) for i in uid])
