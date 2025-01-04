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
# 2025-01-04

"""Sono Chapel Pod firmware"""

# About this code:
__version__ = "0.5.4.0"
__repo__ = "https://github.com/itchy-o/rfid_experiment.git"
__impl_name__ = 'circuitpython'         # sys.implementation.name
__impl_version__ = (9, 2, 1, '')        # sys.implementation.version
__board_id__ = "raspberry_pi_pico_w"    # board.board_id

# The version of sono_protocol.txt we implement here
PROTOCOL_VERSION = const("0.1.0.3")


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

# Setup 5-LED neopixel strip, ensure all LEDs off.
WHITE   = const(0x040404)
RED     = const(0x110000)
GREEN   = const(0x001100)
BLUE    = const(0x000022)
MAGENTA = const(0x110022)
CYAN    = const(0x001122)
BLACK   = const(0)
leds = NeoPixel(pin=board.GP0, n=5, brightness=0.3, auto_write=True)
leds.fill(BLACK)

touch1 = TouchIn(board.GP1)

# Setup Serial Peripheral Interface (SPI).
spi = busio.SPI(clock=board.GP18, MOSI=board.GP19, MISO=board.GP20)

#############################################################################

class PodMessenger:
    """TODO"""
    def __init__(self):
        """Initialize from envars defined in settings.toml"""
        self.ssid         = const(os.getenv('CIRCUITPY_WIFI_SSID'))
        self.passwd       = const(os.getenv('CIRCUITPY_WIFI_PASSWORD'))
        self.pod_id       = const(os.getenv('SONOCHAPEL_POD_ID'))
        self.pod_interval = const(os.getenv('SONOCHAPEL_POD_INTERVAL')/1000.0)
        self.server       = const(os.getenv('SONOCHAPEL_SERVER_IPADDR'))
        self.port         = const(os.getenv('SONOCHAPEL_SERVER_PORT'))
        self.sock         = None
        self.seq          = None
        print("Sending to", self.server, ":", self.port)

    def connect(self):
        print("Connecting to SSID", self.ssid)
        wifi.radio.connect(self.ssid, self.passwd)

#        print("MAC", [hex(i) for i in wifi.radio.mac_address])
        print("ipaddr", wifi.radio.ipv4_address)
#        print("Ping : %f ms" % (wifi.radio.ping(self.server)*3))

        pool = socketpool.SocketPool(wifi.radio)
        self.sock = pool.socket(pool.AF_INET, pool.SOCK_DGRAM)

    def send(self, type, data):
        packet = "%s %d %d %s" % (type, self.pod_id, self.seq, data)
        print(packet)
        self.sock.sendto(packet, (self.server, self.port))
        self.seq += 1

    def sleep(self):
        time.sleep(self.pod_interval)

    # Messages as defined by sono_protocol.txt...

    def sendBOOT(self):
        self.seq = 0
        data = "%s %s" % (PROTOCOL_VERSION, __version__)
        self.send("BOOT", data)

    def sendDATA(self, posx, posy, touch1, num_tags):
        data = "%f %f %d %d" % (posx, posy, touch1, num_tags)
        self.send("DATA", data)

    def sendINFO(self, data):
        self.send("INFO", data)

#############################################################################

class Sensor:
    """TODO"""
    def __init__(self, i, chip_select):
        self.i = i
        leds[self.i] = CYAN
        self.chip_select = chip_select
        self.cs_pin = DigitalInOut(self.chip_select)
        self.pn532 = None
        self.tid = None
        self.coord = None
        self.rfid_timeout = const(os.getenv('SONOCHAPEL_RFID_TIMEOUT')/1000.0)

        try:
            self.pn532 = PN532_SPI(spi=spi, cs_pin=self.cs_pin,
                                irq=None, reset=None, debug=False)
        except:
            print(i, ": sensor not responding, flag it disabled")
            self.pn532 = None
            leds[self.i] = RED
            return

        print(i, ": firmware_version", self.pn532.firmware_version)
        self.pn532.SAM_configuration()
        leds[self.i] = BLACK

    def read(self):
        "Read the sensor; if it detects a valid tag, update its coordinate."
        if self.pn532 is None:
            # Skip this disabled sensor
            leds[self.i] = RED
            return False

        leds[self.i] = WHITE
        id = self.pn532.read_passive_target(timeout=self.rfid_timeout)
        if id is None:
#            print(self.i, ": No tag detected")
            leds[self.i] = BLACK
            return False

        self.tid = "".join("{:02x}".format(i) for i in id)
        print(self.i, "tag id ", self.tid)
        if self.tid not in tag_coords.data:
#            print(self.i, ": Tag id not recognized; a rogue tag?")
            leds[self.i] = MAGENTA
            self.coord = None
            return False

        # This tag is recognized, so update the sensor's coordinate.
        leds[self.i] = GREEN
        self.coord = tag_coords.data[self.tid]
#        self.pn532.power_down()
#        time.sleep(0.1)
        return True

#############################################################################

class SensorDeck:
    """TODO"""
    def __init__(self, cs_gpios):
        self.num_sensors = len(cs_gpios)
        self.sensors = [None] * self.num_sensors
        for i, cs_gpio in enumerate(cs_gpios):
            self.sensors[i] = Sensor(i, cs_gpio)

    def read(self):
        "Read all sensors, return the number of actual tags detected."
        n = 0
        for s in self.sensors:
            if s.read():
                n += 1
        return n

    def coord(self):
        "Return the average of the sensors that have a valid coordinate."
        x = 0.0
        y = 0.0
        n = 0.0
        for s in self.sensors:
            c = s.coord
            if c is not None:
                x += float(c[0])
                y += float(c[1])
                n += 1.0

        if n > 0.0:
            return x/n, y/n

        # No sensors have valid coordinates.
        return 0,0

#############################################################################

# Pins controling each sensor's SPI chip-select (CS).
CS_GPIOS = (board.GP10, board.GP11, board.GP12, board.GP13)

def main():
    leds[4] = WHITE
    print("Sono Chapel version", __version__, "protocol", PROTOCOL_VERSION)

    sd = SensorDeck(CS_GPIOS)

    leds[4] = BLUE
    pm = PodMessenger()
    pm.connect()
    pm.sendBOOT()
    leds[4] = BLACK

    while True:
        count = sd.read()
        x,y = sd.coord()
        t1 = touch1.value
        if t1:
            leds[4] = GREEN
        else:
            leds[4] = BLACK
        pm.sendDATA(x, y, t1, count)
        pm.sleep()

@atexit.register
def shutdown():
    leds.fill(BLACK)
    leds.show()

# vim: set sw=4 ts=8 et ic ai:
