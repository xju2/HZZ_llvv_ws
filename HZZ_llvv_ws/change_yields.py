#!/usr/bin/env python

import os
import glob

def change_file(file_name):
    lumi = 36.1
    out_text = " ggF_eevv & ggF_mmvv \n"

    with open(file_name) as f:
        for line in f:
            items = line[:-1].split('&')
            items[1] = float(items[1])/lumi
            items[2] = float(items[2])/lumi
            out_text += "{} & {:.4f} & {:.4f} \n".format(*items)

    new_name = "normed_"+file_name
    if not os.path.exists(new_name):
        with open(new_name, 'w') as f:
            f.write(out_text)
        print new_name,"is written"
    else:
        print new_name,"is there"

if __name__ == "__main__":
    for file_name in glob.glob("yields_ggH*.txt"):
        change_file(file_name)
