# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import os

script_dir = os.path.join(os.path.dirname(os.path.abspath(os.path.realpath(__file__))), '..')
sys.path.insert(0, os.path.abspath(script_dir))

from HZZ_llvv_ws import prepare_yield_inputs as pp
from HZZ_llvv_ws import xs

import glob

sys.path.insert(0, '/afs/cern.ch/user/x/xju/work/code/root_plot_utils')
from root_plot_utils import maker
from root_plot_utils import AtlasStyle
from root_plot_utils.ploter import Ploter

import ROOT
ROOT.gROOT.SetBatch()

def plot_acceptance(width):
    mass_list = []
    acc_ee_list = []
    acc_mm_list = []
    for file_name in glob.glob("ggH*_wH{}.root".format(width)):
        mass = float(file_name.split('_')[0][3:])
        mass_list.append(mass)
        xs_signal = xs.signal_xs(mass, width)

        f1 = ROOT.TFile.Open(file_name)
        h_sig_ee = f1.Get("mT_ggF_eevv_signal")
        acc_ee_list.append(h_sig_ee.Integral()/xs_signal)

        h_sig_mm = f1.Get("mT_ggF_mmvv_signal")
        acc_mm_list.append(h_sig_mm.Integral()/xs_signal)

    canvas = ROOT.TCanvas()
    gr_ee = maker.maker.graph('gr_ee', mass_list, acc_ee_list)
    gr_mm = maker.maker.graph('gr_mm', mass_list, acc_mm_list)
    gr_ee.SetLineColor(2)

    gr_mm.SetLineColor(4)
    gr_mm.SetMarkerColor(4)

    gr_mm.Draw("AL")
    gr_mm.GetXaxis().SetTitle("mH")
    gr_mm.GetYaxis().SetTitle("Acceptance*Efficiency")
    gr_ee.Draw("L SAME")
    canvas.Draw()
    canvas.SaveAs("acceptance_wH{}.pdf".format(width))
    canvas.SaveAs("acceptance_wH{}.eps".format(width))

if __name__ == "__main__":
    plot_acceptance(1)
