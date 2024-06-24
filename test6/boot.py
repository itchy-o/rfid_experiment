# boot.py

import storage
import usb_hid
import usb_midi

# writable for CPy
#storage.remount("/", readonly=False)

print("usb_hid.disable()")
usb_hid.disable()

print("usb_midi.disable()")
usb_midi.disable()

#eof
