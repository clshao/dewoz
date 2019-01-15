#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Wifi In Zigbee Detection
# Generated: Tue Jul  3 14:24:07 2018
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt4 import Qt
from PyQt4.QtCore import QObject, pyqtSlot
from gnuradio import blocks
from gnuradio import channels
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from math import sin, pi
from optparse import OptionParser
from wifi_phy_hier import wifi_phy_hier  # grc-generated hier_block
import foo
import ieee802_11
import ieee802_15_4
import pmt
import sip
import wizi_det


class wifi_in_zigbee_detection(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Wifi In Zigbee Detection")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Wifi In Zigbee Detection")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "wifi_in_zigbee_detection")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.zigbee_samp_rate = zigbee_samp_rate = 4e6
        self.zigbee_pdu_length = zigbee_pdu_length = 80
        self.z_snr = z_snr = 5
        self.window_size = window_size = 16
        self.wifi_samp_rate = wifi_samp_rate = 20e6
        self.wifi_pdu_length = wifi_pdu_length = 5
        self.w_snr = w_snr = 5
        self.sync_length = sync_length = 320
        self.out_buf_size = out_buf_size = 96000
        self.interval = interval = 3000
        self.encoding = encoding = 0
        self.channel_noise = channel_noise = 0.05

        ##################################################
        # Blocks
        ##################################################
        self._zigbee_pdu_length_range = Range(0, 1500, 1, 80, 200)
        self._zigbee_pdu_length_win = RangeWidget(self._zigbee_pdu_length_range, self.set_zigbee_pdu_length, "zigbee_pdu_length", "counter_slider", int)
        self.top_layout.addWidget(self._zigbee_pdu_length_win)
        self._z_snr_range = Range(-15, 30, 0.1, 5, 200)
        self._z_snr_win = RangeWidget(self._z_snr_range, self.set_z_snr, "z_snr", "counter_slider", float)
        self.top_layout.addWidget(self._z_snr_win)
        self._wifi_pdu_length_range = Range(0, 1500, 1, 5, 200)
        self._wifi_pdu_length_win = RangeWidget(self._wifi_pdu_length_range, self.set_wifi_pdu_length, "wifi_pdu_length", "counter_slider", int)
        self.top_layout.addWidget(self._wifi_pdu_length_win)
        self._w_snr_range = Range(-15, 30, 0.1, 5, 200)
        self._w_snr_win = RangeWidget(self._w_snr_range, self.set_w_snr, "w_snr", "counter_slider", float)
        self.top_layout.addWidget(self._w_snr_win)
        self._interval_range = Range(10, 10000, 1, 3000, 200)
        self._interval_win = RangeWidget(self._interval_range, self.set_interval, "interval", "counter_slider", int)
        self.top_layout.addWidget(self._interval_win)
        self._encoding_options = [0, 1, 2, 3, 4, 5, 6, 7]
        self._encoding_labels = ["BPSK 1/2", "BPSK 3/4", "QPSK 1/2", "QPSK 3/4", "16QAM 1/2", "16QAM 3/4", "64QAM 2/3", "64QAM 3/4"]
        self._encoding_group_box = Qt.QGroupBox("encoding")
        self._encoding_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._encoding_button_group = variable_chooser_button_group()
        self._encoding_group_box.setLayout(self._encoding_box)
        for i, label in enumerate(self._encoding_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._encoding_box.addWidget(radio_button)
        	self._encoding_button_group.addButton(radio_button, i)
        self._encoding_callback = lambda i: Qt.QMetaObject.invokeMethod(self._encoding_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._encoding_options.index(i)))
        self._encoding_callback(self.encoding)
        self._encoding_button_group.buttonClicked[int].connect(
        	lambda i: self.set_encoding(self._encoding_options[i]))
        self.top_layout.addWidget(self._encoding_group_box)
        self.wizi_det_zigbee_sync_0 = wizi_det.zigbee_sync(False, 0.7, 40, 10)
        self.wizi_det_wifi_sniffer_0 = wizi_det.wifi_sniffer(False, 0.14, 1, 25)
        self.wifi_phy_hier_0 = wifi_phy_hier(
            bandwidth=20e6,
            chan_est=0,
            encoding=encoding,
            frequency=2.49e9,
            sensitivity=0.56,
        )
        self.qtgui_time_sink_x_0_0_1_1_0_0 = qtgui.time_sink_c(
        	5000, #size
        	1e6, #samp_rate
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0_0_1_1_0_0.set_update_time(1)
        self.qtgui_time_sink_x_0_0_1_1_0_0.set_y_axis(0, 2)
        
        self.qtgui_time_sink_x_0_0_1_1_0_0.set_y_label('Amplitude', "")
        
        self.qtgui_time_sink_x_0_0_1_1_0_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_0_1_1_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_1_1_0_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0_0_1_1_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0_1_1_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_1_1_0_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_time_sink_x_0_0_1_1_0_0.disable_legend()
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(2*1):
            if len(labels[i]) == 0:
                if(i % 2 == 0):
                    self.qtgui_time_sink_x_0_0_1_1_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0_1_1_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0_1_1_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_1_1_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_1_1_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_1_1_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_1_1_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_1_1_0_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_0_0_1_1_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_1_1_0_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_1_1_0_0_win)
        self.qtgui_time_sink_x_0_0_1_1_0 = qtgui.time_sink_c(
        	5000, #size
        	1e6, #samp_rate
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0_0_1_1_0.set_update_time(1)
        self.qtgui_time_sink_x_0_0_1_1_0.set_y_axis(0, 2)
        
        self.qtgui_time_sink_x_0_0_1_1_0.set_y_label('Amplitude', "")
        
        self.qtgui_time_sink_x_0_0_1_1_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_0_1_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_1_1_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0_0_1_1_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0_1_1_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_1_1_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_time_sink_x_0_0_1_1_0.disable_legend()
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(2*1):
            if len(labels[i]) == 0:
                if(i % 2 == 0):
                    self.qtgui_time_sink_x_0_0_1_1_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0_1_1_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0_1_1_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_1_1_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_1_1_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_1_1_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_1_1_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_1_1_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_0_0_1_1_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_1_1_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_1_1_0_win)
        self.qtgui_time_sink_x_0_0_1_1 = qtgui.time_sink_c(
        	5000, #size
        	1e6, #samp_rate
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0_0_1_1.set_update_time(1)
        self.qtgui_time_sink_x_0_0_1_1.set_y_axis(0, 2)
        
        self.qtgui_time_sink_x_0_0_1_1.set_y_label('Amplitude', "")
        
        self.qtgui_time_sink_x_0_0_1_1.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_0_1_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_1_1.enable_autoscale(True)
        self.qtgui_time_sink_x_0_0_1_1.enable_grid(False)
        self.qtgui_time_sink_x_0_0_1_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_1_1.enable_control_panel(False)
        
        if not True:
          self.qtgui_time_sink_x_0_0_1_1.disable_legend()
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(2*1):
            if len(labels[i]) == 0:
                if(i % 2 == 0):
                    self.qtgui_time_sink_x_0_0_1_1.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0_1_1.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0_1_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_1_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_1_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_1_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_1_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_1_1.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_0_0_1_1_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_1_1.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_1_1_win)
        self.ieee802_15_4_rime_stack_0 = ieee802_15_4.rime_stack(([129]), ([131]), ([132]), ([23,42]))
        self.ieee802_15_4_mac_0 = ieee802_15_4.mac(True)
        self.ieee802_15_4_access_code_prefixer_0 = ieee802_15_4.access_code_prefixer()
        self.ieee802_11_moving_average_xx_1 = ieee802_11.moving_average_ff(window_size )
        self.ieee802_11_moving_average_xx_0 = ieee802_11.moving_average_cc(window_size)
        self.ieee802_11_mac_0 = ieee802_11.mac(([0x23, 0x23, 0x23, 0x23, 0x23, 0x23]), ([0x42, 0x42, 0x42, 0x42, 0x42, 0x42]), ([0xff, 0xff, 0xff, 0xff, 0xff, 255]))
        self.foo_packet_pad_0 = foo.packet_pad(False, False, 0.010, 80, 120)
        (self.foo_packet_pad_0).set_min_output_buffer(96000)
        self.foo_packet_pad2_0 = foo.packet_pad2(False, False, 0.01, 5800, 20000)
        (self.foo_packet_pad2_0).set_min_output_buffer(96000)
        self.foo_burst_tagger_0 = foo.burst_tagger(pmt.intern("pdu_length"), 640)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc(([(1+1j), (-1+1j), (1-1j), (-1+1j), (1+1j), (-1-1j), (-1-1j), (1+1j), (-1+1j), (-1+1j), (-1-1j), (1-1j), (-1-1j), (1-1j), (1+1j), (1-1j), (1-1j), (-1-1j), (1+1j), (-1-1j), (1-1j), (-1+1j), (-1+1j), (1-1j), (-1-1j), (-1-1j), (-1+1j), (1+1j), (-1+1j), (1+1j), (1-1j), (1+1j), (-1+1j), (-1+1j), (-1-1j), (1-1j), (-1-1j), (1-1j), (1+1j), (1-1j), (1+1j), (-1+1j), (1-1j), (-1+1j), (1+1j), (-1-1j), (-1-1j), (1+1j), (-1-1j), (-1-1j), (-1+1j), (1+1j), (-1+1j), (1+1j), (1-1j), (1+1j), (1-1j), (-1-1j), (1+1j), (-1-1j), (1-1j), (-1+1j), (-1+1j), (1-1j), (-1-1j), (1-1j), (1+1j), (1-1j), (1+1j), (-1+1j), (1-1j), (-1+1j), (1+1j), (-1-1j), (-1-1j), (1+1j), (-1+1j), (-1+1j), (-1-1j), (1-1j), (-1+1j), (1+1j), (1-1j), (1+1j), (1-1j), (-1-1j), (1+1j), (-1-1j), (1-1j), (-1+1j), (-1+1j), (1-1j), (-1-1j), (-1-1j), (-1+1j), (1+1j), (1+1j), (-1-1j), (-1-1j), (1+1j), (-1+1j), (-1+1j), (-1-1j), (1-1j), (-1-1j), (1-1j), (1+1j), (1-1j), (1+1j), (-1+1j), (1-1j), (-1+1j), (1-1j), (-1+1j), (-1+1j), (1-1j), (-1-1j), (-1-1j), (-1+1j), (1+1j), (-1+1j), (1+1j), (1-1j), (1+1j), (1-1j), (-1-1j), (1+1j), (-1-1j), (1+1j), (1-1j), (1+1j), (-1+1j), (1-1j), (-1+1j), (1+1j), (-1-1j), (-1-1j), (1+1j), (-1+1j), (-1+1j), (-1-1j), (1-1j), (-1-1j), (1-1j), (1-1j), (1+1j), (1-1j), (-1-1j), (1+1j), (-1-1j), (1-1j), (-1+1j), (-1+1j), (1-1j), (-1-1j), (-1-1j), (-1+1j), (1+1j), (-1+1j), (1+1j), (-1-1j), (1+1j), (-1+1j), (-1+1j), (-1-1j), (1-1j), (-1-1j), (1-1j), (1+1j), (1-1j), (1+1j), (-1+1j), (1-1j), (-1+1j), (1+1j), (-1-1j), (-1+1j), (1-1j), (-1-1j), (-1-1j), (-1+1j), (1+1j), (-1+1j), (1+1j), (1-1j), (1+1j), (1-1j), (-1-1j), (1+1j), (-1-1j), (1-1j), (-1+1j), (-1-1j), (1-1j), (-1-1j), (1-1j), (1+1j), (1-1j), (1+1j), (-1+1j), (1-1j), (-1+1j), (1+1j), (-1-1j), (-1-1j), (1+1j), (-1+1j), (-1+1j), (-1+1j), (1+1j), (-1+1j), (1+1j), (1-1j), (1+1j), (1-1j), (-1-1j), (1+1j), (-1-1j), (1-1j), (-1+1j), (-1+1j), (1-1j), (-1-1j), (-1-1j), (1-1j), (-1+1j), (1+1j), (-1-1j), (-1-1j), (1+1j), (-1+1j), (-1+1j), (-1-1j), (1-1j), (-1-1j), (1-1j), (1+1j), (1-1j), (1+1j), (-1+1j), (1+1j), (-1-1j), (1-1j), (-1+1j), (-1+1j), (1-1j), (-1-1j), (-1-1j), (-1+1j), (1+1j), (-1+1j), (1+1j), (1-1j), (1+1j), (1-1j), (-1-1j)]), 16)
        self.channels_channel_model_0_0 = channels.channel_model(
        	noise_voltage=channel_noise,
        	frequency_offset=(-1)*pi/2,
        	epsilon=1.0,
        	taps=(1, ),
        	noise_seed=0,
        	block_tags=False
        )
        self.channels_channel_model_0 = channels.channel_model(
        	noise_voltage=channel_noise,
        	frequency_offset=2 * pi /3,
        	epsilon=1,
        	taps=(1, ),
        	noise_seed=0,
        	block_tags=False
        )
        self.blocks_vector_source_x_0 = blocks.vector_source_c([0, sin(pi/20), sin(2*pi/20), sin(3*pi/20), sin(4*pi/20), sin(5*pi/20), sin(6*pi/20), sin(7*pi/20), sin(8*pi/20), sin(9*pi/20), sin(10*pi/20), sin(11*pi/20), sin(12*pi/20), sin(13*pi/20), sin(14*pi/20), sin(15*pi/20), sin(16*pi/20), sin(17*pi/20), sin(18*pi/20), sin(19*pi/20)], True, 1, [])
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_gr_complex*1, 20)
        self.blocks_pdu_to_tagged_stream_0_0_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, 'pdu_length')
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(4, gr.GR_LSB_FIRST)
        self.blocks_null_source_0 = blocks.null_source(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0_0_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0_1_0 = blocks.multiply_const_vcc(((10**(z_snr/10.0))**.5, ))
        self.blocks_multiply_const_vxx_0_1 = blocks.multiply_const_vcc(((10**(w_snr/10.0))**.5, ))
        self.blocks_message_strobe_0_0 = blocks.message_strobe(pmt.intern("".join("w" for i in range(wifi_pdu_length))), interval)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.intern("".join("z" for i in range(zigbee_pdu_length))), interval)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_float*1, '/home/ahyhus/gr-wizi_det/examples/Clear_cor_src.bin', True)
        self.blocks_divide_xx_0 = blocks.divide_ff(1)
        self.blocks_delay_0_1 = blocks.delay(gr.sizeof_float*1, 10)
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_gr_complex*1, 16)
        self.blocks_conjugate_cc_0 = blocks.conjugate_cc()
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.ieee802_15_4_rime_stack_0, 'bcin'))    
        self.msg_connect((self.blocks_message_strobe_0_0, 'strobe'), (self.ieee802_11_mac_0, 'app in'))    
        self.msg_connect((self.ieee802_11_mac_0, 'phy out'), (self.wifi_phy_hier_0, 'mac_in'))    
        self.msg_connect((self.ieee802_15_4_access_code_prefixer_0, 'out'), (self.blocks_pdu_to_tagged_stream_0_0_0, 'pdus'))    
        self.msg_connect((self.ieee802_15_4_mac_0, 'pdu out'), (self.ieee802_15_4_access_code_prefixer_0, 'in'))    
        self.msg_connect((self.ieee802_15_4_mac_0, 'app out'), (self.ieee802_15_4_rime_stack_0, 'fromMAC'))    
        self.msg_connect((self.ieee802_15_4_rime_stack_0, 'toMAC'), (self.ieee802_15_4_mac_0, 'app in'))    
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))    
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_delay_0_0, 0))    
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_xx_0, 0))    
        self.connect((self.blocks_add_xx_0, 0), (self.qtgui_time_sink_x_0_0_1_1, 0))    
        self.connect((self.blocks_complex_to_float_0, 1), (self.blocks_delay_0_1, 0))    
        self.connect((self.blocks_complex_to_float_0, 0), (self.blocks_float_to_complex_0, 0))    
        self.connect((self.blocks_complex_to_mag_0, 0), (self.blocks_divide_xx_0, 0))    
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.ieee802_11_moving_average_xx_1, 0))    
        self.connect((self.blocks_conjugate_cc_0, 0), (self.blocks_multiply_xx_0, 1))    
        self.connect((self.blocks_delay_0_0, 0), (self.blocks_conjugate_cc_0, 0))    
        self.connect((self.blocks_delay_0_0, 0), (self.wizi_det_zigbee_sync_0, 2))    
        self.connect((self.blocks_delay_0_1, 0), (self.blocks_float_to_complex_0, 1))    
        self.connect((self.blocks_divide_xx_0, 0), (self.wizi_det_zigbee_sync_0, 0))    
        self.connect((self.blocks_file_source_0, 0), (self.wizi_det_wifi_sniffer_0, 1))    
        self.connect((self.blocks_float_to_complex_0, 0), (self.foo_burst_tagger_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0_1, 0), (self.channels_channel_model_0_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0_1_0, 0), (self.channels_channel_model_0, 0))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.ieee802_11_moving_average_xx_0, 0))    
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.blocks_complex_to_float_0, 0))    
        self.connect((self.blocks_null_source_0, 0), (self.wifi_phy_hier_0, 0))    
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))    
        self.connect((self.blocks_pdu_to_tagged_stream_0_0_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))    
        self.connect((self.blocks_repeat_0, 0), (self.blocks_multiply_xx_0_0, 1))    
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_multiply_xx_0_0, 0))    
        self.connect((self.channels_channel_model_0, 0), (self.blocks_add_xx_0, 0))    
        self.connect((self.channels_channel_model_0, 0), (self.qtgui_time_sink_x_0_0_1_1_0_0, 0))    
        self.connect((self.channels_channel_model_0_0, 0), (self.blocks_add_xx_0, 1))    
        self.connect((self.channels_channel_model_0_0, 0), (self.qtgui_time_sink_x_0_0_1_1_0, 0))    
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.blocks_repeat_0, 0))    
        self.connect((self.foo_burst_tagger_0, 0), (self.foo_packet_pad_0, 0))    
        self.connect((self.foo_packet_pad2_0, 0), (self.blocks_multiply_const_vxx_0_1, 0))    
        self.connect((self.foo_packet_pad_0, 0), (self.blocks_multiply_const_vxx_0_1_0, 0))    
        self.connect((self.ieee802_11_moving_average_xx_0, 0), (self.blocks_complex_to_mag_0, 0))    
        self.connect((self.ieee802_11_moving_average_xx_1, 0), (self.blocks_divide_xx_0, 1))    
        self.connect((self.ieee802_11_moving_average_xx_1, 0), (self.wizi_det_zigbee_sync_0, 1))    
        self.connect((self.wifi_phy_hier_0, 0), (self.foo_packet_pad2_0, 0))    
        self.connect((self.wizi_det_wifi_sniffer_0, 0), (self.blocks_null_sink_0_0_0, 0))    
        self.connect((self.wizi_det_zigbee_sync_0, 0), (self.wizi_det_wifi_sniffer_0, 0))    
        self.connect((self.wizi_det_zigbee_sync_0, 1), (self.wizi_det_wifi_sniffer_0, 2))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "wifi_in_zigbee_detection")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_zigbee_samp_rate(self):
        return self.zigbee_samp_rate

    def set_zigbee_samp_rate(self, zigbee_samp_rate):
        self.zigbee_samp_rate = zigbee_samp_rate

    def get_zigbee_pdu_length(self):
        return self.zigbee_pdu_length

    def set_zigbee_pdu_length(self, zigbee_pdu_length):
        self.zigbee_pdu_length = zigbee_pdu_length
        self.blocks_message_strobe_0.set_msg(pmt.intern("".join("z" for i in range(self.zigbee_pdu_length))))

    def get_z_snr(self):
        return self.z_snr

    def set_z_snr(self, z_snr):
        self.z_snr = z_snr
        self.blocks_multiply_const_vxx_0_1_0.set_k(((10**(self.z_snr/10.0))**.5, ))

    def get_window_size(self):
        return self.window_size

    def set_window_size(self, window_size):
        self.window_size = window_size
        self.ieee802_11_moving_average_xx_1.set_length(self.window_size )
        self.ieee802_11_moving_average_xx_0.set_length(self.window_size)

    def get_wifi_samp_rate(self):
        return self.wifi_samp_rate

    def set_wifi_samp_rate(self, wifi_samp_rate):
        self.wifi_samp_rate = wifi_samp_rate

    def get_wifi_pdu_length(self):
        return self.wifi_pdu_length

    def set_wifi_pdu_length(self, wifi_pdu_length):
        self.wifi_pdu_length = wifi_pdu_length
        self.blocks_message_strobe_0_0.set_msg(pmt.intern("".join("w" for i in range(self.wifi_pdu_length))))

    def get_w_snr(self):
        return self.w_snr

    def set_w_snr(self, w_snr):
        self.w_snr = w_snr
        self.blocks_multiply_const_vxx_0_1.set_k(((10**(self.w_snr/10.0))**.5, ))

    def get_sync_length(self):
        return self.sync_length

    def set_sync_length(self, sync_length):
        self.sync_length = sync_length

    def get_out_buf_size(self):
        return self.out_buf_size

    def set_out_buf_size(self, out_buf_size):
        self.out_buf_size = out_buf_size

    def get_interval(self):
        return self.interval

    def set_interval(self, interval):
        self.interval = interval
        self.blocks_message_strobe_0_0.set_period(self.interval)
        self.blocks_message_strobe_0.set_period(self.interval)

    def get_encoding(self):
        return self.encoding

    def set_encoding(self, encoding):
        self.encoding = encoding
        self._encoding_callback(self.encoding)
        self.wifi_phy_hier_0.set_encoding(self.encoding)

    def get_channel_noise(self):
        return self.channel_noise

    def set_channel_noise(self, channel_noise):
        self.channel_noise = channel_noise
        self.channels_channel_model_0_0.set_noise_voltage(self.channel_noise)
        self.channels_channel_model_0.set_noise_voltage(self.channel_noise)


def main(top_block_cls=wifi_in_zigbee_detection, options=None):
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable real-time scheduling."

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()