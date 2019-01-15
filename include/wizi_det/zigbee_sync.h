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


#ifndef INCLUDED_WIZI_DET_ZIGBEE_SYNC_H
#define INCLUDED_WIZI_DET_ZIGBEE_SYNC_H

#include <wizi_det/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace wizi_det {

    /*!
     * \brief <+description of block+>
     * \ingroup wizi_det
     *
     */
    class WIZI_DET_API zigbee_sync : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<zigbee_sync> sptr;
      static sptr make(bool debug, float correlation, float power, unsigned int plateau);
    };

  } // namespace wizi_det
} // namespace gr

#endif /* INCLUDED_WIZI_DET_ZIGBEE_SYNC_H */

