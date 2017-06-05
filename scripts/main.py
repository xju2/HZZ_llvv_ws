# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import os

script_dir = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
sys.path.insert(0, script_dir+'')

class llvv_ws:
    r"""prepare the inputs for making the interference workspaces
    """
    def __init__(self):
