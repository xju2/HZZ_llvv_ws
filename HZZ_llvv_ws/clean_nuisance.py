#!/usr/bin/env python
import glob

def is_one(line):
    if "=" in line:
        items = line[:-1].split('=')
        up,down = items[1].split()
        if abs(float(up)) == 1.:
            return True
    return False

def is_lumi(line):
    return "ATLAS_lumi" in line

def exchange(line):
    if "=" in line:
        items = line[:-1].split('=')
        down,up = items[1].split()
        if float(down) > 1.0 and float(up) < 1.0:
            res = "{} = {} {}\n".format(items[0], up, down)
        else:
            res = line
    else:
        res = line
    return res

def prune(file_name):
    out_text = ""
    with open(file_name) as f:
        for line in f:
            if is_one(line):
                continue
            if is_lumi(line):
                continue
            line = exchange(line)
            out_text += line

    with open(file_name, 'w') as f:
        f.write(out_text)

if __name__ == "__main__":
    for file_name in glob.glob("norm*_all.txt"):
        print file_name
        prune(file_name)
