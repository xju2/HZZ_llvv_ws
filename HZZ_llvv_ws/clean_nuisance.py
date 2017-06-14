#!/usr/bin/env python
import ROOT

import glob
import math
import subprocess
import sys

def is_lumi(line):
    return "ATLAS_lumi" in line

def regularize(line):
    if "=" in line:
        items = line[:-1].split('=')
        down,up = items[1].split()

        down, up = check(float(down), float(up))
        if down is None:
            return None
        res = "{} = {} {}\n".format(items[0], down, up)
    else:
        res = line
    return res

def check(down, up):
    if down > 1. and up > 1.:
        up = max([down, up])
        return (2.-up, up)
    elif down > 1. and up < 1.:
        return (up, down)
    elif down > 1. and up == 1.:
        return (2.-down, down)
    elif down == 1. and up == 1.:
        return (None, None)
    elif down == 1. and up < 1.:
        return (up, 2-up)
    elif down < 1. and up < 1.:
        down = min([down, up])
        return (down, 2-down)
    else:
        return (down, up)

def prune_norm_sys(file_name):
    out_text = ""
    with open(file_name) as f:
        for line in f:
            if is_lumi(line):
                continue
            line = regularize(line)
            if line:
                out_text += line

    with open(file_name, 'w') as f:
        f.write(out_text)

def variation(hist):
    r""" llvv analysis uses 17 bins for mT,
    but effective only 12 bins. Scale the
    integral to 12, then take the std. dev.
    as variation
    """
    total = 0
    for ibin in range(hist.GetNbinsX()):
        value = hist.GetBinContent(ibin+1)
        if abs(value) > 1E-4:
            total += 1

    hist.Scale(total/hist.Integral())
    vary = 0
    for ibin in range(hist.GetNbinsX()):
        value = hist.GetBinContent(ibin+1)
        if value != 0:
            vary += (value - 1)**2

    return math.sqrt(vary)/total

def prune_shape_sys(file_name):
    # loop all histograms in the file.
    fin = ROOT.TFile.Open(file_name)
    next = ROOT.TIter(fin.GetListOfKeys())
    key = next()
    good_hists = []
    while key:
        key_name = key.GetName()
        hist = key.ReadObj()
        if variation(hist) > 0.01:
            good_hists.append(hist)
        else:
            print hist.GetName(),"removed, in", file_name
        key = next()

    fout = ROOT.TFile.Open("out_temp.root", 'recreate')
    for hist in good_hists:
        hist.Write()
    fout.Close()
    fin.Close()

    exe = ['mv', file_name, file_name+'.bak']
    subprocess.call(exe)
    exe = ['mv', 'out_temp.root', file_name]
    subprocess.call(exe)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print sys.argv[0],"file_name"
        exit(1)

    file_name = sys.argv[1]
    prune_norm_sys(file_name)
    #for file_name in glob.glob("norm*_all.txt"):
    #    print file_name
    #    prune_norm_sys(file_name)

    #prune_shape_sys('test.root')
    #for file_name in glob.glob('sys*root'):
    #    prune_shape_sys(file_name)
