# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-FileCopyrightText: 2023 Mike Weiblen http://mew.cx/
#
# SPDX-License-Identifier: MIT

import board
import busio
import time
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI

spi = busio.SPI(clock=board.GP18, MOSI=board.GP19, MISO=board.GP20)

SS1 = DigitalInOut(board.GP17)
SS2 = DigitalInOut(board.GP21)
SS3 = DigitalInOut(board.GP5)

print("RF1 init")
RF1 = PN532_SPI(spi, SS1, debug=False)
print("RF2 init")
RF2 = PN532_SPI(spi, SS2, debug=False)
print("RF3 init")
RF3 = PN532_SPI(spi, SS3, debug=False)

SENSORS = [RF1, RF2, RF3]

print("version query")
print("RF1.firmware_version ", RF1.firmware_version)
print("RF2.firmware_version ", RF2.firmware_version)
print("RF3.firmware_version ", RF3.firmware_version)

print("configuring")
RF1.SAM_configuration()
RF2.SAM_configuration()
RF3.SAM_configuration()

def read(sensor):
    uid = sensor.read_passive_target(timeout=0.3)
    if uid:
        #print([hex(i) for i in uid], " ", end="")
        print("XXXXX ", end="")
    else:
        print("      ", end="")
    sensor.power_down()
    time.sleep(0.1)

while True:
    read(RF1)
    read(RF2)
    read(RF3)
    print("")

