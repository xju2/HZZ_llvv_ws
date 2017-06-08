#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.insert(0, '/afs/cern.ch/user/x/xju/work/h4l/h4lcode/root_plot_utils')
from root_plot_utils.ploter import Ploter

import ROOT
ROOT.gROOT.SetBatch()

import math

def plot(mass, width, mu, lumi=36.1):
    """
    parameters
    ----------
    mu: signal strength
    """
    in_name = "ggH"+str(mass)+"_wH"+str(width)+".root"
    if not os.path.exists(in_name):
        print in_name,"not there"
        return

    ps = Ploter()
    ps.add_ratio = False
    cmp_dir = "compare_signal_int"
    if not os.path.exists(cmp_dir):
        os.mkdir(cmp_dir)

    fin = ROOT.TFile.Open(in_name)
    ch_names = ['ggF_eevv', 'ggF_mmvv']
    for ch_name in ch_names:
        sig_name = 'mT_{}_signal'.format(ch_name)
        int_hH_name = 'mT_{}_hH'.format(ch_name)
        int_HB_name = 'mT_{}_HB'.format(ch_name)

        h_sig = fin.Get(sig_name)
        h_hH = fin.Get(int_hH_name)
        h_HB = fin.Get(int_HB_name)

        # scale by luminosity and signal strength
        h_sig.Scale(lumi*mu)
        h_hH.Scale(lumi*math.sqrt(mu))
        h_HB.Scale(lumi*math.sqrt(mu))

        sum_name = "mT_{}_Sum".format(ch_name)
        h_sum = h_sig.Clone(sum_name)
        h_sum.Add(h_hH)
        h_sum.Add(h_HB)

        # make a simple comparison
        hist_list = [h_sum, h_sig, h_hH, h_HB]
        tag_list = ["h_sum", "signal", "hH", "HB"]
        options = {
            "out_folder": cmp_dir,
            "add_yields": True,
            "no_fill": True,
            "out_name": "ggH{}_wH{}_{}_mu{}".format(mass, width, ch_name, mu),
            'label': "#mu = {:.4f}".format(mu)
        }
        ps.compare_hists(hist_list, tag_list, **options)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print sys.argv[0],"mass width mu"
        exit(1)

    mass = int(sys.argv[1])
    width = int(sys.argv[2])
    mu = float(sys.argv[3])
    plot(mass, width, mu)
