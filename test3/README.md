# itchy-o/rfid_experiment/test3

test3 focuses on exploring RFID sensor placement.

The sensor deck consists of seven PN532 sensors arranged on a 13-inch hexagon of particleboard.
One sensor is in the center, the other six are in radial slots of the hexagon, allowing positional adjustment.
The sensors are mounted to the deck using velcro to support easy repositioning.

There is also a strip of 8 APA102 RGB LEDs for visual status of tag detection,
to support operation without connecting the serial port to a PC.

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


## test3 Wiring

There are three types of ribbon cables:
- Seven per-sensor "Bus" cables.
- One "Select" cable, with all the sensors' select lines.
- One "LED" control cable.

### Bus Cables (Qty 7)
These lines connect to all seven sensor modules in parallel, except for the SS line.
```
PN532             wire  pico  pico
signal  direction color pin  signal
======= ========= ===== ==== ======
 SCK       <--     vio   24   GP18/SCK0
 MISO      -->     blu   26   GP20/RX0
 MOSI      <--     grn   25   GP19/TX0
 SS        <--     yel   (see Select Cable below)
 VCC       <--     ora   36   3V3OUT
 GND       ---     red   23   GND
 IRQ        x      brn   nc   x
 RST0       x      blk   nc   x
```

### Select Cable (Qty 1)
Each sensor's yellow SS wire is separated from it's Bus cable and spliced into the Select Cable.
```
PN532  wire  pico  pico
select color pin  signal
====== ===== ==== ======
  0     brn   12   GP9
  1     red   14   GP10
  2     ora   15   GP11
  3     yel   16   GP12
  4     grn   17   GP13
  5     blu   19   GP14
  6     vio   20   GP15
```

### LED Cable (Qty 1)
```
 LED   wire   pico  pico
signal color  pin  signal
====== ===== ==== ======
 GND    grn   38   GND
 CLK    blu   31   GP26/SCK1
 DATA   vio   32   GP27/TX1
 5V     gry   40   VBUS
```

