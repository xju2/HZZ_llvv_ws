# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import os

script_dir = os.path.join(os.path.dirname(os.path.abspath(os.path.realpath(__file__))), '..')
sys.path.insert(0, os.path.abspath(script_dir))

from HZZ_llvv_ws import prepare_yield_inputs as pp
from HZZ_llvv_ws.submit import BsubHandle

from optparse import OptionParser
import subprocess

class llvv_ws:
    r"""prepare the inputs for making the interference workspaces
    """
    def __init__(self, opt):
        print "llvv_ws is created"

        # load template
        self.template = script_dir+'/data/config_LWA_template.ini'

        self.opt = opt
        self.bsub_handle = BsubHandle()
        self.bsub_handle.no_submit = not self.opt.submit

        # limit code
        self.code_dir = "/afs/cern.ch/user/x/xju/work/combination/workspaceCombiner/"
        self.exe_limit = self.code_dir+"scripts/run_limit.sh"

    def get_config_name(self):
        return "HZZ_STXS_llvv_mH{}_wH{}.ini".format(self.mass, self.width)

    def get_ws_name(self):
        return 'combined_mH{}_wH{}.root'.format(self.mass, self.width)

    def check_input(self):
        pass

    def process_individual(self, mass, width):
        print "producing mH {} and wH {}".format(mass, width)
        self.mass = mass
        self.width = width

        pp.config_files(
            self.template, mass, width,
            self.get_config_name()
        )
        self.make_ws()
        self.submit_limit()

    def make_ws(self):
        if os.path.isfile(self.get_ws_name()):
            print self.get_ws_name(),"is there"
            return

        exe = ['mainCombiner', self.get_config_name()]
        print exe
        output = subprocess.check_output(exe)
        with open("log.make.mH{}.wH{}".format(self.mass, self.width), 'w') as f:
            f.write(output)

        mv_str = ['mv', 'combined.root', self.get_ws_name()]
        subprocess.call(mv_str)
        print self.get_ws_name(),"is created!"

    def submit_limit(self):
        ws_dir = os.path.dirname(os.path.abspath(__file__))
        out_dir = ws_dir+'/Limits'
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

        run_cmd = " ".join(
            [self.exe_limit, ws_dir+"/"+self.get_ws_name(), 'combined', 'mu', 'obsData',
             'mH={},gamma={}'.format(self.mass, self.width), 'limit', 'obs,exp',
             out_dir, '1', '0:1']
            )
        self.bsub_handle.submit(run_cmd)


if __name__ == "__main__":
    usage = "%prog mass width"
    version="%prog 1.0"
    parser = OptionParser(usage=usage, description="make workspaces", version=version)
    parser.add_option('--submit', default=False, action='store_true', help="If submit Limit jobs")
    (options,args) = parser.parse_args()

    handle = llvv_ws(options)
    mass = int(args[0])
    width = int(args[1])

    handle.process_individual(mass, width)
