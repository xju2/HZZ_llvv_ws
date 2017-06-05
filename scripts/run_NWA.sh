#!/bin/bash

masses="300 400 500 600 700 800 900 1000 1200"
for mass in $masses
do
    echo $mass
    python main.py $mass --submit --hypo NWA
done

#python plot_limit.py limits_with_interference.txt,limits_no_interference.txt withInt,noInt --prod "pp#rightarrowH" --decay "llll/ll#nu#nu" --xsInput xs.txt
