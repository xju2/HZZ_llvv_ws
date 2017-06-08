#!/bin/bash

function do_test(){
    python main.py 410 1 --submit --noInt
}

function run_all(){
    widths="1 5 10 15"
    #widths="1"
    for ((mass=400; mass <=1200; mass+=10))
    do
        for width in $widths
        do
            echo $mass, $width
            python main.py $mass $width --submit --noInt
        done
    done
}
if [ $# -lt 1 ];then
    echo "do_test or run_all"
    exit
fi
$1
