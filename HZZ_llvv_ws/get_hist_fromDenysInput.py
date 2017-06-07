#!/usr/bin/env python
import os
import sys


sys.path.insert(0, '/afs/cern.ch/user/x/xju/work/h4l/h4lcode/root_plot_utils')

from root_plot_utils.ploter import Ploter

import ROOT
ROOT.gROOT.SetBatch()

import array

ps = Ploter()
ps.add_ratio = False

#f1_name = "/afs/cern.ch/work/d/ddenysiu/public/tmp/Int_llvv/test_H_plus_hH.root"
f1_name = "/afs/cern.ch/work/d/ddenysiu/public/forXY/Int_llvv/test_llvv_LWA.root"
ch_names = {
    "ggF_eevv": 0,
    "ggF_mmvv": 1,
}
# widths = [1, 5, 10, 15]
# mass_range = (400, 1210, 10)
# mass_range = (400, 410, 10)

widths = [5, 10, 15]
mass_list = [400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1100, 1200]
#widths = [1]
#mass_list = [400]

# get template from Mariyan's input
# fin_temp = ROOT.TFile.Open("/afs/cern.ch/user/m/mpetrov/public/Combination_work_Updated/pdf_qqZZ_all.root")
# hist_temp = fin_temp.Get("mT-Nominal-ggF_eevv")
# hist_temp.SetDirectory(0)
# fin_temp.Close()

#hist_temp = ROOT.TH1F("temp", "template", 30, 0., 1500.)
xbins = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 800, 950, 1500]
hist_temp = ROOT.TH1F("temp", "template", len(xbins)-1, array.array('f', xbins))

fin = ROOT.TFile.Open(f1_name)
tree = fin.Get("tree_NOMINAL_slim")

cmp_dir = "compare_signal_int"
if not os.path.exists(cmp_dir):
    os.mkdir(cmp_dir)

norm_factor = 36.1 # lumonosity in pb-1
#for mass in range(*mass_range):
for mass in mass_list:
    for width in widths:
        out_name = "ggH"+str(mass)+"_wH"+str(width)+".root"
        has_out = False
        if os.path.exists(out_name):
            fout = ROOT.TFile.Open(out_name)
            has_out = True
        else:
            fout = ROOT.TFile.Open(out_name, 'recreate')


        for chan, cut in ch_names.iteritems():

            # signal only shape
            sig_name = "mT_"+chan+"_signal"
            if has_out:
                h_sig = fout.Get(sig_name)
            else:
                h_sig = hist_temp.Clone(sig_name)
                weight = "w_H___"+str(mass)+"_"+str(width)+"*(pass_to_SR==1 && event_type=="+str(cut)+")"
                tree.Draw("mT_ZZ>>"+h_sig.GetName(), weight)
                h_sig.Scale(1000)
                h_sig.Write()
                h_sig_clone = h_sig.Clone("mT-Nominal-"+chan)
                h_sig_clone.Write()

            # interference of higgs and Higgs
            int_hH_name = "mT_"+chan+"_hH"
            if has_out:
                h_hH = fout.Get(int_hH_name)
            else:
                h_hH = hist_temp.Clone(int_hH_name)
                weight = "w_h_H_"+str(mass)+"_"+str(width)+"*(pass_to_SR==1 && event_type=="+str(cut)+")"
                tree.Draw("mT_ZZ>>"+h_hH.GetName(), weight)
                h_hH.Scale(1000)
                h_hH.Write()

            # interference of Higgs and background
            int_HB_name = "mT_"+chan+"_HB"
            if has_out:
                h_HB = fout.Get(int_HB_name)
            else:
                h_HB = hist_temp.Clone(int_HB_name)
                weight = "w_H_B_"+str(mass)+"_"+str(width)+"*(pass_to_SR==1 && event_type=="+str(cut)+")"
                tree.Draw("mT_ZZ>>"+h_HB.GetName(), weight)
                h_HB.Scale(1000)
                h_HB.Write()

            sum_name = "mT_"+chan+"_Sum"
            h_sum = None
            if has_out:
                h_sum = fout.Get(sum_name)

            if not h_sum:
                h_sum = h_sig.Clone(sum_name)
                h_sum.Add(h_hH)
                h_sum.Add(h_HB)

            h_sig.Scale(norm_factor)
            h_hH.Scale(norm_factor)
            h_HB.Scale(norm_factor)
            h_sum.Scale(norm_factor)

            # make a simple comparison
            hist_list = [h_sum, h_sig, h_hH, h_HB]
            tag_list = ["h_sum", "signal", "hH", "HB"]
            options = {
                "out_folder": cmp_dir,
                "add_yields": True,
                "no_fill": True,
                "out_name": out_name.replace(".root", "_"+chan)
            }
            ps.compare_hists(hist_list, tag_list, **options)

        fout.Close()

fin.Close()
