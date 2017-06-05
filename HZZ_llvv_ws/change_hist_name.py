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

if __name__ == "__main__":
    for file_name in glob.glob("ggH*root"):
        print file_name
        change(file_name)
