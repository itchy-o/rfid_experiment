# SPDX-FileCopyrightText: 2023 Mike Weiblen http://mew.cx/
#
# SPDX-License-Identifier: MIT
#
# assign_xy.py
# Enter X,Y tag locations.
# Turn on logging to save the data.
# 2023-10-20

import tidreader
import valid_tids

def is_valid(tid):
    xy = input("enter X,Y: ")
    if xy != '':
        xy = eval(xy)
        tid = repr(tid)
        print("data[", tid, "] = ", xy)

def main():
    reader = tidreader.TidReader()
    while True:
        t = reader.read()
        if t is None:
            continue

        print(t)
        if t in valid_tids.DATA:
            is_valid(t)
        else:
            print(" ---- UNKNOWN")

# vim: set sw=4 ts=8 et ic ai:
