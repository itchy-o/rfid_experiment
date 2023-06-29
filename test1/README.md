# itchy-o/rfid_experiment/test1

A proof-of-concept demo for using RFID/NFC tags for position sensing within a room.

The idea is to place RFID tag stickers under flooring.
Since the stickers each report a unique ID number, an RFID sensor above the floor can know
where it is by mapping the ID to the tag's known physical position.

In the demo, a 3/4" piece of wood was a standin for the flooring surface.

The hardware consists of a
[Raspberry Pi Pico MCU](https://www.raspberrypi.com/products/raspberry-pi-pico/),
running [CircuitPython 8](https://circuitpython.org/),
connected to a [PN532 RFID sensor board](https://www.ebay.com/sch/i.html?_nkw=pn532)

## Wiring
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
