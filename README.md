# itchy-o/rfid_experiment

## Concept of operation
The objective is to determine the location of a pod within a room using RFID.

This concept is to place RFID tag stickers under flooring at known locations.
Since the stickers each report a unique tag ID number, an RFID sensor above the floor
can know where it is by mapping the tag ID to its known physical position.

## Summary of design
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

## About the RFID tags
The preferred RFID tags are of the
[NTAG21x](https://www.nxp.com/products/rfid-nfc/nfc-hf/ntag-for-tags-and-labels/ntag-213-215-216-nfc-forum-type-2-tag-compliant-ic-with-144-504-888-bytes-user-memory:NTAG213_215_216)
series.
We only depend upon a tag's unique identifier.
We do not use the tag's memory, so the smallest (and cheapest) NTAG213 tags are sufficient.

## Summary of tests
- test1 - Proof of concept for a PN532 sensor reading tags through a block of wood.
- test2 - Three PN532 sensors reading a triangular grid of tags.
- test3 - Seven adjustable PN532 sensors to explore sensor placement.

## Summary of branches
- `main` - The current runtime version.  Intended to be installed verbatim on the CircuitPython device.
- `photos` - Detailed photographs (and other large files) supporting the tests.  _Not_ intended to be installed on the devices.

## Misc
- [PN532 CircuitPython API documentation](https://docs.circuitpython.org/projects/pn532/en/latest/api.html)
