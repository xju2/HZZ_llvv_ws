# -*- coding: utf-8 -*-

import os
import sys

script_dir = os.path.join(os.path.dirname(os.path.abspath(os.path.realpath(__file__))), '..')

import xs

def make_para_xml(out_name, input_ws_name, out_ws_name, mass, width):
    inject_xs = xs.signal_xs(mass, width)*0.2/0.03365/1000  # in unit of pb

    template = script_dir+'/data/para_template_LWA.xml'
    with open(template, 'r') as f:
        filedata = f.read()

    filedata = filedata.replace('INPUTNAME', input_ws_name)
    filedata = filedata.replace('OUTPUTNAME', out_ws_name)
    filedata = filedata.replace('LLVV_INJECT_XS', "{:.4f}".format(inject_xs))

    with open(out_name, 'w') as f:
        f.write(filedata)
    print out_name,"is written"

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print sys.argv[0]," out_name input_ws out_ws mass width"
        exit(1)

    out_name = sys.argv[1]
    input_ws_name = sys.argv[2]
    out_ws_name = sys.argv[3]
    mass = float(sys.argv[4])
    width = float(sys.argv[5])
    make_para_xml(out_name, input_ws_name, out_ws_name, mass, width)
