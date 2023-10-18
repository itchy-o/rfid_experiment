# itchy-o/rfid_experiment/test4

test4 creates a 4 by 4 foot example of "test flooring"
(actually two 2x4ft sections, for easier portability)
using 4"/100mm tag spacing
and reuses the [test3 7-sensor deck](../test3/README.md)

test4 also enhances the software running on the Raspberry Pi Pico.

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

