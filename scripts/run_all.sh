#!/bin/bash

function do_test(){
    python main.py 410 1 --submit
}

function run_all(){
    widths="1 5 10 15"
    for ((mass=400; mass <=1200; mass+=10))
    do
        for width in $widths
        do
            echo $mass, $width
            python main.py $mass $width --submit
        done
    done
}

#do_test
run_all

#python plot_limit.py limits_with_interference.txt,limits_no_interference.txt withInt,noInt --prod "pp#rightarrowH" --decay "llll/ll#nu#nu" --xsInput xs.txt
