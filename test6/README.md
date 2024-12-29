# itchy-o/rfid_experiment/test6

test6 reuses test4's 4x4 test flooring (and its tag_coords.py),
and create several (ideally seven) separate battery-powered 4-sensor decks,
to experiment with manipulating multiple pods.
Raspberry Pi Pico W is used transmit pod state messages via WiFi to the
Q-SYS audio system.

## Summary of sensor design
The hardware consists of a
[Raspberry Pi Pico W MCU](https://www.raspberrypi.com/products/raspberry-pi-pico/)
running
[CircuitPython 8](https://circuitpython.org/),
connected to four
[RFID](https://en.wikipedia.org/wiki/Radio-frequency_identification)
13.56MHz
[PN532 sensor boards](https://www.ebay.com/sch/i.html?_nkw=pn532)
using
[SPI](https://en.wikipedia.org/wiki/Serial_Peripheral_Interface).
