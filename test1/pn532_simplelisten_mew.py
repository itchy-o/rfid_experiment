# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example shows connecting to the PN532 with I2C (requires clock
stretching support), SPI, or UART. SPI is best, it uses the most pins but
is the most reliable and universally supported. In this example, we also connect
IRQ and poll that pin for a card. We don't try to read the card until we know
there is one present. After initialization, try waving various 13.56MHz RFID
cards over it!
"""

import time
import board
import busio
from digitalio import DigitalInOut

from adafruit_pn532.spi import PN532_SPI

# SPI connection:
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs_pin = DigitalInOut(board.D5)
pn532 = PN532_SPI(spi, cs_pin, debug=False)

ic, ver, rev, support = pn532.firmware_version
print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

# Start listening for a card
pn532.listen_for_passive_target()
print("Waiting for RFID/NFC card...")
while True:
    # Check if a card is available to read
    if irq_pin.value == 0:
        uid = pn532.get_passive_target()
        print("Found card with UID:", [hex(i) for i in uid])
        # Start listening for a card again
        pn532.listen_for_passive_target()
    else:
        print(".", end="")
    time.sleep(0.1)
