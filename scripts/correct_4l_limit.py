#!/usr/bin/env python

import sys

def apply_br(file_name):

    out_text = ""
    with open(file_name, 'r') as f:
        for line in f:
            items = line[:-1].split()
            out_text += '{} -1 -1 {:.5f} {:.5f} {:.5f} {:.5f} {:.5f} {:.5f}\n'.format(
                items[0], *[float(x)/0.00452/1000 for x in items[3:]])

    print out_text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print sys.argv[0],'file_name'
        exit(1)

    apply_br(sys.argv[1])
