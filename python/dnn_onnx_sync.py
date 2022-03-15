#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2022 Rutgers University..
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2022 Rutgers..
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#


import numpy as np
from gnuradio import gr
import onnx
import onnxruntime as ort
import onnxruntime.backend as backend
from numpy.fft import fftshift
import cv2
import scipy.signal
from scipy.special import softmax
import sys
import importlib
import importlib.util

class dnn_onnx_sync(gr.sync_block):

    INPUT_TYPES = {
        'float':  np.float32,
        'complex': np.complex64
        }
    
    def __init__(self, onnx_model_file, input_transform_file, onnx_batch_size, onnx_runtime_device, input_transform, input_type, output_transform, in_size, out_size):
        gr.sync_block.__init__(self, name="dnn_onnx_sync", in_sig=[(self.INPUT_TYPES[input_type], in_size)], out_sig=[(np.float32, out_size)])

        self.session = ort.InferenceSession(onnx_model_file, None)
        self.backend = backend.prepare(self.session)
        self.input_transform = input_transform
        self.output_transform = output_transform
        self.input_transform_file = input_transform_file

    def _transformone(self, input_data):
        return np.hstack((np.real(input_data).reshape(128,1), np.imag(input_data).reshape(128,1))).reshape(1,128,2)

    def _transformtwo(self, input_data):
        f, t, Sxx = scipy.signal.spectrogram(input_data, nfft=1024, noverlap=0, return_onesided=False)
        testSxx = Sxx.transpose()
        gray = cv2.resize(np.fft.fftshift(testSxx, axes=1), (28,28), interpolation=cv2.INTER_LINEAR_EXACT).astype(np.float32)/255
        inputmat = gray/np.max(gray)
        inputmat = 1/(inputmat**(0.4))
        return inputmat.reshape(1,1,28,28)
    
    def _outone(self, transformed_input):
        return self.backend.run(transformed_input)[0][0]

    def _outtwo(self, transformed_input):
        return softmax(self.backend.run(transformed_input)[0][0])

    INPUT_TRANSFORM = {
            'RFML': "_transformone",
            'Image': "_transformtwo",
            'Custom': "_transform",
        }

    OUTPUT_TRANSFORM = {
            'Default': "_outone",
            'Softmax': "_outtwo",
        }

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        spec = importlib.util.spec_from_file_location("trans", self.input_transform_file)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        for i in range(0, np.shape(input_items)[1]):
            transformed_input = getattr(self, self.INPUT_TRANSFORM[self.input_transform], m._transform)(input_items[0][i])
            #transformed_input = self._transformtwo(input_items[0][i])
            output_items[0][i] = getattr(self, self.OUTPUT_TRANSFORM[self.output_transform])(transformed_input)
        	
        return len(output_items[0])
