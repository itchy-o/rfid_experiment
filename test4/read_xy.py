# SPDX-FileCopyrightText: 2023 Mike Weiblen http://mew.cx/
#
# SPDX-License-Identifier: MIT
#
# read_xy.py
# Display X,Y of tags.
# 2023-10-20

import board
import tidreader2
import valid_tids
import tag_coords1

def main():
    reader = tidreader2.TidReader(board.GP17)
    while True:
        t = reader.read()
        if t is None:
            continue

        if t in tag_coords1.data:
            print(t," = ",tag_coords1.data[t])
        elif t in valid_tids.DATA:
            print(t," = VALID VALID VALID")
        else:
            print(t," ---- UNKNOWN")

# vim: set sw=4 ts=8 et ic ai:
