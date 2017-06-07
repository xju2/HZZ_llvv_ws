# -*- coding: utf-8 -*-
#!/usr/bin/env python

import ROOT
import os

script_dir = os.path.join(os.path.dirname(os.path.abspath(os.path.realpath(__file__))), '..')

def make_yield_input(file_name, out_name, prefix_name):
    r"""take a input root file and extra the yields from the histograms
    and put them in a text. Used for llvv analysis in LWA results

    Parameters
    ----------
    file_name : str
        name for input root file
    out_name : str
        name for output text file
    prefix_name : str
        prefix str for histogram name
    """
    f1 = ROOT.TFile.Open(file_name)
    h_sig_mm = f1.Get("mT_{}_signal".format(prefix_name.replace("XX", "mm")))
    h_sig_ee = f1.Get("mT_{}_signal".format(prefix_name.replace("XX", "ee")))

    h_hH_mm = f1.Get("mT_{}_hH".format(prefix_name.replace("XX", "mm")))
    h_hH_ee = f1.Get("mT_{}_hH".format(prefix_name.replace("XX", "ee")))

    h_HB_mm = f1.Get("mT_{}_HB".format(prefix_name.replace("XX", "mm")))
    h_HB_ee = f1.Get("mT_{}_HB".format(prefix_name.replace("XX", "ee")))

    out_text = "{} & {}\n".format(prefix_name.replace("XX", "ee"), prefix_name.replace("XX", "mm"))
    out_text += "n_signal  & {:.4f} & {:.4f} \n".format(h_sig_ee.Integral(), h_sig_mm.Integral())
    out_text += "n_hH      & {:.4f} & {:.4f} \n".format(h_hH_ee.Integral(), h_hH_mm.Integral())
    out_text += "n_HB      & {:.4f} & {:.4f} \n".format(h_HB_ee.Integral(), h_HB_mm.Integral())
    out_text += "n_ggZZ    & {:.4f} & {:.4f} \n".format(0.30113, 0.2987)

    with open(out_name, 'w') as f:
        f.write(out_text)

    print out_name,"is written"

def get_coeff_info(mass_list, width_list, coeff_info_name="coefInfo.ini"):
    out_text = ""
    for mass in mass_list:
        for width in width_list:
            out_text += "[sbiFormula_mH{}_w{}]\n".format(mass, width)
            out_text += "data = normed_yields_ggH{}_wH{}.txt\n".format(mass, width)
            out_text += "formula = mu*n_signal + sqrt(mu)*(n_HB+ n_hH) + n_ggZZ\n"
    with open(coeff_info_name, 'w') as f:
        f.write(out_text)

# prepare the configuration files for NWA and LWA.
template_LWA = script_dir+'/data/config_LWA_template.ini'
template_NWA = script_dir+'/data/config_NWA_template.ini'
template_LWA_noInt = script_dir+'/data/config_LWA_template_noInt.ini'

def config_files_LWA(mass, width, out_name):
    out_text = ""
    with open(template_LWA, 'r') as f:
        filedata = f.read()

    filedata = filedata.replace("SECTIONAME", 'sbiFormula_mH{}_w{}'.format(mass, width))
    filedata = filedata.replace("INPUTNAME", 'ggH{}_wH{}'.format(mass, width))

    with open(out_name, 'w') as f:
        f.write(filedata)

def config_files_LWA_noInt(mass, width, out_name):
    out_text = ""
    with open(template_LWA_noInt, 'r') as f:
        filedata = f.read()

    filedata = filedata.replace("YIELDS", 'n_signal,normed_yields_ggH{}_wH{}.txt'.format(mass, width))
    filedata = filedata.replace("INPUTNAME", 'ggH{}_wH{}'.format(mass, width))

    with open(out_name, 'w') as f:
        f.write(filedata)

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

    get_coeff_info(mass_list, widths)
    #exit(0)

    prefix_name = "ggF_XXvv"
    for mass in mass_list:
        for width in widths:
            input_name = "ggH"+str(mass)+"_wH"+str(width)+".root"
            out_name = "normed_yields_"+input_name.replace("root", "txt")
            make_yield_input(input_name, out_name, prefix_name)
