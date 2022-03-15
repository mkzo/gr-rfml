#
# Copyright 2008,2009 Free Software Foundation, Inc.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

# The presence of this file turns this directory into a Python package

'''
This is the GNU Radio RFML module. Place your Python package
description here (python/__init__.py).
'''
import os

# import pybind11 generated symbols into the rfml namespace
try:
    # this might fail if the module is python-only
    from .rfml_python import *
except ModuleNotFoundError:
    pass

# import any pure python here
from .dnn_onnx_sync import dnn_onnx_sync
#
