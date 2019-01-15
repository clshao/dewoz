#!/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir=/home/ahyhus/gr-wizi_det/lib
export PATH=/home/ahyhus/gr-wizi_det/build/lib:$PATH
export LD_LIBRARY_PATH=/home/ahyhus/gr-wizi_det/build/lib:$LD_LIBRARY_PATH
export PYTHONPATH=$PYTHONPATH
test-wizi_det 
