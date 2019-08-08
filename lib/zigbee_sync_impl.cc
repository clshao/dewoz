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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "zigbee_sync_impl.h"

#define dout d_debug && std::cout

using namespace gr::wizi_det;
using namespace std;

static const int PREAMBLE_SAMPLE_CNT = 320 * 8 + 32 * 20; //ZigBee preamble + SFD

zigbee_sync::sptr
zigbee_sync::make(bool debug, float correlation, float power, unsigned int plateau)
{
  return gnuradio::get_initial_sptr
	(new zigbee_sync_impl(debug, correlation, power, plateau));
}


zigbee_sync_impl::zigbee_sync_impl(bool debug, float correlation, float power, unsigned int plateau)
  : gr::block("zigbee_sync",
		  gr::io_signature::make3(3, 3, sizeof(float), sizeof(float), sizeof(gr_complex)),
		  gr::io_signature::make2(2, 2, sizeof(float), sizeof(gr_complex))),
		  d_debug(debug),
		  d_cor(correlation),
		  d_pwr(power),
		  d_plateau(plateau),
		  d_state(SEARCH),
		  d_cor_cnt(0),
		  d_index(0),
		  d_copy_cnt(0),
		  d_pkt_index(0)

{
	set_tag_propagation_policy(block::TPP_DONT);
}


zigbee_sync_impl::~zigbee_sync_impl()
{
}

void
zigbee_sync_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
{
  ninput_items_required[0] = noutput_items;
  ninput_items_required[1] = noutput_items;
  ninput_items_required[2] = noutput_items;
}

int
zigbee_sync_impl::general_work (int noutput_items,
				   gr_vector_int &ninput_items,
				   gr_vector_const_void_star &input_items,
				   gr_vector_void_star &output_items)
{
  const float *in_cor = (const float *) input_items[0];
  const float *in_pwr = (const float *) input_items[1];
  const gr_complex *in_sample = (const gr_complex *) input_items[2];
  float *out_cor = (float *) output_items[0];
  gr_complex *out_sample = (gr_complex *) output_items[1];

  int ninput = std::min(std::min(ninput_items[0], ninput_items[1]), ninput_items[2]);
  int noutput = noutput_items;

  int i = 0;
  int o = 0;

  switch(d_state) {
  case SEARCH:

	  while(i < ninput) {
		  if(in_cor[i] > d_cor && in_pwr[i] > d_pwr) {
			  std::cout << "Cor: " << in_cor[i] << " " << "power: " << in_pwr[i] << std::endl;
			  d_cor_buf[d_cor_cnt] = in_cor[i];
			  d_sample_buf[d_cor_cnt] = in_sample[i];
			  d_cor = 0;
			  d_cor_cnt++;
			  i++;
			  if(d_cor_cnt == d_plateau) {
				  d_index = find_peak(d_cor_buf);
				  d_state = TRANSFER;
				  d_cor_cnt = 0;
				  d_pkt_index++;
				  insert_tag(0, nitems_written(0), PREAMBLE_SAMPLE_CNT - 31, "Preamble start");
				  insert_tag(1, nitems_written(1), PREAMBLE_SAMPLE_CNT - 31, "Preamble start");
				  dout << "ZigBee found!" << std::endl;
				  break;
			  }
		  }
		  else i++;
	  }

	  consume_each(i);
	  return 0;

  case TRANSFER:
	  while(o < noutput) {
		  out_cor[o] = d_cor_buf[d_index];
		  out_sample[o] = d_sample_buf[d_index];
		  o++;
		  d_index++;
		  if(d_index == d_plateau) {
			  d_state = COPY_PREAMBLE;
			  dout << "Transfer ends (ZigBee_Sync)." << std::endl;
			  break;
		  }
	  }

	  consume_each(0);
	  return o;

  case COPY_PREAMBLE: // Preamble = ZigBee preamble + SFD
	  while(i < ninput && o < noutput && d_copy_cnt <= PREAMBLE_SAMPLE_CNT - 31 - d_plateau + d_index) {
		  out_cor[o] = in_cor[i];
		  out_sample[o] = in_sample[i];
		  i++;
		  o++;
		  d_copy_cnt++;
		  if(d_copy_cnt == PREAMBLE_SAMPLE_CNT - 31 - d_plateau + d_index + 1) {
			  d_state = COPY_PAYLOAD;
			  d_index = 0;
			  d_copy_cnt = 0;
			  dout << "COPY_PREAMBLE ends (ZigBee_Sync)." << std::endl;
			  break;
		  }
	  }

	  consume_each(i);
	  return o;

  case COPY_PAYLOAD:
	  while(i < ninput && o < noutput) {
		  if(in_pwr[i] > d_pwr) {
			  out_cor[o] = 0;
			  out_sample[o] = in_sample[i];
			  i++;
			  o++;
		  }
		  else {
			  d_state = SEARCH;
			  insert_tag(0, nitems_written(0), d_pkt_index, "Payload end");
			  insert_tag(1, nitems_written(1), d_pkt_index, "Payload end");
			  dout << "COPY_PAYLOAD ends (ZigBee_Sync)." << std::endl;
			  break;
		  }
	  }

	  consume_each(i);
	  return o;
  }

  throw std::runtime_error("zigbee sync: unknown state");
  return 0;
}

int zigbee_sync_impl::find_peak(float *cor_buf) {
	int i, index;
	float temp_value = 0;

	for(i = 0; i < d_plateau; i++) {
		dout << cor_buf[i] << std::endl;
		if(cor_buf[i] > temp_value) {
			temp_value = cor_buf[i];
			index = i;
		}
	}

	dout << "Peak value: " << temp_value << std::endl;

	return index;
}

void zigbee_sync_impl::insert_tag(unsigned int out_index, uint64_t item, long pkt_index, string str) {
	const pmt::pmt_t key = pmt::string_to_symbol(str);
	const pmt::pmt_t value = pmt::from_long(pkt_index);
	const pmt::pmt_t srcid = pmt::string_to_symbol(name());
	add_item_tag(out_index, item, key, value, srcid);
}

