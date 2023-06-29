# itchy-o/rfid_experiment/test1

RFID test1 proof-of-concept demo, consisting of a
Raspberry Pi Pico MCU,
running CircuitPython 8,
connected to a PN532 RFID sensor board.

## Wiring

PN532                wire    pico    pico    pico
signal   direction   color  signal   pin     gpio
======= =========== ======= ======= ======= =======
 sck        <--       yel    sck      24     GP18
 miso       -->       grn    rx       21     GP16
 mosi       <--       gry    tx       25     GP19
 ss         <--       ora    cs       22     GP17
 vcc        <--       red    3v3out   36     ---
 gnd        ---       blk    gnd      23     ---

