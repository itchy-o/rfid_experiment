# itchy-o/rfid_experiment/test5

test5 reuses test4's 4x4 test flooring (and its tag_coords.py),
and reuses the [test3 7-sensor deck](../test3/README.md)
but with 3 sensors removed to be used on a second sensor deck.

test5 also enhances and fixes bugs in software running on the Raspberry Pi Pico.


## Summary of sensor design
The hardware consists of a
[Raspberry Pi Pico MCU](https://www.raspberrypi.com/products/raspberry-pi-pico/)
running
[CircuitPython 8](https://circuitpython.org/),
connected to
[RFID](https://en.wikipedia.org/wiki/Radio-frequency_identification)
13.56MHz
[PN532 sensor boards](https://www.ebay.com/sch/i.html?_nkw=pn532)
using
[SPI](https://en.wikipedia.org/wiki/Serial_Peripheral_Interface).
