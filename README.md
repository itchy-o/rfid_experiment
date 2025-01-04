# itchy-o/rfid_experiment/README.md

## Concept of operation
The objective is to determine the location of a pod within a room using NFC/RFID.
(Near-Field Communication/Radio Frequency IDentification)

This concept is to place RFID tag stickers under flooring at known locations.
Since the stickers each report a pre-programmed unique tag ID number, an RFID sensor above the floor
can know where it is by mapping the tag ID to its known physical position.

## Summary of sensor design
The hardware consists of a
- [Raspberry Pi Pico](https://www.raspberrypi.com/products/raspberry-pi-pico/)
running [CircuitPython](https://circuitpython.org/), connected to
- [RFID](https://en.wikipedia.org/wiki/Radio-frequency_identification)
13.56MHz [PN532 sensor modules](https://www.ebay.com/sch/i.html?_nkw=pn532+rfid+v3)
communicating via [SPI](https://en.wikipedia.org/wiki/Serial_Peripheral_Interface)

The tags and sensors follow the [ISO 14443-A](https://en.wikipedia.org/wiki/ISO/IEC_14443) standard.

## About the RFID tags
The preferred RFID tags are of the
[NTAG21x](https://www.nxp.com/products/rfid-nfc/nfc-hf/ntag-for-tags-and-labels/ntag-213-215-216-nfc-forum-type-2-tag-compliant-ic-with-144-504-888-bytes-user-memory:NTAG213_215_216)
series.
We only require a tag's unique pre-programmed identifier, which is used to look up its physical location in a table.
The table of tag locations is manually created when the array of tags is built.
We do not need any of the tag's memory, so the least-memory (thus hopefully cheapest?) of the NTAG21x tags is sufficient.

Tags also vary in their physical size, thus the size of their antenna.
The size of the antenna seems to directly affect the distance the sensor can read the tag.
25mm circular tag stickers are common, and have been used in this testing.
32mm tags have been seen for sale.
There are "credit cards" with RFID circuitry embedded; the cards seem to have the largest antenna, and their solid plastic seems very durable.

## Summary of tests
- test1 - Proof of concept for a PN532 sensor reading tags through a block of wood.
- test2 - Build a sensor deck with three PN532 sensors reading a triangular grid of tags on a sheet of paper.
- test3 - Build a sensor deck with seven adjustable PN532 sensors to explore sensor placement.
- test4 - Build a 4x4 foot triangular grid of tags on plywood (16 sqft, ~160 tags total, 100mm tag spacing), and reuse the test3 7-sensor deck.
- test5 - Same hardware as test4, with bug fixes and update to latest CircuitPython.
- test6 - Build eight 4-sensor decks with Raspberry Pi Pico W, to wirelessly communicate with Q-SYS audio system.

## Summary of branches
- `main` - The current runtime version.  Intended to be installed verbatim on the CircuitPython device.
- `photos` - Detailed photographs (and other large files e.g. PDFs) supporting the tests.  _Not_ to be installed on the devices.

## Misc CircuitPython documentation
- [PN532 RFID sensor](https://docs.circuitpython.org/projects/pn532/en/latest/api.html)
- [capacitive touch sensor](https://learn.adafruit.com/circuitpython-essentials/circuitpython-cap-touch)
- [NeoPixel LED strip](https://learn.adafruit.com/circuitpython-essentials/circuitpython-neopixel)
