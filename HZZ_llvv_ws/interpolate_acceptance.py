# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(os.path.realpath(__file__))), '..')))
from HZZ_llvv_ws import helper

import matplotlib.pyplot as plt
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

from scipy import interpolate
import numpy as np

def my_interpolate(file_name, prod='ggH'):
    r""" input is the text file for Yields
    """
    yields_dic, categories = helper.read_yield_input(file_name)
    #print yields_dic
    print categories
    masses = [300, 400, 500, 600, 700, 800, 900, 1000, 1200]
    all_yields_dic = {}
    for ich, category in enumerate(categories):
        all_yields_dic[category] = list(map((lambda x: yields_dic['Ae_{}{}'.format(prod, x)][ich]), masses))

    # plot all acceptances
    interp_list = {}
    for category, yields in all_yields_dic.iteritems():
        f = interpolate.interp1d(masses, yields, 'slinear')
        interp_list[category] = f

        # don't make plots..
        continue

        new_masses = np.arange(300, 1200, 10)
        new_yields = f(new_masses)

        plt.plot(masses, yields, 'o')
        plt.plot(new_masses, new_yields, '-')
        plt.xlabel('$m_{H}$ [GeV]')
        plt.ylabel('Yields for 1 $fb^{-1}$')
        plt.savefig('plots/acceptance/acceptance_{}_{}.png'.format(prod, category))
        plt.close()

    out_text = ""
    for mass in range(300, 1210, 10):
        out_text += "Ae_{}{} & ".format(prod, mass)
        out_text += ' & '.join([np.array_str(interp_list[x](mass)) for x in categories])
        out_text += '\n'

    with open('yields_{}.txt'.format(prod), 'w') as f:
        f.write(out_text)

if __name__ == "__main__":
    my_interpolate('inputs/Yields_13TeV.txt', 'ggH')
    my_interpolate('inputs/Yields_13TeV.txt', "VBFH")
