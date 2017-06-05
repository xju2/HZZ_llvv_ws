#!/usr/bin/evn python

def sum_yields(file_name):
    out_text = ""
    with open(file_name) as f:
        iline = 0
        for line in f:
            if iline == 0:
                items = line[:-1].split('&')
                print items
                out_text += "{} & {}\n".format(*items[1:3])
            else:
                items = line[:-1].split('&')
                name,ggF_ee,ggF_mm,VBF_ee,VBF_mm = items
                ee = float(ggF_ee) + float(VBF_ee)
                mm = float(ggF_mm) + float(VBF_mm)
                out_text += "{} & {:.4f} & {:.4f}\n".format(name, ee, mm)

            iline += 1

    with open(file_name, 'w') as f:
        f.write(out_text)

if __name__ == "__main__":
    sum_yields("Yields_13TeV.txt")
