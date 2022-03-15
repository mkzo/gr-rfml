# Copyright 2020 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

########################################################################
# Check if there is C++ code at all
########################################################################
if(NOT rfml_sources)
    MESSAGE(STATUS "No C++ sources... skipping python bindings")
    return()
endif(NOT rfml_sources)

########################################################################
# Check for pygccxml
########################################################################
GR_PYTHON_CHECK_MODULE_RAW(
    "pygccxml"
    "import pygccxml"
    PYGCCXML_FOUND
    )

include(GrPybind)

########################################################################
# Python Bindings
########################################################################

list(APPEND rfml_python_files
    python_bindings.cc)

GR_PYBIND_MAKE_OOT(rfml
   ../..
   gr::rfml
   "${rfml_python_files}")

install(TARGETS rfml_python DESTINATION ${GR_PYTHON_DIR}/rfml COMPONENT pythonapi)
