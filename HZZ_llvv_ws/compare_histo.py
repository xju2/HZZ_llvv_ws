#!/usr/bin/env python

import sys
import ROOT
import os
import math

sys.path.insert(0, '/afs/cern.ch/user/x/xju/work/h4l/h4lcode/root_plot_utils/')
from root_plot_utils.ploter import Ploter

cmp_dir = "compare_signal_int"
if not os.path.exists(cmp_dir):
    os.mkdir(cmp_dir)

def compare(file_name):
    f1 = ROOT.TFile.Open(file_name)
    h_sig = f1.Get('mT_mm_signal')
    h_hH = f1.Get('mT_mm_hH')
    h_HB = f1.Get('mT_mm_HB')
    h_sig.Sumw2()
    h_hH.Sumw2()
    h_HB.Sumw2()

    #kappa = 0.462236
    kappa = 0.241128
    h_sig.Scale(kappa)
    h_hH.Scale(math.sqrt(kappa))
    h_HB.Scale(math.sqrt(kappa))

    h_sum = h_sig.Clone("mT_mm_sum")
    h_sum.Add(h_hH)
    h_sum.Add(h_HB)

    ps = Ploter()
    hist_list = [h_sum, h_sig, h_hH, h_HB]
    tag_list = ['sum', 'signal', 'Int_hH', 'Int_HB']
    options = {
        "out_folder": cmp_dir,
        "add_yields": True,
        "no_fill": True,
        "add_ratio": False,
        "out_name": os.path.basename(file_name).replace(".root", "")
    }
    ps.compare_hists(hist_list, tag_list, **options)

if __name__ == "__main__":
    compare('with_interference/ggH400_wH15.root')
