#!/bin/bash

widths="1 5 10 15"
masses="400 450 500 550 600 650 700 750 800 850 900 950 1000 1100 1200"
for mass in $masses
do
    for width in $widths
    do
        echo $mass, $width
        python main.py $mass $width --submit
    done
done

#python plot_limit.py limits_with_interference.txt,limits_no_interference.txt withInt,noInt --prod "pp#rightarrowH" --decay "llll/ll#nu#nu" --xsInput xs.txt
