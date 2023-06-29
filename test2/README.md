# itchy-o/rfid_experiment/test2

This experiment is to determine how many RFID tags are need per floor area (i.e.: the "tag density").

The goal is to "always" have a tag being sensed (to some positional tolerance), so the sensor doesn't get lost in-between tags.
The tags are cheap but not free, so there is motivation to minimize the tag density to keep costs down.
The tag cost could be significant for position sensing in a large room.

The sensor consists of a foamcore "sensor deck" with three PN532 RFID sensors arranged in an
equilateral triangle with radially-symmetric orientation for areal coverage.
The sensors are packed tightly without overlapping.
The resulting center-to-center spacing of the three sensors is 52, 49, 50 mm, for a
triangular area of approx 1095 mm^2

The circuit consists of a
[Raspberry Pi Pico MCU](https://www.raspberrypi.com/products/raspberry-pi-pico/),
running [CircuitPython 8](https://circuitpython.org/),
connected to three [PN532 RFID sensor boards](https://www.ebay.com/sch/i.html?_nkw=pn532)
using SPI.  Data is reported via Pico's USB serial port.

## Wiring
## ROUGH DRAFT
```
PN532                wire    pico    pico    pico
signal   direction   color  signal   pin     gpio
======= =========== ======= ======= ======= =======
 sck        <--       yel    sck      24     GP18
 miso       -->       grn    rx       21     GP16
 mosi       <--       gry    tx       25     GP19
 ss         <--       ora    cs       22     GP17
 vcc        <--       red    3v3out   36     ---
 gnd        ---       blk    gnd      23     ---
```
