#!/usr/bin/env python
import ROOT
ROOT.gROOT.SetBatch()

import os
import sys
import math
from array import array
from optparse import OptionParser

sys.path.insert(0, "/afs/cern.ch/user/x/xju/work/code/root_plot_utils")
from root_plot_utils.adder import adder
from root_plot_utils import AtlasStyle

sys.path.insert(0, "/afs/cern.ch/work/x/xju/code/check_workspace")
from check_workspace.helper import get_mass


class LimitPloter:
    def __init__(self, file_list, tag_list, options):
        print "Hello LimitPloter"
        self.file_list = file_list
        self.tag_list = tag_list
        self.opt = options

        self.is_blind = options.is_blind
        self.lumi = 36.1
        self.out_name = options.out
        self.prod_name = options.prod

        self.hvt = options.hvt
        if self.hvt:
            print "Doing HVT signal"

        if options.xsInput:
            self.get_xs_input(options.xsInput)
        else:
            self.xs_map = None

    def get_xs_input(self, file_name):
        print "Getting cross sections from", file_name
        self.xs_map = {}
        with open(file_name) as f:
            for line in f:
                mass, xs = line[:-1].split()
                self.xs_map[int(mass)] = eval(xs)

    def process(self):
        limits_ = []
        for file_, tag_ in zip(file_list, tag_list):
            limits_.append( self.get_graph_from_file(file_, tag_) )

        if len(limits_) < 1:
            print "nothing happens"
            return

        # if more than 1, plot uncertainty band only for the 1st.
        # the rest will be only expected and observed limit
        h_obs, h_exp, h_1s, h_2s = limits_[0]
        x_min = ROOT.Double(0)
        x_max = ROOT.Double(0)
        dummy_p = ROOT.Double(0)
        h_obs.GetPoint(0, x_min, dummy_p)
        h_obs.GetPoint(h_obs.GetN()-1, x_max, dummy_p)
        h_obs.Draw("LP")
        y_min = ROOT.TMath.MinElement(h_obs.GetN(), h_obs.GetY())
        y_max = ROOT.TMath.MaxElement(h_obs.GetN(), h_obs.GetY())
        print "range: ",x_min, x_max, y_min, y_max

        unit = "95% C.L. limit on #sigma("+self.prod_name+") #times BR("\
                +self.prod_name.split('rightarrow')[1]+"#rightarrowZZ) [pb]"
        if self.hvt:
            unit = "95% C.L. limit on #sigma(HVT) #times BR(WZ) [pb]"
            self.opt.titleX = "m_{HVT} [GeV]"

        dummy=ROOT.TH2F("dummy",";"+self.opt.titleX+";"+unit,
                        1000, x_min, x_max,
                        3000, y_min*10E-2, y_max*1E2)
        dummy.GetXaxis().SetNdivisions(509)
        dummy.GetXaxis().SetLabelSize(0.035)
        dummy.GetYaxis().SetLabelSize(0.035)
        dummy.GetYaxis().SetTitleSize(0.04)

        canvas = ROOT.TCanvas("canvas2", " ", 600, 600)
        canvas.SetLogy()
        dummy.Draw()
        h_2s.Draw("3")
        h_1s.Draw("3")
        h_exp.Draw("L")
        if not self.is_blind:
            h_obs.Draw("LP")

        legend = ROOT.myLegend(0.56, 0.60, 0.83, 0.90)
        # setup legend
        if not self.is_blind:
            legend.AddEntry(h_obs, "Observed #it{CL_{s}} limit", "l")
        legend.AddEntry(h_exp, "Expected #it{CL_{s}} limit", "l")
        legend.AddEntry(h_1s, "Expected #pm 1 #sigma", "f")
        legend.AddEntry(h_2s, "Expected #pm 2 #sigma", "f")

        # add other channels
        colors = [4, 6, 8 ]
        line_style = [2, 4]
        for irange in range(1, len(limits_)):
            h_obs, h_exp, h_1s, h_2s = limits_[irange]
            h_exp.Draw("L")
            h_exp.SetLineColor( colors[irange-1] )
            h_exp.SetMarkerColor( colors[irange-1] )
            h_exp.SetLineStyle( line_style[irange-1] )
            h_exp.SetLineWidth(2)
            legend.AddEntry(h_exp, tag_list[irange]+" Expected", "L")
            if not self.is_blind:
                pass 
                # h_obs.SetLineColor( colors[irange-1] )
                # h_obs.SetMarkerColor( colors[irange-1] )
                # h_obs.Draw("LP")
                # legend.AddEntry(h_obs, tag_list[irange], "L")

        legend.Draw()

        x_off_title = 0.20
        adder.add_text(x_off_title, 0.85, 1, "#bf{#it{ATLAS}} Preliminary")
        adder.add_text(x_off_title, 0.80, 1, "13 TeV, {:.1f} fb^{{-1}}".format(self.lumi))
        if self.hvt:
            adder.add_text(x_off_title, 0.75, 1, "HVT#rightarrowWZ#rightarrow"+self.opt.decay)
        else:
            adder.add_text(x_off_title, 0.75, 1, self.opt.prod+"#rightarrowZZ#rightarrow"+self.opt.decay)

        if self.opt.label:
            adder.add_text(x_off_title, 0.70, 1, self.opt.label)

        canvas.SaveAs(self.out_name+".eps")
        canvas.SaveAs(self.out_name+".pdf")
        canvas.SaveAs(self.out_name+".C")
        canvas.SaveAs(self.out_name+".root")

    def create_TGraphAsymmErrors(self, x_, nominal_, up_, down_):
        zero_ = array('f', [0]*len(x_))
        up_var_ = [x-y for x,y in zip(up_, nominal_)]
        down_var_ = [x-y for x,y in zip(nominal_, down_)]
        gr_error = ROOT.TGraphAsymmErrors(
            len(x_), array('f',x_), array('f',nominal_),
            zero_, zero_,
            array('f', down_var_), array('f', up_var_)
        )
        return gr_error

    def get_graph_from_list(self,
        mass_list, obs_list, exp_list,
        up_1sig_list, up_2sig_list,
        down_1sig_list, down_2sig_list
    ):
        zero_list = [0]*len(mass_list)
        print mass_list
        print exp_list
        gr_obs = ROOT.TGraph(len(mass_list), array('f', mass_list), array('f', obs_list))
        gr_exp = ROOT.TGraph(len(mass_list), array('f', mass_list), array('f', exp_list))
        gr_1sig = self.create_TGraphAsymmErrors(mass_list, exp_list, up_1sig_list, down_1sig_list)
        gr_2sig = self.create_TGraphAsymmErrors(mass_list, exp_list, up_2sig_list, down_2sig_list)
        gr_obs.SetLineWidth(2)
        gr_obs.SetLineStyle(1)
        gr_obs.SetMarkerStyle(20)
        gr_obs.SetMarkerSize(0.5)

        gr_exp.SetLineWidth(2)
        gr_exp.SetLineStyle(2)
        gr_exp.SetMarkerSize(0.5)

        gr_1sig.SetFillStyle(1001)
        gr_1sig.SetFillColor(ROOT.kGreen)
        gr_2sig.SetFillStyle(1001)
        gr_2sig.SetFillColor(ROOT.kYellow)
        return (gr_obs, gr_exp, gr_1sig, gr_2sig)

    def get_graph_from_file(self, file_name, option):
        mass_list = []
        obs_list = []
        exp_list = []
        up_2sig_list = []
        up_1sig_list = []
        down_1sig_list = []
        down_2sig_list = []

        if self.in_pb:
            unit_scale = 1E-3
        else:
            unit_scale = 1
        print file_name
        whole_list = []
        with open(file_name, 'r') as f:
            for line in f:
                items = line.split()

                mass_ = float(get_mass(items[0]))
                xs_scale = 1.0
                if self.xs_map:
                    try:
                        xs_scale = self.xs_map[int(mass_)]
                        print "xs for", mass_, xs_scale
                    except KeyError:
                        print mass_," not in ",self.opt.xsInput

                w_xs = xs_scale
                start_i = 3
                one_entry = ( mass_,
                      float(items[start_i])*w_xs, # -2
                      float(items[start_i+1])*w_xs, # -1
                      float(items[start_i+2])*w_xs, # median
                      float(items[start_i+3])*w_xs, # +1
                      float(items[start_i+4])*w_xs, # +2
                      float(items[start_i+5])*w_xs, # obs
                    )

        # sort the whole list
        return self.get_graph_from_list (
            mass_list, obs_list,
            exp_list,
            up_1sig_list,
            up_2sig_list,
            down_1sig_list,
            down_2sig_list
        )

if __name__ == "__main__":
    usage = "%prog [option] file_list tag_list"
    parser = OptionParser(description="plot limits", usage=usage)
    parser.add_option("-b", "--blind", dest='is_blind', default=False, help="if data is blind", action="store_true")
    parser.add_option("--prod", default="gg#rightarrowH", help="ggF production")
    parser.add_option("-o", "--outname", dest='out', default="combined_limit", help="out name")
    parser.add_option("-c", "--convert", dest='convert', default=False, help="need convert to pb", action="store_true")
    parser.add_option("-H", "--HVT", dest='hvt', default=False, help="HVT signal", action="store_true")
    parser.add_option("--RSG", default=False, help="RSG signal", action="store_true")
    parser.add_option("--titleX", default="m_{H} [GeV]", help="title of x-axis")
    parser.add_option("--decay", default="llll/ll#nu#nu", help="decay channels")
    parser.add_option("--xsInput", default=None, help="input cross sections")
    parser.add_option("--label", default=None, help="additional label")
    (options,args) = parser.parse_args()

    if len(args) < 2:
        parser.print_help()
        exit(1)

    file_list = args[0].split(',')
    tag_list = args[1].split(',')
    if len(file_list) != len(tag_list):
        print "files do not match tags"
        exit(2)

    limit_ploter = LimitPloter(file_list, tag_list, options)
    limit_ploter.process()
