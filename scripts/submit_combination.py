#!/usr/bin/env python
"""
submit the combination jobs
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(os.path.realpath(__file__))), '..')))

import commands
import subprocess
from optparse import OptionParser

from HZZ_llvv_ws.submit import BsubHandle
from HZZ_llvv_ws.llvv_ws_LWA import llvv_ws_LWA

class Combination:
    def __init__(self, tag, options):
        self.code_dir = "/afs/cern.ch/user/x/xju/work/combination/workspaceCombiner/"
        self.exe_comb = self.code_dir+"scripts/run_combination.sh"
        self.exe_limit = self.code_dir+"scripts/run_limit.sh"

        self.wk_dir = "/afs/cern.ch/user/x/xju/work/combination/run_area/LWA_4l_llvv/"
        self.input_dir = self.wk_dir+"inputs"
        self.ws_out_dir = self.wk_dir+"workspace/"
        self.limit_out_dir = self.wk_dir+"limits/"

        self.bsub_handle = BsubHandle()
        self.bsub_handle.no_submit = True

        self.opt = options
        self.tag = tag

        self.mass = -1
        self.width = -1


    def get_xml(self):
        return self.code_dir+'cfg/combination_llll_llvv_HZZFrameWork_LWA.xml'

    def split_ws(self, in_ws, out_ws):
        print "split {} to {}".format(in_ws, out_ws)
        cmd = 'manager -w split -f {} -i all -p {} --editRFV true'.format(in_ws, out_ws)
        subprocess.call(cmd.split())

    def get_input(self):
        llll_input = os.path.join(self.input_dir, 'HZZllll_LWA_wH{}_splitted.root'.format(self.width))

        # split the llvv inputs, because of RooFormula
        llvv_input = os.path.join(self.input_dir,'llvv', self.tag,\
                                  'combined_mH{}_wH{}_splitted.root'.format(self.mass, self.width))

        print llvv_input
        if not os.path.exists(llvv_input):
            llvv_input_org = llvv_input.replace('_splitted','')
            self.split_ws(llvv_input_org, llvv_input)

        in_str = '"HZZllvv_LWA_splitted.root:{} HZZllll_LWA_splitted.root:{}"'.format(llvv_input, llll_input)
        return in_str

    def get_out_name(self):
        return os.path.join(self.ws_out_dir, self.tag,
                            "combined_mH{}GeV_wH{}_beforePara.root".format(self.mass, self.width))

    def comb_cmd(self):
        in_ws = self.get_input()
        xml = self.get_xml()
        out_name = self.get_out_name()
        run_cmd = " ".join([self.exe_comb, in_ws, xml, out_name])
        return run_cmd

    def process(self, mass, width):
        self.mass = mass
        self.width = width
        self.bsub_handle.submit(self.comb_cmd())
        self.bsub_handle.print_summary()

if __name__ == "__main__":
    usage = "%prog [option] version mass width"
    parser = OptionParser(description="submit jobs for combination", usage=usage)
    parser.add_option('-s', '--sub', dest='sub', default=False, action="store_true", help="Submit")

    options,args = parser.parse_args()

    if len(args) < 3:
        parser.print_help();
        exit(0)

    comb = Combination(args[0], options)
    if options.sub:
        comb.bsub_handle.no_submit = False
        print "submitting the JOBS"

    mass = int(args[1])
    width = int(args[2])
    comb.process(mass, width)

