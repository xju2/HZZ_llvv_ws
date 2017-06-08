#!/usr/bin/env python

import os
import sys
import commands
from optparse import OptionParser

script_dir = os.path.join(os.path.dirname(os.path.abspath(os.path.realpath(__file__))), '..')
sys.path.insert(0, os.path.abspath(script_dir))
from HZZ_llvv_ws.submit import BsubHandle

workdir = os.getcwd()

usage = "%prog [option] input_ws ana_name ws_name mu_name data_name fix_var"
parser = OptionParser(description="calculate limit", usage=usage)
parser.add_option('--nosub', default=False, action="store_true", help="do not submit")
options,args = parser.parse_args()

input_ws = args[0]
ana_name = args[1]
ws_name = args[2]
mu_name = args[3]
data_name = args[4]
fix_vars = args[5]
if len(args) > 6:
    fix_other_poi = args[6]
else:
    fix_other_poi = "0:1"

exe = "/afs/cern.ch/user/x/xju/work/combination/workspaceCombiner/scripts/run_limit.sh"
data_opt = "obs,exp" #obs, exp
cal_opt = "limit" # limit,pvalue
out_name = workdir

out_name += "/"+ana_name+"_Limit/"

print out_name
bsub_handle = BsubHandle()

bsub_handle.no_submit = options.nosub

run_cmd = exe+" "+input_ws+" "+ws_name+" "+mu_name+" "+\
        data_name+" "+fix_vars+" "+cal_opt+" "+data_opt+" "+\
        out_name+" 1 "+fix_other_poi

bsub_handle.submit(run_cmd)
#bsub_handle.print_summary()
