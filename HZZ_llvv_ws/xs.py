# -*- coding: utf-8 -*-

import ROOT
import os
import sys

if not hasattr(ROOT, 'getHiggsXS'):
    ROOT.gROOT.LoadMacro(os.path.dirname(os.path.abspath(os.path.realpath(__file__)))+"/cross_section.cxx")

def signal_xs(mass, width):
    r"""return inclusive cross section (gg->H->ZZ->4l) in unit of fb
    """
    return ROOT.getHiggsXS(mass, width)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print sys.argv[0],"mass width"
        exit(1)

    mass = float(sys.argv[1])
    width = float(sys.argv[2])
    print signal_xs(mass, width)
