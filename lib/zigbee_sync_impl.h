/* -*- c++ -*- */
/* 
 * Copyright 2017 <Chenglong Shao>.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifndef INCLUDED_WIZI_DET_ZIGBEE_SYNC_IMPL_H
#define INCLUDED_WIZI_DET_ZIGBEE_SYNC_IMPL_H

#include <wizi_det/zigbee_sync.h>
#include <string>

using namespace std;

namespace gr {
  namespace wizi_det {

    class zigbee_sync_impl : public zigbee_sync
    {
     private:
      bool d_debug;
      float d_cor;
      float d_pwr;
      unsigned int d_plateau;
      enum {SEARCH, TRANSFER, COPY_PREAMBLE, COPY_PAYLOAD} d_state;
      short d_cor_cnt;
      float d_cor_buf[10];
      gr_complex d_sample_buf[10];
      int d_index;
      int d_copy_cnt;
      long d_pkt_index;

     public:
      zigbee_sync_impl(bool debug, float correlation, float power, unsigned int plateau);
      ~zigbee_sync_impl();

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);
      int find_peak(float *cor_buf);
      void insert_tag(unsigned int out_index, uint64_t item, long pkt_index, string str);

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);
    };

  } // namespace wizi_det
} // namespace gr

#endif /* INCLUDED_WIZI_DET_ZIGBEE_SYNC_IMPL_H */

