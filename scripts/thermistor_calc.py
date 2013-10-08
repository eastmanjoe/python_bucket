#!/usr/bin/env python

import math

value = 2.31858

A = .0009376
B = .0002208
C = .0000001276
Ve = 5
constant = 24900
offset = -273.15

try:
    R = (constant * (value / Ve)) / (1 - (value / Ve))

    T1 = A + (B * math.log(R)) + (C * (math.log(R))**3)
    T1 = (1 / T1) + offset

    # value = T1
    print T1

except:
    value = float('nan')