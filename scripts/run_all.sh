#!/bin/bash

function change {
cat HZZ_STXS_llvv_400.ini | sed 's/400/700/g' > HZZ_STXS_llvv_700.ini
cat HZZ_STXS_llvv_400.ini | sed 's/400/900/g' > HZZ_STXS_llvv_900.ini
cat HZZ_STXS_llvv_400.ini | sed 's/400/1200/g' > HZZ_STXS_llvv_1200.ini
}

function make_ws {
if [ ! -f ${ws_name} ]; then
    mainCombiner HZZ_STXS_llvv_${mass}.ini >& log.make.${mass}
    mv combined.root ${ws_name}
else
    echo "${ws_name} is there"
fi
}

function  limits {
get_stats ${ws_name} combined mu obsData ModelConfig 1 mH=${mass} limit obs,exp 0:1 >& log.fit.${mass}
}

change 
masses="700 900 1200"
for mass in $masses
do
    echo $mass
    ws_name=combined_${mass}.root
    make_ws
    limits
done

#python plot_limit.py limits_with_interference.txt,limits_no_interference.txt withInt,noInt --prod "pp#rightarrowH" --decay "llll/ll#nu#nu" --xsInput xs.txt
