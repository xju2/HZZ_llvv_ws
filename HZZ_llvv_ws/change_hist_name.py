#!/usr/bin/env python

import ROOT
import glob

def change(file_name):
    fin = ROOT.TFile.Open(file_name, "update")
    h_mm = fin.Get("mT_ggF_mmvv_signal")
    h_ee = fin.Get("mT_ggF_eevv_signal")

    mm_name = "mT_ggF_mmvv"
    if not fin.Get(mm_name):
        h_mm_new = h_mm.Clone(mm_name)
        h_mm_new.Write()
    else:
        print mm_name,"is there"

    ee_name = "mT_ggF_eevv"
    #ee_name = "mT-Nominal-ggF_eevv"
    if not fin.Get(ee_name):
        h_ee_new = h_ee.Clone(ee_name)
        h_ee_new.Write()
    else:
        print ee_name," is there"

    fin.Close()

def add_more(file_name, outname):
    fin = ROOT.TFile.Open(file_name)
    h_mm = fin.Get("mT_mm")
    h_ee = fin.Get("mT_ee")

    h_mm_ggF = h_mm.Clone("mT-Nominal-ggF_mmvv")
    h_mm_VBF = h_mm.Clone("mT-Nominal-VBF_mmvv")
    h_ee_ggF = h_ee.Clone("mT-Nominal-ggF_eevv")
    h_ee_VBF = h_ee.Clone("mT-Nominal-VBF_eevv")

    fout = ROOT.TFile.Open(outname, 'recreate')
    h_mm_ggF.Write()
    h_mm_VBF.Write()
    h_ee_ggF.Write()
    h_ee_VBF.Write()
    fout.Close()

    fin.Close()

def new_hist(old_hist, hist_name):
    r"""create a new histogram based on the input histogram.
    Old histograms with various binning are converted to
    new histograms with equal binning
    """
    h_temp = ROOT.TH1F(hist_name, hist_name, 30, 0, 1500)
    f_ref = ROOT.TFile.Open('/afs/cern.ch/user/m/mpetrov/public/Combination_llvv/20170605_inputs_same_binning/qqZZ.root')
    h_ref = f_ref.Get('mT_ee')
    for i in range(17):
        mT = old_hist.GetBinLowEdge(i+1)
        if mT <= 650:
            h_temp.SetBinContent(i+1, old_hist.GetBinContent(i+1))
        elif mT <= 700: # oldbin= 15, new == 15,16
            total = old_hist.GetBinContent(i+1)
            bin13 = h_ref.GetBinContent(i+1)
            bin14 = h_ref.GetBinContent(i+2)
            h_temp.SetBinContent(i+1, total*bin13/(bin13+bin14))
            h_temp.SetBinContent(i+2, total*bin14/(bin13+bin14))
        elif mT <= 800: #oldbin = 16, new=17, 18, 19
            total = old_hist.GetBinContent(i+1)
            bin17 = h_ref.GetBinContent(17)
            bin18 = h_ref.GetBinContent(18)
            bin19 = h_ref.GetBinContent(19)
            h_temp.SetBinContent(17, total*bin17/(bin17+bin18+bin19))
            h_temp.SetBinContent(18, total*bin18/(bin17+bin18+bin19))
            h_temp.SetBinContent(19, total*bin19/(bin17+bin18+bin19))
        else: #oldbin = 17, new=20,21,22,23,24,25,26,27,28,29,30
            total = old_hist.GetBinContent(i+1)
            total_ref = h_ref.Integral(20, 30)
            for new_bin in range(20, 31):
                h_temp.SetBinContent(new_bin, total*h_ref.GetBinContent(new_bin)/total_ref)

    return h_temp

def change_binning(file_name, out_name):
    fin = ROOT.TFile.Open(file_name)
    h_mm = fin.Get("mT-Nominal-ggF_mmvv")
    h_ee = fin.Get("mT-Nominal-ggF_eevv")

    h_mm_new = new_hist(h_mm, "mT_ggF_mmvv");
    h_mm_new.SetDirectory(0)
    h_ee_new = new_hist(h_ee, "mT_ggF_eevv");
    h_ee_new.SetDirectory(0)

    fout = ROOT.TFile(out_name, "recreate")
    h_mm_new.SetName("mT-Nominal-ggF_mmvv")
    h_mm_new.Write()
    h_ee_new.SetName("mT-Nominal-ggF_eevv")
    h_ee_new.Write()
    fout.Close()

    fin.Close()

def make_same_binning():
    masses = [300, 400, 500, 600, 700, 800, 900, 1000, 1200]
    source_dir = '/afs/cern.ch/user/m/mpetrov/public/Combination_llvv/20170605_inputs_same_binning/'
    for mass in masses:
        add_more(source_dir+'ggH{}.root'.format(mass), 'pdf_ggH{}_all.root'.format(mass))
        add_more(source_dir+'VBFH{}.root'.format(mass), 'pdf_VBFH{}_all.root'.format(mass))

    add_more(source_dir+'qqZZ.root', 'pdf_qqZZ_all.root')
    add_more(source_dir+'ggZZ.root', 'pdf_ggZZ_all.root')
    add_more(source_dir+'WZ.root', 'pdf_WZ_all.root')
    add_more(source_dir+'Other.root', 'pdf_Other_all.root')

    change_binning('bak_nominal_shape/pdf_emu_all.root', 'pdf_emu_all.root')
    change_binning('bak_nominal_shape/pdf_Zjets_all.root', 'pdf_Zjets_all.root')

if __name__ == "__main__":
    for file_name in glob.glob("ggH*root"):
        print file_name
        change(file_name)
    #make_same_binning()
