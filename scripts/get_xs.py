#!/usr/bin/env python

import os
import sys

script_dir = os.path.join(os.path.dirname(os.path.abspath(os.path.realpath(__file__))), '..')
sys.path.insert(0, os.path.abspath(script_dir))

from HZZ_llvv_ws import xs

width = 15
out = ""
for mass in range(400, 1210, 10):
    out += "{} {:.4f}*0.2/0.03365/0.04044/1000\n".format(mass, xs.signal_xs(mass, width))

with open('xs_wH{}.txt'.format(width), 'w') as f:
    f.write(out)
