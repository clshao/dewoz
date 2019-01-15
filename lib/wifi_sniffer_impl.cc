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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "wifi_sniffer_impl.h"
#include <math.h>

#define dout d_debug && std::cout

using namespace gr::wizi_det;
using namespace std;

static const int SEARCH_WIN = 480;
static const int COR_NUM_TH = 250;

wifi_sniffer::sptr
wifi_sniffer::make(bool debug, float cor_diff_th, float fft_pwr_th, float fft_sc_th)
{
  return gnuradio::get_initial_sptr
	(new wifi_sniffer_impl(debug, cor_diff_th, fft_pwr_th, fft_sc_th));
}

wifi_sniffer_impl::wifi_sniffer_impl(bool debug, float cor_diff_th, float fft_pwr_th, float fft_sc_th)
  : gr::block("wifi_sniffer",
		  gr::io_signature::make3(3, 3, sizeof(float), sizeof(float), sizeof(gr_complex)),
		  gr::io_signature::make(1, 1, sizeof(gr_complex))),
		  d_debug(debug),
		  d_cor_diff_th(cor_diff_th),
		  d_fft_pwr_th(fft_pwr_th),
		  d_fft_sc_th(fft_sc_th),
		  d_state(PREAMBLE),
		  d_cor_len(0),
		  d_cor_win(0),
		  d_cor_cnt(0),
		  d_tag_state(0),
		  d_fft_cnt(0),
		  d_skip_cnt(0),
		  d_fft_state(ONGOING)
{
	set_tag_propagation_policy(block::TPP_DONT);
}

wifi_sniffer_impl::~wifi_sniffer_impl()
{
}

void
wifi_sniffer_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
{
	ninput_items_required[0] = noutput_items;
	ninput_items_required[1] = noutput_items;
	ninput_items_required[2] = noutput_items;
}

int
wifi_sniffer_impl::general_work (int noutput_items,
				   gr_vector_int &ninput_items,
				   gr_vector_const_void_star &input_items,
				   gr_vector_void_star &output_items)
{
	const float *in_cor = (const float *) input_items[0];
	const float *in_clr_cor = (const float *) input_items[1];
	const gr_complex *in_sample = (const gr_complex *) input_items[2];
	gr_complex *out_sample = (gr_complex *) output_items[0];

	int ninput = std::min(std::min(ninput_items[0], ninput_items[1]), ninput_items[2]);
	int noutput = noutput_items;

	int i = 0;
	int o = 0;

	if(d_state == PREAMBLE) {
		const uint64_t nread_preamble = nitems_read(0);
		const pmt::pmt_t key_preamble = pmt::string_to_symbol("Preamble start");
		get_tags_in_range(d_tags_preamble, 0, nread_preamble, nread_preamble + ninput, key_preamble);
		if (d_tags_preamble.size()) {
			//dout << "Find tag 'Preamble start'." << std::endl;
			std::sort(d_tags_preamble.begin(), d_tags_preamble.end(), gr::tag_t::offset_compare);

			const uint64_t offset_preamble = d_tags_preamble.front().offset;

			if (offset_preamble > nread_preamble) {
				ninput = offset_preamble - nread_preamble;
			} else {
				d_cor_len = pmt::to_long(d_tags_preamble.front().value);
			}
		}
	}
	else {
		const uint64_t nread_payload = nitems_read(2);
		const pmt::pmt_t key_payload = pmt::string_to_symbol("Payload end");
		get_tags_in_range(d_tags_payload, 2, nread_payload, nread_payload + ninput, key_payload);
		if (d_tags_payload.size()) {
			d_tag_state = true;
			dout << "Find tag 'Payload end'." << std::endl;
			std::sort(d_tags_payload.begin(), d_tags_payload.end(), gr::tag_t::offset_compare);

			const uint64_t offset_payload = d_tags_payload.front().offset;

			if (offset_payload > nread_payload) {
				ninput = offset_payload - nread_payload;
			}
		}
	}

	switch(d_state) {
	case PREAMBLE:

		dout << "Enter PREAMBLE (Wi-Fi_Sniffer)." << std::endl;

		while(i < ninput && o < noutput) {
			d_cor_diff[d_cor_win] = abs(in_cor[i] - in_clr_cor[i]);
			out_sample[o] = in_sample[i];
			i++;
			o++;
			d_cor_win++;
			d_cor_cnt++;
			if(d_cor_win == SEARCH_WIN && d_cor_cnt != d_cor_len) {
				if(find_wifi_in_preamble(d_cor_diff, d_cor_win)) {
					d_state = COPY_PREAMBLE;
					d_cor_win = 0;
					d_cor_cnt =0;
					d_cor_len = 0;
					std::cout << "Wi-Fi found in preamble." << std::endl;
					break;
				}
				else {
					d_cor_win = 0;
				}
			}
			else if(d_cor_cnt == d_cor_len) {
				d_cor_cnt = 0;
				d_cor_len = 0;
				if(find_wifi_in_preamble(d_cor_diff, d_cor_win)) {
					d_state = COPY_PREAMBLE;
					d_cor_win = 0;
					std::cout << "Wi-Fi found in preamble." << std::endl;
					break;
				}
				else {
					d_state = PAYLOAD;
					d_cor_win = 0;
					dout << "Wi-Fi not found in preamble." << std::endl;
					break;
				}
			}
		}

		consume_each(i);
		return o;

	case COPY_PREAMBLE:

		dout << "Enter COPY_PREAMBLE (Wi-Fi_Sniffer)." << std::endl;

		while(i < ninput && o < noutput) {
			out_sample[o] = in_sample[i];
			i++;
			o++;
			if(d_tag_state && i == ninput) {
				d_state = PREAMBLE;
				dout << "COPY_PREAMBLE ends (Wi-Fi_Sniffer)." << std::endl;
			}
		}

		consume_each(i);
		return o;

	case PAYLOAD:

		dout << "Enter PAYLOAD (Wi-Fi_Sniffer)." << std::endl;

		switch(d_fft_state) {
		case ONGOING:

			dout << "ONGOING (Wi-Fi_Sniffer)" << std::endl;

			while(i < ninput && o < noutput) {
				d_fft_buf[d_fft_cnt] = in_sample[i];
				out_sample[o] = in_sample[i];
				i++;
				o++;
				d_fft_cnt++;
				if(d_fft_cnt == 80) {
					if(fft_80(d_fft_buf) >= d_fft_sc_th) {
						d_fft_cnt = 0;
						d_state = COPY_PAYLOAD;
						std::cout << "Wi-Fi found in payload." << std::endl;
						break;
					}
					else { //Skip the following 240 samples
						d_fft_cnt = 0;
						d_fft_state = SKIPPING;
						break;
					}
				}
			}

			if(d_tag_state && i == ninput) {
				d_fft_cnt = 0;
				d_tag_state = false;
				d_state = PREAMBLE;
				std::cout << "Payload assessment ends (ongoing). Wi-Fi not found." << std::endl;
			}

			consume_each(i);
			return o;

		case SKIPPING:

			dout << "SKIPPING (Wi-Fi_Sniffer)" << std::endl;

			while(i < ninput && o < noutput) {
				out_sample[o] = in_sample[i];
				i++;
				o++;
				d_skip_cnt++;
				if(d_skip_cnt == 240) {
					d_skip_cnt = 0;
					d_fft_state = ONGOING;
					if(d_tag_state && i == ninput) {
						d_tag_state = false;
						d_state = PREAMBLE;
						std::cout << "Payload assessment ends (skipping). Wi-Fi not found." << std::endl;
					}
					break;
				}
			}

			consume_each(i);
			return o;

		}

		throw std::runtime_error("wifi sniffer: unknown FFT state");
		return 0;

	case COPY_PAYLOAD:

		dout << "Enter COPY_PAYLOAD (Wi-Fi_Sniffer)." << std::endl;

		while(i < ninput && o < noutput) {
			out_sample[o] = in_sample[i];
			i++;
			o++;
			if(d_tag_state && i == ninput) {
				d_state = PREAMBLE;
				dout << "COPY_PAYLOAD ends (Wi-Fi_Sniffer)." << std::endl;
			}
		}

		consume_each(i);
		return o;

	}

	throw std::runtime_error("wifi sniffer: unknown state");
	return 0;
}

bool wifi_sniffer_impl::find_wifi_in_preamble(float *cor_diff, unsigned long count) {
	bool wifi_found;
	int num = 0;

	if(count == SEARCH_WIN) {
		for(int i = 0; i < SEARCH_WIN - 1; i++) {
			num += cor_diff[i] > d_cor_diff_th ? 1 : 0;
		}
		wifi_found = num >= COR_NUM_TH ? true : false;
	}
	else {
		for(int i = 0; i < count - 1; i++) {
			num += cor_diff[i] > d_cor_diff_th ? 1 : 0;
		}
		wifi_found = num >= count / 2 ? true : false;
	}

	//std::cout << "Sample: " << num << " " << "Count: " << count << std::endl;

	return wifi_found;
}

int wifi_sniffer_impl::fft_80(gr_complex *time) {
	gr_complex freq[80];
	int num = 0;

	for (int index = 0; index < 80; index++) {
		for (int element = 0; element < 80; element ++) {
			freq[index] += time[element] * gr_complex(cos(2*M_PI*element*index/80), -sin(2*M_PI*element*index/80));
		}

		if ((abs(freq[index] / gr_complex(80, 0)) * 5) >= d_fft_pwr_th) {
			num++;
		}
	}

	//std::cout << "subcarrier num: " << num << std::endl;

	return num;
}

