# -*- coding: utf-8 -*-

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