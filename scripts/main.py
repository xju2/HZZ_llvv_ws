#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(os.path.realpath(__file__))), '..')))

from HZZ_llvv_ws import prepare_yield_inputs as pp
from HZZ_llvv_ws.submit import BsubHandle
from HZZ_llvv_ws.llvv_ws_LWA import llvv_ws_LWA as ws_lwa

from optparse import OptionParser
import subprocess

class Main:
    r"""prepare the inputs for making the interference workspaces
    """
    def __init__(self, opt):
        print "Main is created"

        self.opt = opt
        self.bsub_handle = BsubHandle()
        self.bsub_handle.no_submit = not self.opt.submit

        # workspace for LWA
        input_name = "/afs/cern.ch/work/d/ddenysiu/public/forXY/Int_llvv/test_llvv_LWA.root"
        self.ws_handler = ws_lwa(input_name)

        # limit code
        self.code_dir = "/afs/cern.ch/user/x/xju/work/combination/workspaceCombiner/"
        self.exe_limit = self.code_dir+"scripts/run_limit.sh"

        # setup directories
        pwd = os.path.dirname(os.path.abspath(__file__))
        self.log_dir = os.path.join(pwd, 'Logs')
        if not os.path.exists(self.log_dir):
            os.mkdir(self.log_dir)
        self.config_dir = os.path.join(pwd, 'config_files')
        if not os.path.exists(self.config_dir):
            os.mkdir(self.config_dir)
        self.ws_dir = os.path.join(pwd, 'workspaces')
        if not os.path.exists(self.ws_dir):
            os.mkdir(self.ws_dir)




    def get_config_name(self):
        if hasattr(self, 'width'):
            return "HZZ_STXS_llvv_mH{}_wH{}.ini".format(self.mass, self.width)
        else:
            return "{}/HZZ_STXS_llvv_mH{}.ini".format(self.config_dir, self.mass)

    def get_ws_name(self):
        if hasattr(self, 'width'):
            return 'combined_mH{}_wH{}.root'.format(self.mass, self.width)
        else:
            return '{}/combined_mH{}.root'.format(self.ws_dir, self.mass)

    def process_LWA(self, mass, width):
        print "producing mH {} and wH {}".format(mass, width)

        self.mass = mass
        self.width = width

        self.make_ws()
        self.submit_limit()

    def process_NWA(self, mass):
        print "producing mH {}".format(mass)
        self.mass = mass
        pp.config_files_NWA(mass, self.get_config_name())
        self.make_ws()
        self.submit_limit()

    def make_ws(self):
        if os.path.isfile(self.get_ws_name()):
            print self.get_ws_name(),"is there"
            return

        if hasattr(self, 'width'):
            log_name = "Logs/log.make.mH{}.wH{}".format(self.mass, self.width)
            config_name = self.ws_handler.get_workspace_config(self.mass, self.width, not self.opt.noInt)
        else:
            log_name = "{}/log.make.mH{}".format(self.log_dir, self.mass)
            config_name = self.get_config_name()

        exe = ['mainCombiner', config_name]
        print exe
        output = subprocess.check_output(exe)

        with open(log_name, 'w') as f:
            f.write(output)

        mv_str = ['mv', 'combined.root', self.get_ws_name()]
        subprocess.call(mv_str)
        print self.get_ws_name(),"is created!"

    def get_limit_cmd(self, ws_dir, poi_name, fix_str, out_dir, other_poi="0:0"):
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

        run_cmd = " ".join(
            [self.exe_limit, os.path.abspath(self.get_ws_name()), 'combined', poi_name, 'obsData',
             fix_str, 'limit', 'obs,exp', out_dir, '1', other_poi]
        )
        return run_cmd

    def submit_limit(self):
        pwd = os.path.dirname(os.path.abspath(__file__))

        if hasattr(self, 'width'):
            fix_str = 'mH={},gamma={}'.format(self.mass, self.width)
            out_dir = pwd+'/Limits'
            self.bsub_handle.submit(self.get_limit_cmd(pwd, 'mu', fix_str, out_dir))
        else:
            fix_str = 'mH={}'.format(self.mass)
            poi_name = "mu_ggF"
            out_dir = pwd+'/ggF_Limits'
            self.bsub_handle.submit(self.get_limit_cmd(pwd, poi_name, fix_str, out_dir, "0:0"))

            poi_name = "mu_VBF"
            out_dir = pwd+'/VBF_Limits'
            self.bsub_handle.submit(self.get_limit_cmd(pwd, poi_name, fix_str, out_dir, "0:0"))

if __name__ == "__main__":
    usage = "%prog mass width"
    version="%prog 1.0"
    parser = OptionParser(usage=usage, description="make workspaces", version=version)
    parser.add_option('--submit', default=False, action='store_true', help="If submit Limit jobs")
    parser.add_option('--hypo', default="LWA", help="which hypothesis, LWA or NWA")
    parser.add_option('--noInt', default=False, action='store_true', help="no interference")
    (options,args) = parser.parse_args()

    handle = Main(options)
    mass = int(args[0])
    if options.hypo == "LWA":
        width = int(args[1])
        handle.process_LWA(mass, width)
    else:
        handle.process_NWA(mass)
