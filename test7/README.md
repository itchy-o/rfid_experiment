# itchy-o/rfid_experiment/test7/README.md

test7 reuses test6's eight (7+1 spare) individual 4-sensor decks, and builds a
new 6x6 floor panel with (25+26)*5*3=765 tags in 70mm triangles.
This configuration is scheduled for test at HQ 2025-03-02, and first public
appearance during Som Saptalahn at Fiske Planetarium 2025-03-15.

IMPORTANT: Due to the huge number of tags in tag_coords.py causing memory
exhaustion errors, this code uses a different syntax to initialize the tag
mapping dictionary.  It is probably worth further optimizing that file by
precompiling to a binary .mpy file using the mpy-cross utility.

The coordinate values returned from the pods on the 6x6 panel:
X = 1 to 30, Y = 1 to 51

## Summary of pod hardware
Each Sono Chapel pod consists of:
- A [Raspberry Pi Pico W](https://www.raspberrypi.com/products/raspberry-pi-pico/)
running [CircuitPython](https://circuitpython.org/)
- Four [RFID](https://en.wikipedia.org/wiki/Radio-frequency_identification)
13.56MHz [PN532 sensor modules](https://www.ebay.com/sch/i.html?_nkw=pn532+rfid+v3)
communicating via [SPI](https://en.wikipedia.org/wiki/Serial_Peripheral_Interface)
- One [capacitive touch input](https://learn.adafruit.com/circuitpython-essentials/circuitpython-cap-touch)
- A [NeoPixel strip](https://learn.adafruit.com/circuitpython-essentials/circuitpython-neopixel)
of five RGB LEDs, for status indication
- A USB 5V powerbank battery

## Summary of files
- [settings.toml](settings.toml) specifies tweakable parameters that control operation.
- [sono_protocol.txt](sono_protocol.txt) describes the messages transmitted by the pods.
- [tag_coords.py](tag_coords.py) specifies the coordinates of tags on a panel, or special commands.

#EOF
