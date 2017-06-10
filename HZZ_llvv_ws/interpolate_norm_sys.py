# -*- coding: utf-8 -*-

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(os.path.realpath(__file__))), '..')))
from HZZ_llvv_ws import helper

import numpy as np
import matplotlib.pyplot as plt

class interpolate:
    r""" interpolate normalization systematic. search the input text files based on
    the mass and production mode!
    """
    def __init__(self, input_dir, prod):
        self.input_dir = input_dir
        self.prod = prod
        self. masses = [300, 400, 500, 600, 700, 800, 900, 1000, 1200]
        self.sys_dic_whole = {}

    def get_file_name(self, mass):
        return "norm_{}{}_all.txt".format(self.prod, mass)

    def run(self):
        sys_list = []
        for mass in self.masses:
            sys_list.append(helper.get_sys(os.path.join(self.input_dir, self.get_file_name(mass))))

        # generate masses from linear interpolation
        # take the systematic in 300 GeV
        self.get_interpolation(sys_list)
        for mass in range(300, 1210, 10):
            file_full_path = os.path.join(self.input_dir, self.get_file_name(mass))
            if os.path.exists(file_full_path):
                print file_full_path,"is there"
                continue
            else:
                self.make_sys(mass)
                print file_full_path,"is written"

    def get_interpolation(self, sys_list):
        if len(self.masses) != len(sys_list):
            print "inputs does not match", len(self.masses), len(sys_list)

        sys_dic = sys_list[0]
        for key, np_dic in sys_dic.iteritems():
            # loop each section, i.e. category
            if key not in self.sys_dic_whole:
                self.sys_dic_whole[key] = {}

            for nuisance in np_dic.keys():
                # loop over systematic
                # for each sys, get the value for each masss.
                down_list = []
                up_list = []
                for imass in range(len(self.masses)):
                    try:
                        down_value = sys_list[imass][key][nuisance][0]
                        up_value = sys_list[imass][key][nuisance][1]
                    except KeyError:
                        down_value = 0.9999
                        up_value = 1.0001

                    down_list.append(down_value)
                    up_list.append(up_value)

                self.sys_dic_whole[key][nuisance] = (down_list, up_list)

        #print self.sys_dic_whole

    def make_sys(self, mass):
        out_text = ""
        for key, np_dic in self.sys_dic_whole.iteritems():
            out_text += "[{}]\n".format(key)
            for nuisance in np_dic.keys():
                down_list, up_list = np_dic[nuisance]
                down = np.interp(mass, self.masses, down_list)
                up = np.interp(mass, self.masses, up_list)
                out_text += "{} = {:.4f} {:.4f}\n".format(nuisance, down, up)

                ## make a plot
                #plt.plot(self.masses, down_list, 'o')
                #int_list = np.linspace(300, 400, 10)
                #down_int = np.interp(int_list, self.masses, down_list)
                #plt.plot(int_list, down_int, '-x')
                ##plt.show()
                #plt.savefig('intepolate_{}_{}_{}.png'.format(self.prod, key, nuisance))
                #plt.close()
        with open(os.path.join(self.input_dir, self.get_file_name(mass)), 'w') as f:
            f.write(out_text)

if __name__ == "__main__":
    sys_int = interpolate('/afs/cern.ch/user/x/xju/work/h4l/highmass/workspaces/LLVV/NWA_sameBinning/inputs', 'ggH')
    sys_int.run()
