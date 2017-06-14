# -*- coding: utf-8 -*-

import os
import sys

import ROOT
import helper

class llvv_ws_LWA:
    r"""prepare the inputs for making the interference workspace.
    """
    def __init__(self, signal_input_name):
        """
        parameters
        ----------
        signal_input_name comes from Denys, containing the signal
        and inteference of (h-H) and (H-B)!
        """
        self.fin = ROOT.TFile.Open(signal_input_name)
        self.tree = self.fin.Get("tree_NOMINAL_slim")

        self.template = os.path.join(os.path.dirname(os.path.abspath(os.path.realpath(__file__))), '..')+\
                '/data/config_LWA_template.ini'
        self.template_no_int = os.path.join(os.path.dirname(os.path.abspath(os.path.realpath(__file__))), '..')+\
                '/data/config_LWA_template_noInt.ini'
        self.lumi = 36.1
        self.mm_ch_name = "ggF_mmvv"
        self.ee_ch_name = 'ggF_eevv'

        # book directories
        self.config_dir = "config"
        helper.check_dir(self.config_dir)
        self.ws_dir = 'workspaces'
        helper.check_dir(self.ws_dir)
        self.inputs_dir = 'inputs'
        helper.check_dir(self.inputs_dir)

        # to be define in the fly
        self.mass = -1
        self.width = -1

    def get_workspace_config(self, mass, width, with_int=True):
        self.mass = mass
        self.width = width

        # input histograms
        if not os.path.exists(self.get_input_hist_name()):
            self.make_input_hist()
        else:
            print self.get_input_hist_name(),"is there"

        # yields for signal and interference
        if not os.path.exists(self.get_yields_name()):
            self.make_yields()
        else:
            print self.get_yields_name(),"is there"

        if with_int:
            # parametrization of coefficiency
            if not os.path.exists(self.get_coeff_name()):
                self.make_coeff()
            else:
                print self.get_coeff_name(),"is there"

            if not os.path.exists(self.get_config_name()):
                self.config_files_LWA()
        else:
            if not os.path.exists(self.get_config_name()):
                self.config_files_LWA_noInt()

        return self.get_config_name()

    # make inputs...
    def make_input_hist(self):
        r"""prepare the input histograms, based one Denys's input
        e.g ggH400_wH1.root
        """
        ch_names = {
            self.ee_ch_name: 0,
            self.mm_ch_name: 1,
        }
        hist_temp = ROOT.TH1F("temp", "template", 30, 0., 1500.)

        out_name = self.get_input_hist_name()
        fout = ROOT.TFile.Open(out_name, 'recreate')
        for chan, cut in ch_names.iteritems():
            # signal only shape
            sig_name = "mT_"+chan+"_signal"
            h_sig = hist_temp.Clone(sig_name)
            weight = "w_H___"+str(self.mass)+"_"+str(self.width)+"*(pass_to_SR==1 && event_type=="+str(cut)+")"
            self.tree.Draw("mT_ZZ>>"+h_sig.GetName(), weight)
            h_sig.Scale(1000)
            h_sig.Write()
            h_sig_clone = h_sig.Clone("mT-Nominal-"+chan)
            h_sig_clone.Write()

            # interference of higgs and Higgs
            int_hH_name = "mT_"+chan+"_hH"
            h_hH = hist_temp.Clone(int_hH_name)
            weight = "w_h_H_"+str(self.mass)+"_"+str(self.width)+"*(pass_to_SR==1 && event_type=="+str(cut)+")"
            self.tree.Draw("mT_ZZ>>"+h_hH.GetName(), weight)
            h_hH.Scale(1000)
            h_hH.Write()

            # interference of Higgs and background
            int_HB_name = "mT_"+chan+"_HB"
            h_HB = hist_temp.Clone(int_HB_name)
            weight = "w_H_B_"+str(self.mass)+"_"+str(self.width)+"*(pass_to_SR==1 && event_type=="+str(cut)+")"
            self.tree.Draw("mT_ZZ>>"+h_HB.GetName(), weight)
            h_HB.Scale(1000)
            h_HB.Write()
        fout.Close()

    def make_yields(self):
        r"""take a input root file and extra the yields from the histograms
        and put them in a text.
        """
        f1 = ROOT.TFile.Open(self.get_input_hist_name())

        h_sig_mm = f1.Get("mT_{}_signal".format(self.mm_ch_name))
        h_sig_ee = f1.Get("mT_{}_signal".format(self.ee_ch_name))
        h_hH_mm = f1.Get("mT_{}_hH".format(self.mm_ch_name))
        h_hH_ee = f1.Get("mT_{}_hH".format(self.ee_ch_name))
        h_HB_mm = f1.Get("mT_{}_HB".format(self.mm_ch_name))
        h_HB_ee = f1.Get("mT_{}_HB".format(self.ee_ch_name))

        out_text = "{} & {}\n".format(self.ee_ch_name, self.mm_ch_name)
        out_text += "n_signal  & {:.4f} & {:.4f} \n".format(h_sig_ee.Integral(), h_sig_mm.Integral())
        out_text += "n_hH      & {:.4f} & {:.4f} \n".format(h_hH_ee.Integral(), h_hH_mm.Integral())
        out_text += "n_HB      & {:.4f} & {:.4f} \n".format(h_HB_ee.Integral(), h_HB_mm.Integral())
        out_text += "n_ggZZ    & {:.4f} & {:.4f} \n".format(0.30113, 0.2987)

        with open(self.get_yields_name(), 'w') as f:
            f.write(out_text)
        print self.get_yields_name(),"is written"

    def make_coeff(self):
        r"""make coefficiency, e.g coeffInfo_xx.ini
        """
        out_text = "[{}]\n".format(self.get_section_name())
        out_text += "data = {}\n".format(self.get_yields_name())
        #out_text += "formula = mu*n_signal + sqrt(mu)*(n_HB+ n_hH) + n_ggZZ\n"
        out_text += "formula = mu*n_signal + sqrt(mu)*(n_HB+ n_hH)\n"
        with open(self.get_coeff_name(), 'w') as f:
            f.write(out_text)
        print self.get_coeff_name(),"is written"

    # define common names for various inputs
    def get_coeff_name(self):
        return os.path.join(self.inputs_dir, 'coefInfo_mH{}_wH{}.ini'.format(self.mass, self.width))

    def get_input_hist_name(self):
        return os.path.join(self.inputs_dir, 'ggH{}_wH{}.root'.format(self.mass, self.width))

    def get_section_name(self):
        return 'sbiFormula_mH{}_wH{}'.format(self.mass, self.width)

    def get_config_name(self):
        return os.path.join(self.config_dir, "HZZ_STXS_llvv_mH{}_wH{}.ini".format(self.mass, self.width))

    def get_yields_name(self):
        return os.path.join(self.inputs_dir, "normed_yields_ggH{}_wH{}.txt".format(self.mass, self.width))

    # produce the configuration file for LWA with interference
    def config_files_LWA(self):
        r"""main program to produce the configuration file for a mass and width
        with interference
        """
        out_text = ""
        with open(self.template, 'r') as f:
            filedata = f.read()

        filedata = filedata.replace("INPUTDIR", os.path.abspath(self.inputs_dir))
        filedata = filedata.replace("SECTIONAME", self.get_section_name())
        filedata = filedata.replace("INPUTNAME", os.path.basename(self.get_input_hist_name()))
        filedata = filedata.replace("COEFF", self.get_coeff_name())

        with open(self.get_config_name(), 'w') as f:
            f.write(filedata)

    def config_files_LWA_noInt(self):
        r"""main program to produce the configuration file for a mass and width
        without interference
        """
        out_text = ""
        with open(self.template_no_int, 'r') as f:
            filedata = f.read()

        filedata = filedata.replace("INPUTDIR", os.path.abspath(self.inputs_dir))
        filedata = filedata.replace("YIELDS", 'n_signal,{}'.format(self.get_yields_name()))
        filedata = filedata.replace("INPUTNAME", self.get_input_hist_name())

        with open(self.get_config_name(), 'w') as f:
            f.write(filedata)
