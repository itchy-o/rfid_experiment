# itchy-o/rfid_experiment/test6/README.md

test6 reuses test4's "4x4" floor panel,
and builds eight (7+1 spare) individual battery-powered 4-sensor decks,
to experiment with manipulating multiple pods.
Raspberry Pi Pico W is used to transmit pod state messages via WiFi to the
Q-SYS audio system.

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
