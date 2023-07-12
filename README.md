# itchy-o/rfid_experiment

## Concept of operation

The objective is to determine the location of a pod within a room using RFID.

The idea is to place RFID tag stickers under flooring at known locations.
Since the stickers each report a unique ID number, an RFID sensor above the floor can know
where it is by mapping the ID to the tag's known physical position.

-------

## TODO raw notes to be integrated/refined...

The circuit consists of a
[Raspberry Pi Pico MCU](https://www.raspberrypi.com/products/raspberry-pi-pico/),
running [CircuitPython 8](https://circuitpython.org/),
connected to three [PN532 RFID sensor boards](https://www.ebay.com/sch/i.html?_nkw=pn532)
using SPI.  Data is reported via Pico's USB serial port.

[PN532 CircuitPython API documentation](https://docs.circuitpython.org/projects/pn532/en/latest/api.html)

- must set RFID switches to enable SPI interface.
- include pix and refs to "NTAG216 – NFC Transparent Label RFID tag sticker"
- include area of perimeter of test2 sensors.
- include dimensions of my sample tag stickers.

