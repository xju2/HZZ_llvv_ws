# -*- coding: utf-8 -*-
import os

def get_sys(file_name):
    """
    This will read text file for systematics,
    and returen a dictionary
    """
    sys_map = {}
    curr_section = ''
    with open(file_name) as f:
        for line in f:
            line = line.strip()
            if len(line) <= 0:
                continue

            if line.startswith('#'):
                continue

            # update the current section and add a section to the map
            if '[' in line:
                curr_section = line[1:-1].strip()
                if curr_section not in sys_map:
                    sys_map[curr_section] = {}
                continue

            sys_name = line.split('=')[0].strip()
            low, high = line.split('=')[1].split()
            sys_map[curr_section][sys_name] = (float(low), float(high))
    return sys_map

def read_yield_input(file_name):
    r"""Read the text file Yields
    """
    yields_dic = {}
    categories = None
    with open(file_name, 'r') as f:
        iline = 0
        for line in f:
            if iline == 0:
                categories = [x.strip() for x in line[:-1].split('&')]
            else:
                items = line.split('&')
                yields_dic[items[0].strip()] = [float(x.strip()) for x in items[1:]]
            iline += 1

    return yields_dic,categories

def check_dir(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
