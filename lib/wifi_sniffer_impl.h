/* -*- c++ -*- */
/* 
 * Copyright 2017 <+YOU OR YOUR COMPANY+>.
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

#ifndef INCLUDED_WIZI_DET_WIFI_SNIFFER_IMPL_H
#define INCLUDED_WIZI_DET_WIFI_SNIFFER_IMPL_H

#include <wizi_det/wifi_sniffer.h>

namespace gr {
  namespace wizi_det {

    class wifi_sniffer_impl : public wifi_sniffer
    {
     private:
      bool d_debug;
      float d_cor_diff_th;
      float d_fft_pwr_th;
      float d_fft_sc_th;
      enum {PREAMBLE, COPY_PREAMBLE, PAYLOAD, COPY_PAYLOAD} d_state;
      std::vector<gr::tag_t> d_tags_preamble;
      std::vector<gr::tag_t> d_tags_payload;
      unsigned long d_cor_len;
      unsigned long d_cor_win;
      unsigned long d_cor_cnt;
      float d_cor_diff[480];
      bool d_tag_state;
      gr_complex d_fft_buf[80];
      unsigned int d_fft_cnt;
      unsigned int d_skip_cnt;
      enum {ONGOING, SKIPPING} d_fft_state;


     public:
      wifi_sniffer_impl(bool debug, float cor_diff_th, float fft_pwr_th, float fft_sc_th);
      ~wifi_sniffer_impl();

      // Where all the action really happens
      void forecast(int noutput_items, gr_vector_int &ninput_items_required);
      bool find_wifi_in_preamble(float *, unsigned long);
      int fft_80(gr_complex *);

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);
    };

  } // namespace wizi_det
} // namespace gr

#endif /* INCLUDED_WIZI_DET_WIFI_SNIFFER_IMPL_H */

