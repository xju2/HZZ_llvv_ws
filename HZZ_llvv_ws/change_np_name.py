# -*- coding: utf-8 -*-

import glob
def change_ggF_theory(file_name):
    with open(file_name, 'r') as f:
        filedata = f.read()

    filedata = filedata.replace('ATLAS_SigPDF', 'pdf_Higgs_ggH')
    filedata = filedata.replace('ATLAS_SigQCD', 'QCDscale_ggH')
    filedata = filedata.replace('ATLAS_SigSHW', 'ATLAS_Showering_ggF')

    with open(file_name, 'w') as f:
        f.write(filedata)

def change_VBF_theory(file_name):
    with open(file_name, 'r') as f:
        filedata = f.read()

    filedata = filedata.replace('ATLAS_SigPDF', 'pdf_Higgs_qqH')
    filedata = filedata.replace('ATLAS_SigQCD', 'QCDscale_qqH')
    filedata = filedata.replace('ATLAS_SigSHW', 'ATLAS_Showering_VBF')

    with open(file_name, 'w') as f:
        f.write(filedata)

if __name__ == "__main__":
    for file_name in glob.glob("norm_cSys_ggH*.txt"):
        change_ggF_theory(file_name)

    for file_name in glob.glob("norm_cSys_VBFH*.txt"):
        change_VBF_theory(file_name)
