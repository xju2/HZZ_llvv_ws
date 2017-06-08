# -*- coding: utf-8 -*-
#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch()

import os
import sys

# prepare the configuration files for NWA and LWA.
template_NWA = os.path.join(os.path.dirname(os.path.abspath(os.path.realpath(__file__))), '..')+\
        '/data/config_NWA_template.ini'

def config_files_NWA(mass, out_name):
    out_text = ""
    with open(template_NWA, 'r') as f:
        filedata = f.read()

    filedata = filedata.replace('EXPECTED_GGF', "Ae_ggH{}".format(mass))
    filedata = filedata.replace('EXPECTED_VBF', "Ae_VBFH{}".format(mass))
    filedata = filedata.replace('MASS', "{}".format(mass))

    with open(out_name, 'w') as f:
        f.write(filedata)

if __name__ == "__main__":
    widths = [1, 5, 10, 15]
    mass_list = [400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1100, 1200]
