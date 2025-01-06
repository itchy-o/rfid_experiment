# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-FileCopyrightText: 2023-2025 Mike Weiblen http://mew.cx/
#
# SPDX-License-Identifier: MIT
#
# rfid_experiment/test6/test6.py
# Developed using CircuitPython 9.2.x on Raspberry Pi Pico W.
# Read NTAG21x RFID tags using four PN532 sensor modules.
# Indicate which sensors are detecting tags using an LED strip.
# Part of the Sono Chapel position-sensing experiments.
# 2025-01-05

"""Sono Chapel Pod firmware"""

# About this code:
__version__ = "0.5.4.2"
__repo__ = "https://github.com/itchy-o/rfid_experiment.git"
__impl_name__ = 'circuitpython'         # sys.implementation.name
__impl_version__ = (9, 2, 1, '')        # sys.implementation.version
__board_id__ = "raspberry_pi_pico_w"    # board.board_id

# The version of sono_protocol.txt we implement here:
PROTOCOL_VERSION = const("0.1.0.3")

#############################################################################

import board
import busio
import time
import atexit
import os
import wifi
import socketpool
import tag_coords
from touchio import TouchIn
from neopixel import NeoPixel
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI
from micropython import const

#############################################################################

class PodMessenger:
    """Send messages to server via WiFi"""

    def __init__(self):
        """Initialize from settings.toml"""
        self.pod_id    =  const(os.getenv('SONOCHAPEL_POD_ID'))
        self.msg_delay =  const(os.getenv('SONOCHAPEL_MSG_DELAY')/1000.0)
        self.server    = (const(os.getenv('SONOCHAPEL_SERVER_IPADDR')),
                          const(os.getenv('SONOCHAPEL_SERVER_PORT')))
        self.sock = None
        self.seq  = None

    def connect(self):
        print("We are pod_id", self.pod_id,
            "mac", ":".join("{:02x}".format(i) for i in wifi.radio.mac_address))

        ssid   = os.getenv('CIRCUITPY_WIFI_SSID')
        passwd = os.getenv('CIRCUITPY_WIFI_PASSWORD')
        print("Connecting to SSID", ssid)
        wifi.radio.connect(ssid, passwd)

        print("We are pod_id", self.pod_id,
            "ip", wifi.radio.ipv4_address)
        print("Sending to", self.server)

        # a single socket we reuse forever
        pool = socketpool.SocketPool(wifi.radio)
        self.sock = pool.socket(pool.AF_INET, pool.SOCK_DGRAM)

    def send(self, type, data):
        packet = "%s %d %d %s" % (type, self.pod_id, self.seq, data)
        print(packet)
        self.sock.sendto(packet, self.server)
        self.seq += 1
        time.sleep(self.msg_delay)

    # Messages as defined by sono_protocol.txt:

    def sendBOOT(self):
        self.seq = 0
        data = "%s %s" % (PROTOCOL_VERSION, __version__)
        self.send("BOOT", data)

    def sendDATA(self, posx, posy, t1, num_tags):
        data = "%.3f %.3f %d %d" % (posx, posy, t1, num_tags)
        self.send("DATA", data)

    def sendINFO(self, data):
        self.send("INFO", data)

#############################################################################

class Sensor:
    """A single PN532 RFID sensor module"""

    def __init__(self, i, spi, chip_select):
        self.i = i
        self.pn532 = None
        self.coord = None
        self.rfid_timeout = const(os.getenv('SONOCHAPEL_RFID_TIMEOUT')/1000.0)
        leds[self.i] = CYAN

        try:
            cs_pin=DigitalInOut(chip_select)
            self.pn532 = PN532_SPI(spi=spi, cs_pin=cs_pin, debug=False)
        except:
            pm.sendINFO("sensor %d not responding, flag as disabled" % i)
            self.pn532 = None
            leds[self.i] = RED
            return

        pm.sendINFO("sensor %d firmware_version %s" % (i, self.pn532.firmware_version))
        self.pn532.SAM_configuration()
        leds[self.i] = BLACK

    def read(self):
        "Read the sensor, returning True if coordinate is updated."
        print(">>>>>>> reading sensor", self.i)
        if self.pn532 is None:
            # Skip this disabled sensor
            return False

        leds[self.i] = WHITE
        id = self.pn532.read_passive_target(timeout=self.rfid_timeout)
        if id is None:
            # no tag detected
            leds[self.i] = BLACK
            self.coord = None
            return False

        tag_id = "".join("{:02x}".format(i) for i in id)
        try:
            coord = tag_coords.data[tag_id]
        except:
#            pm.sendINFO("sensor %d ROGUE TAG %s" % (self.i, tag_id))
            leds[self.i] = MAGENTA
            self.coord = None
            return False

        # This tag is recognized: update our coordinate, return True.
        leds[self.i] = GREEN
        self.coord = coord
        return True

#############################################################################

class SensorDeck:
    """The pod's collection of Sensors"""

    def __init__(self, spi):
        "Construct all the Sensors for this SensorDeck"
        # Pins for each sensor's SPI chip-select (CS) signal:
        CS_GPIOS = (board.GP10, board.GP11, board.GP12, board.GP13)

        self.sensors = [None] * len(CS_GPIOS)
        self.lastCoord = (0,0)
        for i, cs_gpio in enumerate(CS_GPIOS):
            self.sensors[i] = Sensor(i, spi, cs_gpio)

    def readAll(self):
        "Read all sensors once."
        for s in self.sensors:
            s.read()

    def readOne(self):
        "Infinite iterator that reads a single sensor."
        while True:
            for s in self.sensors:
                yield s.read()

    def coord(self):
        "Return the average of sensors that have valid coordinates."
        n,x,y = 0,0,0
        for s in self.sensors:
            c = s.coord
            if c is not None:
                n += 1
                x += c[0]
                y += c[1]

        if n == 0:
            x,y = self.lastCoord
        else:
            x /= n
            y /= n
            self.lastCoord = x,y

        return n,x,y

#############################################################################
# Globals

# Set up 5-LED neopixel strip
WHITE   = const(0x040404)
RED     = const(0x110000)
GREEN   = const(0x001100)
BLUE    = const(0x000022)
MAGENTA = const(0x110022)
CYAN    = const(0x001122)
BLACK   = const(0)
leds = NeoPixel(pin=board.GP0, n=5, brightness=0.5, auto_write=True)

pm = PodMessenger()

#############################################################################

def main():
    leds.fill(BLACK)
    print("Sono Chapel version", __version__, "protocol", PROTOCOL_VERSION)

    leds.fill(BLUE)
    pm.connect()
    pm.sendBOOT()

    touch1 = TouchIn(board.GP1)

    leds.fill(BLACK)
    spi = busio.SPI(clock=board.GP18, MOSI=board.GP19, MISO=board.GP20)
    sd = SensorDeck(spi)

    while True:
        t1 = touch1.value
        leds[4] = GREEN if t1 else BLACK

        sd.readAll()
        num_tags, x, y = sd.coord()
        pm.sendDATA(x, y, t1, num_tags)

# TODO sd.readOne()

@atexit.register
def shutdown():
    leds.fill(BLACK)
    leds.show()

# vim: set sw=4 ts=8 et ic ai:
