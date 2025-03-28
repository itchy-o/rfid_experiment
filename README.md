### With the unveiling of _SonoChapel_ during [itchy-O's](https://itchyo.com/) [SÖM SÂPTÂLAHN](https://alternativetentacles.com/blogs/news/itchy-o-som-saptalahn-transmission-is-now-live) [release event](https://www.kickstarter.com/projects/itchyo/som-saptalahn-album-release-vinyl-and-more/) at [Fiske Planetarium](https://www.colorado.edu/fiske/) on [2025-03-15](https://itchyo.com/som-saptalahn-album-release/) , this project exits its experimental phase.<br><br>Future development will occur in the [SonoChapel_v1](https://github.com/itchy-o/SonoChapel_v1) repo.

-----

# itchy-o/rfid_experiment/README.md

## Concept of operation
The objective is to determine the location of a pod within a room using NFC/RFID.
(Near-Field Communication/Radio Frequency IDentification)

This concept is to place RFID tag stickers under flooring at known locations.
Since the stickers each report a pre-programmed unique tag_id number, an RFID sensor above the floor
can know where it is by mapping the tag_id to its known coordinate.

## Summary of sensor design
The hardware consists of a
- [Raspberry Pi Pico W](https://www.raspberrypi.com/products/raspberry-pi-pico/)
running [CircuitPython](https://circuitpython.org/), connected to
- [RFID](https://en.wikipedia.org/wiki/Radio-frequency_identification)
13.56MHz [PN532 sensor modules](https://www.ebay.com/sch/i.html?_nkw=pn532+rfid+v3)
communicating via [SPI](https://en.wikipedia.org/wiki/Serial_Peripheral_Interface)

The tags and sensors follow the [ISO 14443-A](https://en.wikipedia.org/wiki/ISO/IEC_14443) standard.

## About the RFID tags
The preferred RFID tags are of the
[NTAG21x](https://www.nxp.com/products/rfid-nfc/nfc-hf/ntag-for-tags-and-labels/ntag-213-215-216-nfc-forum-type-2-tag-compliant-ic-with-144-504-888-bytes-user-memory:NTAG213_215_216)
series.
We only require a tag's unique pre-programmed identifier, which we use to look up its coordinate in the tag_coords.py table.
That table of tag coordinates must be manually created when a new array of tags is built.
We do not need any of the tag's memory, so the least-memory (thus hopefully cheapest?) of the NTAG21x tags is sufficient.
NTAG213 seem a very common and inexpensive 13.56MHz tag.

Tags also vary in their physical size, thus the size of their antenna.
The size of the antenna probably affects the distance the sensor can read the tag.
25mm circular tag stickers are common, and have been used in this testing.
32mm tags have been seen for sale.
There are "credit cards" with RFID circuitry embedded; cards could have the largest antenna, and their solid plastic seems very durable.

## Summary of tests
- test1 - Proof of concept for a PN532 sensor reading tags through a block of wood.
- test2 - Build a sensor deck with three PN532 sensors reading a triangular grid of tags on a sheet of paper.
- test3 - Build a sensor deck with seven adjustable PN532 sensors to explore sensor placement.
- test4 - Build a 4x4 foot triangular grid of tags on plywood (16 sqft, ~160 tags total, 100mm tag spacing), and reuse the test3 7-sensor deck.
- test5 - Same hardware as test4, with bug fixes and update to latest CircuitPython.
- test6 - Build eight 4-sensor decks with Raspberry Pi Pico W, to wirelessly communicate with Q-SYS audio system.
- test7 - Build a 6x6 foot triangular grid of tags on plywood (36 sqft, 765 tags total, 70mm tag spacing), and reuse the eight test6 4-sensor pods.

## Summary of branches
- `main` - The released runtime version.  Intended to be installed on the CircuitPython device.
- `photos` - Detailed photographs (and other large files e.g. PDFs) supporting the tests.  _Not_ to be installed on the devices.

## Misc CircuitPython documentation
- [PN532 RFID sensor](https://docs.circuitpython.org/projects/pn532/en/latest/api.html)
- [PN532 module pinout](https://components101.com/wireless/pn532-nfc-rfid-module)
- [capacitive touch sensor](https://learn.adafruit.com/circuitpython-essentials/circuitpython-cap-touch)
- [NeoPixel LED strip](https://learn.adafruit.com/circuitpython-essentials/circuitpython-neopixel)
