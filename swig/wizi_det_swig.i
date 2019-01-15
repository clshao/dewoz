/* -*- c++ -*- */

#define WIZI_DET_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "wizi_det_swig_doc.i"

%{
#include "wizi_det/wifi_sniffer.h"
#include "wizi_det/zigbee_sync.h"
%}


%include "wizi_det/wifi_sniffer.h"
GR_SWIG_BLOCK_MAGIC2(wizi_det, wifi_sniffer);
%include "wizi_det/zigbee_sync.h"
GR_SWIG_BLOCK_MAGIC2(wizi_det, zigbee_sync);
